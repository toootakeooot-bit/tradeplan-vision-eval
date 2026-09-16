# Price Verification Policy

TC Entry Episode の TP/SL 結果を後付け推測で確定しないための価格照合ルール。

## Evidence levels

1. `PROVIDER_INTRADAY_EXACT`
   - TC判定と同一Provider/同等銘柄の時系列OHLCまたはtick。
   - TP/SLの到達順が判定可能なら結果確定に使用できる。

2. `INTRADAY_PROXY`
   - 別Providerだが同一原資産のM1/M5等。
   - 水準から十分離れていてProvider差で結論が変わらない場合のみ補助的に確定候補とする。
   - 境界付近はUNRESOLVEDを維持する。

3. `DAILY_COARSE`
   - 日足OHLCのみ。
   - 『その日のレンジに水準が含まれた可能性』の確認にだけ使う。
   - Entry時刻より前の高安を含むため、TP/SL到達や順序の確定には使用しない。

4. `NONE`
   - 価格履歴なし。

## Resolution rule

- Entry成立時の `entry_price / initial_sl / initial_tp` は凍結。
- LONG: high >= TP でTP候補、low <= SLでSL候補。SHORTは逆。
- Entry時刻以降のデータのみ評価する。
- 同一足内でTPとSLの双方へ到達し順序不明なら `UNKNOWN_SAME_BAR`。
- Provider差、時刻基準、銘柄差が結論に影響し得る場合は `UNRESOLVED` を維持する。
- 日足レンジだけを根拠に勝ち/負けを確定しない。

## Recovery handling

RECOVERYイベントはcanonical slotではなく `evaluation_time_jst` をEntry/Direction評価時刻として使う。canonical slotは運用監査用に保持する。
