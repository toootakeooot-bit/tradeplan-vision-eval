# TC Evaluation Ingestion Flow

## Goal

TC定期判定を「通知」ではなく「検証可能な監査履歴」として残す。Gmailは通知コピーであり、今後の一次原本にはしない。

## Live flow

1. **TC periodic judgement completes**
   - canonical cycle keyを確定。
   - 各銘柄の実際のmarket-data取得時刻を保存。

2. **Raw snapshot first**
   - `data/raw/YYYY/MM/DD/` にTC出力を保存。
   - 原文/Native結果に存在しない値を補完しない。
   - RECOVERYの場合はcanonical slotとactual snapshot timeを両方保存。

3. **Normalize event**
   - `data/events/YYYY/MM/YYYY-MM-DD.jsonl` に銘柄単位で追記。
   - 必須: event_id / canonical time / evaluation_time / symbol / direction / entry_status。
   - 正式ACTIONABLE/TRADE時のみEntry/SL/TPをformal planとして保存。
   - HOLDのpotentialPositionは`candidate_plan`へ保存し、Entry Episode化しない。

4. **Update episodes**
   - Direction Episode: LONG/SHORT継続を1シナリオ化。
   - Entry Episode: ACTIONABLE/TRADEの機会だけ作成。
   - 初期Entry/SL/TPは凍結。

5. **Update active state**
   - `state/active_episodes.json` を更新。
   - direction: 現在進行中の方向Episode。
   - entry: TP/SL結果が未解決のEntry Episode。

6. **Price outcome check**
   - Entry時刻以降の価格履歴でTP/SL到達順を確認。
   - Provider整合したintraday priceを優先。
   - 日足だけでは勝敗確定しない。

7. **Human report**
   - 朝: 前夜からの変化、ACTIVE方向、未解決Entryの進捗。
   - 夕: 当日Direction変化、新規Entry、TP/SL到達、異常。
   - 週次: Trade Planとして機能したか、方向/Entryタイミング/SL・TP/癖を総括。

## Backfill flow

過去データは以下の優先順位で使用する。

1. 保存済みTC raw/native output
2. 保存済み定期結果
3. Gmail通知本文
4. その他の明示的な記録

チャット要約や記憶から数値を推測して監査原本を作らない。

## Idempotency

- `event_id` と `canonical_cycle_key` で重複を防止。
- 既存raw/eventは都合よく上書きしない。
- 誤り訂正が必要な場合は訂正理由と元値を残す。
- Episodeは派生データなのでraw/eventから再生成可能にする。
