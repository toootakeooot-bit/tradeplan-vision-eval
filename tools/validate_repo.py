#!/usr/bin/env python3
"""Lightweight integrity checks for tradeplan-vision-eval.

Standard-library only so it can run locally or in GitHub Actions without extra packages.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

EVENT_REQUIRED = {"event_id", "timestamp_jst", "symbol", "source", "direction", "entry_status"}
DIRECTION_REQUIRED = {"episode_id", "symbol", "direction", "started_at", "status", "first_event_id", "latest_event_id"}
ENTRY_REQUIRED = {"entry_episode_id", "direction_episode_id", "symbol", "direction", "entry_at", "entry_price", "status"}

DIRECTIONS = {"LONG", "SHORT", "NONE", "UNDETERMINED"}
ENTRY_STATUSES = {"ACTIONABLE", "TRADE", "WAIT", "HOLD", "INVALID", "UNDETERMINED", "ERROR"}


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def load_json(path: Path, errors: list[str]):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # pragma: no cover - CLI diagnostic
        fail(errors, f"{path.relative_to(ROOT)}: invalid JSON: {exc}")
        return None


def main() -> int:
    errors: list[str] = []
    events: dict[str, dict] = {}

    # Events
    for path in sorted((ROOT / "data" / "events").rglob("*.jsonl")):
        for lineno, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if not raw.strip():
                continue
            try:
                event = json.loads(raw)
            except Exception as exc:
                fail(errors, f"{path.relative_to(ROOT)}:{lineno}: invalid JSON: {exc}")
                continue
            missing = EVENT_REQUIRED - event.keys()
            if missing:
                fail(errors, f"{path.relative_to(ROOT)}:{lineno}: missing event fields {sorted(missing)}")
                continue
            eid = event["event_id"]
            if eid in events:
                fail(errors, f"duplicate event_id: {eid}")
            events[eid] = event
            if event["direction"] not in DIRECTIONS:
                fail(errors, f"{eid}: invalid direction {event['direction']}")
            if event["entry_status"] not in ENTRY_STATUSES:
                fail(errors, f"{eid}: invalid entry_status {event['entry_status']}")
            raw_ref = event.get("raw_ref")
            if raw_ref and not (ROOT / raw_ref).exists():
                fail(errors, f"{eid}: raw_ref not found: {raw_ref}")
            if event["entry_status"] in {"ACTIONABLE", "TRADE"} and event.get("backfill_confidence") != "PARTIAL":
                if event.get("entry") is None or event.get("sl") is None or not event.get("tp"):
                    fail(errors, f"{eid}: formal entry status lacks frozen Entry/SL/TP")

    # Direction episodes
    direction_eps: dict[str, dict] = {}
    direction_dir = ROOT / "data" / "episodes" / "direction"
    if direction_dir.exists():
        for path in sorted(direction_dir.glob("*.json")):
            ep = load_json(path, errors)
            if not isinstance(ep, dict):
                continue
            missing = DIRECTION_REQUIRED - ep.keys()
            if missing:
                fail(errors, f"{path.relative_to(ROOT)}: missing fields {sorted(missing)}")
                continue
            eid = ep["episode_id"]
            if eid in direction_eps:
                fail(errors, f"duplicate direction episode_id: {eid}")
            direction_eps[eid] = ep
            if ep["direction"] not in {"LONG", "SHORT"}:
                fail(errors, f"{eid}: invalid direction {ep['direction']}")
            for ref_name in ("first_event_id", "latest_event_id", "closed_by_event_id"):
                ref = ep.get(ref_name)
                if ref and ref not in events:
                    fail(errors, f"{eid}: {ref_name} not found: {ref}")

    # Entry episodes
    entry_eps: dict[str, dict] = {}
    entry_dir = ROOT / "data" / "episodes" / "entry"
    if entry_dir.exists():
        for path in sorted(entry_dir.glob("*.json")):
            ep = load_json(path, errors)
            if not isinstance(ep, dict):
                continue
            missing = ENTRY_REQUIRED - ep.keys()
            if missing:
                fail(errors, f"{path.relative_to(ROOT)}: missing fields {sorted(missing)}")
                continue
            eid = ep["entry_episode_id"]
            if eid in entry_eps:
                fail(errors, f"duplicate entry episode_id: {eid}")
            entry_eps[eid] = ep
            if ep["direction_episode_id"] not in direction_eps:
                fail(errors, f"{eid}: direction_episode_id not found: {ep['direction_episode_id']}")
            src = ep.get("source_event_id")
            if src and src not in events:
                fail(errors, f"{eid}: source_event_id not found: {src}")
            if ep.get("initial_sl") is None or not ep.get("initial_tp"):
                fail(errors, f"{eid}: missing frozen initial SL/TP")

    # Cross-check Direction Episode -> Entry Episode references.
    for did, dep in direction_eps.items():
        for entry_id in dep.get("entry_episode_ids", []):
            if entry_id not in entry_eps:
                fail(errors, f"{did}: entry_episode_id not found: {entry_id}")
            elif entry_eps[entry_id].get("direction_episode_id") != did:
                fail(errors, f"{did}: entry {entry_id} points to another direction episode")

    # Active state
    state_path = ROOT / "state" / "active_episodes.json"
    if state_path.exists():
        state = load_json(state_path, errors)
        if isinstance(state, dict):
            for symbol, did in state.get("direction", {}).items():
                if did not in direction_eps:
                    fail(errors, f"active direction {symbol}: unknown episode {did}")
                elif direction_eps[did].get("status") != "ACTIVE":
                    fail(errors, f"active direction {symbol}: episode {did} is not ACTIVE")
            for symbol, ids in state.get("entry", {}).items():
                for entry_id in ids:
                    if entry_id not in entry_eps:
                        fail(errors, f"active entry {symbol}: unknown episode {entry_id}")
                    elif entry_eps[entry_id].get("status") not in {"OPEN", "UNRESOLVED"}:
                        fail(errors, f"active entry {symbol}: episode {entry_id} is already closed")

    print(f"events={len(events)} direction_episodes={len(direction_eps)} entry_episodes={len(entry_eps)}")
    if errors:
        print(f"FAILED: {len(errors)} integrity issue(s)")
        for item in errors:
            print(f"- {item}")
        return 1
    print("OK: repository integrity checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
