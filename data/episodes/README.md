# Episodes

`direction/` と `entry/` は `data/events` から派生させる評価用データ。

## Direction Episode
- 同一銘柄・同一方向（LONG / SHORT）の継続を1シナリオとしてまとめる。
- LONG/SHORT が初めて明示された時点で開始する。
- 同方向の HOLD / ACTIONABLE / TRADE は同じDirection Episodeを継続する。
- 明示的な NONE、または反対方向が出た時点で終了する。
- ERROR / UNDETERMINED は「観測不能」として扱い、それだけでは既存Direction Episodeを終了しない。
- RECOVERY時は canonical slot ではなく `evaluation_time_jst`（実際の市場取得時刻）をEpisode時刻に使う。

## Entry Episode
- 正式な ACTIONABLE / TRADE を起点に作成する。
- HOLD時の `candidate_plan` はEntry Episodeを新規作成しない。
- 同じACTIONABLE状態が連続するだけなら同一Entry機会として扱う。いったんHOLD/WAIT/NONE/反対方向へ移行した後に再びACTIONABLEになった場合は新しいEntry Episodeとする。
- Entry Episode成立時の初期 Entry / SL / TP は凍結し、後から上書きしない。
- `signal_ended_at` はEntryシグナルが継続しなくなった時刻であり、TP/SLによる決済時刻とは別物。
- TP/SL到達を価格履歴で確定できるまでは `status=UNRESOLVED` とする。
- 同一足内でTPとSLの双方に到達し順序を確定できない場合は `first_exit_event=UNKNOWN_SAME_BAR` とする。

## Audit rule
Episodeは派生データ。監査原本は `data/raw` と `data/events`。Episodeは原本から再生成可能でなければならない。
