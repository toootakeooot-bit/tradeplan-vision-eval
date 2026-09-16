# Backfill Policy

過去TC判定を評価リポジトリへ移行する際の監査ルール。

## Source priority

1. TC Native の保存済み原判定
2. TC判定をそのまま送信したGmail通知
3. ChatGPT上に残る完全な判定本文
4. 要約・記憶・断片的スニペット

## Confidence

- `NATIVE`: TC Native原判定を直接保存
- `EXACT`: Gmail等に完全な判定内容が残っており、Entry/SL/TP/方向を確定可能
- `PARTIAL`: 方向やEntry状態など一部のみ確定可能
- `UNKNOWN`: 内容を監査可能な形で復元できない

`PARTIAL` / `UNKNOWN` から、欠けている Entry / SL / TP を推測して補完してはならない。

## Recovery runs

RECOVERYメールは canonical slot と actual execution time を分けて保存する。
定期枠の評価には canonical slot を用い、データ鮮度監査には actual execution time を残す。

## Duplicate handling

補送メールや再送メールは新しいTC判定として数えない。保存済み結果の再送であることが確認できる場合、元eventへの参照として扱う。

## Immutable fields

Entry Episode成立時の以下を凍結する。

- entry_at
- entry_price
- initial_sl
- initial_tp

後続判定でSL/TPが変更された場合は履歴として追加し、初期値を上書きしない。

## Price outcome

TP/SL到達順が同一足OHLCだけでは確定できない場合、`UNKNOWN_SAME_BAR` とする。
TC理論結果と実MT4約定結果は別データとして扱う。
