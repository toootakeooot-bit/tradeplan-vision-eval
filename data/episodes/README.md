# Episodes

`direction/` と `entry/` は `data/events` から派生させる評価用データ。

- Direction Episode: 同一銘柄・同一方向の継続を1シナリオとしてまとめる
- Entry Episode: 正式な ACTIONABLE / TRADE を起点に追跡する
- HOLD時の candidate_plan はEntry Episodeを新規作成しない
- Entry Episode成立後の初期 Entry / SL / TP は凍結
- Episode生成ルールが未確定な期間は、先にeventsのみ保存し後から再生成する

このフォルダのEpisodeは派生データであり、監査原本は `data/raw` と `data/events`。
