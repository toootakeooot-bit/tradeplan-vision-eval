# TC検証 Evening — 2026-09-16

## まず結論

- **現在の方向Episode:** GOLD LONGのみACTIVE。USDJPY / US100は明示方向なし（NONE）。
- **本日17時台までの正式Entry:** 新規ACTIONABLE / TRADEなし。
- **過去からTP/SL結果を追跡中:** 5 Entry Episodes（GOLD 2 / USDJPY 2 / US100 1）。
- **利益評価:** まだ確定しない。日足OHLCだけではEntry後のTP/SL到達順を保証できないため、5件すべてUNRESOLVEDを維持。

## Direction Episode

### GOLD
- GOLD-DIR-0001: SHORT / CLOSED（9/15 09:28頃 → 9/16 10:25:30）
- GOLD-DIR-0002: LONG / CLOSED（9/16 10:25:30 → 12:03:03）
- GOLD-DIR-0003: **LONG / ACTIVE**（9/16 17:36:28〜）
- 17:03 RECOVERYでは3TF bullish一致だが正式EntryはHOLD。

### USDJPY
- USDJPY-DIR-0001: LONG / CLOSED（9/15 09:26頃 → 9/16 10:26:50）
- 以降は時間軸競合により方向NONE。

### US100
- US100-DIR-0001: SHORT / CLOSED（9/15 17:34:28 → 21:03）
- US100-DIR-0002: LONG / CLOSED（9/15 21:03 → 9/16 10:27:59）
- 以降は方向NONE。

## Entry Episode（正式ACTIONABLE / TRADEのみ）

| ID | 方向 | Entry | SL | TP1 | 現在 |
|---|---|---:|---:|---:|---|
| GOLD-ENT-0001 | SHORT | 4287.655 | 4302.214 | 4262.888 | UNRESOLVED |
| GOLD-ENT-0002 | SHORT | 4282.57 | 4310 | 4264.945 | UNRESOLVED |
| USDJPY-ENT-0001 | LONG | 154.544 | 154.000 | 154.892 | UNRESOLVED |
| USDJPY-ENT-0002 | LONG | 154.908 | 154.647 | 155.188 | UNRESOLVED |
| US100-ENT-0001 | LONG | 29109.3 | 28967 | 29280.2 | UNRESOLVED |

## 監査メモ

- RECOVERY判定はcanonical slotと実取得時刻を分離。Episodeは実取得時刻 `evaluation_time_jst` を使用。
- 9/15 12:03はNative取得前の障害としてERROR保存し、Episodeを強制終了していない。
- HOLDのcandidate_planはEntry Episodeに数えていない。
- Gmailで確認できた定期通知は実質9/15以降。9/14以前の正式定期通知は今回の検索では見つからなかったため、現時点のEpisode開始は9/15を起点としている。
- 日足価格は補助証拠として保存済み。TP/SL結果確定にはProvider整合したIntradayデータを優先する。
