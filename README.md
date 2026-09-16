# tradeplan-vision-eval

TC (TradingCursor) の定期エントリー判定を実運用で監視し、Trade Plan が実際に利益につながるかを検証・評価するための専用リポジトリ。

## Evaluation model

- Direction Episode: LONG/SHORT の方向継続を1つのシナリオとして追跡
- Entry Episode: ACTIONABLE/TRADE になった機会を別途追跡
- 同方向の定期判定は判定回数として重複計上しない
- Entry成立時の Entry / SL / TP / 時刻は初期値として凍結保存
- その後の価格推移で TP / SL 到達と到達順を追跡
- 同一足で TP/SL の両方に到達し順序を確定できない場合は UNKNOWN_SAME_BAR
- TC理論結果と実MT4約定結果は分離
- 朝夕は進行中Episodeの状態、週次は総括評価を報告

## Repository layout

```text
schema/                       JSON schema
data/events/YYYY/MM/          正規化イベント (JSONL)
data/raw/YYYY/MM/DD/          TC原判定の保存
data/episodes/direction/       Direction Episode
data/episodes/entry/           Entry Episode
state/active_episodes.json     現在追跡中のEpisode
reports/daily/YYYY-MM-DD/      morning / evening
reports/weekly/                週次評価
docs/BACKFILL_POLICY.md        過去履歴移行ルール
```

## Audit rule

`data/raw` と `data/events` は追記型の監査ログとして扱う。過去のTC判定を後から都合よく書き換えない。Episode側の状態更新とレポートは派生データとして扱う。
