# Reporting Policy

ユーザーが短時間でTCの状態と検証進捗を理解できることを最優先にする。

## Morning / Evening

冒頭は必ず次の順序。

1. **結論**
   - 利益評価: `YES / NO / 判断保留`
   - ACTIVE Direction: 銘柄と方向のみ
   - 新規Entry: 有無
   - TP/SL確定: 有無

2. **変化した銘柄だけ詳しく**
   - 方向が変わった
   - ACTIONABLE/TRADEになった
   - TP/SLに到達した
   - ERROR/RECOVERYが発生した

3. **追跡中Entry**
   - ID / 方向 / Entry / SL / TP1 / 状態
   - 毎回全履歴を再掲しない。

## Weekly

勝率を主指標にしない。次を優先する。

- TCの方向認識は継続性があるか
- WAIT/HOLDからEntryへ移るタイミングは妥当か
- Entry後、SLとTPのどちらへ先に到達するか
- 方向は正しいがEntryが早すぎる/遅すぎる事例があるか
- 銘柄や相場環境ごとの癖が見えるか
- 障害/RECOVERYが検証を歪めていないか

## Status wording

- `ACTIVE`: 現在継続中のDirection Episode。
- `ACTIONABLE / TRADE`: 正式なEntry機会。Entry Episodeを作る。
- `HOLD / WAIT`: Entry機会を新規作成しない。
- `UNRESOLVED`: Entryは成立したがTP/SL結果をまだ確定できない。
- `CLOSED (Direction)`: 方向シナリオ終了。トレード損益確定とは別。
- `UNKNOWN_SAME_BAR`: 同一足内でTP/SL双方に到達し順序不明。

## Human-readable rule

- 『Directionが当たった』と『Entryで利益が出た』を混同しない。
- candidate_planとformal Entryを混同しない。
- signal_ended_atとTP/SL決済を混同しない。
- データ不足時は無理に勝敗を付けず『判断保留』と書く。
