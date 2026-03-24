---
name: btc-bottom-model
description: Bitcoin bottom-timing judgment model. By tracking 6 core indicators (RSI technical oversold, volume dry-up, MVRV ratio, social media fear index, miner shutdown price, long-term holder behavior), it comprehensively evaluates whether Bitcoin has entered a bottom-fishing zone and outputs a bottom-fishing rating and position-building recommendations. When users mention topics such as Bitcoin bottom-fishing, whether BTC has bottomed out, Bitcoin oversold, MVRV, miner shutdown price, long-term holder LTH, Bitcoin fear index, whether to buy Bitcoin, BTC position entry timing, crypto market bottom signals, Bitcoin cycle bottom, etc., be sure to use this skill. Even if the user simply asks "Can I buy the dip on Bitcoin now?" or "Has BTC finished dropping?", this skill should be triggered to provide a structured analysis framework.
output:
  directory: "~/.openclaw/workspace/output/tech-earnings-deepdive"
  naming: "{YYYY-MM-DD}_BTC_bottom.{ext}"
  formats: ["html", "md"]  # HTML 优先，除非用户要求否则不输出 MD
  examples:
    - "2026-03-24_BTC_bottom.html"
    - "2026-03-20_BTC_bottom.html"
  note: "Sub-skill of tech-earnings-deepdive. All outputs go to the same directory. Default format: HTML."
---

# Bitcoin Bottom-Timing Judgment Model

This skill helps you systematically determine whether Bitcoin has entered a bottom zone worth building a position in. Through a comprehensive evaluation of 6 on-chain and market indicators, it avoids blind "catching a falling knife" style bottom-fishing and identifies entry opportunities with higher probability.

## Use Cases

Use this skill when users ask the following types of questions:
- Has Bitcoin bottomed out / Can I buy the dip
- Where is BTC in the current cycle
- Do on-chain data support building a position
- Where is the miner cost floor
- What are long-term holders doing

## Analysis Framework

### 6 Core Bottom-Fishing Indicators

For each indicator, use web_search to search for the latest data, then evaluate according to the criteria below.

#### Indicator 1: K-line Technical Indicator — RSI Oversold

**What it is**: RSI (Relative Strength Index) is a technical analysis tool that measures the speed and magnitude of price movements, with values ranging from 0-100. In simple terms: the lower the RSI, the more severe the recent decline and selling pressure. Here we focus specifically on the "weekly level" (i.e., using each week as one candlestick), because the weekly timeframe filters out the short-term noise of daily charts and better reflects medium- to long-term trends.

**Search keywords**: `Bitcoin weekly RSI` or `BTC RSI 14 current`

**Bottom signal criteria**:
- Weekly RSI < 30 → ✅ Triggered: Severely oversold, historically this level often corresponds to cycle bottom zones
- Weekly RSI 30-45 → 🟡 Approaching: Weak but not at extremes
- Weekly RSI > 45 → ❌ Not triggered: Not in an oversold state

**Key interpretation**: The number of times Bitcoin's weekly RSI has dropped below 30 in history can be counted on one hand (2015, late 2018, March 2020, late 2022), and each time corresponded to a major bottom. However, note that RSI can remain at low levels for a period of time — it doesn't mean "it bounces as soon as it bottoms."

---

#### Indicator 2: Volume Dry-up

**What it is**: After a round of panic selling, if trading volume significantly contracts (below the recent 30-day average volume), it indicates that selling pressure has been exhausted — everyone who wanted to sell has already sold. This is an important precursor to bottom formation. Volume refers to the total amount (or total value) of Bitcoin traded during a given period.

**Search keywords**: `Bitcoin trading volume 30 day average` or `BTC daily volume declining`

**Bottom signal criteria**:
- Current daily volume < 70% of 30-day average → ✅ Triggered: Selling exhaustion, selling pressure dried up
- Volume near the 30-day average → 🟡 Neutral
- Volume far above the 30-day average → ❌ Not triggered: Market is still actively selling

**Key interpretation**: The hallmark of panic selling is "high-volume crash," while the hallmark of a bottom is "low-volume base building." If the price has already dropped significantly but volume has contracted, it indicates that selling momentum is weakening.

---

#### Indicator 3: MVRV Ratio (Market Value to Realized Value)

**What it is**: This is an on-chain indicator unique to Bitcoin.
- **Market Value (market cap)** = current price × total circulating supply, which is what we commonly refer to as Bitcoin's total market cap
- **Realized Value (realized market cap)** = the total value calculated by pricing each Bitcoin at the price when it was last transferred. It can be simply understood as "the average cost basis of all holders"

When MVRV < 1.0, it means the market as a whole is at a loss (current market value is below the sum of everyone's cost basis), which has historically been an excellent long-term buying zone.

**Search keywords**: `Bitcoin MVRV ratio` or `BTC MVRV glassnode`

**Bottom signal criteria**:
- MVRV < 1.0 → ✅ Triggered: Overall market at a loss, historic bottom zone
- MVRV 1.0-1.5 → 🟡 Low but not extreme
- MVRV > 1.5 → ❌ Not triggered: Market overall in profit

**Key interpretation**: MVRV < 1 has only occurred a few times in Bitcoin's history (2011, 2015, 2018-2019, 2022), each lasting only a short period, and all were followed by enormous price increases. This is one of the most reliable cycle bottom indicators.

---

#### Indicator 4: Social Media Fear Index

**What it is**: By analyzing the sentiment of Bitcoin discussions on social platforms such as Twitter (X), Reddit, Telegram, etc., a "fear/greed" score is calculated. Commonly used tools include Alternative.me's Fear & Greed Index, as well as various sentiment analysis tools based on natural language processing. 0 = Extreme Fear, 100 = Extreme Greed.

**Search keywords**: `crypto fear and greed index` or `Bitcoin fear greed index today`

**Bottom signal criteria**:
- Fear index < 25 (Extreme Fear) → ✅ Triggered: Market is permeated with panic, often a contrarian indicator
- Fear index 25-45 → 🟡 Leaning fearful but not extreme
- Fear index > 45 → ❌ Not triggered: Market sentiment is normal or leaning greedy

**Key interpretation**: Buffett's famous quote "Be greedy when others are fearful" applies equally to the crypto market. When social media is flooded with talk of "going to zero" or "never touching it again," it's often near the bottom. However, extreme fear can persist for weeks or even months.

---

#### Indicator 5: Miner Shutdown Price

**What it is**: Bitcoin miners need to pay electricity costs to run mining machines. When the Bitcoin price drops below a certain mining machine's mining cost, operating that machine becomes unprofitable, and miners will choose to shut down. The shutdown price of mainstream miners (such as Bitmain Antminer S19 series or the newer S21 series) forms a "natural floor" — because when a large number of miners are forced to shut down, network hashrate decreases, mining difficulty adjusts, and eventually a new equilibrium is reached.

**Search keywords**: `Bitcoin mining cost per BTC` or `Bitcoin miner breakeven price` or `Antminer S19 shutdown price`

**Bottom signal criteria**:
- Current price near or below mainstream miner shutdown price → ✅ Triggered: Price approaching production cost floor
- Current price 20-50% above shutdown price → 🟡 Miners under pressure but still profitable
- Current price far above shutdown price → ❌ Not triggered: Miners are well profitable

**Key interpretation**: The miner shutdown price adjusts with changes in electricity costs, mining machine efficiency, and network difficulty. After each halving (mining reward halved), the shutdown price rises significantly. Focus on the cost floor of the latest generation of mainstream miners, not outdated and inefficient ones.

---

#### Indicator 6: Long-Term Holder Behavior (LTH — Long Term Holders)

**What it is**: On-chain data classifies addresses that have held Bitcoin for more than 155 days (approximately 5 months) as "Long-Term Holders" (LTH). LTH Supply Ratio = BTC held by long-term holders ÷ total circulating BTC supply. When this ratio increases, it means more and more coins are transferring from short-term traders to "diamond hands."

**Search keywords**: `Bitcoin long term holder supply ratio` or `BTC LTH supply glassnode`

**Bottom signal criteria**:
- LTH supply ratio continuously rising and > 70% → ✅ Triggered: Smart money is accumulating, bottom signal
- LTH supply ratio stable → 🟡 Neutral
- LTH supply ratio declining → ❌ Not triggered: Long-term holders are selling (typically occurs at bull market tops)

**Key interpretation**: Long-term holders are typically "veterans" who have experienced multiple bull and bear cycles. When they accumulate heavily at low prices, it indicates that these experienced investors believe the current price has long-term value. This is one of the most meaningful "smart money" indicators.

---

### Comprehensive Evaluation Logic

Count how many of the 6 indicators have triggered a bottom signal:

| Triggered Indicators | Bottom Rating | Position-Building Recommendation |
|-----------|---------|---------|
| 0-1 | ❌ Weak (Not recommended) | Wait and watch, no rush to enter |
| 2 | 🟡 Weak | Small exploratory position (5-10% of total position) |
| 3 | 🟡 Moderate | Begin building position in batches (10-20% of total position) |
| 4 | ✅ Strong | Batch position-building signal, can increase size (20-40% of total position) |
| 5 | ✅✅ Very Strong | Heavy position bottom-fishing signal (40-60% of total position) |
| 6 | 🔥 Extremely Strong (Historic bottom) | Maximize position (60-80% of total position), this opportunity is very rare |

**Note**: Position ratios refer to the proportion of your total funds planned for the crypto market, not your total personal assets. Please adjust according to your own risk tolerance.

## Output Format

Use the following structured template to output the analysis results:

```
# 🔍 Bitcoin Bottom-Timing Analysis Report

**Date**: [current date]
**BTC Current Price**: $[price]

## 📊 Indicator Dashboard

| Indicator | Current Value | Bottom Signal | Description |
|------|---------|---------|------|
| Weekly RSI | [value] | [Triggered/Not triggered] | [Brief description] |
| Volume Change | [relative to 30-day avg] | [Triggered/Not triggered] | [Brief description] |
| MVRV Ratio | [value] | [Triggered/Not triggered] | [Brief description] |
| Fear & Greed Index | [value] | [Triggered/Not triggered] | [Brief description] |
| Miner Shutdown Price | $[price] | [Triggered/Not triggered] | [Brief description] |
| LTH Supply Ratio | [percentage] | [Triggered/Not triggered] | [Brief description] |

## 🚦 Overall Rating

**Bottom Rating**: [Extremely Strong / Very Strong / Strong / Moderate / Weak / Not recommended]
**Triggered Indicators**: [X] / 6

## 💰 Position-Building Recommendations

[Provide specific position-building strategy based on the rating, including:]
- Recommended position ratio
- Batch entry schedule (e.g., enter in 3 batches, 1 week apart)
- Stop-loss reference level

## 📈 Historical Reference

[If multiple signals are currently triggered, mention how similar situations performed historically]

## ⚠️ Risk Disclaimer

- This model is based on historical data backtesting and does not guarantee future effectiveness
- The crypto market is extremely volatile; a "bottom" may persist for months
- Even if all indicators are triggered, prices may still drop further
- Never invest more than you can afford to lose
- DCA (dollar-cost averaging) is recommended over going all-in at once
- The above analysis is for reference only and does not constitute investment advice
```

## Execution Steps

1. First search for Bitcoin's current price
2. Use web_search to search for the latest data for each of the 6 indicators
3. If precise values for a certain indicator cannot be found, try to obtain approximate data from public reports on on-chain data platforms such as Glassnode, CoinGlass, CryptoQuant
4. Evaluate each indicator one by one according to the signal criteria
5. Count the number of triggers to arrive at an overall rating
6. Generate the report using the output template
7. Append main data source links at the end of the report

## Important Reminders

- Some on-chain data (such as MVRV, LTH Supply) require paid subscriptions to platforms like Glassnode to access precise real-time data; free searches may only find data cited by analysts or slightly delayed data
- The miner shutdown price changes with the halving cycle, electricity prices, and mining machine iterations — pay attention to data timeliness
- If reliable data for a certain indicator cannot be found, honestly state so rather than guessing
- These indicators are suitable for judging medium- to long-term cycle bottoms (weekly/monthly level), not for short-term trading
- All recommendations are for reference only and do not constitute investment advice
