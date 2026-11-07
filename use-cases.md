# 2,179 ways to use YouTube Transcript Tool

Every entry is a different job the tool can do: **what to collect** (keywords, channels and the settings
that matter), **what to do with it** (the question or analysis for your AI), and **what you build** in
the end. They're starting points — change the topic, the time window or the deliverable to fit your work.

New here? Read [Using it with AI](README.md#using-it-with-ai) and the
[big-jobs playbook](README.md#big-jobs-read-thousands-of-videos-distill-the-knowledge-build-with-it) in the
README first: most entries assume either an upload of a `combined\` file or Claude Code reading the
output folder (and, for large collections, writing `notes/` and `knowledge/`).

**Reading an entry**
- *Collect* — keywords in quotes go into `keywords` (or the window); settings in `code` go into
  `config.toml`; "channels" means *Whole channels…* / `channels = [...]`.
- *Do* — what to ask the AI, or what to have Claude Code do across the files.
- *Build* — the thing you end up with.

Transcripts are what YouTubers *say*. For health, legal and money topics the results are maps of opinion
and questions for a professional, not advice; trading ideas get backtested, not trusted. Summarise and
cite creators — don't republish their work.

## Contents

- **[Money and markets](#money-and-markets)** (220) — [Trading](#trading) · [Investing & personal finance](#investing--personal-finance) · [Crypto & web3](#crypto--web3) · [Real estate](#real-estate)
- **[Business growth](#business-growth)** (218) — [Startups & entrepreneurship](#startups--entrepreneurship) · [Marketing & advertising](#marketing--advertising) · [SEO & content marketing](#seo--content-marketing) · [Sales & customer success](#sales--customer-success)
- **[Commerce, products and market intelligence](#commerce-products-and-market-intelligence)** (218) — [E-commerce & retail](#e-commerce--retail) · [Product management & UX research](#product-management--ux-research) · [Competitive intelligence & market research](#competitive-intelligence--market-research) · [Brand, PR & reputation monitoring](#brand-pr--reputation-monitoring)
- **[AI, software and security](#ai-software-and-security)** (220) — [AI & machine learning](#ai--machine-learning) · [Software development & vibe coding](#software-development--vibe-coding) · [DevOps, cloud & homelab](#devops-cloud--homelab) · [Cybersecurity — defensive only](#cybersecurity--defensive-only)
- **[Data, automation, making and design](#data-automation-making-and-design)** (217) — [Data, analytics & building on the tool's output](#data-analytics--building-on-the-tools-output) · [No-code, automation & productivity tools](#no-code-automation--productivity-tools) · [Hardware, electronics & making](#hardware-electronics--making) · [Web design, UI/UX & graphic design](#web-design-uiux--graphic-design)
- **[Creators and media](#creators-and-media)** (217) — [YouTube creators & video production](#youtube-creators--video-production) · [Podcasting, audio & music production](#podcasting-audio--music-production) · [Writing, publishing & journalism](#writing-publishing--journalism) · [Photography, film & visual arts](#photography-film--visual-arts)
- **[Learning and research](#learning-and-research)** (217) — [Education, teaching & self-study](#education-teaching--self-study) · [Language learning](#language-learning) · [Academic research & science](#academic-research--science) · [History, philosophy, religion & the humanities](#history-philosophy-religion--the-humanities)
- **[Health, food, family and personal growth](#health-food-family-and-personal-growth)** (219) — [Health, fitness & wellbeing](#health-fitness--wellbeing) · [Food, cooking & drink](#food-cooking--drink) · [Parenting, family & relationships](#parenting-family--relationships) · [Productivity, mental models & personal development](#productivity-mental-models--personal-development)
- **[Home, hobbies, sports and travel](#home-hobbies-sports-and-travel)** (217) — [Home, DIY & vehicles](#home-diy--vehicles) · [Gaming & esports](#gaming--esports) · [Sports, coaching & outdoors](#sports-coaching--outdoors) · [Travel, culture & lifestyle](#travel-culture--lifestyle)
- **[Work, society and industry](#work-society-and-industry)** (216) — [Careers, jobs, HR & management](#careers-jobs-hr--management) · [Law, policy, government & civic life](#law-policy-government--civic-life) · [Nonprofits, community, local business & causes](#nonprofits-community-local-business--causes) · [Industries & trades](#industries--trades)

## Money and markets

### Trading

1. **Pre-market watchlist brief** — Collect: "premarket movers", "gap up stocks", `within = "today"`, `min_views = 500`. Do: list each ticker named with the creator's thesis and levels. Build: a 7am one-page brief to check against your own charts.
2. **Strategy backtest queue** — Collect: "opening range breakout", "ORB strategy", `within = "year"`, `min_duration = 600`. Do: extract exact entry, stop and target rules per video. Build: a CSV of rule sets to backtest before risking a dollar.
3. **Trading psychology flashcards** — Collect: "trading psychology", "revenge trading", "FOMO trading". Do: pull recurring mental traps and the fixes coaches propose. Build: an Anki deck of 100 cards to review before each session.
4. **Prop firm rules table** — Collect: "prop firm review", "funded account rules", `within = "month"`, `top_comments = 30`. Do: tabulate drawdown, payout and consistency rules per firm. Build: a comparison table flagged "verify on the firm's site".
5. **Options Greeks syllabus** — Collect: 4 options-educator channels, `channel_max_videos = 50`, `chapters`. Do: order delta, gamma, theta, vega, skew by prerequisite. Build: a 10-module beginner course with `timestamps` links to each explanation.
6. **Earnings-week sentiment sheet** — Collect: one keyword per ticker via `[[keyword_settings]]`, `within = "week"`. Do: tag each creator's call bull/bear/neutral with reasons. Build: a table to compare against the actual post-earnings move.
7. **Creator track-record audit** — Collect: one trading channel via `channels`, `channel_within = "year"`. Do: extract every dated price call and target. Build: a spreadsheet scoring each public call against real prices.
8. **Forex session SOP** — Collect: "London session forex", "New York open forex", `min_duration = 480`. Do: summarise which pairs and hours creators favour and why. Build: a session-by-session SOP card to run on a demo account.
9. **Futures spec cheat sheet** — Collect: "ES futures", "micro futures for beginners", "NQ futures". Do: extract stated tick values, margins, hours; flag contradictions. Build: a cheat sheet with every number marked to verify against exchange specs.
10. **Viral setup hype watch** — Collect: "trading strategy", `rising_views_per_day = 2000`, `within = "week"`. Do: find which setups are suddenly spreading and what is promised. Build: a weekly note on what new traders are being sold.
11. **Hidden-gem educator list** — Collect: "order flow trading", "footprint chart", `max_views = 5000`, `min_duration = 900`. Do: rank by depth of explanation, not views. Build: a curated list of under-the-radar educators with best-video links.
12. **Trading journal template** — Collect: "trading journal", "how I review my trades", `top_comments = 20`. Do: list the fields pros track and their review routines. Build: a spreadsheet journal plus a weekly review checklist.
13. **Signal-group scam checklist** — Collect: "trading signals group", "copy trading scam", `top_comments = 50`, `include_description`. Do: list red flags creators and commenters warn about. Build: a one-page scam checklist for beginners.
14. **Risk coach Claude skill** — Collect: 3 risk-management channels via `channels`, `sponsorblock`. Do: map->reduce into `knowledge/risk.md` on sizing and stops. Build: a Claude skill that critiques a planned trade against those principles.
15. **Indicator glossary** — Collect: "RSI explained", "VWAP explained", "MACD strategy", "ATR stop loss". Do: define each indicator, default settings and stated failure modes. Build: a searchable glossary linking the clearest explanation.
16. **Fed-day reaction log** — Collect: "FOMC", "Fed meeting market reaction", `within = "today"` via `schedule_daily.bat`. Do: compare positioning before vs reactions after. Build: a running log of Fed-day narratives versus outcomes.
17. **Options strategy decision tree** — Collect: "iron condor", "credit spread", "covered call", "straddle", `min_duration = 600`. Do: extract when each is said to fit (IV, outlook, risk). Build: a decision tree from market view to strategy, for paper trading.
18. **Swing setups digest** — Collect: "swing trade setups this week", `within = "week"`, `min_views = 1000`. Do: cluster tickers and themes repeated across creators. Build: a weekly newsletter citing each creator with links, no buy/sell calls.
19. **Exit reasoning casebook** — Collect: day-trading channels, `channel_tabs = "streams"`, `remove_filler_words`. Do: find moments where the trader explains why they exit. Build: a casebook of exits with `timestamps` to each moment.
20. **Payout-denial dataset** — Collect: "prop firm payout denied", "prop firm scam", `within = "year"`, `top_comments = 50`. Do: tag each complaint by the rule cited. Build: a dataset showing which rules most often trip traders up.
21. **Global retail strategy survey** — Collect: "day trading" in Spanish, Portuguese and Hindi via `languages`, `translate = "en"`. Do: compare the strategies each region teaches. Build: a memo on how retail trading education differs worldwide.
22. **Market-structure lesson plan** — Collect: "bid ask spread explained", "market makers explained", "order types". Do: pull accurate plain-language analogies. Build: a high-school economics lesson with 3 short clips linked via `timestamps`.
23. **Crash-day briefing** — Collect: "market crash today", "VIX spike", `within = "today"`, `rising_views_per_day = 5000`. Do: summarise what creators blame and recommend. Build: a same-day briefing separating reported facts from speculation.
24. **Backtest code generator** — Collect: "pine script strategy", "python backtesting", `subtitles_only`. Do: restate each strategy as unambiguous rules. Build: Claude Code writes backtests with out-of-sample tests for every rule set.
25. **Platform comparison table** — Collect: "thinkorswim vs tradingview", "NinjaTrader review", "best trading platform", `top_comments = 30`. Do: tabulate fees, features, complaints. Build: a comparison table with "verify" flags.
26. **Desk rules card** — Collect: "trading rules I follow", "rules for day trading", 50+ videos. Do: count how often each rule recurs across creators. Build: a printable 10-rule card ranked by consensus.
27. **Win-rate claim audit** — Collect: "90% win rate strategy", "never lose a trade", `top_comments = 30`. Do: log each statistic with its stated sample size and conditions. Build: a skeptic's sheet ranking claims by how testable they are.
28. **Position sizing calculator** — Collect: "position sizing", "risk of ruin", "kelly criterion trading". Do: reconcile the formulas and flag math errors. Build: a spreadsheet calculator with notes on where creators disagree.
29. **Trader interview database** — Collect: "funded trader interview", "trader podcast", `min_duration = 1800`. Do: extract each guest's style, timeframe, market and key lesson. Build: a filterable database of public trader interviews.
30. **Evening recap bot** — Collect: "stock market today", `within = "today"`, daily runs. Do: summarise the day's top 5 narratives with sources. Build: a Discord or Slack bot post each evening from the `combined/` file.
31. **Unusual-options-flow check** — Collect: "unusual options activity", `within = "week"`. Do: log each flagged ticker, direction and date. Build: a sheet comparing flagged flow with price two weeks later.
32. **Prop challenge prep plan** — Collect: "how I passed FTMO", "pass prop firm challenge", `min_duration = 600`. Do: extract phases, risk per trade and timelines described. Build: a 30-day challenge rehearsal plan for a demo account.
33. **Candlestick quiz** — Collect: "candlestick patterns", "price action trading", `chapters`. Do: pull each pattern's definition and the context creators say it needs. Build: a 50-question quiz with explanations and clip links.
34. **Trader tax questions** — Collect: "wash sale rule", "trader tax status", "mark to market election". Do: map what creators claim and where they conflict. Build: a question list for a CPA, explicitly not tax advice.
35. **News-day rule set** — Collect: "NFP trading", "CPI forex", `within = "year"`. Do: compare approaches to high-impact news: sit out, fade or breakout. Build: a news-day rule set to paper-test for a month.
36. **Educator content gaps** — Collect: "options trading for beginners", `within = "month"`, `top_comments = 50`. Do: find viewer questions nobody answers. Build: a 20-video content calendar for your own trading channel.
37. **Retail algo stack map** — Collect: "algorithmic trading", "trading bot python", "QuantConnect", `within = "year"`. Do: list tools, languages and data sources mentioned. Build: a landscape map of the retail algo stack.
38. **Day-job lifestyle fit** — Collect: "scalping", "swing trading with a full time job", "day trading full time". Do: extract stated screen time, hours and stress. Build: a style-vs-schedule comparison for part-time traders.
39. **Blown-account post-mortems** — Collect: "my biggest trading loss", "blew my account", `top_comments = 20`. Do: classify root causes: leverage, no stop, revenge. Build: a cause-ranked library of cautionary stories.
40. **Commodity seasonality claims** — Collect: "natural gas seasonality", "gold futures outlook", "crude oil trading", `within = "month"`. Do: extract seasonal claims. Build: a calendar of claims to check against historical charts.
41. **Course due diligence** — Collect: "<course name> review", `top_comments = 50`, `exclude_channels` = the seller's channel. Do: summarise independent opinions and complaints. Build: a questions checklist to answer before paying.
42. **Mentor matcher** — Collect: 10 educator channels, `channel_max_videos = 20`. Do: profile each by timeframe, instruments, risk style and teaching level. Build: a matrix to choose the educator that fits your goals.
43. **Psychology podcast digest** — Collect: trading psychology podcast channels, `min_duration = 2400`, `remove_filler_words`. Do: reduce each episode to 5 takeaways. Build: a weekly reading digest for people who skip audio.
44. **Platform setup SOP** — Collect: "DOM trading setup", "hotkeys day trading", `chapters`. Do: extract configuration steps in order. Build: a setup checklist for a new trading workstation.
45. **IV crush worksheet** — Collect: "IV crush explained", "earnings expected move". Do: extract worked examples and the formula used. Build: a fill-in worksheet to compute expected move before earnings.
46. **0DTE debate brief** — Collect: "0DTE options", `within = "month"`, `top_comments = 30`. Do: map arguments for and against and the evidence each side cites. Build: a balanced two-column debate brief.
47. **Retail discourse dataset** — Collect: "day trading", `within = "any"`, proxies for thousands of videos, `yt.py export`. Do: measure topic shifts by year. Build: a .jsonl research dataset and charts of retail narratives over time.
48. **Personal trading library** — Collect: your favourite educators via `channels`, `timestamps`. Do: run `yt.py find "stop loss"` and similar queries. Build: a searchable archive that jumps to the exact second something was said.
49. **Prop industry monitor** — Collect: "prop firm", `within = "today"`, daily runs. Do: watch `trends.html` for spikes in rule-change or shutdown talk. Build: a daily monitor of prop industry news.
50. **Correlation primer** — Collect: "currency correlation", "hedging forex", "DXY and gold". Do: extract stated correlations and their caveats. Build: a primer with a correlation table to verify against live data.
51. **Shorts myth sheet** — Collect: "trading tips", `include_shorts = true`, `max_duration = 60`. Do: flag oversimplified or wrong claims. Build: a myth-vs-reality explainer for beginners.
52. **Replay practice drills** — Collect: "market replay practice", "bar replay", "chart time drills". Do: extract the drills creators use and their targets. Build: a 4-week deliberate-practice schedule.
53. **Community FAQ** — Collect: your own channel via `only_channels`, `top_comments = 100`. Do: cluster recurring viewer questions. Build: a FAQ page and pinned answers for your trading Discord.
54. **OPEX explainer** — Collect: "OPEX week", "gamma exposure", "quad witching". Do: explain claims about dealer hedging and pinning. Build: an explainer plus an expiry calendar listing claims to check.
55. **Quarterly attention report** — Collect: niche keywords widened with the related keywords finder. Do: compare per-topic attention in `trends.html` over a quarter. Build: a quarterly report for a fintech marketing team.

[↑ Contents](#contents)

### Investing & personal finance

56. **Dividend research list** — Collect: "dividend stocks to buy", `within = "month"`, `min_views = 2000`. Do: tabulate tickers, stated yields, reasons and risks. Build: a research list to check yields and payout ratios yourself.
57. **Budget method chooser** — Collect: "zero based budget", "50/30/20 rule", "envelope budgeting". Do: compare steps, who each fits, and pitfalls. Build: a one-page chooser plus a starter budget spreadsheet.
58. **New-grad retirement guide** — Collect: "401k explained", "Roth IRA for beginners", `within = "year"`. Do: extract core concepts and common misunderstandings. Build: a plain-language guide with questions for HR or an advisor.
59. **ETF matchup table** — Collect: "VOO vs VTI", "SCHD vs VYM", "VT vs VTI". Do: summarise each side's arguments and fees cited. Build: a comparison table to verify on the fund providers' sites.
60. **FIRE scenario worksheet** — Collect: "coast FIRE", "lean FIRE", "FIRE movement critique". Do: extract savings rates, withdrawal assumptions and critiques. Build: a worksheet listing each assumption to stress-test.
61. **Insurance jargon decoder** — Collect: "term vs whole life insurance", "umbrella insurance explained", "deductible vs out of pocket". Do: define terms and note sales tactics flagged. Build: a glossary plus questions for an agent.
62. **Tax-prep checklist** — Collect: "tax deductions 2026", "tax refund tips", `within = "month"`. Do: list each claim and what needs verifying. Build: a document checklist and question list for your tax preparer.
63. **Kids money curriculum** — Collect: "teach kids about money", "financial literacy for kids". Do: extract age-appropriate activities and games. Build: a 6-week family or classroom activity plan.
64. **Guidance change tracker** — Collect: company earnings-call uploads via `only_channels`, `min_duration = 1800`. Do: summarise guidance, margins and tone versus last quarter. Build: a quarter-over-quarter guidance tracker.
65. **Berkshire Q&A index** — Collect: "Berkshire Hathaway annual meeting", `min_duration = 3600`, `chapters`, `timestamps`. Do: map->reduce answers by topic. Build: a topic-indexed knowledge base of public Buffett and Munger answers.
66. **Fear-cycle advice study** — Collect: "should I sell my stocks", `published_after` / `published_before` around 2020, 2022 and 2025 drawdowns. Do: compare advice by period. Build: a report on how advice shifts with fear.
67. **Workplace wellness series** — Collect: 5 educator channels, `channel_max_videos = 30`. Do: draft a curriculum on budgeting, debt and benefits. Build: a lunch-and-learn series outline that links and cites the source videos.
68. **Debt payoff calculator** — Collect: "debt snowball vs avalanche", "pay off credit card debt". Do: extract the methods and the edge cases creators raise. Build: a spreadsheet that runs both methods on your numbers.
69. **Fee drag calculator** — Collect: "expense ratio explained", "financial advisor fees worth it", "AUM fee". Do: collect fee arguments and examples. Build: a 30-year fee-impact calculator plus questions for your advisor.
70. **Bear-case stress test** — Collect: "<ticker> stock analysis", `within = "month"`, plus a `max_views = 3000` run for small analysts. Do: separate bull and bear arguments. Build: a thesis doc listing counterarguments to research.
71. **Equity comp questions** — Collect: "RSU taxes explained", "ESPP explained", "ISO vs NSO". Do: map the decisions employees face and creators' disagreements. Build: a decision worksheet to bring to a CPA.
72. **Passive vs picking debate** — Collect: "index funds vs stock picking", "Bogleheads", "why I stopped stock picking". Do: map the evidence each side cites. Build: a balanced debate summary with sources for a book club.
73. **Credit score myth sheet** — Collect: "credit score myths", `include_shorts = true`. Do: list claims and which ones contradict each other. Build: a myth-vs-fact sheet checked against credit bureau pages.
74. **HSA strategy notes** — Collect: "HSA investing", "HSA triple tax advantage". Do: summarise strategies and stated eligibility rules. Build: a one-page summary with every rule marked to verify with IRS guidance.
75. **New-parent money checklist** — Collect: "529 plan explained", "life insurance for new parents", "budget for a baby". Do: order the tasks creators recommend by urgency. Build: a first-year checklist for expecting parents.
76. **Weekly macro digest** — Collect: "recession", "interest rates", "inflation report", `within = "week"`, `min_views = 5000`. Do: summarise the dominant narratives. Build: a weekly macro section for a personal finance newsletter.
77. **Robo-advisor comparison** — Collect: "Betterment review", "Wealthfront review", "robo advisor vs DIY", `top_comments = 30`. Do: tabulate fees, features and complaints. Build: a comparison table to verify on provider sites.
78. **Side-hustle reality check** — Collect: "side hustle 2026", `top_comments = 50`. Do: compare creators' income claims with what commenters report. Build: a hype-vs-reality table of side hustles.
79. **Advisor interview script** — Collect: "questions to ask a financial advisor", "fiduciary vs broker". Do: extract questions and the warning-sign answers. Build: a printable interview script for hiring an advisor.
80. **Withdrawal strategy map** — Collect: "4% rule", "bucket strategy retirement", "sequence of returns risk". Do: map strategies and their assumptions. Build: a comparison chart to review with a planner.
81. **Social Security factors** — Collect: "when to claim social security", "spousal benefits". Do: list the factors and scenarios creators discuss. Build: a decision-factors sheet to verify on ssa.gov and with a planner.
82. **Annuity pitch decoder** — Collect: "annuity pros and cons", "indexed annuity explained", `top_comments = 30`. Do: list surrender charges, caps and riders discussed. Build: questions to ask before signing any annuity.
83. **Couples money conversation** — Collect: "joint vs separate finances", "money talk with partner". Do: extract systems couples use and conflict points. Build: a structured conversation guide for two people.
84. **Bilingual educator notes** — Collect: "finanzas personales", "invertir para principiantes", `languages = ["es"]`, `translate = "en"`. Do: compare framing with English content. Build: notes for a bilingual financial literacy class.
85. **Budget app gap analysis** — Collect: "budgeting app review", "YNAB alternatives", `top_comments = 50`. Do: extract praised features and repeated complaints. Build: a feature-gap analysis for a fintech startup.
86. **Book companion notes** — Collect: "The Intelligent Investor summary", "Psychology of Money summary". Do: align video explanations to chapters. Build: chapter-by-chapter companion notes with links.
87. **Small-cap scouting list** — Collect: "small cap stock analysis", `max_views = 2000`, `min_duration = 900`. Do: list companies covered by only one or two creators. Build: an under-covered research queue, not a buy list.
88. **Cited-answers RAG bot** — Collect: 20 finance channels, `yt.py export`. Do: embed the .jsonl and answer "what do creators say about X" with citations. Build: a private RAG assistant that always shows sources.
89. **Inflation hedge debate** — Collect: "I bonds", "TIPS explained", "gold as inflation hedge". Do: summarise each asset's case and critiques. Build: a side-by-side brief with questions to research.
90. **Frugal tips ranking** — Collect: "frugal living tips", `include_shorts = true`, 100+ videos. Do: count which tips recur and estimated savings claimed. Build: a ranked printable list for a household.
91. **Car purchase checklist** — Collect: "car loan tips", "lease vs buy car", "dealer finance office". Do: extract negotiation steps and add-ons to refuse. Build: a dealership checklist to take on the day.
92. **Estate planning questions** — Collect: "will vs trust", "beneficiary designation mistakes". Do: list concepts and common mistakes. Build: a questions list for an estate attorney, not legal advice.
93. **Cross-country investing table** — Collect: "UK ISA explained", "investing in Canada TFSA", "Australia super", `languages`. Do: compare account types by country. Build: a table for expats to verify locally.
94. **Disclosed portfolio tracker** — Collect: "dividend portfolio update", channels, `channel_within = "year"`. Do: extract holdings creators publicly disclose each month. Build: a chart of the most-held stocks among dividend YouTubers.
95. **College finance flashcards** — Collect: "compound interest explained", "APR vs APY", "credit card interest". Do: extract definitions and worked examples. Build: an Anki deck for a freshman financial literacy course.
96. **Bias pre-decision check** — Collect: "behavioral finance", "loss aversion investing", "recency bias". Do: list each bias with the investor mistake it causes. Build: a 10-question checklist to run before any big decision.
97. **IPO buzz tracker** — Collect: "IPO", `within = "week"`, `rising_views_per_day = 1000`. Do: log which listings draw hype and the claims made. Build: a tracker comparing hype with performance after 90 days.
98. **Year-end tax-loss checklist** — Collect: "tax loss harvesting", "year end tax moves". Do: extract steps and the rules creators warn about. Build: a December checklist with each rule marked to confirm with a CPA.
99. **Sponsor conflict map** — Collect: top finance channels, `include_description`, `sponsorblock = false`. Do: tally which products sponsor which channels. Build: a sponsor map so viewers can spot conflicts of interest.
100. **Automation SOP** — Collect: "automate your finances", "pay yourself first". Do: extract the transfer order and timing creators use. Build: a step-by-step SOP for setting up automatic paycheck routing.
101. **Insurance claim checklist** — Collect: "home insurance claim tips", "insurance claim denied", `top_comments = 30`. Do: extract documentation steps and pitfalls. Build: a claim-day checklist for homeowners and renters.
102. **Credentialed educator directory** — Collect: finance channels, `include_description`. Do: note which creators state CFP, CFA or CPA credentials and their topics. Build: a directory to verify through the credential bodies.
103. **Student loan monitor** — Collect: "student loan forgiveness", "SAVE plan", `within = "today"`, daily runs. Do: summarise new claims each day. Build: a daily alert where every claim links to "verify on studentaid.gov".
104. **Rebalancing rules** — Collect: "rebalancing portfolio", "threshold vs calendar rebalancing". Do: extract rule variants and their trade-offs. Build: a written rebalancing policy for your own portfolio.
105. **Call-in show problem dataset** — Collect: money call-in show channels, `min_duration = 2400`, `remove_filler_words`. Do: classify each caller's problem. Build: a dataset of the most common household money problems.
106. **Beginner investing skill** — Collect: 5 educator channels, `sponsorblock`. Do: map->reduce into `knowledge/investing.md`. Build: a Claude skill that answers with "here is what creators say, and what to verify".
107. **Narrative shift report** — Collect: "best stocks to buy now", daily runs. Do: diff the dated copies in `lists/` month over month. Build: a report on how the "hot" picks changed through the year.
108. **Freelancer tax calendar** — Collect: "1099 taxes", "quarterly estimated taxes", "self employed deductions". Do: extract deadlines and record-keeping tips. Build: a quarterly calendar checklist to confirm with a tax pro.
109. **Screener presets** — Collect: "stock screener settings", "how I find stocks", `min_duration = 600`. Do: extract each creator's screening criteria. Build: a set of screener presets to test, labelled by source.
110. **Savings rate comparison** — Collect: "high yield savings account", "money market vs HYSA", `within = "month"`. Do: list accounts and rates mentioned with dates. Build: a comparison sheet to confirm on bank sites.

[↑ Contents](#contents)

### Crypto & web3

111. **Wallet security checklist** — Collect: "seed phrase security", "crypto wallet security", `min_duration = 480`. Do: extract every protective step recommended. Build: a self-custody checklist ordered by impact.
112. **Daily scam alert digest** — Collect: "crypto scam", "fake airdrop", `within = "today"`, daily runs. Do: summarise new scam patterns reported. Build: a daily alert for a community channel with source links.
113. **DeFi concept map** — Collect: "how Aave works", "Uniswap explained", "liquidity pool explained". Do: connect concepts like collateral, liquidation and slippage. Build: a concept map with timestamped explanations.
114. **Regulation weekly brief** — Collect: "SEC crypto", "MiCA", "stablecoin bill", `within = "week"`. Do: summarise developments and attribute each claim. Build: a weekly brief with every item marked to check against official sources.
115. **Price-call audit** — Collect: 5 crypto influencer channels, `channel_within = "year"`. Do: extract dated public price predictions. Build: a scorecard comparing each call with actual prices.
116. **Narrative heatmap** — Collect: "AI crypto", "RWA tokens", "restaking", "memecoins", daily runs. Do: compare attention per narrative in `trends.html`. Build: a monthly heatmap of which narratives are rising or fading.
117. **Hardware wallet comparison** — Collect: "Ledger vs Trezor", "best hardware wallet", `top_comments = 30`. Do: tabulate features, setup issues and complaints. Build: a comparison table for buyers.
118. **Crypto tax questions** — Collect: "crypto taxes explained", "DeFi taxes", "staking rewards tax". Do: map claims and disagreements by country. Build: a question list for an accountant, not tax advice.
119. **On-chain analysis course** — Collect: "on-chain analysis", "MVRV explained", "exchange flows", `chapters`. Do: order metrics by difficulty. Build: an 8-lesson self-study course with linked explanations.
120. **Rug-pull pattern library** — Collect: "rug pull explained", "how this project scammed", `within = "any"`. Do: extract the warning signs that preceded each collapse. Build: a pattern library for due diligence.
121. **Project DD template** — Collect: "how to research altcoins", "tokenomics red flags". Do: compile the questions careful researchers ask. Build: a reusable due-diligence template with scoring.
122. **Halving claims check** — Collect: "bitcoin halving cycle", `published_after` a year before the last halving. Do: list predictions made. Build: a sheet comparing cycle claims with what happened.
123. **Staking risk table** — Collect: "ETH staking", "liquid staking risks", "restaking risks". Do: extract mechanisms, lockups and risks named. Build: a risk-comparison table for options considered.
124. **Airdrop hype check** — Collect: "airdrop", `rising_views_per_day = 3000`, `within = "week"`. Do: list hyped airdrops and the wallet permissions they need. Build: a caution list of what each one asks you to sign.
125. **Solidity learning path** — Collect: "solidity tutorial", "smart contract security basics", `min_duration = 1200`. Do: order lessons and note outdated versions. Build: a 6-week developer learning path.
126. **Exchange incident monitor** — Collect: "exchange hack", "withdrawals paused", `within = "today"`, `rising_views_per_day = 2000`. Do: flag reports about platforms you use. Build: a daily incident note to verify with the exchange.
127. **Podcast knowledge base** — Collect: 4 crypto podcast channels via `channels`, `min_duration = 2700`. Do: map->reduce each episode into `notes/`. Build: `knowledge/<topic>.md` files on L2s, regulation and stablecoins.
128. **Asian market perspectives** — Collect: Korean and Japanese crypto keywords, `languages`, `translate = "en"`. Do: compare popular tokens and narratives with English YouTube. Build: a monthly "what Asia is watching" note.
129. **Stablecoin primer for finance teams** — Collect: "stablecoins explained", "USDC vs USDT", "stablecoin reserves". Do: explain mechanics and stated risks. Build: a briefing for a CFO evaluating payments.
130. **NFT boom-bust history** — Collect: "NFT", `published_after = 2021-01-01`, `published_before = 2023-12-31`. Do: trace how narratives peaked and turned. Build: a historical report for a researcher.
131. **Layer-2 comparison** — Collect: "Arbitrum vs Optimism", "Base chain", "zk rollup vs optimistic", `within = "year"`. Do: tabulate tech, fees and trade-offs. Build: a comparison table to confirm with docs.
132. **ETF flows commentary** — Collect: "bitcoin ETF flows", `within = "week"`. Do: summarise how creators interpret inflows and outflows. Build: a weekly note comparing commentary with reported flow data.
133. **Blockchain basics lesson** — Collect: "blockchain explained simply", "what is a hash". Do: pick the clearest analogies for teenagers. Build: a 45-minute lesson plan with clip links and a quiz.
134. **Approval-scam defence guide** — Collect: "wallet drainer", "token approval scam", "revoke approvals". Do: extract how victims were tricked and how to check approvals. Build: a defensive monthly wallet-hygiene routine.
135. **DAO governance study** — Collect: "DAO governance", "governance attack", `min_duration = 900`. Do: classify governance models and failures discussed. Build: a research summary of public DAO governance debates.
136. **Conference talk digest** — Collect: "Devcon", "ETHDenver", "Bitcoin conference", `min_duration = 1200`. Do: summarise each talk's main claim. Build: a searchable digest for people who skipped the event.
137. **Small builder discovery** — Collect: "building on Solana", "web3 dev log", `max_views = 1000`. Do: list projects and the problems they target. Build: a scouting list of early builders for a grants team.
138. **Shorts vs long-form claims** — Collect: "crypto", `include_shorts = true`, then a `min_duration = 1200` run. Do: compare risk language in each format. Build: a media-literacy note on how shorts frame crypto.
139. **Crypto jargon flashcards** — Collect: "crypto terms explained", "DeFi glossary". Do: extract definitions with examples. Build: an Anki deck of 150 terms for newcomers.
140. **Public founder statements timeline** — Collect: interviews with a named public crypto CEO, `min_duration = 1200`, `timestamps`. Do: extract claims about plans and dates. Build: a timeline comparing statements with outcomes.
141. **Token comment sentiment** — Collect: "<token> news", `within = "week"`, `top_comments = 50`. Do: classify comment mood and recurring concerns. Build: a weekly sentiment chart for a project's community team.
142. **Bear market lessons** — Collect: "crypto bear market", `published_after = 2022-05-01`, `published_before = 2023-06-30`. Do: extract what holders say they learned. Build: a lessons document to reread during euphoria.
143. **Inheritance plan questions** — Collect: "crypto inheritance", "what happens to crypto when you die". Do: list approaches and failure modes. Build: questions for an estate attorney plus a key-access documentation outline.
144. **Gas fee tips** — Collect: "lower gas fees", "when are gas fees cheapest". Do: extract practical tips and when they apply. Build: a cheat sheet for users of each chain.
145. **Wallet app gap analysis** — Collect: "best crypto wallet app", "wallet app review", `top_comments = 50`. Do: extract UX complaints and wishes. Build: a feature-priority list for a wallet product team.
146. **Sponsored content check** — Collect: crypto channels, `include_description`, `sponsorblock = false`. Do: tally promoted exchanges and tokens. Build: a disclosure table showing which creators promote what.
147. **Trading bot claims** — Collect: "crypto trading bot", "grid bot results", `top_comments = 30`. Do: log claimed returns and conditions. Build: a list of claims to backtest on historical data before use.
148. **Lightning dev notes** — Collect: "Lightning Network tutorial", "run a bitcoin node", `chapters`. Do: extract setup steps and common errors. Build: a node-setup SOP for a home server.
149. **Jurisdiction comparison** — Collect: "crypto regulation" per country, `languages`, `translate`. Do: summarise rules creators describe per country. Build: a comparison table flagged to verify with regulators.
150. **Research dataset** — Collect: 50 crypto channels, proxies, `yt.py export`. Do: tag topics by month. Build: a .jsonl and .csv dataset for academic work on crypto discourse.
151. **Mining economics sheet** — Collect: "bitcoin mining profitability", "home mining setup". Do: extract hardware, power and cost figures stated. Build: a profitability spreadsheet with inputs to replace with your own numbers.
152. **ZK proofs explainer** — Collect: "zero knowledge proofs explained", "zk snarks", `min_duration = 600`. Do: layer explanations from analogy to math. Build: a three-level explainer for a blog post with citations.
153. **Story leads for journalists** — Collect: crypto keywords, `rising_views_per_day = 5000`, `within = "today"`. Do: list projects suddenly getting attention. Build: a lead sheet of stories to report independently.
154. **Family scam guide** — Collect: "crypto romance scam", "pig butchering scam", "fake crypto investment". Do: extract how victims were approached. Build: a plain-language guide for older relatives.
155. **Pre-crash archive** — Collect: "best altcoins", daily runs. Do: use dated `lists/` copies to show what was promoted before a drop. Build: an evidence-backed retrospective of promoted tokens.
156. **Token unlock watch** — Collect: "token unlock", "vesting schedule", `within = "month"`. Do: note tokens creators flag for upcoming unlocks. Build: a calendar to cross-check with official tokenomics docs.
157. **Bridge risk explainer** — Collect: "crypto bridge hack", "how bridges work". Do: extract how bridge failures happened. Build: a risk explainer with a pre-bridge checklist.
158. **Weekly crypto newsletter** — Collect: 10 keywords, `within = "week"`, `min_views = 10000`, `sponsorblock`. Do: summarise top stories, citing creators. Build: a weekly newsletter draft from the `combined/` files.
159. **Brand mention monitor** — Collect: your company's name, `title_must_contain`, daily runs, `top_comments = 30`. Do: flag misinformation and support complaints. Build: a daily report for compliance and support teams.
160. **Web3 game reviews** — Collect: "web3 game review", "play to earn", `top_comments = 30`. Do: separate gameplay opinions from token talk. Build: a review roundup table for gamers.
161. **Hackathon idea bank** — Collect: conference talks, `min_duration = 1200`. Do: extract problems speakers call unsolved. Build: an idea bank for hackathon teams with source links.
162. **Treasury company commentary** — Collect: "bitcoin treasury company", "MicroStrategy bitcoin", `within = "month"`. Do: map bull and bear arguments. Build: a debate brief on corporate bitcoin treasuries.
163. **CBDC debate map** — Collect: "CBDC", "digital euro", "digital dollar", `languages`, `translate`. Do: map privacy, policy and adoption arguments. Build: a balanced debate map for a civics class.
164. **Onboarding pain points** — Collect: "how to buy crypto for beginners", `top_comments = 50`. Do: extract where commenters got stuck. Build: a UX research summary for an exchange's onboarding team.
165. **Claim checker skill** — Collect: security and scam-awareness channels, `sponsorblock`. Do: map->reduce into `knowledge/crypto-redflags.md`. Build: a Claude skill that flags red flags in any pasted crypto pitch.

[↑ Contents](#contents)

### Real estate

166. **Rental deal analyzer** — Collect: "rental property analysis", "cash on cash return", `min_duration = 600`. Do: extract formulas and default assumptions used. Build: a deal spreadsheet with each assumption editable and sourced.
167. **House hacking playbook** — Collect: "house hacking", "buy a duplex live in one unit". Do: extract steps, financing types and pitfalls. Build: a step-by-step playbook for a first-time buyer.
168. **BRRRR SOP** — Collect: "BRRRR method", "cash out refinance rental", `chapters`. Do: order each stage with the risks named. Build: an SOP with checkpoints for each stage.
169. **Flip overrun library** — Collect: "house flip gone wrong", "flipping mistakes", `top_comments = 20`. Do: classify overruns by cause. Build: a contingency checklist and budget buffer guide.
170. **Mortgage rate commentary** — Collect: "mortgage rates", `within = "week"`, `min_views = 2000`. Do: summarise forecasts and reasoning. Build: a weekly note that logs forecasts to compare with actual rates later.
171. **Lender question list** — Collect: "first time home buyer mistakes", "questions to ask a mortgage lender". Do: extract questions and fee traps. Build: a printable list for lender calls.
172. **Commission rule explainer** — Collect: "NAR settlement", "buyer agent commission", `within = "year"`. Do: summarise how creators interpret changes. Build: an explainer for buyers to confirm with their agent and state rules.
173. **Tenant screening SOP** — Collect: "tenant screening", "rental application process". Do: extract steps and fair housing cautions raised. Build: a consistent screening SOP to review with a local attorney.
174. **City market comparison** — Collect: "<city> housing market" per city via `[[keyword_settings]]`, `within = "month"`. Do: compare inventory, price and sentiment claims. Build: a city-by-city table to check with MLS data.
175. **CRE metrics primer** — Collect: "cap rate explained", "NOI", "DSCR", `chapters`. Do: extract definitions and worked examples. Build: a commercial underwriting primer with practice problems.
176. **STR regulation watch** — Collect: "Airbnb ban", "short term rental rules", `within = "month"`. Do: list cities discussed and rules claimed. Build: a watchlist to verify with each city's code.
177. **Landlord law questions** — Collect: "landlord tenant law", "security deposit rules". Do: map common disputes and claims by state. Build: a question list for a local attorney, not legal advice.
178. **Agent content calendar** — Collect: "buying a home in <your city>", `top_comments = 50`. Do: extract buyers' unanswered questions. Build: a 12-week video and blog calendar for a local agent.
179. **Inspection red flags** — Collect: "home inspection red flags", "what inspectors look for". Do: extract issues and rough costs mentioned. Build: a walkthrough checklist to bring to showings.
180. **Contractor bid SOP** — Collect: "hiring contractors for flips", "scope of work template". Do: extract how investors scope, bid and pay draws. Build: a bid-comparison sheet and draw schedule template.
181. **1031 exchange questions** — Collect: "1031 exchange explained", "1031 mistakes". Do: list timelines and pitfalls claimed. Build: questions for a qualified intermediary and CPA.
182. **Syndication due diligence** — Collect: "real estate syndication red flags", "passive investing syndication", `top_comments = 30`. Do: extract questions to ask sponsors. Build: an LP due-diligence questionnaire.
183. **REIT vs direct comparison** — Collect: "REIT vs rental property", "REITs explained". Do: compare returns, effort, liquidity and taxes discussed. Build: a decision table for a passive investor.
184. **Wholesaling legality map** — Collect: "wholesaling real estate legal", "wholesaling license required". Do: list states creators flag as restricted. Build: a map of claims to verify with state real estate commissions.
185. **Renovation ROI table** — Collect: "renovations that add value", "worst renovations for resale". Do: tabulate projects and claimed returns. Build: a ranked table to check against local appraiser opinion.
186. **License exam flashcards** — Collect: "real estate exam prep", "real estate math", `chapters`. Do: extract terms and formula problems. Build: an Anki deck for license exam study.
187. **Crash prediction audit** — Collect: "housing market crash", `within = "any"`, older runs via `published_before`. Do: extract dated predictions. Build: a scorecard of public housing crash calls versus outcomes.
188. **Small-market investor finds** — Collect: "investing in small town rentals", `max_views = 3000`. Do: list towns and reasons named. Build: a scouting list of markets to research with local data.
189. **PM hiring guide** — Collect: "hiring a property manager", "property management fees". Do: extract fee structures and contract red flags. Build: an interview script and contract checklist.
190. **Section 8 pros and cons** — Collect: "Section 8 rental investing", `top_comments = 30`. Do: map landlords' reported pros, cons and processes. Build: a balanced brief to verify with the local housing authority.
191. **Renter rights guide** — Collect: "tenant rights", "landlord won't fix", "renters rights". Do: extract common issues and what to document. Build: a renter's documentation guide noting local laws vary.
192. **Loan type explainer** — Collect: "FHA vs conventional", "VA loan explained", "ARM vs fixed". Do: compare requirements and trade-offs stated. Build: a comparison table to confirm with a lender.
193. **Rent pricing method** — Collect: "how to price rent", "rent comps". Do: extract methods landlords use. Build: a rent-setting worksheet with comp fields.
194. **STR listing optimization** — Collect: "Airbnb listing tips", "Airbnb photos", "superhost tips". Do: extract changes hosts credit for bookings. Build: a listing audit checklist.
195. **Office distress monitor** — Collect: "office real estate crisis", "CRE loan defaults", `within = "week"`. Do: summarise distress narratives by city. Build: a weekly CRE distress note for an analyst.
196. **Buying abroad research** — Collect: "buying property in Portugal", "buy house Mexico foreigner", `languages`, `translate`. Do: extract processes and pitfalls. Build: a country checklist for a lawyer consultation.
197. **Seller prep checklist** — Collect: "home staging tips", "preparing house to sell". Do: order tasks by cost and claimed impact. Build: a 30-day pre-listing checklist.
198. **Underwriting assistant skill** — Collect: 4 real estate podcast channels, `min_duration = 2400`, `sponsorblock`. Do: map->reduce into `knowledge/underwriting.md`. Build: a Claude skill that challenges assumptions in a deal you paste.
199. **Land investing notes** — Collect: "land investing", "raw land due diligence". Do: extract due diligence steps like zoning, access and utilities. Build: a land DD checklist.
200. **Mobile home park primer** — Collect: "mobile home park investing", `min_duration = 900`. Do: summarise economics and risks discussed. Build: a primer for an investor considering the niche.
201. **Self-storage primer** — Collect: "self storage investing", "storage facility conversion". Do: extract metrics and risks. Build: a one-page niche overview with research questions.
202. **Brokerage training course** — Collect: 5 agent-training channels, `channel_max_videos = 40`, `chapters`. Do: organise into new-agent topics. Build: a 90-day onboarding curriculum linking to source videos.
203. **Ethical negotiation scripts** — Collect: "real estate negotiation", "how to negotiate a house price". Do: extract honest tactics and when they apply. Build: a negotiation prep sheet for buyers.
204. **Closing cost checklist** — Collect: "closing costs explained", "closing disclosure review". Do: extract fees and errors to catch. Build: a checklist for reviewing a closing disclosure with your lender.
205. **Down payment aid list** — Collect: "down payment assistance", "first time buyer grants", `within = "year"`. Do: list programs creators mention by state. Build: a list to verify with state housing agencies.
206. **HOA red flags** — Collect: "HOA red flags", "HOA special assessment", `top_comments = 30`. Do: extract documents to request and warning signs. Build: an HOA review checklist for buyers.
207. **Proptech landscape** — Collect: "property management software", "real estate CRM review", `within = "year"`. Do: list tools and complaints by category. Build: a landscape map for a proptech founder.
208. **Climate-risk insurance brief** — Collect: "Florida home insurance crisis", "California insurance non renewal", `within = "month"`. Do: summarise reported premium trends. Build: a brief for buyers to verify with insurers.
209. **Housing sentiment dataset** — Collect: "housing market", proxies, `within = "any"`, `yt.py export`. Do: score sentiment by month. Build: a dataset correlating creator sentiment with sales data for research.
210. **Morning housing news bot** — Collect: "housing market news", "mortgage news", `within = "today"`, daily runs. Do: summarise top stories. Build: a Slack post each morning for a brokerage team.
211. **ADU build guide** — Collect: "build an ADU", "ADU cost breakdown", `chapters`. Do: extract phases, permits and cost ranges. Build: a phase plan with permit questions for the city.
212. **Rent vs buy debate** — Collect: "rent vs buy", "is buying a house worth it". Do: map the assumptions each side uses. Build: a calculator template where you plug in your own numbers.
213. **Investor tax questions** — Collect: "cost segregation", "real estate depreciation", "real estate professional status". Do: list strategies and their stated conditions. Build: questions for a real estate CPA.
214. **Lease clause library** — Collect: "lease clauses landlords", "rental agreement tips". Do: extract clauses and the problems each addresses. Build: a clause checklist to review with an attorney.
215. **Eviction process overview** — Collect: "eviction process" with state names, `title_must_contain`. Do: summarise described steps and timelines by state. Build: an overview marked "verify with local court".
216. **Commercial lease terms** — Collect: "commercial lease negotiation", "triple net lease explained". Do: extract terms and negotiation points. Build: a term-sheet checklist for a small business tenant.
217. **Deal sourcing methods** — Collect: "off market deals", "driving for dollars", "direct mail real estate". Do: compare methods by cost, time and compliance notes. Build: a sourcing strategy comparison table.
218. **Affordability lesson** — Collect: "housing affordability crisis", "why houses are expensive". Do: pick clips covering supply, rates and zoning. Build: a high-school economics lesson with discussion questions.
219. **Low appraisal playbook** — Collect: "appraisal came in low", "appraisal gap". Do: extract options buyers and sellers describe. Build: a decision tree for a low-appraisal scenario to discuss with your agent.
220. **Guru course vetting** — Collect: "<real estate course> review", `top_comments = 50`, `exclude_channels` = the seller. Do: summarise independent experiences. Build: a vetting checklist before buying any investing course.

[↑ Contents](#contents)

## Business growth

### Startups & entrepreneurship

221. **Failure pre-mortem** — Collect: "why my startup failed", "shutting down my startup", `within = "year"`. Do: tag each story's root cause (no demand, cofounder split, ran out of cash). Build: a pre-mortem checklist to score your own idea against.
222. **Pain-point miner** — Collect: "I hate [tool]", "[industry] software is broken", `top_comments = 30`. Do: extract recurring complaints from transcripts and comments, count repeats. Build: a ranked problem list with timestamp evidence for validation.
223. **Pitch critic skill** — Collect: channels of accelerators and VC podcasts, every video. Do: map -> reduce into `knowledge/pitching.md` of recurring investor objections. Build: a Claude skill that critiques your deck and cites the source timestamps.
224. **Deck teardown checklist** — Collect: "pitch deck teardown", "seed deck review", `min_duration = 600`. Do: list what reviewers praise or cut slide by slide. Build: a slide-by-slide checklist with common red flags per slide.
225. **Term sheet glossary** — Collect: "term sheet explained", "liquidation preference", "pro rata rights". Do: define each term as explainers describe it, note disagreements. Build: a glossary plus a list of questions to ask your lawyer before signing.
226. **Founder story dataset** — Collect: founder interview podcast channels, `channel_max_videos = 300`. Do: extract founder age, idea origin, months to first revenue, funding path. Build: a CSV dataset via `yt.py export` for spotting patterns.
227. **Daily funding briefing** — Collect: "raises seed round", "series A", `within = "today"`, `schedule_daily.bat`. Do: summarise who raised, sector and what founders say they'll build. Build: a 5-minute morning briefing for an angel investor.
228. **Bakery startup costs** — Collect: "how much it cost to open my bakery", "opening a coffee shop cost". Do: pull every cost line owners mention (lease, ovens, permits). Build: a startup cost table per business type, marked as anecdotal ranges.
229. **Franchise due diligence** — Collect: "franchise owner honest review", "[brand] franchise regrets", `top_comments = 20`. Do: list hidden fees and support problems owners describe. Build: questions to put to the franchisor and a franchise attorney.
230. **Bootstrap vs VC map** — Collect: "bootstrapping vs venture capital", "why I didn't raise", `within = "year"`. Do: sort arguments by stage, business model and founder goals. Build: a comparison table and a decision tree for your situation.
231. **Customer interview script** — Collect: "customer discovery interviews", "the mom test", "problem interview mistakes". Do: extract good vs leading questions with examples. Build: a printable interview script and a note-taking template.
232. **SaaS pricing experiments** — Collect: "how we priced our SaaS", "raised prices", `chapters`. Do: list each pricing change founders describe and its claimed effect. Build: an experiment log of pricing tests to try, ordered by risk.
233. **Niche demand radar** — Collect: 30 idea keywords like "AI agent for [niche]", `rising_views_per_day = 500`, daily runs. Do: watch `trends.html` for niches gaining attention. Build: a weekly shortlist of emerging niches with view-velocity notes.
234. **Competitor founder watch** — Collect: `only_channels` = competing founders' public channels, `channel_within = "week"`. Do: note announced features, pricing hints, roadmap talk. Build: a dated competitor changelog in `lists/`.
235. **Launch-day SOP** — Collect: "Product Hunt launch", "how we launched", `within = "year"`. Do: build a timeline of what founders did T-30 days to T+7. Build: a launch SOP with owner, task and day for each step.
236. **Cofounder split worksheet** — Collect: "cofounder equity split", "vesting cliff explained", "cofounder breakup". Do: list factors founders weigh and conflicts they regret. Build: a discussion worksheet two cofounders fill in before talking to a lawyer.
237. **Entrepreneurship case pack** — Collect: university entrepreneurship lecture channels, `min_duration = 1800`. Do: pick 8 founder talks, summarise decision points. Build: classroom case studies with discussion questions and timestamped clips.
238. **Ecosystem outside the US** — Collect: "startup India", "Gründerszene", "startup Brasil", `languages`, `translate`. Do: compare funding climate, regulation and talent themes per region. Build: a regional startup ecosystem brief for a global investor.
239. **First-hire scorecard** — Collect: "first employee startup", "hiring mistakes early stage", `exclude_words = "Shorts"`. Do: extract traits and interview questions founders recommend. Build: a hiring scorecard template for employee #1-#5.
240. **Time to $1k MRR** — Collect: "indie hacker MRR", "my SaaS reached", `max_views = 30000`. Do: extract months from start to each revenue milestone. Build: a timeline chart dataset showing realistic ranges for solo founders.
241. **Grant application prep** — Collect: "SBIR grant tips", "Innovate UK grant", "EIC accelerator application". Do: list what applicants say reviewers rewarded. Build: a grant checklist to verify against each program's official rules.
242. **Entity choice questions** — Collect: "Delaware C corp vs LLC", "where to incorporate startup". Do: map trade-offs creators describe and where they disagree. Build: a question list for an accountant and lawyer, not a recommendation.
243. **Founder burnout map** — Collect: "founder burnout", "founder mental health", `within = "year"`. Do: catalogue warning signs and coping habits founders describe. Build: a self-check page with resources, framed as experiences, not medical advice.
244. **TV pitch deal dataset** — Collect: "Dragons' Den pitch", "Shark Tank pitch" clips; repeat detection drops re-uploads. Do: extract ask, valuation, objections, outcome. Build: a dataset of why investors say no, for pitch prep.
245. **FBA beginner traps** — Collect: "Amazon FBA mistakes", "FBA first year results", `min_views = 10000`. Do: list mistakes and the cost each one caused. Build: a beginner checklist sorted by how often the mistake comes up.
246. **Cleaning business 90 days** — Collect: "how I started a cleaning business", "first cleaning clients", `max_views = 50000`. Do: sequence the steps owners took to first 10 clients. Build: a 90-day launch plan with weekly goals.
247. **Metrics flashcards** — Collect: "CAC LTV explained", "burn multiple", "net revenue retention explained". Do: extract definitions, formulas and example numbers. Build: Anki flashcards for a first-time founder preparing for investor meetings.
248. **Investor thesis tracker** — Collect: channels of VC firms and partner podcasts, `channel_within = "month"`. Do: note sectors and signals each firm says it's backing. Build: a table matching your startup to investors whose public thesis fits.
249. **Demo day anatomy** — Collect: "demo day pitch", accelerator demo day playlists. Do: time when each pitch states problem, traction and ask using `timestamps`. Build: stats on pitch structure plus a 2-minute pitch template.
250. **Accelerator comparison** — Collect: "YC experience", "Techstars review", "is an accelerator worth it", `top_comments = 20`. Do: compare equity taken, perks, and alumni complaints. Build: a comparison table for choosing where to apply.
251. **No-code MVP stack** — Collect: "built my MVP with no code", "Bubble vs Webflow MVP", `within = "year"`. Do: list tools used, limits hit, when founders rebuilt in code. Build: a decision tree for picking an MVP stack.
252. **AI moat memo** — Collect: "AI startup moat", "GPT wrapper", "defensibility AI", `within = "month"`. Do: summarise each argument for and against thin AI startups. Build: a 2-page memo for a board discussion on defensibility.
253. **Exit prep checklist** — Collect: "how I sold my business", "acquisition process founder", "Acquire.com sale". Do: extract what buyers asked for and what delayed deals. Build: an exit-readiness checklist to start 12 months before selling.
254. **Buying a small business** — Collect: "buying a business SBA loan", "search fund", "acquisition entrepreneurship". Do: list screening criteria and deal-killers buyers mention. Build: deal screening questions to review with a broker and accountant.
255. **Founder newsletter** — Collect: 15 startup keywords, `within = "week"`, `min_views = 20000`, `sponsorblock`. Do: pick the five most useful ideas of the week with timestamp links. Build: a weekly founder newsletter that summarises and cites.
256. **Founder-talk RAG bot** — Collect: 50 founder and investor channels, all videos, proxies for scale. Do: `yt.py export` to .jsonl, embed chunks. Build: a RAG chatbot that answers startup questions and links to the exact second it quotes.
257. **Pivot pattern catalogue** — Collect: "how we pivoted", "our pivot story", `min_duration = 480`. Do: classify the trigger (churn, sales cycle, new insight) and what changed. Build: a catalogue of pivot patterns with warning signals.
258. **Solopreneur week plan** — Collect: "solopreneur daily routine", "one person business schedule", `max_views = 50000`. Do: extract how time splits across build, sell, admin. Build: time-block templates for a one-person business.
259. **Student club syllabus** — Collect: "startup school lecture", "how to start a startup" playlists. Do: map topics into 6 sessions with key clips. Build: a student entrepreneurship club syllabus with timestamped viewing and exercises.
260. **Market sizing worksheet** — Collect: "TAM SAM SOM explained", "bottom-up market sizing". Do: extract the methods and common mistakes investors call out. Build: a fill-in market sizing worksheet with a worked example.
261. **Board meeting kit** — Collect: "how to run a board meeting", "startup board deck", `chapters`. Do: extract agenda items, cadence and prep tips. Build: a board meeting agenda and deck template for a newly funded startup.
262. **Crowdfunding postmortems** — Collect: "Kickstarter campaign postmortem", "what I'd do differently Kickstarter". Do: extract pre-launch steps, budget surprises, shipping delays. Build: a campaign timeline and budget checklist.
263. **Build-in-public norms** — Collect: "build in public", "sharing my revenue publicly", `top_comments = 25`. Do: list which metrics founders share and how audiences react. Build: a guide on what to disclose and what to keep private.
264. **Remote startup ops** — Collect: "remote first startup", "async company culture", `within = "year"`. Do: extract rituals, tools and documents founders say they rely on. Build: an operations SOP for a 5-15 person remote team.
265. **Hardware risk register** — Collect: "hardware startup manufacturing", "working with a factory in Shenzhen", `min_duration = 900`. Do: list risks (tooling, MOQ, certifications) and fixes. Build: a manufacturing risk register.
266. **Climate tech market map** — Collect: "climate tech startup", "carbon removal startup", `within = "year"`, `min_views = 3000`. Do: group companies mentioned by sub-sector and business model. Build: a market map table with source links.
267. **Talk quote finder** — Collect: your saved founder library. Do: `yt.py find "default alive"` and similar phrases across all transcripts. Build: slide quotes for your own talk, each attributed with a link to the exact second.
268. **Investor update template** — Collect: "monthly investor update", "how to write investor updates". Do: extract sections investors say they read and what annoys them. Build: an investor update template plus a Claude prompt to draft it from your metrics.
269. **Startup job due diligence** — Collect: `only_channels` = the hiring founder's public channel and podcast guest spots. Do: list claims about runway, roadmap and culture. Build: questions to ask in your interview before joining.
270. **Bank loan business plan** — Collect: "small business loan approval tips", "business plan for bank". Do: extract what loan officers say they look for. Build: a business plan outline tailored for a lender, with items to confirm with your bank.
271. **Etsy first-year ledger** — Collect: "Etsy shop first year", "Etsy fees explained", `max_views = 40000`. Do: extract fees, material costs and hours sellers report. Build: a profit-and-time ledger template for a craft side business.
272. **Contradiction map** — Collect: top startup advisors' channels. Do: find topics where they give opposite advice (raise early vs late, niche vs broad). Build: an "it depends" decision tree showing which conditions favor each view.
273. **Idea validator skill** — Collect: "validate startup idea", "landing page smoke test", "pre-sell before building". Do: map -> reduce into `knowledge/validation.md`. Build: a Claude skill that walks you through validation steps and kill criteria.
274. **Small-town business ideas** — Collect: "business ideas small town", "rural business success", `max_views = 30000`, `top_comments = 30`. Do: list businesses owners say work in low-density areas and why. Build: an idea shortlist with local demand questions.

[↑ Contents](#contents)

### Marketing & advertising

275. **Meta creative test matrix** — Collect: "Facebook ads creative testing", "Meta Advantage+", `within = "month"`. Do: extract test structures, budgets and kill rules media buyers describe. Build: a creative testing spreadsheet template.
276. **Ads platform change log** — Collect: "Google Ads update", "Meta ads new feature", `within = "today"`, daily runs. Do: summarise each reported change and who is affected. Build: a running change log, flagged until confirmed by official docs.
277. **Google Ads audit** — Collect: "Google Ads audit", "wasted ad spend", `min_duration = 600`, `chapters`. Do: extract each check auditors run and the fix. Build: an account audit checklist an agency junior can run in an hour.
278. **Subject line test plan** — Collect: "email subject lines that work", "open rate tips", `within = "year"`. Do: name the principles behind examples (curiosity, specificity). Build: a list of principles and an A/B test plan, not a copied swipe file.
279. **Deliverability checklist** — Collect: "Gmail sender requirements", "DMARC setup", "emails going to spam". Do: list technical steps and warm-up advice with dates. Build: a deliverability checklist to verify against provider documentation.
280. **Welcome sequence outline** — Collect: "welcome email sequence", "onboarding emails ecommerce", `top_comments = 15`. Do: extract email order, timing and purpose of each. Build: a 7-email welcome sequence outline for your brand.
281. **Short-form hook bank** — Collect: "TikTok hooks", "Reels hook", `include_shorts`, `max_duration = 60`, `within = "week"`. Do: classify opening lines by hook type. Build: a hook framework list with patterns to adapt in your own words.
282. **Micro-influencer shortlist** — Collect: niche keywords, `min_views = 2000`, `max_views = 50000`, `within = "month"`. Do: score each public channel's topic fit and what viewers ask in comments. Build: a sheet of micro-creators to pitch.
283. **Sponsor read study** — Collect: niche videos with `sponsorblock` off. Do: compare how creators integrate sponsors: placement minute, length, disclosure wording. Build: a brief for your influencer campaign on formats that feel natural.
284. **Brand share of voice** — Collect: category keywords, `within = "month"`. Do: count mentions of your brand vs competitors in transcripts using keyword mentions. Build: a monthly share-of-voice chart for the marketing team.
285. **Copy formula flashcards** — Collect: "copywriting formulas", "AIDA PAS explained", "direct response copywriting". Do: extract each formula with a structure and example. Build: flashcards for a junior copywriter.
286. **Landing page CRO checklist** — Collect: "landing page teardown", "conversion rate optimization", `min_views = 5000`. Do: list each critique and the suggested fix. Build: a CRO checklist sorted by page section.
287. **Webinar funnel map** — Collect: "webinar funnel", "evergreen webinar", `chapters`. Do: extract each funnel stage, tool and conversion claim. Build: a funnel diagram with metrics to track, claims marked as unverified.
288. **Agency onboarding SOP** — Collect: "agency client onboarding", "marketing agency process", `within = "year"`. Do: list steps, documents and access requests. Build: a client onboarding SOP and kickoff questionnaire.
289. **Brand perception report** — Collect: "[brand] review", "[brand] honest opinion", `top_comments = 50`. Do: cluster praise and complaints across reviews and comments. Build: a brand perception report with quotes linked by `timestamps`.
290. **Launch reaction dashboard** — Collect: your product name, `within = "today"`, `rising_views_per_day = 1000`. Do: summarise first-day reactions and confusion points. Build: a launch-day reaction dashboard from `trends.html` and `video_list.html`.
291. **Big game ad ranking** — Collect: "Super Bowl ads", `published_after` game day, `top_comments = 30`. Do: rank ads by attention and how reviewers explain wins and flops. Build: a ranking table with lessons for your own creative.
292. **Intern marketing course** — Collect: "digital marketing for beginners" from 5 educator channels. Do: map topics into 8 modules. Build: an intern onboarding course with timestamped videos, quizzes and a mini project per module.
293. **LinkedIn post rules** — Collect: "LinkedIn algorithm", "LinkedIn posting strategy", `within = "month"`. Do: list claims and where creators disagree. Build: a posting-rules sheet for B2B staff, with claims to test on your own account.
294. **Tracking setup guide** — Collect: "server side tracking", "GA4 setup", "Conversions API", `min_duration = 600`. Do: extract implementation steps and common errors. Build: an implementation checklist for your analytics engineer.
295. **Privacy change memo** — Collect: "cookie deprecation", "consent mode v2", "iOS privacy ads", `within = "year"`. Do: summarise how marketers say measurement changes. Build: an impact memo with questions for your privacy counsel.
296. **Budget benchmark claims** — Collect: "marketing budget percentage", "CAC benchmarks ecommerce". Do: log every benchmark number with source and date. Build: a spreadsheet of claimed benchmarks to verify before using in planning.
297. **Voice-of-customer phrases** — Collect: product category reviews, `top_comments = 40`. Do: extract the words buyers use for problems and outcomes. Build: a phrase bank for ad copy in customers' own language.
298. **Retargeting playbook** — Collect: "retargeting ads strategy", "remarketing audiences", `within = "year"`. Do: list audience windows, frequency caps and creative per stage. Build: a retargeting setup sheet per funnel stage.
299. **Affiliate program compare** — Collect: "best affiliate programs [niche]", "affiliate marketing honest", `max_views = 100000`. Do: compare commission, cookie length and complaints. Build: a comparison table with terms to verify on each site.
300. **Podcast ad buying** — Collect: "podcast advertising results", "host read ads", `top_comments = 15`. Do: extract pricing models, tracking methods and what brands learned. Build: a podcast ad buying checklist.
301. **Solo creator calendar** — Collect: your niche keywords, `within = "week"`, related keywords finder. Do: spot recurring audience questions. Build: a 4-week content calendar for a solopreneur's personal brand.
302. **Ad localization notes** — Collect: category keywords in target markets, `languages = ["ja","de"]`, `translate`. Do: compare appeals, humor and claims local creators use. Build: localization notes for adapting ads per market.
303. **Exec jargon glossary** — Collect: "ROAS vs MER", "incrementality explained", "attribution models". Do: extract plain-language definitions. Build: a one-page glossary for executives reading marketing reports.
304. **Agency pitch angles** — Collect: `only_channels` = the prospect company's channel and its CEO's public interviews. Do: list stated priorities and challenges. Build: pitch angles and discovery questions for the agency's first meeting.
305. **Ad copy reviewer skill** — Collect: 10 direct-response and ad creative channels, all videos. Do: map -> reduce into `knowledge/ad-copy.md`. Build: a Claude skill that reviews your draft ads against those principles and cites sources.
306. **Pinterest strategy** — Collect: "Pinterest marketing", "Pinterest for business", `within = "year"`. Do: extract pin formats, posting cadence and traffic claims. Build: a Pinterest launch checklist for a home-decor shop.
307. **Community marketing rules** — Collect: "Reddit marketing", "community led growth", `top_comments = 30`. Do: list what communities reward and what gets brands banned. Build: honest participation guidelines for your team.
308. **SMS compliance questions** — Collect: "SMS marketing compliance", "TCPA texting rules". Do: list the rules creators mention and where they disagree. Build: a question list for counsel before launching SMS, not legal guidance.
309. **Viral campaign library** — Collect: "marketing campaign case study", "why this ad went viral", `min_views = 50000`. Do: extract idea, channel, budget hints, result. Build: a searchable case library in `knowledge/campaigns.md`.
310. **Shorts vs long form** — Collect: "shorts vs long form", "does posting shorts hurt", `within = "month"`. Do: compare creators' reported results by channel size. Build: a decision table for a brand choosing its YouTube format mix.
311. **MMM primer** — Collect: "marketing mix modeling explained", "Robyn MMM", "Meridian MMM", `min_duration = 900`. Do: summarise concepts, data needs and pitfalls. Build: a primer and a data readiness checklist.
312. **Trade show plan** — Collect: "trade show marketing", "booth design tips", "event lead capture". Do: list pre-show, at-show and follow-up tactics. Build: a trade show plan with timeline and lead follow-up template.
313. **Naming and packaging** — Collect: "brand naming process", "packaging design mistakes", `min_views = 5000`. Do: extract naming criteria and packaging tests designers use. Build: a scoring rubric for candidate names and package concepts.
314. **UGC rate benchmarks** — Collect: "UGC creator rates", "how much to charge for UGC", `max_views = 50000`. Do: log rates by deliverable and usage rights mentioned. Build: a rate card benchmark table for briefing UGC creators.
315. **A/B testing pitfalls** — Collect: "A/B testing mistakes", "statistical significance marketing". Do: extract errors (peeking, small samples) and rules of thumb. Build: a pre-launch test checklist and a sample-size note.
316. **AI marketing tool review** — Collect: "best AI marketing tools", `within = "month"`, `exclude_words = "giveaway"`. Do: compare tools on use case, price and reported flaws. Build: a comparison table for a team picking one tool.
317. **Ad prompt library** — Collect: "ChatGPT prompts for ads", "Claude for copywriting", `within = "month"`. Do: extract prompt structures that experts say work. Build: a team prompt library with your own tested variants.
318. **Weekly marketing digest** — Collect: 20 marketing keywords, `within = "week"`, `min_views = 10000`, `sponsorblock`. Do: summarise the week's tactics and news with links. Build: a Monday digest email for the marketing team.
319. **Klaviyo flow recipes** — Collect: "Klaviyo flows", "abandoned cart email", "post-purchase flow". Do: extract triggers, delays and content per flow. Build: a flow recipe sheet for a Shopify store.
320. **Exam question bank** — Collect: "marketing principles lecture", "4 Ps explained", `min_duration = 1200`. Do: turn concepts into questions with timestamped answers. Build: a question bank for a marketing professor's midterm.
321. **Nonprofit appeal planner** — Collect: "nonprofit fundraising campaign", "year end giving appeal", `within = "year"`. Do: extract appeal structure, channels and timing. Build: a year-end campaign calendar for a small nonprofit.
322. **Restaurant local marketing** — Collect: "restaurant marketing ideas", "restaurant Instagram", `max_views = 50000`. Do: list low-budget tactics owners tried and results. Build: a 30-day local marketing plan for one restaurant.
323. **Ad comment FAQs** — Collect: your category's top videos, `top_comments = 50`. Do: extract repeated questions and doubts viewers raise. Build: an FAQ block and objection-answering ad variants.
324. **Positioning worksheet** — Collect: "product positioning", "April Dunford positioning", "category design". Do: summarise steps for defining alternatives and differentiators. Build: a positioning worksheet a team fills in during a workshop.
325. **Brand voice guide** — Collect: "brand voice examples", "tone of voice guidelines", `within = "year"`. Do: extract dimensions and do/don't examples. Build: a brand voice guide with a Claude prompt that checks copy against it.
326. **HubSpot automation recipes** — Collect: "HubSpot workflows", "lead scoring setup", `min_duration = 480`. Do: extract triggers, branches and properties used. Build: an automation recipe book for marketing ops.
327. **App store listing** — Collect: "App Store optimization", "ASO screenshots", `within = "year"`. Do: list title, keyword and screenshot practices with claimed results. Build: an ASO checklist for a new mobile app.
328. **Black Friday calendar** — Collect: "Black Friday email strategy", `published_after` / `published_before` set to last October-December. Do: extract timing and offer types brands used. Build: a promo campaign calendar for this season.
329. **Hook type dataset** — Collect: 2,000 Shorts in one niche, `include_shorts`, proxies. Do: `yt.py export`, label first lines by hook type. Build: a research dataset correlating hook type with views per day.

[↑ Contents](#contents)

### SEO & content marketing

330. **Core update tracker** — Collect: "Google core update", "rankings dropped", `within = "today"`, daily runs. Do: summarise what SEOs report seeing, by site type. Build: an update log with every claim marked unconfirmed until Google confirms.
331. **Official vs community** — Collect: `only_channels` = Google Search Central, plus "SEO myth" videos. Do: compare official statements with popular SEO claims. Build: a table of claims, official position and timestamp links.
332. **AI Overviews evidence** — Collect: "AI Overviews traffic", "click through rate drop AI", `within = "month"`. Do: log each data point creators share, with sample size. Build: an evidence table for a client asking about AI search impact.
333. **AI search citation tests** — Collect: "get cited by ChatGPT", "LLM SEO", "generative engine optimization", `within = "month"`. Do: list tactics and what evidence backs each. Build: a test plan to check which tactics work on your site.
334. **Technical audit checklist** — Collect: "technical SEO audit", "crawl budget", "indexing issues", `chapters`. Do: extract each check, tool and fix. Build: a technical audit checklist ordered by impact.
335. **Core Web Vitals tickets** — Collect: "improve INP", "LCP fix", "Core Web Vitals WordPress", `min_duration = 480`. Do: extract causes and fixes. Build: developer ticket templates with symptom, cause, fix and how to verify.
336. **Schema by page type** — Collect: "schema markup tutorial", "product schema", "FAQ schema changes". Do: list which schema types creators recommend per page type and recent changes. Build: a JSON-LD checklist to validate with Google's tools.
337. **Google Business Profile SOP** — Collect: "Google Business Profile ranking factors", "GBP optimization", `within = "year"`. Do: list factors and disputed claims. Build: a GBP setup and monthly upkeep SOP for local businesses.
338. **Service-area pages** — Collect: "local SEO for plumbers", "service area pages", `max_views = 30000`. Do: extract page structure and what local SEOs say works. Build: a city landing page template that avoids thin duplicate content.
339. **Topic cluster map** — Collect: seed keyword, then related keywords finder (autocomplete, shared title phrases, tags). Do: group related terms by intent. Build: a topic cluster map with pillar and supporting article ideas.
340. **Content brief skill** — Collect: target keyword, `within = "year"`, `top_comments = 20`. Do: extract subtopics experts cover and questions viewers still ask. Build: a Claude skill that turns any keyword run into a writer's content brief.
341. **Own channel titles** — Collect: your niche, `within = "month"`, `min_views = 10000`. Do: compare titles and keyword mentions of top videos vs the rest. Build: title and description guidelines for your YouTube channel.
342. **Video-to-blog repurposing** — Collect: `only_channels` = your own channel, `timestamps`, `chapters`. Do: turn each video into an article outline with embedded timestamp links. Build: blog drafts that extend your own videos.
343. **White-hat link tactics** — Collect: "link building strategy", "digital PR", `exclude_words = "PBN"`. Do: list tactics and outreach approaches, drop manipulative ones. Build: a white-hat link-building playbook with effort estimates.
344. **Programmatic SEO risks** — Collect: "programmatic SEO case study", "pSEO penalty", `within = "year"`. Do: compare successes and penalties by page quality. Build: a risk/benefit table and quality gates before publishing at scale.
345. **Site migration checklist** — Collect: "site migration SEO", "domain change traffic loss", `min_duration = 600`. Do: extract steps and failure stories. Build: a migration checklist with pre-, during- and post-launch checks.
346. **Author page spec** — Collect: "E-E-A-T explained", "author bio SEO", `within = "year"`. Do: list signals creators say matter and which are speculation. Build: an author page and editorial disclosure spec.
347. **Content refresh SOP** — Collect: "content decay", "update old blog posts", "content pruning". Do: extract how to pick pages to refresh, merge or remove. Build: a quarterly content refresh SOP with decision rules.
348. **Client SEO report** — Collect: "SEO reporting for clients", "Looker Studio SEO dashboard". Do: list metrics agencies show and how they explain them. Build: a monthly client report template with plain-language commentary prompts.
349. **SEO tool comparison** — Collect: "Ahrefs vs Semrush", "best SEO tools", `within = "month"`, `top_comments = 20`. Do: compare features, pricing and complaints. Build: a comparison table for a small agency choosing a stack.
350. **Hreflang checklist** — Collect: "international SEO", "hreflang mistakes", `languages`, `translate`. Do: extract setup rules and common errors from several languages. Build: a hreflang and localization checklist for a multi-country site.
351. **Ecommerce category pages** — Collect: "ecommerce SEO", "category page SEO", "faceted navigation". Do: extract page elements and crawl control advice. Build: a category page template and facet indexing rules.
352. **SEO interview flashcards** — Collect: "SEO interview questions", "SEO specialist interview". Do: extract questions and model answers. Build: flashcards for a junior preparing for an SEO job interview.
353. **Beginner SEO course** — Collect: "SEO for beginners" from 5 educator channels, `min_duration = 900`. Do: arrange topics into a 4-week path. Build: a course outline with timestamped videos, homework and a site audit project.
354. **FAQ from comments** — Collect: your topic, `top_comments = 50`. Do: extract questions viewers ask that videos left unanswered. Build: an FAQ section for your article answering those questions in your own words.
355. **Rising topic calendar** — Collect: 25 niche keywords, daily runs. Do: read `trends.html` for topics gaining attention week over week. Build: an editorial calendar that schedules articles before topics peak.
356. **Same-day newsjacking** — Collect: industry keywords, `within = "today"`, `rising_views_per_day = 2000`. Do: summarise the story and the angles nobody covered. Build: three same-day article angles for the content team.
357. **SEO myth table** — Collect: "SEO myths", "does word count matter", "domain authority myth". Do: list each myth and the evidence or test cited. Build: a myth-vs-evidence table for training clients and staff.
358. **Leak commentary map** — Collect: "Google API leak", "Google documentation leak", `published_after` the leak date. Do: list attributes discussed and how confident analysts are. Build: a table of attributes with confidence levels, not ranking rules.
359. **Topical authority hub** — Collect: "topical authority", "content hub", `within = "year"`. Do: extract how creators structure hubs and interlink. Build: a hub architecture diagram for one subject on your site.
360. **AI-assisted writing policy** — Collect: "AI content SEO", "helpful content", `within = "month"`. Do: summarise where creators draw the line on AI drafting. Build: an editorial policy for AI-assisted writing with review steps.
361. **Log file SOP** — Collect: "log file analysis SEO", "Googlebot crawl logs", `min_duration = 600`. Do: extract tools, filters and what patterns to look for. Build: a step-by-step log analysis SOP.
362. **JavaScript SEO tree** — Collect: "JavaScript SEO", "client side rendering SEO", "Next.js SEO". Do: extract symptoms and diagnostic steps. Build: a decision tree for debugging rendering and indexing of JS sites.
363. **SaaS content mix** — Collect: "SaaS content marketing", "bottom of funnel content", `max_views = 50000`. Do: compare how SaaS marketers split TOFU/BOFU content. Build: a content mix plan for a B2B SaaS blog.
364. **Exec interview articles** — Collect: `only_channels` = your company's channel of executive talks. Do: extract key arguments with timestamps. Build: thought-leadership article drafts approved by the executives quoted.
365. **Distribution checklist** — Collect: "content distribution strategy", "repurpose content", `within = "year"`. Do: list channels and formats per piece. Build: a distribution checklist attached to every published article.
366. **Podcast show notes** — Collect: your podcast's YouTube channel, `chapters`, `timestamps`, `remove_filler_words`. Do: summarise each episode with key moments. Build: SEO-friendly show notes pages with timestamped links.
367. **Cited expert quotes** — Collect: public expert channels on your topic. Do: `yt.py find` for statements on a claim. Build: an article that summarises and cites public expert views with links to the exact second.
368. **Intent classifier data** — Collect: 500 queries via related keywords finder, transcripts of top videos. Do: `yt.py export`, label informational, commercial, navigational. Build: a dataset to train or test a search intent classifier.
369. **Google Discover guide** — Collect: "Google Discover traffic", "Discover optimization", `within = "year"`. Do: extract image, headline and topic factors reported. Build: Discover guidelines for a news or hobby publisher.
370. **Beyond-Google visibility** — Collect: "Perplexity SEO", "Bing SEO", "ChatGPT search", `within = "month"`. Do: list how each engine sources results. Build: a checklist of visibility steps per engine.
371. **Forums in SERPs memo** — Collect: "Reddit in Google results", "forum SEO", `within = "year"`. Do: summarise impact and honest participation approaches. Build: a strategy memo that rules out fake accounts and astroturfing.
372. **Etsy listing SEO** — Collect: "Etsy SEO", "Etsy tags", `max_views = 50000`, `within = "year"`. Do: extract title, tag and photo practices sellers report. Build: a listing optimization checklist.
373. **Manual action recovery** — Collect: "manual action recovery", "site reputation abuse", "reconsideration request". Do: extract causes, cleanup steps and timelines. Build: a recovery plan template.
374. **Internal linking rules** — Collect: "internal linking strategy", "anchor text internal links", `chapters`. Do: extract rules and tools practitioners use. Build: an internal linking rulebook and a Claude prompt that suggests links for a draft.
375. **Traffic forecast model** — Collect: "SEO forecasting", "predict organic traffic". Do: list inputs and assumptions forecasters use and their caveats. Build: a forecasting spreadsheet with a clear assumptions tab.
376. **Writing style guide** — Collect: top educator channels in your niche, `remove_filler_words`. Do: analyse how they explain complex ideas (analogies, order, examples). Build: a writing style guide for your blog in your own rules.
377. **Niche glossary page** — Collect: beginner videos in your niche. Do: extract terms viewers need explained and how experts define them. Build: a glossary page written in your words with links to source videos.
378. **Honest comparison pages** — Collect: "[product A] vs [product B]", `top_comments = 30`, `within = "year"`. Do: gather pros, cons and dealbreakers reviewers report. Build: research notes for a fair comparison page you test yourself.
379. **Client SEO newsletter** — Collect: 15 SEO keywords, `within = "week"`, `sponsorblock`. Do: pick changes that matter to small business clients. Build: a monthly plain-language newsletter an agency sends to clients.
380. **SEO auditor skill** — Collect: 12 technical SEO channels, all videos, proxies. Do: map -> reduce into `knowledge/technical-seo.md`. Build: a Claude skill that reviews crawl exports and explains issues with source citations.
381. **Underserved topic finder** — Collect: niche keywords, `max_views = 5000`, `within = "year"`. Do: find queries where top videos barely mention the keyword (low keyword mentions). Build: a list of underserved topics to cover in video and text.
382. **Video rich results** — Collect: "video SEO", "video indexing Google", "key moments". Do: extract markup and page setup steps. Build: a checklist to get your own videos showing in Google with key moments.
383. **Zero-click strategy** — Collect: "zero click searches", "brand search SEO", `within = "year"`. Do: summarise how SEOs measure value without clicks. Build: a KPI framework for content that earns visibility but not visits.

[↑ Contents](#contents)

### Sales & customer success

384. **Cold email rubric** — Collect: "cold email teardown", "cold email that got replies", `within = "year"`. Do: extract what reviewers praise and cut. Build: a scoring rubric SDRs run on every draft before sending.
385. **Cold call opener drills** — Collect: "cold call opener", "cold calling live", `min_duration = 300`. Do: classify openers and what follows each. Build: a call script plus Claude roleplay prompts to practice the first 30 seconds.
386. **Objection library** — Collect: "objection handling", "price objection", "we're happy with our vendor". Do: pair each objection with responses experts give. Build: an objection-to-response library with timestamp links for training.
387. **Negotiation prep sheet** — Collect: "negotiation tactics", "tactical empathy", "BATNA explained", `min_duration = 600`. Do: extract prep steps and question types. Build: a one-page negotiation prep worksheet for a big deal.
388. **Discovery framework compare** — Collect: "MEDDIC", "SPIN selling", "BANT vs MEDDPICC". Do: summarise each framework's questions and best fit. Build: a comparison table and a discovery call template.
389. **Buyer roleplay bot** — Collect: sales trainer channels, all videos, `remove_filler_words`. Do: map -> reduce into `knowledge/buyer-personas.md`. Build: a Claude prompt that plays a skeptical buyer and scores your call afterwards.
390. **Account brief** — Collect: `only_channels` = target company's channel, plus its executives' public conference talks. Do: list stated priorities and pain points. Build: an account brief for a rep's first meeting.
391. **SDR ramp plan** — Collect: "SDR training", "first 90 days in sales", `within = "year"`. Do: extract skills, activities and metrics per phase. Build: a 30-60-90 day onboarding plan for new SDRs.
392. **Churn playbook** — Collect: "reduce churn SaaS", "customer churn reasons", `min_views = 5000`. Do: list churn causes and interventions with claimed results. Build: a churn playbook mapping each warning sign to an action.
393. **Customer onboarding checklist** — Collect: "customer onboarding best practices", "time to value", `chapters`. Do: extract steps and milestones. Build: a customer onboarding checklist and kickoff email template.
394. **De-escalation scripts** — Collect: "angry customer", "de-escalation techniques", "customer service training". Do: extract phrases and steps trainers recommend. Build: support de-escalation scripts and macro drafts.
395. **Help center from videos** — Collect: `only_channels` = your product tutorial channel, `timestamps`. Do: turn each tutorial into steps. Build: help center articles that link to the exact second in your own videos.
396. **Competitor battlecards** — Collect: "[competitor] review", "[competitor] problems", `top_comments = 40`. Do: extract weaknesses users report and switching reasons. Build: battlecards with fair, sourced talking points.
397. **Competitor daily alert** — Collect: competitor names, `within = "today"`, daily runs. Do: flag new reviews, announcements and complaints. Build: a daily Slack-ready alert for the sales team.
398. **Buyer-side procurement** — Collect: "negotiating with vendors", "SaaS procurement tips", "software contract negotiation". Do: list tactics buyers use. Build: a buyer's negotiation checklist for a procurement team renewing software.
399. **Car buying prep** — Collect: "car dealership negotiation", "dealer add-ons", `top_comments = 30`. Do: list tactics and fees consumers report. Build: a car buying checklist of questions to ask and figures to verify.
400. **Follow-up cadence** — Collect: "sales follow up", "follow up email sequence", `within = "year"`. Do: extract number of touches, spacing and channels. Build: a multi-touch follow-up sequence template.
401. **Social selling routine** — Collect: "LinkedIn social selling", "LinkedIn prospecting", `within = "month"`. Do: extract daily actions and messaging examples. Build: a 20-minute daily routine for reps.
402. **Demo script** — Collect: "software demo best practices", "demo mistakes", `min_duration = 480`. Do: extract structure, timing and recovery tips. Build: a demo script skeleton with discovery recap and close.
403. **Call review rubric** — Collect: "sales coaching", "call review", "sales manager coaching". Do: extract what coaches listen for. Build: a call review rubric managers use in weekly 1:1s.
404. **Forecast definitions** — Collect: "sales forecasting", "commit vs best case", "pipeline review". Do: summarise category definitions and inspection questions. Build: forecast category definitions and a pipeline review agenda.
405. **Security review readiness** — Collect: "enterprise sales security questionnaire", "SOC 2 for startups sales". Do: list documents buyers request. Build: a readiness checklist to confirm with your security lead.
406. **Comp plan comparison** — Collect: "sales compensation plan", "OTE explained", "accelerators commission". Do: compare structures and incentives each creates. Build: a comp plan comparison table for a sales leader.
407. **QBR template** — Collect: "quarterly business review", "QBR customer success", `chapters`. Do: extract sections and what customers value. Build: a QBR deck template and prep checklist.
408. **Expansion signals** — Collect: "upsell existing customers", "expansion revenue", `within = "year"`. Do: list signals CSMs watch and how they open the conversation. Build: an expansion signal list for CRM alerts.
409. **Survey design guide** — Collect: "NPS survey mistakes", "customer feedback survey", "CSAT vs NPS". Do: extract question wording and timing advice. Build: a survey design guide with question templates.
410. **Health score spec** — Collect: "customer health score", "churn prediction customer success". Do: list inputs and weightings practitioners use. Build: a health score model spec to test against your own churn data.
411. **Listing presentation** — Collect: "real estate listing presentation", "listing appointment script", `max_views = 50000`. Do: extract structure and seller objections. Build: a listing presentation outline for a new agent.
412. **Retail floor cards** — Collect: "retail sales techniques", "upselling in store", `include_shorts`. Do: extract greetings, questions and add-on suggestions. Build: pocket training cards for seasonal retail staff.
413. **CRM comparison** — Collect: "best CRM small business", "HubSpot vs Pipedrive", `within = "year"`, `top_comments = 20`. Do: compare features, price and complaints. Build: a CRM comparison table for a 5-person team.
414. **AI SDR evaluation** — Collect: "AI SDR", "AI sales agent results", `within = "month"`. Do: separate demos from reported results and complaints. Build: an evaluation memo with pilot criteria.
415. **Team sales digest** — Collect: sales podcast channels, `channel_within = "week"`, `sponsorblock`. Do: pick three tactics worth testing each week. Build: a Friday digest for the sales floor with timestamp links.
416. **Japan business etiquette** — Collect: "Japanese business etiquette", "営業 マナー", `languages`, `translate`. Do: extract meeting, gift and follow-up norms. Build: localized etiquette notes for reps selling into Japan.
417. **First 10 customers** — Collect: "founder led sales", "how I got my first customers", `max_views = 50000`. Do: extract channels and scripts founders used. Build: a first-10-customers playbook for a technical founder.
418. **Freelancer proposals** — Collect: "freelance proposal template", "how to write a proposal", `within = "year"`. Do: extract sections and pricing presentation tips. Build: a proposal template for freelance designers.
419. **Scoping call script** — Collect: "agency pricing conversation", "value based pricing", `min_duration = 600`. Do: extract questions that uncover budget and scope. Build: a scoping call script for agency owners.
420. **Customer case studies** — Collect: `only_channels` = your company's webinar channel of customer talks. Do: extract problem, solution, results and quotes. Build: case study drafts sent to each customer for approval.
421. **Contact center QA** — Collect: "call center quality assurance", "QA scorecard", `chapters`. Do: extract criteria and calibration methods. Build: a QA scorecard and calibration session guide.
422. **Support chatbot rollout** — Collect: "AI customer support chatbot", "support automation", `within = "month"`. Do: list rollout steps, failure cases and handoff rules. Build: a deployment checklist with escalation rules to humans.
423. **Webinar Q&A mining** — Collect: `only_channels` = your own webinar channel, `timestamps`. Do: extract every customer question asked live. Build: an FAQ page plus a product feedback list for the product team.
424. **Booth conversation script** — Collect: "trade show booth sales", "booth staff training". Do: extract openers and qualifying questions. Build: a booth conversation script and lead note card.
425. **Partner program design** — Collect: "channel partner program", "reseller program SaaS", `min_duration = 600`. Do: list tiers, margins and enablement used. Build: a partner program design draft.
426. **Renewal timeline** — Collect: "SaaS renewal process", "renewal negotiation", `within = "year"`. Do: extract when CSMs start and what risks they check. Build: a 120-day renewal timeline with tasks.
427. **SDR interview kit** — Collect: "hiring SDRs", "sales interview questions", "sales roleplay interview". Do: extract questions and red flags. Build: an interview kit with scorecard for sales leaders.
428. **Career changer flashcards** — Collect: "sales terms explained", "ARR ACV pipeline explained". Do: extract definitions and examples. Build: flashcards for someone moving into tech sales from another field.
429. **Outreach compliance questions** — Collect: "CAN-SPAM cold email", "GDPR cold email B2B". Do: list the rules creators cite and where they conflict. Build: a question list for counsel before scaling outreach, not legal advice.
430. **Sales psychology claims** — Collect: "sales psychology", "persuasion techniques sales". Do: list claims and whether a study is named. Build: a claims-to-verify table, dropping manipulative tactics from your training.
431. **Live chat macros** — Collect: "live chat sales ecommerce", "chat support price objections". Do: extract replies that address shipping, price and sizing doubts. Build: live chat macros for an online store.
432. **Buyer persona notes** — Collect: "day in the life of a procurement manager", "IT director day", `max_views = 50000`. Do: extract priorities and frustrations practitioners describe. Build: buyer persona documents for messaging.
433. **Coaching clip library** — Collect: public sales call breakdown channels. Do: `yt.py find "send me some information"` and similar brush-offs. Build: a coaching clip library linking to the exact second each is handled.
434. **Cancellation reasons** — Collect: "why I cancelled [product]", "switching from [product]", `top_comments = 30`. Do: tag each reason (price, missing feature, support). Build: a cancellation reasons dataset for the retention team.
435. **ROI calculator** — Collect: "value selling", "ROI business case sales", `min_duration = 480`. Do: extract cost and benefit inputs sellers use. Build: an ROI calculator spreadsheet with assumptions the buyer edits.
436. **Win/loss guide** — Collect: "win loss analysis", "why we lose deals", `within = "year"`. Do: extract interview questions and categorization schemes. Build: a win/loss interview guide and tagging sheet.
437. **Objection classifier data** — Collect: 1,000 sales training videos, proxies, `yt.py export`. Do: label objection snippets by type. Build: a .jsonl dataset to test an objection classifier for call notes.
438. **Video prospecting script** — Collect: "video prospecting", "Loom sales video", `max_duration = 900`. Do: extract structure, length and personalization tips. Build: a 60-second prospecting video script template.

[↑ Contents](#contents)

## Commerce, products and market intelligence

### E-commerce & retail

439. **Weekly trending-product radar** — Collect: "amazon finds", "tiktok made me buy it", `within = "week"`, `rising_views_per_day = 2000`. Do: list every product named, count channels per product. Build: ranked spreadsheet of products gaining buzz.
440. **Private-label improvement spec** — Collect: "<product> review", "<product> problems", `min_duration = 300`, `top_comments = 30`. Do: cluster defects and wished-for features. Build: spec sheet for a supplier listing fixes to make in your version.
441. **Shopify app shortlist** — Collect: "best shopify apps", "shopify reviews app", `within = "year"`, `sponsorblock`. Do: tabulate apps, use case, price mentioned, cons. Build: comparison table to pick one app per store function.
442. **Dropshipping supplier vetting checklist** — Collect: "cj dropshipping review", "aliexpress supplier scam", `max_views = 50000`. Do: extract red flags and test-order steps. Build: printable checklist for vetting a new supplier.
443. **Amazon seller policy watch** — Collect: "amazon seller update", "fba fee change", `within = "today"`, daily schedule. Do: summarise each change, flag claims to confirm in Seller Central. Build: morning briefing for a seller team.
444. **BFCM playbook from last year** — Collect: "black friday shopify results", `published_after` last Oct, `published_before` last Dec. Do: list tactics with stated results and failures. Build: dated BFCM run-sheet for this year.
445. **Packaging design brief from unboxings** — Collect: "<category> unboxing", `include_shorts`, `top_comments = 20`. Do: note what unboxers praise, mock or throw away. Build: packaging brief with must-haves and things to avoid.
446. **Honest small-reviewer consensus** — Collect: "<product> honest review", `max_views = 10000`, `exclude_words = ["sponsored","gifted"]`. Do: compare small-creator verdicts to big ones. Build: unbiased pros/cons summary for a buying decision.
447. **Product page FAQ from objections** — Collect: "<product> worth it", "<product> after 6 months", `top_comments = 40`. Do: pull recurring buyer doubts and how owners answer them. Build: 15-question FAQ block for the product page.
448. **Etsy listing SEO checklist** — Collect: channels of Etsy coaches, `channel_within = "year"`. Do: extract title, tag and photo rules; mark where coaches disagree. Build: one-page listing checklist for a new Etsy seller.
449. **Amazon PPC test plan** — Collect: "amazon ppc strategy", "sponsored products campaign structure", `min_duration = 900`. Do: turn each tactic into a hypothesis with a metric. Build: 8-week PPC experiment plan to test, not trust.
450. **3PL comparison sheet** — Collect: "shipbob review", "3pl warehouse experience", "fulfillment center switch", `within = "year"`. Do: extract fees, onboarding issues, error stories. Build: spreadsheet scoring 3PLs on criteria you care about.
451. **Tariff & de minimis tracker** — Collect: "tariffs ecommerce", "de minimis", `within = "week"`, `exclude_channels` for clickbait. Do: log each claimed rule change with date and source video. Build: change log to verify with a customs broker.
452. **Store teardown CRO audit** — Collect: "shopify store review", "store teardown", `timestamps`. Do: extract every critique pattern (hero, trust badges, speed). Build: 40-point CRO audit you run on your own store.
453. **Support macros by complaint type** — Collect: "<your category> problems", "<product> not working", `top_comments = 25`. Do: group issues and draft calm replies with fixes owners found. Build: helpdesk macro library.
454. **Store-tour new-product spotting** — Collect: "costco new items", "trader joes haul", `within = "week"`. Do: list products shown with price and reaction. Build: weekly sheet of new SKUs for a grocery category buyer.
455. **Asian product trend import ideas** — Collect: "daiso haul", "olive young haul", `languages = ["ja","ko"]`, `translate`. Do: find products popular there but rarely reviewed in English. Build: import-idea shortlist with demand notes.
456. **Retail arbitrage beginner course** — Collect: "retail arbitrage for beginners", "sourcing at walmart", `max_duration = 1800`. Do: order concepts from basics to scaling, note risks. Build: 6-lesson course outline with quizzes.
457. **Print-on-demand niche finder** — Collect: "print on demand niche", "merch by amazon niche", related keywords finder. Do: list niches, saturation claims, design styles. Build: niche scorecard with 30 design briefs.
458. **TikTok Shop live selling SOP** — Collect: "tiktok shop live tips", "live selling script", `within = "month"`. Do: extract run-of-show, hooks, host roles. Build: SOP and timed script template for a 60-minute live.
459. **Ecommerce email flow templates** — Collect: "klaviyo flows", "abandoned cart email", `chapters`. Do: map each flow's triggers, timing and messages. Build: flow blueprint doc with original copy drafts per step.
460. **Product photo shot list** — Collect: "product photography at home", "amazon main image tips", `min_duration = 480`. Do: extract setups, angles, lighting gear. Build: shot list and gear list for shooting a 10-SKU catalogue.
461. **Supplier negotiation prompt** — Collect: "negotiate with alibaba supplier", "moq negotiation", `timestamps`. Do: pull tactics and phrasing patterns. Build: Claude prompt that role-plays a supplier so you can practise.
462. **Crowdfunding launch timeline** — Collect: "kickstarter postmortem", "what i learned crowdfunding", `min_duration = 600`. Do: extract dated pre-launch steps and mistakes. Build: week-by-week timeline from T-90 to fulfilment.
463. **Subscription box churn reasons** — Collect: "cancelled subscription box", "<box name> review", `top_comments = 30`. Do: list why people cancel or stay. Build: churn-reason matrix with retention offers to test.
464. **Visual merchandising checklist** — Collect: "visual merchandising tips", "retail window display", channels of VM trainers. Do: extract rules for layout, sightlines, signage. Build: store walk checklist for a boutique manager.
465. **Shrink-reduction staff training** — Collect: "retail loss prevention training", "reduce shrink small store", `max_duration = 1200`. Do: keep defensive, customer-friendly practices only. Build: 20-minute staff training module with quiz.
466. **"X vs Y" buying guide** — Collect: "<product A> vs <product B>", `min_views = 20000`, `within = "year"`. Do: tabulate specs and verdicts with links. Build: comparison table for an affiliate guide that cites each reviewer.
467. **Listing grader Claude skill** — Collect: "amazon listing optimization", "a+ content tips", `within = "year"`. Do: map -> reduce into `knowledge/listings.md`. Build: Claude skill that grades a pasted listing and suggests fixes.
468. **Buyer personas from comments** — Collect: "<category> review", `top_comments = 50`, `include_description`. Do: cluster commenters by stated use, budget, frustration. Build: 4 buyer personas with quotes and links.
469. **Seasonal demand calendar** — Collect: 20 category keywords, daily schedule for a year. Do: read `trends.html` for when new videos and attention spike. Build: month-by-month calendar for stock buys and promo timing.
470. **Creator seeding outreach list** — Collect: "<category> review", `max_views = 20000`, `subtitles_only`. Do: list channels reviewing your category, their tone and audience. Build: outreach sheet of public channels to offer samples.
471. **Sustainable packaging options** — Collect: "compostable mailers review", "eco packaging small business", `within = "year"`. Do: list materials, suppliers named, cost and durability claims. Build: options table to verify with samples.
472. **Marketplace expansion comparison** — Collect: "walmart marketplace seller", "ebay vs amazon seller", "temu seller experience". Do: compare fees, approval, traffic, pitfalls. Build: decision matrix for which marketplace to add next.
473. **Inventory forecasting template** — Collect: "inventory forecasting ecommerce", "reorder point formula", `min_duration = 600`. Do: extract formulas and inputs explained. Build: spreadsheet template with reorder points and safety stock.
474. **Chargeback prevention SOP** — Collect: "shopify chargeback", "ecommerce fraud prevention", `within = "year"`. Do: list defensive steps and evidence to keep. Build: SOP for handling disputes with an evidence checklist.
475. **Product compliance question list** — Collect: "cpsc compliance amazon", "ce marking small business", `min_duration = 600`. Do: map what creators say applies to which products. Build: questions to bring to a compliance consultant.
476. **Canton Fair trip prep** — Collect: "canton fair tips", "yiwu market sourcing", `within = "year"`. Do: extract logistics, booth etiquette, sample handling. Build: trip prep checklist and day plan for a first sourcing visit.
477. **Review response templates** — Collect: "respond to negative reviews", "review management small business", `max_duration = 1200`. Do: extract structures that de-escalate. Build: response templates for 1-, 3- and 5-star reviews.
478. **Thrift flipping "what sells" list** — Collect: "what sold on ebay this week", "poshmark sales", `within = "month"`. Do: log items, brands and sale prices mentioned. Build: hobbyist's cheat sheet of brands to grab at thrift stores.
479. **Sneaker drop demand tracker** — Collect: "<shoe> release", "<shoe> on feet", `within = "today"`, `rising_views_per_day = 5000`. Do: score hype and fit/quality complaints per release. Build: daily drop tracker for a resale shop.
480. **Refurb "known issues" database** — Collect: "<device> problems after 1 year", "<device> common faults". Do: list failure modes and checks per model. Build: inspection checklist per model for a refurbished-electronics seller.
481. **New-hire ecommerce KPI flashcards** — Collect: "ecommerce metrics explained", "aov ltv cac", `max_duration = 900`. Do: extract definitions, formulas and examples. Build: 60 flashcards for onboarding store staff.
482. **CPG launch category review** — Collect: "new snacks 2026", "new drink review", `within = "month"`. Do: list launches, flavours, price and taste verdicts. Build: monthly category review deck for a retail buyer.
483. **Cart abandonment test backlog** — Collect: "reduce cart abandonment", "checkout optimization shopify", `within = "year"`. Do: list tactics with claimed impact. Build: prioritised A/B test backlog with ICE scores.
484. **Bundle & upsell offer matrix** — Collect: "upsell ideas shopify", "product bundles aov", `chapters`. Do: catalogue offer types and where they appear in the funnel. Build: offer matrix mapped to your own catalogue.
485. **Reality check for new store owners** — Collect: "first month shopify results", "dropshipping failed", `max_views = 30000`. Do: tally reported revenue, ad spend and failure reasons. Build: realistic-expectations report for beginners.
486. **Account suspension causes map** — Collect: "amazon account suspended", "plan of action amazon", `within = "year"`. Do: list causes and what sellers say helped. Build: map of risks plus questions for a specialist, not legal advice.
487. **Support chatbot from your own demos** — Collect: your brand's channel, `channel_max_videos = 200`, `timestamps`. Do: export to .jsonl and index for RAG. Build: support bot that answers with links to the exact second.
488. **Landed cost calculator** — Collect: "landed cost explained", "import duty calculation", "freight forwarder fees". Do: list every cost line creators include. Build: spreadsheet calculator with inputs to confirm with your forwarder.
489. **Holiday gift guide research** — Collect: "gift guide 2026", "gifts for <persona>", `within = "month"`, `min_views = 10000`. Do: count products recommended across guides. Build: consensus gift guide page that credits each source video.
490. **Dupe demand finder** — Collect: "<brand> dupe", "cheaper alternative to <product>", `within = "month"`. Do: list which premium products people want cheaper versions of. Build: list of affordable-alternative product gaps.
491. **Retail AI tool landscape** — Collect: "retail ai tools", "inventory ai", "ai for shopify", `within = "month"`. Do: list tools, use cases and limits mentioned. Build: shortlist for a store owner with pilot criteria per tool.
492. **Price anchoring playbook** — Collect: "pricing psychology ecommerce", "charm pricing", "compare at price", `min_duration = 480`. Do: extract tactics and ethics caveats. Build: playbook of honest pricing tests for a product page.
493. **Return-rate reduction plan** — Collect: "why I returned <product>", "<product> sizing", `top_comments = 30`. Do: list return reasons (fit, expectation gap, damage). Build: size guide and product-copy fixes to cut returns.

[↑ Contents](#contents)

### Product management & UX research

494. **Pain-point matrix for a SaaS category** — Collect: "<app> review", "problems with <app>", `within = "year"`, `top_comments = 30`. Do: cluster pains by severity and frequency. Build: pain-point matrix that seeds a product opportunity doc.
495. **Feature requests from tutorial comments** — Collect: competitor tutorial channels, `channel_max_videos = 100`, `top_comments = 50`. Do: extract "I wish it could..." requests and count. Build: feature-request backlog ranked by mentions.
496. **Onboarding teardown checklist** — Collect: "onboarding teardown", "user onboarding examples", `timestamps`. Do: list patterns, anti-patterns and the apps cited. Build: onboarding checklist to audit your first-run flow.
497. **Jobs-to-be-done map** — Collect: "how I use <app>", "my <app> workflow", `min_duration = 600`. Do: extract the job, trigger and desired outcome per video. Build: JTBD map with quotes linked to the second.
498. **Workaround-based usability issues** — Collect: "<app> tips and tricks", "<app> hack", `timestamps`. Do: find steps where creators explain workarounds for missing or hidden features. Build: usability issue list for designers.
499. **Launch-day reaction briefing** — Collect: "<your product>", `within = "today"`, daily schedule, `top_comments = 20`. Do: summarise first reactions, bugs and confusion. Build: launch-day briefing posted to the team channel.
500. **Switcher churn analysis** — Collect: "why I switched from <app>", "<app> to <rival> migration", `within = "year"`. Do: list push and pull reasons. Build: churn-driver ranking with retention ideas per driver.
501. **Personas from day-in-the-life vlogs** — Collect: "day in the life <role>", `min_duration = 480`, `max_views = 100000`. Do: note tools, frustrations, goals, environment. Build: 3 evidence-backed personas with links.
502. **Accessibility audit from disabled creators** — Collect: "blind iphone user apps", "accessibility review app", "screen reader test". Do: list barriers and praised patterns. Build: accessibility audit checklist for your product.
503. **Customer vocabulary glossary** — Collect: user-made videos about your category, `remove_filler_words`. Do: list the words users use vs your UI labels. Build: microcopy glossary mapping jargon to user language.
504. **PM interview prep flashcards** — Collect: PM interview channels, "product sense interview", `min_duration = 900`. Do: extract question types and answer structures. Build: Anki-style flashcards and a mock-question bank.
505. **Prioritisation framework decision tree** — Collect: "rice prioritization", "kano model", "moscow method", `max_duration = 1200`. Do: compare when each fits. Build: decision tree telling a junior PM which framework to use.
506. **Design system principles doc** — Collect: "design system talk", Config conference channel, `chapters`. Do: extract governance, tokens and adoption lessons. Build: draft principles and rollout plan for your design system.
507. **Competitor changelog reactions** — Collect: "<rival> new update", `within = "week"`, `top_comments = 20`. Do: tag each shipped feature with user reaction. Build: weekly table of competitor releases and reception.
508. **Pricing page reaction research** — Collect: "<app> pricing change", "<app> price increase", `top_comments = 40`. Do: extract what users call fair or unfair. Build: pricing research memo with willingness-to-pay signals.
509. **Beta tester bug themes** — Collect: "<product> beta hands on", "<os> beta bugs", `within = "week"`. Do: list reported bugs and how often each appears. Build: triage sheet the QA team can verify.
510. **Hardware durability requirements** — Collect: "<device> after 1 year", "<device> broke", `min_duration = 360`. Do: extract failure points and use conditions. Build: durability requirement list for the next hardware revision.
511. **Patch reception per change** — Collect: "<game> patch notes reaction", `within = "week"`, `top_comments = 30`. Do: score sentiment per individual change. Build: patch-reaction table for the game design team.
512. **User research methods course** — Collect: "user interview tips", "usability testing", NN/g-style channels. Do: order methods by when to use them. Build: 5-module course for junior researchers with exercises.
513. **Survey question bank** — Collect: pain-point keywords for your domain, `top_comments = 30`. Do: turn each recurring theme into neutral survey questions. Build: validated-looking question bank to pilot with real users.
514. **Interview discussion guide** — Collect: "<task> frustrating", "<task> how I do it", `max_views = 50000`. Do: list themes and open questions worth probing. Build: 45-minute user interview guide.
515. **Feature demo frequency proxy** — Collect: tutorials about your product, `channel_within = "year"`, `timestamps`. Do: count which features creators actually demo. Build: heatmap of shown vs ignored features.
516. **Migration friction spec** — Collect: "migrate from <rival> to <app>", "import data <app>", `timestamps`. Do: list where migrations break. Build: requirements spec for an import tool.
517. **Top-bug list from fix videos** — Collect: "<app> not working fix", "<app> error", `within = "month"`, `rising_views_per_day = 300`. Do: rank issues by fast-rising fix videos. Build: bug list for QA with repro clues.
518. **Regional UX issues** — Collect: "<app> review" with `languages = ["pt","hi","id"]`, `translate`. Do: find issues unique to each market (payments, language, data cost). Build: localisation backlog per region.
519. **Mobile UX pattern library** — Collect: "app design review", "best mobile app ux", `timestamps`. Do: catalogue patterns with app examples and time links. Build: pattern library page the design team can browse.
520. **AI feature trust concerns** — Collect: "<app> ai feature review", "turn off ai <app>", `top_comments = 40`. Do: list trust, privacy and accuracy worries. Build: concern list with design mitigations to test.
521. **PLG experiment backlog** — Collect: "product led growth case study", "freemium conversion", `min_duration = 900`. Do: extract experiments with claimed results. Build: backlog of PLG experiments sized for your team.
522. **Keynote launch narrative template** — Collect: Apple, Google and Samsung event channels, `channel_tabs = ["streams"]`, `chapters`. Do: map the story structure of each reveal. Build: launch narrative template for your next release.
523. **Product Hunt launch checklist** — Collect: "product hunt launch", "how we got #1 product hunt", `within = "year"`. Do: extract prep steps and timing. Build: launch-day checklist with a T-minus schedule.
524. **PMF signals checklist** — Collect: founder interviews, "how we found product market fit", `min_duration = 1200`. Do: list signals founders say told them they had PMF. Build: checklist to judge your own traction honestly.
525. **Retention metrics primer** — Collect: "retention cohort analysis", "churn metrics saas", `max_duration = 1500`. Do: extract definitions and common mistakes. Build: one-page primer plus a cohort spreadsheet template.
526. **Roadmap template from practitioners** — Collect: "product roadmap template", "now next later roadmap", `chapters`. Do: compare formats and when each works. Build: roadmap template and a guide to presenting it.
527. **Stakeholder management SOP** — Collect: "stakeholder management product manager", "saying no as a pm". Do: extract scripts, meeting rituals and escalation steps. Build: SOP for running quarterly planning with stakeholders.
528. **Design critique rubric** — Collect: "design critique session", "how to give design feedback", `timestamps`. Do: extract the questions good critics ask. Build: critique rubric and facilitation script for weekly crits.
529. **Wishlist desirability ranking** — Collect: "what I want in <next version>", "<product> wishlist", `within = "month"`. Do: count each wished feature across creators. Build: desirability ranking to compare with your roadmap.
530. **Exit survey from "why I quit" videos** — Collect: "why I stopped using <app>", "deleted <app>", `top_comments = 30`. Do: list exit reasons in users' words. Build: exit survey with answer options that match real reasons.
531. **Classroom requirements for edtech** — Collect: "teacher review <edtech app>", "classroom tech tools", `min_duration = 480`. Do: extract teacher constraints (time, devices, privacy). Build: requirements list for a classroom product.
532. **Empathy map for a professional user** — Collect: "nurse charting epic", "ehr frustrations", `max_views = 50000`. Do: sort quotes into says, thinks, does, feels. Build: empathy map poster for a healthcare software team.
533. **Power-user settings spec** — Collect: "<app> advanced tips", "<app> power user", `min_duration = 900`. Do: list customisations power users build themselves. Build: spec for an advanced-settings panel.
534. **Weekly voice-of-customer newsletter** — Collect: product and rival keywords, daily schedule, `within = "week"`. Do: pick the 5 most useful clips and quotes. Build: weekly VoC email for the whole company with time links.
535. **VoC analyst Claude skill** — Collect: a year of pain-point keywords, map -> reduce into `knowledge/`. Do: define how to answer "what do users say about X". Build: Claude skill that answers with cited, timestamped evidence.
536. **Labelled feedback dataset** — Collect: category review keywords, `top_comments = 50`, `yt.py export`. Do: label snippets as bug, request, praise, confusion. Build: .jsonl dataset to train or test a feedback classifier.
537. **Smart-home setup frustrations** — Collect: "<device> setup problems", "smart home setup fail", `timestamps`. Do: mark each setup step where users get stuck. Build: redesigned out-of-box flow with fixes per step.
538. **First-five-minutes timeline** — Collect: "<app> first impressions", `max_views = 20000`, `timestamps`. Do: log what new users do and say minute by minute. Build: timeline of first-run reactions for an onboarding review.
539. **Demand check before building** — Collect: "how to <task>", related keywords finder, `within = "year"`. Do: measure video count, views per day and complaints about current tools. Build: go/no-go memo for a feature idea.
540. **Analytics tool selection** — Collect: "amplitude vs mixpanel", "posthog review", `within = "year"`. Do: compare setup effort, pricing, limits. Build: weighted selection table for your team's analytics stack.
541. **Deprecation comms playbook** — Collect: "google killed <product>", "<feature> removed reaction", `top_comments = 30`. Do: find what made users angrier or calmer. Build: playbook for announcing a feature sunset.
542. **Opportunity solution tree** — Collect: your category's pain-point videos, map -> reduce. Do: arrange outcomes, opportunities, solution ideas from evidence. Build: opportunity solution tree in Markdown for discovery planning.
543. **Heuristics lecture with real examples** — Collect: "app ux fail", "bad ui design", `timestamps`. Do: match each example to a Nielsen heuristic. Build: lecture slides for a UX class, each heuristic with a cited video moment.
544. **Car infotainment HMI requirements** — Collect: "<car> infotainment review", "touchscreen car controls", `min_duration = 480`. Do: list distraction and reach complaints. Build: HMI requirement list for an automotive UX team.
545. **Game tutorial FTUE checklist** — Collect: "first hour <game>", "game tutorial design", `timestamps`. Do: note where players quit, skip or praise the tutorial. Build: first-time-user-experience checklist for game designers.
546. **Dark-pattern ethics checklist** — Collect: "dark patterns", "annoying app notifications", `timestamps`. Do: catalogue patterns users call manipulative, with app examples. Build: ethics checklist used in every design review.

[↑ Contents](#contents)

### Competitive intelligence & market research

547. **Competitor channel diff briefing** — Collect: 5 rival brand channels, `channel_within = "week"`, daily schedule. Do: summarise new videos and what changed in messaging. Build: daily diff briefing in the team's inbox.
548. **Messaging matrix from webinars** — Collect: rivals' channels, `channel_tabs = ["streams"]`, `min_duration = 1800`. Do: extract claims, proof points and target audience per rival. Build: messaging matrix for the marketing team.
549. **Earnings call strategy summary** — Collect: "<company> earnings call", "<company> investor day", `within = "month"`. Do: extract stated priorities, numbers and risks. Build: strategy summary with quotes to check against filings.
550. **TAM assumptions register** — Collect: "<industry> market size", "<industry> industry analysis", `min_duration = 600`. Do: list every TAM figure, its source and method. Build: assumptions register to verify before a pitch deck.
551. **Emerging topic radar** — Collect: 30 industry keywords, daily schedule. Do: read `trends.html` for topics with rising new-video counts. Build: monthly radar chart of emerging, peaking and fading topics.
552. **Positioning map** — Collect: rivals' brand channels and "<rival> review", `within = "year"`. Do: score how each is described on 2 key axes. Build: 2x2 positioning map with evidence links per dot.
553. **Competitor pricing tracker** — Collect: "<rival> pricing", "<rival> price increase", `within = "week"`, `title_must_contain = ["price"]`. Do: log pricing changes users mention. Build: dated pricing tracker to confirm on rivals' sites.
554. **Sales battlecards** — Collect: "<rival> review", "<rival> vs <you>", `top_comments = 30`. Do: extract strengths, weak spots and objections. Build: one-page battlecard per rival with talk tracks.
555. **Trade show floor report** — Collect: "ces 2026", "<show> booth tour", `within = "week"`, `include_shorts`. Do: list launches, demos and recurring themes. Build: trade show report for colleagues who could not attend.
556. **Startup landscape from demo days** — Collect: "yc demo day", "startup pitch <sector>", `within = "year"`. Do: tag each startup by problem, model, stage. Build: landscape spreadsheet of new entrants in your sector.
557. **Weekly industry newsletter** — Collect: 10 industry podcast channels, `channel_within = "week"`, `sponsorblock`. Do: pick top stories and disagreements. Build: weekly newsletter for clients that links to each source.
558. **Market entry brief** — Collect: "<category>" in local language, `languages = ["de"]`, `translate`. Do: list local players, habits and price norms. Build: market entry brief for a German launch with items to verify locally.
559. **Win/loss themes** — Collect: "why I chose <rival>", "<you> vs <rival> which one", `top_comments = 40`. Do: tally decision factors. Build: win/loss theme report for sales and product.
560. **CEO statement timeline** — Collect: "<rival CEO> interview", `within = "year"`, `timestamps`. Do: log each public claim about strategy with date. Build: timeline of stated priorities to compare against what shipped.
561. **Franchise due diligence questions** — Collect: "<franchise> franchise review", "owning a <franchise>", `min_duration = 900`. Do: list reported costs, hours, problems. Build: questions to ask the franchisor and a lawyer.
562. **Local business unit economics** — Collect: "start a car wash business", "car wash profit", `max_views = 100000`. Do: extract costs, prices and volumes owners report. Build: unit-economics model with every assumption marked to verify.
563. **SWOT from analyst talks** — Collect: "<company> analysis", "<company> stock deep dive", `min_duration = 900`. Do: sort arguments into a SWOT, note bull vs bear. Build: SWOT with citations, framed as opinion map, not advice.
564. **Category POV paper** — Collect: "what is <new category>", "<category> explained", `within = "year"`. Do: compare how vendors define the category. Build: point-of-view paper defining the category your way.
565. **Integration ecosystem map** — Collect: "<rival> integrations", "<rival> with zapier", `timestamps`. Do: list partner tools shown with each rival. Build: ecosystem map showing integration gaps you could fill.
566. **VC thesis comparison** — Collect: VC firm channels, "<sector> investment thesis", `channel_within = "year"`. Do: extract where investors expect value to go. Build: table of VC theses for a founder's fundraising prep.
567. **Gen Z consumer trend report** — Collect: "gen z trend", "gen z doesn't buy", `within = "month"`, `include_shorts`. Do: list behaviours and products cited. Build: trend report with hypotheses for brand teams to test.
568. **Hardware teardown cost notes** — Collect: "<device> teardown", "bill of materials <device>", `chapters`. Do: list components and cost estimates given. Build: rough cost-structure table labelled as estimates.
569. **Reviewer benchmark table** — Collect: "<product category> benchmark", `min_views = 50000`, `within = "month"`. Do: extract numbers per product per reviewer. Build: cross-reviewer benchmark table showing where results conflict.
570. **Behaviour-shift hypotheses** — Collect: "glp-1 food industry", "ozempic snacks sales", `within = "year"`. Do: list claimed demand shifts by category. Build: hypotheses list for a food company's strategy team to test with data.
571. **Regulatory landscape timeline** — Collect: "<industry> regulation", "<law> explained", `within = "year"`. Do: log rules, dates and who they affect. Build: timeline to review with counsel, not a legal opinion.
572. **AI tool market map** — Collect: "best ai tools for <job>", "<tool> alternatives", `within = "month"`. Do: tag tools by function, price tier, audience. Build: market map grid refreshed monthly.
573. **Content gap analysis vs rivals** — Collect: rival brand channels, `channel_max_videos = 300`. Do: list topics they cover and where views per day are high. Build: list of topics rivals own and gaps you can cover.
574. **Share-of-voice chart** — Collect: one keyword per rival, `within = "week"`, daily schedule. Do: count new videos and keyword mentions per rival per week. Build: share-of-voice chart from `trends.html` data.
575. **Early-adopter signals** — Collect: "<new tech>", `max_views = 5000`, `within = "month"`. Do: find tinkerers' use cases before mainstream coverage. Build: early-signal memo on where a technology is heading.
576. **Quarterly competitive review deck** — Collect: all rival keywords, `published_after` quarter start. Do: map -> reduce into `knowledge/competitors.md`. Build: quarterly review deck with moves, threats and responses.
577. **New entrant alert** — Collect: "new <category> startup", "<category> just launched", `within = "week"`, `rising_views_per_day = 500`. Do: list unknown brand names. Build: new-entrant alert with a one-line profile each.
578. **Competitor distribution channels** — Collect: "where to buy <rival>", "<rival> retail", "<rival> reseller". Do: list channels, retailers and partners mentioned. Build: distribution map showing where you are absent.
579. **Supply chain risk register** — Collect: "<component> shortage", "shipping delays <region>", `within = "week"`. Do: log risks with source and date. Build: risk register with likelihood/impact to confirm with suppliers.
580. **Budget vs premium tier map** — Collect: "best budget <product>", "is premium <product> worth it". Do: map brands to price tiers and value claims. Build: tier map to find an underserved price point.
581. **Forecast dissent map** — Collect: think-tank and university channels, "<industry> outlook 2027", `min_duration = 1800`. Do: list each forecast and who disagrees. Build: dissent map for a planning offsite.
582. **Neighbourhood comparison** — Collect: "living in <neighbourhood>", "moving to <city> pros and cons", `max_views = 50000`. Do: compare costs, commute, amenities claims. Build: comparison table to verify before buying property.
583. **Restaurant concept validation** — Collect: "<cuisine> restaurant <city>", "food tour <city>", `within = "year"`. Do: list existing spots, gaps, price points. Build: concept validation memo for a new restaurant.
584. **Exec one-pager on a market** — Collect: "<market> explained", "<market> 2026", `min_views = 20000`, `sponsorblock`. Do: summarise size claims, players, risks in 300 words. Build: one-pager for a board pre-read with sources.
585. **Business plan class template** — Collect: "market research for business plan", "competitor analysis example", `max_duration = 1200`. Do: extract steps students skip. Build: market-research worksheet template for a business class.
586. **NGO sector landscape** — Collect: "<cause> nonprofit", "<cause> charity explained", `within = "year"`. Do: list organisations, approaches and funding models mentioned. Build: landscape for a foundation's grant strategy.
587. **Release cadence timeline** — Collect: rival keywords plus "update", `published_after` 2 years ago, `lists/` history. Do: date every announced release. Build: release cadence timeline to predict the next launch window.
588. **Attribute ownership matrix** — Collect: "<rival> review" for 6 rivals, `min_views = 10000`. Do: count which attributes (fast, cheap, reliable) reviewers tie to each. Build: matrix of which brand owns which attribute.
589. **Hype cycle placement** — Collect: "<tech> is overhyped", "<tech> real use cases", `within = "year"`. Do: rate tone and evidence over time. Build: hype-cycle chart placing 10 technologies with reasoning.
590. **Market research Q&A bot** — Collect: a year of industry keywords, `yt.py export`. Do: embed the .jsonl for retrieval. Build: internal Q&A bot that answers market questions with timestamped links.
591. **Segment discovery from comments** — Collect: "<category> for beginners", "<category> for professionals", `top_comments = 50`. Do: cluster commenters by need and context. Build: segment list with size hints from views per day.
592. **Five-market comparison** — Collect: same keyword in 5 languages, `translate`, per-keyword `[[keyword_settings]]`. Do: compare adoption, pricing talk and objections. Build: country comparison table for expansion order.
593. **Installer perspective on adoption** — Collect: "heat pump installer", "installing <tech> problems", `max_views = 30000`. Do: list installer objections and customer questions. Build: adoption-barrier report for a manufacturer.
594. **Esports market snapshot** — Collect: "esports business", "esports team revenue", `within = "year"`. Do: extract revenue streams, sponsors and risks named. Build: market snapshot for a brand considering esports.
595. **Competitor-brief Claude skill** — Collect: rival keywords on daily schedule, `CLAUDE.md` in output. Do: define the brief format and sources to cite. Build: Claude skill that writes a fresh brief on any rival on demand.
596. **Failure pattern list** — Collect: "why <startup> failed", "<company> shutdown", `min_duration = 600`. Do: extract causes per failure. Build: pre-mortem checklist of failure patterns in your sector.
597. **M&A implications memo** — Collect: "<acquirer> acquires <target>", `within = "week"`, `top_comments = 20`. Do: list analyst and user takes on impact. Build: implications memo for your leadership with open questions.
598. **Feature parity tracker** — Collect: rival channels, `channel_within = "month"`, monthly runs. Do: log features shown per rival vs yours. Build: feature parity table updated monthly, with `lists/` for history.
599. **Cloud keynote comparison** — Collect: "re:invent keynote", "google cloud next keynote", "microsoft ignite keynote", `min_duration = 3600`. Do: compare strategic bets. Build: side-by-side direction table for an IT strategy team.
600. **Freelance demand scan** — Collect: "most in-demand freelance skills", "<service> clients 2026", `within = "month"`. Do: list services, rates and saturation claims. Build: shortlist of niches for a freelancer to test.
601. **Rival support benchmark** — Collect: "<rival> customer service", "<rival> support experience", `within = "year"`. Do: compare reported response times and fixes. Build: support benchmark to set your own service-level targets.

[↑ Contents](#contents)

### Brand, PR & reputation monitoring

602. **Daily brand mention alert** — Collect: "<brand>", "<brand> review", `within = "today"`, `min_views = 0`, daily schedule. Do: summarise each new video's stance. Build: morning alert listing every mention with a link.
603. **Weekly sentiment chart** — Collect: brand keywords, `within = "week"`. Do: classify each video positive, mixed or negative with a reason. Build: weekly sentiment chart and the top three drivers.
604. **Crisis dashboard** — Collect: "<brand> recall", "<brand> scandal", `rising_views_per_day = 1000`, `within = "today"`. Do: track spread and repeated claims. Build: crisis dashboard from `trends.html` refreshed every run.
605. **Sponsored read audit** — Collect: your sponsored creators' videos, `sponsorblock` off. Do: check each read against your key messages and claims. Build: audit table of message accuracy per creator.
606. **Competitor sponsorship landscape** — Collect: "<rival>" sponsor keywords, `sponsorblock` off, `within = "month"`. Do: list creators reading rival ads and the offers used. Build: sponsorship landscape map for media planning.
607. **Organic fan creator list** — Collect: "<brand>", `max_views = 20000`, `exclude_words = ["sponsored","ad"]`. Do: find creators who praise you unprompted. Build: partnership shortlist of public channels to approach.
608. **Spokesperson message consistency** — Collect: your executives' public interviews, `timestamps`. Do: compare key messages across appearances. Build: media-training notes on drift, with clips to review.
609. **Press conference quote log** — Collect: "<brand> press conference", `within = "today"`, `timestamps`. Do: extract every quotable line with speaker. Build: quote log with links to the exact second for the comms team.
610. **Misinformation correction list** — Collect: "<brand>" plus "truth", "exposed", `within = "month"`. Do: list factual claims and mark which are wrong per your records. Build: correction sheet with honest, sourced responses.
611. **Recall support FAQ** — Collect: "<product> recall", `within = "week"`, `top_comments = 40`. Do: extract what worried customers ask most. Build: support FAQ and call-centre script for the recall.
612. **Brand voice guide from own channel** — Collect: your brand channel, `channel_max_videos = 100`. Do: describe tone, phrases and structure in top-performing videos. Build: brand voice guide with examples to keep.
613. **Monthly earned media report** — Collect: brand keywords, `within = "month"`, `min_views = 5000`. Do: total views, mentions and top quotes. Build: earned media report for leadership from `video_list.csv`.
614. **Crisis comms playbook** — Collect: "pr crisis case study", "worst corporate apology", `min_duration = 600`. Do: extract what responses helped or worsened outcomes. Build: crisis playbook with steps by hour.
615. **Apology effectiveness rubric** — Collect: public company apology videos and reaction videos, `top_comments = 30`. Do: link apology features to reception. Build: rubric for reviewing a draft statement.
616. **Event sponsorship recap** — Collect: "<event> highlights", "<event> vlog", `within = "week"`. Do: count brand mentions and context. Build: sponsorship exposure recap for the partner team.
617. **Creator brand-safety check** — Collect: a candidate creator's public channel, `channel_within = "year"`. Do: flag public statements conflicting with your brand values. Build: brand-safety checklist result before signing a deal.
618. **Comment sentiment on own videos** — Collect: your channel, `top_comments = 50`, `channel_within = "month"`. Do: group comments into praise, complaints, questions. Build: monthly community report with reply priorities.
619. **Exec thought-leadership plan** — Collect: rival execs' talks, "<industry> keynote", `within = "year"`. Do: map topics already crowded vs open. Build: speaking topic plan for your CEO.
620. **Campaign message pull-through** — Collect: brand + campaign keywords, `published_after` launch date. Do: count how often creators repeat each campaign message. Build: pull-through scorecard per message.
621. **Non-English reputation check** — Collect: "<brand>", `languages = ["es","fr","ja"]`, `translate`. Do: compare themes per market. Build: market-by-market reputation summary for regional PR leads.
622. **Employer brand gaps** — Collect: "working at <brand>", "<brand> interview experience", `within = "year"`. Do: aggregate themes, not individuals. Build: employer brand gap list for HR and recruiting marketing.
623. **Cause awareness tracker** — Collect: "<cause>" keywords, daily schedule, `include_shorts`. Do: track new videos and attention around your campaign. Build: awareness tracker for a nonprofit board update.
624. **Public official mentions tracker** — Collect: "<politician> <your industry>", `within = "week"`, `timestamps`. Do: log public statements about your company or sector. Build: public-affairs tracker with exact-second links.
625. **Viral service failure SOP** — Collect: "terrible customer service <industry>", `rising_views_per_day = 2000`. Do: extract what turned complaints viral. Build: service recovery SOP for frontline staff.
626. **PR pitch calendar** — Collect: niche channels covering your field, `channel_within = "month"`. Do: list recurring topics and seasonal angles. Build: pitch calendar matching your news to what each show covers.
627. **Podcast guesting shortlist** — Collect: "<topic> podcast", `channel_tabs = ["streams","videos"]`, `min_duration = 2400`. Do: list shows that interview guests in your niche. Build: guesting shortlist with episode angles.
628. **Press kit FAQ** — Collect: "<brand>" reviews, `top_comments = 30`. Do: list questions creators and viewers keep asking. Build: press kit FAQ and fact sheet answering them.
629. **Rebrand reaction tracking** — Collect: "<brand> new logo", "<brand> rebrand", `within = "week"`, `top_comments = 40`. Do: sort reactions by element (name, logo, colours). Build: rebrand feedback summary for the design agency.
630. **Big-game ad scorecard** — Collect: "super bowl ads ranked", "best ads <year>", `within = "week"`. Do: tally rankings and reasons per ad. Build: ad reaction scorecard for a creative team's review.
631. **Brand association map** — Collect: "<brand>", `within = "year"`, `yt.py find`. Do: list words and topics said near the brand name. Build: association word map to compare with your intended positioning.
632. **Ambassador fit memo** — Collect: a celebrity's public interviews and channel, `within = "year"`. Do: summarise public stances and audience reaction. Build: fit memo for an ambassador decision.
633. **Negative-wave anomaly alert** — Collect: brand keywords, daily schedule. Do: flag days where many new videos repeat one claim. Build: anomaly alert prompting an honest public response, not suppression.
634. **Restaurant vlogger reviews** — Collect: "<restaurant name>", "<city> food review", `max_views = 50000`. Do: list praise and complaints by dish and service. Build: owner's action plan and polite reply drafts.
635. **Destination perception report** — Collect: "visiting <city>", "<city> travel vlog", `languages` of key source markets, `translate`. Do: map perceptions by country. Build: perception report for a tourism board.
636. **Fan pulse report** — Collect: "<team> fan reaction", "<team> podcast", `within = "week"`. Do: track mood about coaching, signings, ticket prices. Build: weekly fan pulse report for the club's comms team.
637. **Album reception summary** — Collect: "<artist> <album> reaction", "<album> review", `within = "week"`. Do: aggregate verdicts by track. Build: reception summary for the label, quoting briefly with credit.
638. **BookTube reception digest** — Collect: "<book title> review", `max_views = 30000`, `within = "month"`. Do: list praised and criticised elements. Build: reception digest for the publisher; ask reviewers before quoting.
639. **Post-patch community update** — Collect: "<game> update", `within = "today"`, `top_comments = 30`. Do: extract top grievances and misunderstandings. Build: draft community update addressing them directly.
640. **Crisis tabletop exercise** — Collect: "<industry> data breach response", "product recall press", `min_duration = 600`. Do: build a scenario timeline from public cases. Build: tabletop exercise script with injects for a PR team drill.
641. **Defamation consult evidence log** — Collect: "<brand>", `timestamps`, `within = "month"`. Do: log claims verbatim with time links, no actions taken. Build: neutral evidence log plus questions for a lawyer.
642. **Sponsor disclosure check** — Collect: your paid creators' videos, `sponsorblock` off, `chapters`. Do: check each discloses the paid relationship clearly. Build: disclosure compliance sheet to share with creators.
643. **Partnership announcement reception** — Collect: "<brand> x <partner>", `within = "week"`, `top_comments = 30`. Do: separate audience reactions to each brand. Build: partner perception note for the next co-branding decision.
644. **Annual reputation audit** — Collect: brand keywords, `within = "year"`, `library.html`. Do: map -> reduce into themes by quarter. Build: year-in-review reputation audit with turning points.
645. **Proof points from praise** — Collect: "<brand> review", `min_views = 10000`, `within = "year"`. Do: extract what reviewers praise with evidence. Build: proof-point list for marketing, each linked to its source.
646. **Media monitoring Claude skill** — Collect: daily brand runs, `CLAUDE.md` in the output folder. Do: define summary rules, alert thresholds, tone labels. Build: Claude skill that writes a cited monitoring report on request.
647. **Exec weekly PR digest** — Collect: brand, rival and industry keywords, `within = "week"`, `sponsorblock`. Do: pick five items that matter and why. Build: 1-page Friday digest for the executive team.
648. **Greenwashing risk check** — Collect: "<brand> sustainability", "<brand> greenwashing", `within = "year"`. Do: list public challenges to your green claims. Build: risk list for legal and sustainability teams to verify.
649. **Founder personal brand plan** — Collect: founders in your niche, `channel_within = "year"`, `min_views = 20000`. Do: find topics and formats that perform. Build: 12-week content plan for the founder.
650. **Conference coverage recap** — Collect: "<conference> recap", `within = "week"`, `title_must_contain = ["<conference>"]`. Do: find mentions of your talk or booth. Build: event coverage recap with clips for the sales team.
651. **Seeding campaign recap** — Collect: "<product> unboxing", `published_after` ship date, `include_shorts`. Do: list which seeded creators posted and what they said. Build: seeding recap with reach and key quotes.
652. **Holding statement bank** — Collect: past brand-crisis coverage in your industry, `min_duration = 300`. Do: list scenario types that recur. Build: bank of pre-approved holding statements per scenario.
653. **Mentions dataset for BI** — Collect: brand keywords on daily schedule, `yt.py export`. Do: add sentiment and topic columns. Build: .csv feed for a Looker or Power BI reputation dashboard.
654. **Meme and nickname glossary** — Collect: "<brand> meme", "<brand>" with `include_shorts`, `within = "month"`. Do: list nicknames, in-jokes and their origin videos. Build: glossary so social staff understand references.
655. **Five-year perception shift** — Collect: "<brand> review" with `published_before` 2022 and `published_after` 2025. Do: compare themes then vs now. Build: before/after perception report for a brand strategy review.
656. **Affiliate claim accuracy check** — Collect: "<brand> discount code", "<product> review", `sponsorblock` off. Do: flag affiliate claims that overstate specs or results. Build: correction list sent to affiliate partners.

[↑ Contents](#contents)

## AI, software and security

### AI & machine learning

657. **Daily AI release radar** — Collect: "new AI model", "just released" with `within = "today"`, `rising_views_per_day = 5000`. Do: list each launch, maker, claimed benchmarks, open or closed weights. Build: a 5-bullet morning briefing for Slack.
658. **Local LLM hardware picker** — Collect: "local LLM GPU", "run llama on mac", `within = "year"`, `top_comments = 20`. Do: extract tokens/sec per GPU, RAM and model size testers report. Build: a hardware-vs-speed spreadsheet with source links.
659. **Ollama beginner cheat sheet** — Collect: "ollama tutorial", `min_duration = 480`, `subtitles_only`. Do: pull the exact commands, flags and model tags demonstrated. Build: a one-page cheat sheet with `timestamps` links to each demo.
660. **Prompt technique library** — Collect: "prompt engineering", `within = "year"`, `min_views = 50000`. Do: extract every named technique with example wording and claimed use. Build: a searchable `knowledge/prompting.md`.
661. **ComfyUI workflow index** — Collect: channels of top ComfyUI node creators, `chapters`. Do: map each workflow to its nodes, models and purpose. Build: a table of workflows by task (upscale, inpaint, video) with chapter links.
662. **AI video generator scorecard** — Collect: "veo vs sora", "kling ai review", "runway gen" `within = "month"`. Do: tally reviewer verdicts on motion, prompt adherence, clip length, price. Build: a monthly-refreshed scorecard.
663. **Agent framework decision tree** — Collect: "langgraph tutorial", "crewai", "autogen" `within = "year"`. Do: extract when reviewers recommend each and why people abandon them. Build: a decision tree for picking an agent framework.
664. **LoRA fine-tuning recipe cards** — Collect: "fine tune llama lora", "unsloth", `min_duration = 900`. Do: pull dataset sizes, hyperparameters, VRAM and training times stated. Build: recipe cards per model size, marked "verify on your data".
665. **AI prediction ledger** — Collect: "AGI by", "AI will replace" `within = "week"`, `top_comments = 30`. Do: separate dated, checkable predictions from vibes; record who said what. Build: a ledger to re-score in 12 months.
666. **Paper explainer reading list** — Collect: Yannic Kilcher, Two Minute Papers channels, `channel_within = "month"`. Do: list papers covered with a one-line contribution each. Build: a reading list ranked by how many explainers covered it.
667. **Eval plan generator** — Collect: "LLM evaluation", "evals for LLM apps", `subtitles_only`. Do: extract eval types (golden sets, LLM-as-judge, pairwise) and pitfalls. Build: a Claude skill that drafts an eval plan for a described app.
668. **RAG pre-launch checklist** — Collect: "RAG tutorial", "RAG mistakes", `top_comments = 20`. Do: gather chunking, embedding and reranking advice plus failures commenters hit. Build: a go/no-go checklist for a RAG feature.
669. **Benchmark claim audit** — Collect: "beats GPT", "state of the art" `within = "month"`, sort by keyword mentions. Do: list every benchmark number quoted, model and video. Build: a CSV of claims to check against official leaderboards.
670. **Hidden-gem AI tutorials** — Collect: "AI automation tutorial", `max_views = 5000`, `within = "month"`. Do: find niche, practical workflows big channels skip. Build: a "20 under-the-radar tutorials" newsletter section.
671. **Outside-the-bubble AI digest** — Collect: Chinese and French AI keywords with `languages` and `translate = "en"`. Do: note what those creators cover that English channels don't. Build: a weekly non-English AI digest.
672. **Self-study ML syllabus** — Collect: Stanford CS229/CS224N playlists and Andrej Karpathy's channel. Do: order topics by dependency and note prerequisites. Build: a 12-week syllabus with timestamped lecture links.
673. **ML interview flashcards** — Collect: "machine learning interview questions", `min_duration = 600`. Do: extract Q&A pairs on bias-variance, regularisation, metrics, leakage. Build: a 200-card Anki deck.
674. **Image prompt style sheet** — Collect: "midjourney prompts", "flux prompt guide" `within = "month"`. Do: extract style terms, parameters and negative-prompt tips with examples. Build: a style reference sheet for a design team.
675. **AI subscription change log** — Collect: "chatgpt plus worth it", "claude pro limits" `within = "week"`. Do: note price and usage-limit changes creators report, with dates. Build: a change log to verify against vendor pages.
676. **Production AI case-study database** — Collect: AI Engineer and similar conference channels, `channel_within = "year"`. Do: extract company, use case, stack and measured results. Build: a filterable case-study table for sales decks.
677. **AI safety position map** — Collect: "AI alignment", "AI safety debate" interviews, `min_duration = 1800`. Do: map public figures' stated positions, arguments and cruxes. Build: an argument map for a reading group.
678. **Which-quant-to-download guide** — Collect: "GGUF quantization", "Q4 vs Q8", `top_comments = 15`. Do: summarise reported quality-vs-size trade-offs. Build: a plain-language explainer with a RAM-to-quant lookup table.
679. **Open-source voice stack** — Collect: "whisper local", "open source text to speech" `within = "year"`. Do: list tools, reported latency, hardware and licences. Build: a stack recommendation doc for a voice-assistant project.
680. **Early AI topic detector** — Collect: 30 AI keywords on `schedule_daily.bat`. Do: watch `trends.html` for spikes in new videos and attention. Build: a weekly shortlist of topics to cover before they peak.
681. **AI agents keyword map** — Collect: seed "AI agents" through the related keywords finder. Do: cluster suggestions into subtopics and intent. Build: a keyword map that drives a 3-month content calendar.
682. **AI literacy lesson** — Collect: "how ChatGPT works explained", `max_duration = 900`, `include_shorts = false`. Do: extract the simplest analogies for tokens, training, hallucination. Build: a 45-minute high-school lesson plan.
683. **Hallucination example bank** — Collect: "AI hallucination examples", "ChatGPT got it wrong", `top_comments = 25`. Do: catalogue concrete failures by type. Build: a staff training deck on checking AI output.
684. **Official announcement timeline** — Collect: OpenAI, Anthropic, Google DeepMind channels, `channel_max_videos = 30`. Do: extract features announced per event with dates. Build: a timeline of first-party AI announcements.
685. **Open-weights licence questions** — Collect: "llama license", "open source AI license" `within = "year"`. Do: list the licence terms creators discuss and their interpretations. Build: a per-model question list for legal review.
686. **Internal agent build SOP** — Collect: "n8n AI agent", "make.com AI agent", `min_views = 20000`. Do: extract repeatable build steps, nodes and error-handling tips. Build: an SOP for an ops team building internal agents.
687. **MCP server catalogue** — Collect: "MCP server", "model context protocol" `within = "month"`. Do: list servers demoed, what they connect to and setup gotchas. Build: a catalogue table with demo timestamps.
688. **Data labelling guidelines** — Collect: "data annotation guidelines", "label studio", `subtitles_only`. Do: extract QA methods and agreement tips. Build: a labelling guideline template for a new annotation team.
689. **Kaggle competition starter** — Collect: "kaggle grandmaster", "kaggle solution walkthrough", `min_duration = 1200`. Do: extract recurring winning moves (CV setup, features, ensembling). Build: a competition starter checklist.
690. **Graded CV project list** — Collect: "YOLO tutorial", "opencv project" `within = "year"`. Do: list projects with difficulty, dataset and hardware needed. Build: a graded project list for a bootcamp.
691. **Conference themes for lab meeting** — Collect: NeurIPS/ICML talk playlists. Do: map -> reduce: a note per talk in `notes/`, then cross-talk themes. Build: `knowledge/neurips-themes.md` for a lab meeting.
692. **AI app idea scorecard** — Collect: "AI SaaS idea", "my AI app makes", `top_comments = 30`. Do: separate revenue claims from evidence; collect commenter objections. Build: a validation scorecard for one idea.
693. **Reusable eval prompt set** — Collect: "GPT vs Claude test", "LLM comparison" `within = "month"`. Do: extract the exact test prompts reviewers use and what each probes. Build: a JSON prompt set for your own model evals.
694. **Executive AI briefing** — Collect: "generative AI for business leaders", `min_duration = 600`, `sponsorblock`. Do: distil risks, costs and opportunities in non-technical words. Build: a 2-page board briefing.
695. **Embedding model matrix** — Collect: "embedding models compared", "vector database" `within = "year"`. Do: extract dimensions, cost, multilingual claims. Build: a selection matrix for a RAG build, claims flagged to test.
696. **AI music landscape note** — Collect: "suno", "udio", "AI music copyright" `within = "month"`. Do: summarise capabilities, legal debates and musician reactions. Build: a landscape note for an indie label.
697. **Support chatbot risk register** — Collect: "AI customer service agent", `top_comments = 20`. Do: collect what worked, failures and escalation designs described. Build: a rollout risk register for a support team.
698. **Weekly fastest-rising tools** — Collect: "new AI tool" `within = "week"`, `rising_views_per_day = 2000`, `exclude_words = "giveaway"`. Do: rank by views per day. Build: a top-10 tools newsletter segment.
699. **Math-for-ML refresher** — Collect: 3Blue1Brown and StatQuest channels. Do: map each video to linear algebra, calculus or probability concepts. Build: a refresher roadmap plus flashcards.
700. **RL and RLHF glossary** — Collect: "reinforcement learning explained", "RLHF", `subtitles_only`. Do: extract term definitions in creators' plain words. Build: a glossary with links to the exact second.
701. **AI art ethics debate pack** — Collect: "AI art ethics", "AI copyright lawsuit" `within = "year"`, `top_comments = 20`. Do: collect strongest arguments per side. Build: a classroom debate pack with motion, cards and sources.
702. **GPU rental cost estimate** — Collect: "runpod", "rent cloud GPU" `within = "year"`. Do: extract quoted hourly prices and hidden costs. Build: a spreadsheet estimating a 7B LoRA run, prices marked "check current".
703. **Founder interview position table** — Collect: long-form interviews via `only_channels` (Lex Fridman, Dwarkesh). Do: extract each guest's stated views on scaling and open source. Build: a quote-cited position table.
704. **AI accessibility resource guide** — Collect: "AI for blind users", "AI accessibility tools" `within = "year"`. Do: list tools, tasks they help with and user feedback. Build: a guide for a disability services office.
705. **AI news RAG chatbot** — Collect: 50 AI channels daily, then `yt.py export`. Do: embed the .jsonl into a vector store. Build: a bot answering "what did creators say about X this week" with links.
706. **Agent failure-mode review** — Collect: "AI agent failed", "agents don't work", `top_comments = 20`. Do: categorise failures (loops, tool misuse, cost blow-ups). Build: a design-review checklist for agent projects.
707. **Synthetic data how-to** — Collect: "synthetic data generation LLM", `min_duration = 600`. Do: extract generation techniques, quality filters and stated risks. Build: a how-to guide for a data team.
708. **Vetted AI tools for teachers** — Collect: "AI tools for teachers" `within = "month"`, `max_views = 20000`. Do: list tools teachers actually use and classroom caveats. Build: a vetted tool list for a school.
709. **Edge AI build guide** — Collect: "raspberry pi AI", "jetson orin nano" `within = "year"`. Do: extract models run, reported fps and setup steps. Build: a hobbyist build guide with a parts list.
710. **Asian AI talks in English** — Collect: Japanese and Korean AI conference talks, `translate = "en"`. Do: summarise key results and demos. Build: English summaries for a global team wiki.
711. **Model-picker Claude skill** — Collect: "which LLM should I use", "best model for coding" `within = "month"`. Do: map task types to models creators recommend. Build: a Claude skill that suggests a model and cites the consensus.

[↑ Contents](#contents)

### Software development & vibe coding

712. **Claude Code team playbook** — Collect: "claude code" `within = "month"`, `min_views = 10000`, `chapters`. Do: extract CLAUDE.md setups, subagent, hook and slash-command workflows. Build: a team playbook with timestamp links.
713. **AI coding tool verdicts** — Collect: "cursor vs claude code", "copilot vs" `within = "month"`, `top_comments = 30`. Do: tally verdicts by task type (refactor, greenfield, debugging). Build: a comparison table for a tooling decision.
714. **Vibe coding guardrails** — Collect: "vibe coding mistakes", "AI broke my app", `top_comments = 25`. Do: categorise failures (no tests, leaked keys, spaghetti). Build: a guardrails checklist for non-programmers shipping apps.
715. **Framework migration runbook** — Collect: "next.js app router migration", `subtitles_only`. Do: list breaking changes, gotchas and the step order demoed. Build: a migration runbook with links to each demo.
716. **30-day Rust plan** — Collect: "learn rust" playlists, `min_duration = 1200`. Do: order concepts and note where learners get stuck (from comments). Build: a 30-day plan with daily exercises.
717. **Architecture talk knowledge base** — Collect: GOTO, NDC and InfoQ channels, `channel_within = "year"`. Do: map -> reduce notes per talk into patterns and trade-offs. Build: `knowledge/architecture.md`.
718. **Debugging technique flashcards** — Collect: "how I debug", "debugging tips", `min_views = 20000`. Do: extract techniques (bisect, minimal repro, logging strategy). Build: flashcards for junior developers.
719. **System design study guide** — Collect: "system design interview", `min_duration = 1800`. Do: extract each problem's components, bottlenecks and trade-offs. Build: a study guide of 25 worked designs.
720. **Salary negotiation prep** — Collect: "software engineer salary negotiation" `within = "year"`, `top_comments = 20`. Do: map tactics and reported ranges as opinions. Build: a prep worksheet of questions and claims to check.
721. **Weekly "what changed" note** — Collect: "react 19", "python 3.14", "node 24" `within = "week"`. Do: summarise new features and adoption caveats raised. Build: a weekly upgrade note for the team channel.
722. **PR review checklist** — Collect: "code review best practices", `subtitles_only`. Do: extract review criteria and reviewer anti-patterns. Build: a PR checklist plus a pull-request template.
723. **Coding club curriculum** — Collect: freeCodeCamp channel, `channel_max_videos = 200`, `min_duration = 3600`. Do: cluster courses by topic and difficulty. Build: a two-term curriculum for a school coding club.
724. **Testing policy doc** — Collect: "TDD debate", "unit vs integration tests", `top_comments = 20`. Do: map arguments for each style and when each wins. Build: a written testing policy for a codebase.
725. **Agent rules starter kit** — Collect: "CLAUDE.md example", "cursor rules" `within = "month"`. Do: extract rule files and conventions shown on screen and explained. Build: starter CLAUDE.md and .cursorrules templates.
726. **Indie stack spreadsheet** — Collect: "I built a SaaS", `max_views = 10000`, `within = "year"`. Do: extract stack, time to launch and revenue claims (unverified). Build: a spreadsheet of indie stacks.
727. **Error-to-fix index** — Collect: broad coding tutorials, then `yt.py find "cannot read properties of undefined"`. Do: locate videos where each error gets fixed. Build: a personal error index linking to the exact second.
728. **Monolith vs microservices ADR** — Collect: "microservices vs monolith", `min_duration = 900`. Do: extract decision criteria and regret stories. Build: an ADR template pre-filled with considerations.
729. **API style guide** — Collect: "REST API design", "GraphQL vs REST". Do: extract naming, versioning, pagination and error-format advice. Build: a house API style guide.
730. **Game engine matrix** — Collect: "godot vs unity", "unreal 5 beginner" `within = "year"`. Do: record verdicts by genre, team size and platform. Build: an engine decision matrix for a small studio.
731. **Cross-platform mobile RFC** — Collect: "flutter vs react native", "kotlin multiplatform", `top_comments = 20`. Do: summarise performance and hiring arguments. Build: an RFC draft for a CTO.
732. **Refactoring dojo katas** — Collect: "refactoring legacy code", `chapters`. Do: extract before/after examples and the moves used. Build: a set of kata exercises for a team dojo.
733. **Vibe coding course for owners** — Collect: "build an app with AI no coding" `within = "month"`, `max_duration = 1800`. Do: sequence the steps beginners follow. Build: a 5-lesson course for small-business owners.
734. **First contribution onboarding** — Collect: "first open source contribution". Do: extract steps, etiquette and common rejections. Build: an onboarding doc for students joining open-source projects.
735. **Core Web Vitals checklist** — Collect: "core web vitals", "web performance" `within = "year"`. Do: extract fixes ranked by claimed impact. Build: a performance audit checklist for a marketing site.
736. **Database choice tree** — Collect: "postgres vs mongodb", "sqlite in production". Do: map arguments by workload type. Build: a decision tree for picking a datastore.
737. **Pro debugging clip index** — Collect: known streamers with `channel_tabs = "streams"`. Do: find problem-solving moments and what unlocked them. Build: a "watch how pros debug" index with timestamps.
738. **1:1 question bank** — Collect: "engineering manager advice", "staff engineer" `min_duration = 1200`. Do: extract recurring advice on growth and feedback. Build: a 1:1 question bank for new tech leads.
739. **Take-home grading rubric** — Collect: "coding interview from the interviewer side". Do: extract what interviewers say they score. Build: a fair, written rubric for take-home assignments.
740. **Standup dev news digest** — Collect: Fireship, Theo, ThePrimeagen with `channel_within = "today"`, `sponsorblock`. Do: summarise news items only. Build: a 3-minute standup digest.
741. **Docs backlog from comments** — Collect: tutorials others made about your library, `top_comments = 50`. Do: find recurring confusion in comments. Build: a docs improvement backlog ranked by frequency.
742. **DevRel content gaps** — Collect: "<your framework> tutorial" `within = "year"`. Do: find topics with few, old or low-view videos. Build: a DevRel content plan for next quarter.
743. **SQL window function snippets** — Collect: "SQL window functions", `timestamps`. Do: extract each query pattern and the problem it solves. Build: a snippet library with links to explanations.
744. **Front-end a11y audit** — Collect: "web accessibility aria", "screen reader testing". Do: extract checks and common mistakes. Build: an accessibility audit checklist for front-end PRs.
745. **Legacy stack onboarding** — Collect: "COBOL", "Delphi" with `within = "any"`. Do: gather rare expert knowledge and tooling tips. Build: onboarding notes for a maintenance team.
746. **Branching strategy SOP** — Collect: "git rebase vs merge", "trunk based development". Do: summarise arguments and team-size fit. Build: a team branching SOP.
747. **AI-written PR review** — Collect: "AI generated code security", "AI code review" `within = "year"`. Do: list flaw types reviewers keep finding. Build: a checklist for reviewing AI-written pull requests.
748. **Stale tutorial warnings** — Collect: one framework with `within = "any"` and again with `within = "month"`. Do: diff APIs taught then vs now. Build: a "don't follow these old patterns" note for learners.
749. **TypeScript generics flashcards** — Collect: "TypeScript generics", "conditional types", `subtitles_only`. Do: extract examples and explanations. Build: an Anki deck with code snippets.
750. **Stack recommender skill** — Collect: "best tech stack 2026", `top_comments = 20`. Do: capture the reasoning behind each recommendation. Build: a Claude skill that proposes a stack and cites why.
751. **Human-AI pairing dataset** — Collect: "claude code real project", `min_duration = 2400`. Do: code how often presenters correct the AI and the type of correction. Build: a dataset for a study on AI-assisted coding.
752. **SDK pain-point report** — Collect: tutorials for your API and competitors', `top_comments = 30`. Do: compare pain points mentioned. Build: a product feedback report for a dev-tools team.
753. **Kids Python lessons** — Collect: "python for kids", `max_duration = 1200`. Do: extract projects and explanations that land with children. Build: a 6-lesson sequence for a primary teacher.
754. **Language momentum radar** — Collect: Rust, Go, Zig, Gleam keywords daily. Do: read `trends.html` for new videos and attention over time. Build: a quarterly tech-radar chart.
755. **Clean code debate summary** — Collect: "clean code is bad", "uncle bob" `top_comments = 20`. Do: present each side's strongest points fairly. Build: a balanced reading summary for a book club.
756. **WebAssembly use-case catalogue** — Collect: "webassembly in production", "wasm use cases". Do: list real deployments and stated benefits. Build: a catalogue for an architecture review.
757. **Burnout retro guide** — Collect: "developer burnout", `top_comments = 30`. Do: extract recurring themes and team practices people credit (not medical advice). Build: a team retro discussion guide.
758. **Freelance pricing worksheet** — Collect: "freelance developer rates", "how to price dev projects". Do: map pricing models and reported pitfalls. Build: a pricing worksheet with questions to answer.
759. **Discord coding tip bot** — Collect: "coding tip", `include_shorts = true`, `max_duration = 60`. Do: extract one-line tips and dedupe. Build: a Discord bot posting one tip a day with source credit.
760. **Maintainer governance ideas** — Collect: "open source maintainer burnout", "project governance". Do: extract funding and governance models. Build: a GOVERNANCE.md draft for a growing project.
761. **Multilingual teaching notes** — Collect: Spanish and Hindi coding channels, `translate = "en"`. Do: note teaching approaches and examples. Build: design notes for a multilingual programming course.
762. **Support macros from own videos** — Collect: your company channel, all videos. Do: `yt.py find` each common support question. Build: support macros that link to the exact second.
763. **Low-code vs custom tree** — Collect: "bubble.io review", "retool vs custom". Do: extract limits users hit and cost stories. Build: a decision tree for a business choosing how to build.
764. **Data pipeline pattern reference** — Collect: "dbt tutorial", "airflow best practices", `min_duration = 900`. Do: extract patterns and anti-patterns. Build: a pattern reference for a data engineering team.
765. **Claude Code skills backlog** — Collect: "claude code skills", "claude code hooks" `within = "week"`. Do: list community skills and hooks and what they automate. Build: a backlog of skills to build for your repo.
766. **Technical writing guide** — Collect: "technical writing for developers", "write good docs". Do: extract structure and style rules. Build: a docs style guide plus a README template.

[↑ Contents](#contents)

### DevOps, cloud & homelab

767. **AWS SAA study plan** — Collect: "AWS solutions architect associate" playlists, `min_duration = 1200`. Do: map videos to exam domains and extract facts. Build: a 6-week study plan plus flashcards.
768. **Kubernetes troubleshooting runbook** — Collect: "CrashLoopBackOff", "kubernetes troubleshooting", `timestamps`. Do: extract symptoms, commands and fixes. Build: a runbook keyed by error, linked to demos.
769. **Homelab starter shopping list** — Collect: "homelab beginner" `within = "year"`, `top_comments = 20`. Do: extract recommended gear, prices and regrets. Build: a starter shopping list at three budgets.
770. **NAS OS decision matrix** — Collect: "synology vs truenas vs unraid" `within = "year"`. Do: tally verdicts on expansion, apps and reliability. Build: a decision matrix for a first NAS.
771. **Self-hosted app catalogue** — Collect: "self hosted apps", "must have docker containers" `within = "year"`. Do: list apps, purpose and setup difficulty. Build: a catalogue with compose notes per app.
772. **Cloud savings checklist** — Collect: "AWS cost optimization", "cut cloud bill". Do: extract tactics and the savings creators claim. Build: a savings checklist to test against your own bill.
773. **Terraform style guide** — Collect: "terraform best practices", "terraform modules", `min_duration = 900`. Do: extract layout, state and module conventions. Build: a team Terraform style guide.
774. **CI/CD template set** — Collect: "github actions tutorial", "gitlab ci pipeline". Do: extract workflows shown (test, build, deploy, cache). Build: reusable pipeline templates with notes.
775. **Postmortem lessons database** — Collect: SREcon and other conference playlists. Do: note per talk: trigger, detection gap, fix, lesson. Build: a searchable lessons-learned database.
776. **Proxmox install SOP** — Collect: "proxmox setup", "proxmox beginner" `within = "year"`, `chapters`. Do: extract install and post-install steps. Build: an SOP with chapter links for each step.
777. **Home VLAN plan** — Collect: "VLAN homelab", "unifi network setup". Do: extract segmentation schemes (IoT, guest, servers). Build: a network plan and firewall rule table for your house.
778. **Remote access guide** — Collect: "tailscale homelab", "wireguard setup" `within = "year"`. Do: compare approaches and setup steps. Build: a step-by-step guide for reaching home services safely.
779. **Cloud announcement digest** — Collect: AWS, Google Cloud, Azure channels with `channel_within = "today"`. Do: summarise launches relevant to your stack. Build: a daily Slack digest.
780. **re:Invent knowledge base** — Collect: re:Invent session playlists. Do: map -> reduce: note per session, then themes by service. Build: `knowledge/reinvent.md` for planning next year.
781. **Kubernetes-or-not memo** — Collect: "do you need kubernetes", "kubernetes alternatives", `top_comments = 30`. Do: map arguments by team size. Build: a one-page memo for a small team.
782. **Observability reference architecture** — Collect: "opentelemetry", "prometheus grafana tutorial". Do: extract components and data flow. Build: a reference architecture diagram description.
783. **On-call handbook** — Collect: "on call best practices", "SRE alert fatigue". Do: extract rotations, alert hygiene and handoff habits. Build: an on-call handbook for a new SRE team.
784. **Docker beginner lessons** — Collect: "docker tutorial for beginners", `max_duration = 1800`. Do: sequence concepts and exercises. Build: a 4-lesson plan for a college lab.
785. **3-2-1 backup worksheet** — Collect: "homelab backup strategy", "restic", "backblaze b2". Do: extract tools and setups. Build: a worksheet that turns your data into a backup plan.
786. **Low-power homelab sheet** — Collect: "low power homelab", "idle power consumption". Do: extract measured idle watts per device. Build: a spreadsheet estimating yearly electricity cost.
787. **Mini PC comparison** — Collect: "N100 mini pc", "mini pc homelab" `within = "year"`, `max_views = 50000`. Do: extract specs, thermals, quirks. Build: a comparison table for a cluster build.
788. **Home Assistant recipes** — Collect: "home assistant automations" `within = "year"`. Do: extract trigger-condition-action recipes. Build: a recipe list sorted by room.
789. **Platform engineering trend chart** — Collect: "platform engineering", "internal developer platform" daily. Do: read `trends.html`. Build: a trend chart for a leadership slide.
790. **Multi-cloud debate map** — Collect: "multi cloud strategy", "single cloud". Do: map the arguments and stated failure stories. Build: a balanced discussion doc for an architecture board.
791. **Serverless cold-start guide** — Collect: "lambda cold start", "serverless pitfalls". Do: extract mitigations and when serverless is advised against. Build: a pattern guide.
792. **GitOps setup steps** — Collect: "argo cd tutorial", "flux cd" `subtitles_only`. Do: extract repo layouts and steps. Build: a GitOps setup guide for a staging cluster.
793. **Linux sysadmin Anki deck** — Collect: "linux interview questions", "linux sysadmin". Do: extract Q&A pairs. Build: an Anki deck of commands and concepts.
794. **First cloud cert decision** — Collect: "AWS vs Azure vs GCP certification" `top_comments = 30`. Do: map advice by career goal. Build: a decision tree for choosing a first cloud cert.
795. **Cloud migration risk register** — Collect: "cloud migration lessons", "lift and shift mistakes". Do: extract risks and mitigations. Build: a risk register for a migration project.
796. **FinOps showback model** — Collect: "finops", "cloud cost allocation" talks. Do: extract tagging and showback practices. Build: a showback model proposal for finance.
797. **Reverse proxy comparison** — Collect: "traefik vs caddy vs nginx proxy manager". Do: extract config effort and features. Build: a comparison plus starter configs to adapt.
798. **Quiet rack build** — Collect: "server rack noise", "quiet homelab". Do: extract fan, enclosure and placement tips. Build: a noise-reduction checklist for a flat.
799. **Media server pick** — Collect: "jellyfin vs plex", `top_comments = 20`. Do: tally reasons people switch. Build: a decision card for a family media server.
800. **Small-office IT SOP** — Collect: "small business IT setup", "IT on a budget". Do: extract essentials (backups, accounts, updates). Build: an SOP for a 10-person office.
801. **Ansible playbook backlog** — Collect: "ansible homelab", "ansible tutorial". Do: list tasks people automate. Build: a prioritised backlog of playbooks for your servers.
802. **Postgres restore runbook** — Collect: "postgres backup restore", "pg_dump vs pgbackrest". Do: extract procedures and gotchas. Build: a tested-restore runbook.
803. **DR drill plan** — Collect: "disaster recovery test", "DR tabletop". Do: extract drill formats and metrics (RTO/RPO). Build: a disaster-recovery drill plan.
804. **Niche homelab inspiration** — Collect: "homelab tour", `max_views = 3000`, `within = "month"`. Do: note unusual builds and ideas. Build: an inspiration board for your next project.
805. **Chaos experiment list** — Collect: "chaos engineering", "game day". Do: extract experiments and safety rules. Build: a starter list of chaos experiments for staging.
806. **Outage early warning** — Collect: "AWS outage", "azure down" `within = "today"`, `rising_views_per_day = 1000`. Do: flag fresh outage chatter. Build: a scheduled alert to cross-check with status pages.
807. **ZFS cheat sheet** — Collect: "zfs explained", "zfs pool layout". Do: extract terms and recommended layouts. Build: a glossary plus a pool-planning cheat sheet.
808. **Pi k3s cluster guide** — Collect: "raspberry pi kubernetes", "k3s cluster" `within = "year"`. Do: extract parts and steps. Build: a weekend build guide.
809. **DevOps course outline** — Collect: TechWorld with Nana and similar channels, `channel_max_videos = 100`. Do: order topics. Build: a 10-week DevOps course outline for a bootcamp.
810. **GPU passthrough notes** — Collect: "proxmox GPU passthrough", `top_comments = 20`. Do: extract steps and hardware-specific fixes. Build: a troubleshooting note per GPU vendor.
811. **Network-wide ad blocking** — Collect: "pi-hole vs adguard home". Do: compare and extract setup steps. Build: a household setup guide with rollback steps.
812. **IPv6 home guide** — Collect: "ipv6 homelab", "ipv6 explained". Do: extract concepts and config steps. Build: a plain-language IPv6 explainer for hobbyists.
813. **Observability vendor questions** — Collect: "datadog pricing", "grafana cloud review", `top_comments = 30`. Do: collect billing surprises users describe. Build: a procurement question list.
814. **DevOps skills gap worksheet** — Collect: "devops roadmap 2026" `within = "year"`. Do: list skills mentioned by frequency. Build: a self-assessment worksheet for career changers.
815. **Vendor training RAG** — Collect: your cloud vendor's channel, then `yt.py export`. Do: embed transcripts. Build: an internal Q&A bot for engineers with links to source seconds.
816. **German and Japanese homelab ideas** — Collect: German and Japanese homelab keywords, `translate = "en"`. Do: note gear and approaches rare in English videos. Build: a monthly roundup.
817. **Firmware hold-off watchlist** — Collect: "unifi update problems", "firmware bug" `within = "week"`. Do: flag reported regressions. Build: a "wait before upgrading" watchlist.
818. **Licence change timeline** — Collect: "opentofu", "terraform license change", "redis license". Do: extract dates and community responses. Build: a timeline for a tooling risk review.
819. **Load test plan template** — Collect: "k6 load testing", "locust tutorial". Do: extract scenarios and metrics used. Build: a load test plan template.
820. **Secrets tool comparison** — Collect: "hashicorp vault", "sops", "secrets management". Do: compare setup effort and fit. Build: a comparison for a platform team.
821. **Homelab vs cloud TCO** — Collect: "homelab vs cloud cost", `top_comments = 20`. Do: extract costs people report. Build: a TCO spreadsheet with your own numbers.

[↑ Contents](#contents)

### Cybersecurity — defensive only

822. **Security+ study plan** — Collect: "security+ SY0-701" playlists, `min_duration = 900`. Do: map videos to exam domains. Build: a 6-week study plan with timestamped review links.
823. **CISSP domain flashcards** — Collect: "CISSP domain", `subtitles_only`. Do: extract definitions and "think like a manager" principles. Build: an Anki deck per domain.
824. **Windows 11 hardening checklist** — Collect: "windows 11 hardening", "windows security settings" `within = "year"`. Do: extract settings and their trade-offs. Build: a checklist for a home PC.
825. **Family router checklist** — Collect: "secure your home router", "wifi security". Do: extract steps in plain words. Build: a printable checklist for non-technical families.
826. **Phishing awareness module** — Collect: "phishing examples explained", `top_comments = 20`. Do: extract red flags with real examples. Build: a 20-minute training module with a quiz.
827. **SOC morning brief** — Collect: security news channels with `channel_within = "today"`, `sponsorblock`. Do: summarise incidents and advisories. Build: a morning brief, each item linked to verify.
828. **Breach lessons library** — Collect: "data breach explained", "incident response case study". Do: note entry point, detection gap, response, lesson. Build: a lessons-learned library.
829. **Password manager comparison** — Collect: "bitwarden vs 1password", "password manager review", `sponsorblock`. Do: tally non-sponsored verdicts. Build: a comparison table for an office.
830. **Parents' privacy guide** — Collect: "kids online privacy", "parental controls" `within = "year"`. Do: extract settings and conversation tips. Build: a family privacy guide.
831. **Ransomware tabletop** — Collect: "ransomware tabletop exercise", "ransomware response small business". Do: extract scenarios and decisions. Build: a tabletop exercise for a 20-person firm.
832. **SOC analyst roadmap** — Collect: "SOC analyst career", "how to get into cybersecurity" `top_comments = 30`. Do: map skills and entry routes. Build: a 12-month roadmap.
833. **Detection engineering backlog** — Collect: "detection engineering", "sigma rules" `min_duration = 900`. Do: extract detection ideas and data sources. Build: a backlog of detections to write and test.
834. **Cloud misconfig audit** — Collect: "S3 bucket misconfiguration", "cloud security posture". Do: extract common misconfigurations. Build: an audit checklist for your own accounts.
835. **Zero trust for executives** — Collect: "zero trust explained", `max_duration = 1200`. Do: distil concepts without jargon. Build: a 1-page executive explainer.
836. **MFA rollout plan** — Collect: "MFA rollout", "passkeys enterprise". Do: extract rollout phases and user objections. Build: a rollout plan plus user FAQ.
837. **Patch priority list** — Collect: "CVE" plus your vendors' names `within = "week"`, `rising_views_per_day = 500`. Do: list vulnerabilities discussed. Build: a priority list to confirm against vendor advisories.
838. **Blue-team talk knowledge base** — Collect: BSides and DEF CON blue-team playlists. Do: map -> reduce notes per talk into themes. Build: `knowledge/blue-team.md` for a SOC wiki.
839. **Browser privacy settings** — Collect: "browser privacy settings", "firefox hardening". Do: extract settings and breakage warnings. Build: a settings guide with a "minimal vs strict" profile.
840. **Seniors scam handout** — Collect: "tech support scam", "elder scams" `within = "year"`. Do: extract scam scripts and warning signs. Build: a large-print handout for a library session.
841. **SOC 2 readiness questions** — Collect: "SOC 2 compliance", "ISO 27001 explained". Do: extract controls and evidence auditors want. Build: a readiness question list to review with an auditor.
842. **GDPR questions for counsel** — Collect: "GDPR for small business", `subtitles_only`. Do: list obligations creators describe. Build: questions to take to a data-protection lawyer, not legal advice.
843. **OWASP Top 10 dev training** — Collect: "OWASP top 10 explained", `chapters`. Do: extract each risk and its prevention. Build: a developer training session with secure-code examples.
844. **Wazuh SOC homelab** — Collect: "wazuh homelab", "build a SOC lab". Do: extract architecture and setup steps. Build: a lab guide for practising detection at home.
845. **Threat modelling workshop** — Collect: "threat modeling STRIDE", "threat modeling workshop". Do: extract facilitation steps. Build: a workshop template with worksheets.
846. **EDR procurement scorecard** — Collect: "EDR comparison", "crowdstrike vs defender", `top_comments = 20`. Do: extract evaluation criteria and complaints. Build: a vendor scorecard.
847. **Identity theft recovery steps** — Collect: "identity theft what to do". Do: extract steps creators recommend. Build: a checklist to verify against official government guidance.
848. **Social engineering drills** — Collect: "social engineering awareness", "pretexting examples". Do: extract defensive response patterns. Build: role-play scenarios for front-desk staff training.
849. **Phone privacy guide** — Collect: "iphone privacy settings", "android privacy" `within = "year"`. Do: extract settings by OS. Build: a phone privacy guide for staff.
850. **"My data leaked" checklist** — Collect: "data breach what to do", "have i been pwned". Do: extract response steps. Build: a personal checklist for after a breach notice.
851. **Security newsletter** — Collect: security news and interview channels `within = "week"`, `sponsorblock`. Do: pick top stories with context. Build: a weekly internal security newsletter.
852. **IR playbook** — Collect: "incident response process", "NIST incident response". Do: extract phases, roles and comms steps. Build: an incident response playbook.
853. **Splunk query cheat sheet** — Collect: "splunk tutorial", "SPL queries", `timestamps`. Do: extract searches and their purpose. Build: a query cheat sheet for new analysts.
854. **Cyber hygiene for kids** — Collect: "internet safety for kids", `max_duration = 600`. Do: extract age-appropriate messages. Build: a primary-school lesson with activities.
855. **Security budget slide** — Collect: "CISO board presentation", "security budget". Do: extract framing advice and metrics. Build: a board slide outline.
856. **Supply-chain security policy** — Collect: "SBOM explained", "software supply chain security". Do: extract controls (pinning, signing, SBOMs). Build: a policy draft for an engineering org.
857. **Email auth setup** — Collect: "SPF DKIM DMARC explained", `chapters`. Do: extract setup order and monitoring tips. Build: a step checklist for a domain owner.
858. **OPNsense hardening** — Collect: "opnsense setup", "pfsense firewall rules" `within = "year"`. Do: extract baseline rules and settings. Build: a firewall baseline for a home lab.
859. **Small office physical security** — Collect: "office physical security", "clean desk policy". Do: extract low-cost controls. Build: a walk-through audit form.
860. **Monthly awareness topics** — Collect: scam keywords daily via `schedule_daily.bat`. Do: read `trends.html` for rising scam types. Build: a monthly awareness email topic calendar.
861. **Non-English threat roundup** — Collect: security keywords in other languages, `translate = "en"`. Do: summarise regional scam and incident trends. Build: a regional roundup for a global company.
862. **Blue-team cert comparison** — Collect: "CySA+ vs BTL1", "GCIH worth it", `top_comments = 20`. Do: compare cost, difficulty and job value claims. Build: a comparison table.
863. **Security interview prep** — Collect: "SOC analyst interview questions", `min_duration = 600`. Do: extract Q&A pairs. Build: a mock-interview script.
864. **Forensic evidence SOP** — Collect: "digital forensics basics", "chain of custody". Do: extract evidence-handling steps. Build: an evidence handling SOP for an IT team.
865. **Data broker opt-out** — Collect: "remove yourself from data brokers". Do: extract opt-out steps for your own records. Build: a personal opt-out checklist with a re-check schedule.
866. **Passkeys explainer** — Collect: "passkeys explained", `max_duration = 900`. Do: extract how they work and common confusions. Build: a staff FAQ.
867. **VPN claims reality check** — Collect: "do you need a VPN", `sponsorblock`, `exclude_words = "sponsored"`. Do: list claims and rebuttals. Build: an honest what-VPNs-do-and-don't table.
868. **Small-creator security tips** — Collect: "home network security", `max_views = 5000`, `within = "month"`. Do: find practical tips large channels miss. Build: a curated tips list.
869. **AI-in-SOC evaluation** — Collect: "AI SOC analyst", "AI for threat detection" `within = "year"`. Do: extract claims and limits practitioners describe. Build: evaluation questions for vendors.
870. **Public incident timeline** — Collect: "ransomware attack" news `within = "year"`, `min_views = 20000`. Do: list publicly reported incidents by sector. Build: a timeline for an annual risk report.
871. **Startup security onboarding** — Collect: "security for startups", "security culture". Do: extract first-year priorities. Build: a new-hire security onboarding module.
872. **Immutable backup design** — Collect: "immutable backups ransomware", "air gapped backup". Do: extract designs and costs. Build: a backup architecture proposal.
873. **Remote work security policy** — Collect: "remote work security", "BYOD policy". Do: extract policy elements. Build: a remote work security policy draft.
874. **Gaming account safety** — Collect: "protect steam account", "roblox account security" `within = "year"`. Do: extract settings and scam warnings. Build: a parent checklist.
875. **Vulnerability disclosure setup** — Collect: "vulnerability disclosure program", "security.txt". Do: extract steps and response SLAs. Build: a disclosure policy and intake process.
876. **Security Q&A Claude skill** — Collect: vetted security awareness channels, then `CLAUDE.md` in the output folder. Do: answer staff questions from transcripts only. Build: a Claude skill that cites the exact second.

[↑ Contents](#contents)

## Data, automation, making and design

### Data, analytics & building on the tool's output

877. **Niche RAG chatbot with citations** — Collect: 10 expert channels, all videos, `timestamps = true`. Do: `yt.py export`, chunk and embed the .jsonl, retrieve per question. Build: a chatbot whose every answer links to the exact second it came from.
878. **Topic heat index** — Collect: 20 industry keywords daily via `schedule_daily.bat`, `within = "today"`. Do: pull new-video counts and attention per day from trends.html into a sheet. Build: a weekly chart of which topics are heating up or cooling off.
879. **Substance score vs clickbait** — Collect: "best budget laptop" `within = "month"`. Do: rank video_list.csv by keyword mentions per minute, flag high-view videos that barely say it. Build: a filter that surfaces videos that actually cover the topic.
880. **RAG evaluation set** — Collect: 200 tutorials on one topic, `chapters = true`. Do: have Claude write question/answer pairs per chapter with the video ID and second as ground truth. Build: a QA benchmark to score retrieval and chunking choices.
881. **Product sentiment timeline** — Collect: "Pixel 11 review" daily, `within = "week"`, `top_comments = 30`. Do: score transcript and comment sentiment per day using the dated lists/ copies. Build: a sentiment line chart from launch week onward.
882. **First-seen glossary** — Collect: "AI agents" with `within = "any"`, then daily. Do: find the earliest publish date each new term appears in any transcript. Build: a glossary of emerging jargon with "first said on YouTube" dates and links.
883. **Topic model of a whole niche** — Collect: 2,000 "personal finance" videos via proxies, `min_duration = 300`. Do: embed the export .jsonl, cluster with BERTopic, label clusters with Claude. Build: a topic map with cluster sizes and 3 exemplar videos each.
884. **Channel co-coverage network** — Collect: 30 related keywords in one niche. Do: link channels that appear under the same keywords in video_list.csv, weight by count. Build: a Gephi graph showing which creators own which subtopics.
885. **What correlates with traction** — Collect: 3 months of lists/ for one niche. Do: regress views per day on duration, title length, upload weekday and keyword mentions. Build: a notebook of correlations, labelled clearly as not causes.
886. **Cross-country framing study** — Collect: "electric cars" with `languages = ["de","ja","pt"]`, `translate`. Do: code each video's main argument and tone with Claude, compare languages. Build: a coded CSV and chart for a media-studies paper, cited by ID.
887. **Creator vs audience gap** — Collect: "intermittent fasting" `top_comments = 50`. Do: list claims creators make, then the pushback in comments, and match the two. Build: a table of contested points, framed as a map of opinion to check with a doctor.
888. **Team transcript search page** — Collect: everything the team monitors, run daily. Do: wrap `yt.py find` in a small Flask app with filters by keyword and date. Build: an internal search box that returns quotes with links to the second.
889. **Prediction scorecard** — Collect: "bitcoin price prediction" monthly, `within = "month"`. Do: extract each stated target, date and channel into rows, then fill in the real outcome later. Build: a forecaster accuracy table (a record, not trading advice).
890. **Chapter-level search index** — Collect: long tutorials with `chapters = true`, `min_duration = 1200`. Do: split each transcript at chapter marks and embed each section separately. Build: a search that lands on the right chapter instead of a 2-hour video.
891. **Entity knowledge graph** — Collect: "home lab" videos `within = "year"`. Do: extract tools, brands and "works with" relations with Claude into triples. Build: a Neo4j graph you can query for which tools are paired most often.
892. **SQL over your library** — Collect: all runs to date. Do: load the `yt.py export` .csv into SQLite and serve it with Datasette. Build: a browsable database where anyone can write SQL against views, dates and channels.
893. **Best upload time heatmap** — Collect: 1,500 videos from 50 channels in one niche. Do: group the export by publish weekday and hour against views per day. Build: a heatmap of when the niche's videos tend to take off.
894. **Title pattern mining** — Collect: "productivity" `within = "year"`, `min_views = 1000`. Do: extract n-grams from titles and compare median views per day with vs without each. Build: a ranked list of title phrases tied to above-median traction.
895. **Video length sweet spot** — Collect: one keyword across `within = "year"` with no duration filter. Do: bin by duration and plot views per day per bin, shorts separate via `include_shorts`. Build: a chart of which lengths perform in that niche.
896. **Emerging channel finder** — Collect: niche keywords with `max_views = 5000` and `rising_views_per_day = 300`. Do: group by channel and track their views per day across dated lists/. Build: a spreadsheet of small channels growing fastest.
897. **Pain-point frequency table** — Collect: "[your product category] review" `top_comments = 40`. Do: extract every complaint and wish from transcripts and comments, merge duplicates, count. Build: a ranked pain-point sheet for a product roadmap.
898. **Speaker pace and clarity stats** — Collect: newest 50 videos from 12 explainer channels. Do: compute words per minute, sentence length and reading level per channel. Build: a comparison table for creators studying delivery.
899. **Segmentation benchmark** — Collect: 300 videos with creator-made `chapters = true`. Do: hide chapters, ask models to segment the transcript, compare to the real chapter times. Build: a dataset and score for topic-segmentation models.
900. **Subtitle quality audit** — Collect: the same keyword twice, with and without `subtitles_only`. Do: compare error rates on names and jargon between the two sets. Build: a report on when auto-captions are good enough for your pipeline.
901. **Consensus matrix** — Collect: 100 videos on "sourdough hydration". Do: map step writes a note per video into notes/, reduce step tallies who recommends what. Build: knowledge/sourdough.md with a table of how many sources back each claim.
902. **Pandas starter notebook** — Collect: any run. Do: write a loader for the export .jsonl that adds word counts, mention density and publish week. Build: a reusable Jupyter template every new analysis starts from.
903. **Competitor channel tracker** — Collect: `only_channels` = 5 rival brands, `channel_within = "month"`. Do: count product mentions, new features named and upload cadence per month. Build: a monthly competitor briefing with numbers and quotes.
904. **Spike alert** — Collect: 40 keywords daily, `within = "today"`. Do: compute a rolling z-score on daily new-video counts from trends.html and flag spikes. Build: a script that posts "topic X just tripled" to Slack.
905. **Sponsor landscape** — Collect: a niche with `include_description = true`. Do: extract sponsor brands and promo codes named in descriptions, count per channel. Build: a table of which brands sponsor the niche, for creators pitching deals.
906. **Filler-word linguistics** — Collect: interview channels with `remove_filler_words = false`. Do: count "um", "like", hedges per 1,000 words by speaker type and length. Build: a small corpus study of spoken hedging habits.
907. **Seasonal demand curve** — Collect: "vegetable garden" monthly for a year, `within = "month"`. Do: plot new videos and views per day by subtopic per month from lists/. Build: a seasonal calendar of when each subtopic peaks.
908. **Interactive video map** — Collect: library of 5 keywords. Do: embed every transcript, project to 2D with UMAP, colour by keyword. Build: an HTML scatter where hovering shows the title and click opens the video.
909. **Audience question dataset** — Collect: "learn Python" `top_comments = 50`. Do: pull every question asked in comments, cluster and count. Build: a frequency-ranked FAQ dataset showing what learners get stuck on.
910. **Stated price tracker** — Collect: "RTX 5070 price" weekly. Do: extract prices said in transcripts with date and region. Build: a table of how quoted prices shift, flagged as what reviewers said, to verify at retailers.
911. **Tool popularity census** — Collect: "my developer setup 2026" `within = "year"`. Do: extract every editor, terminal and app named, count channels that mention each. Build: a ranked census of tools real developers show.
912. **News event timeline** — Collect: an event's keyword with `published_after`/`published_before` around the date. Do: order videos by publish time and extract each new claim. Build: a timeline graphic of how coverage evolved, each point cited.
913. **Book mention reading list** — Collect: "books that changed my life" `within = "any"`. Do: extract every book title and author said, merge spellings, count mentions. Build: a reading list ranked by how many creators recommend each.
914. **Channel evolution study** — Collect: one public creator's channel, all videos, `channel_within = "any"`. Do: chart views per day, length and topics by year from library.html. Build: a report on how the channel's focus and reach changed.
915. **Disputed-claims report** — Collect: "creatine" `within = "year"`. Do: after map->reduce, find notes that contradict each other on the same question. Build: a list of disputed claims with both sides cited, as questions for a professional.
916. **Keyword portfolio by yield** — Collect: seed terms plus the related keywords finder output. Do: run all for a week, measure new on-topic videos per keyword per day. Build: a pruned keyword list keeping only terms that pay their way.
917. **Video type classifier** — Collect: 1,000 mixed videos on a topic. Do: label each as tutorial/review/news/opinion with Claude, train a small classifier on transcripts. Build: a model that tags future runs automatically.
918. **Lead-lag with outside data** — Collect: "air fryer" daily for 6 months. Do: join trends.html attention with Google Trends or your sales by week, test lags. Build: a chart showing whether YouTube attention leads or follows demand.
919. **Nightly warehouse load** — Collect: all keywords on `schedule_daily.bat`. Do: after each run, load `yt.py export` into Postgres or BigQuery with an upsert on video ID. Build: a SQL warehouse with views for "new today" and "top risers".
920. **Looker Studio for marketers** — Collect: brand and competitor keywords weekly. Do: push the export .csv to Google Sheets and connect it. Build: a KPI dashboard of mentions, views per day and new videos a non-technical team can read.
921. **Claim propagation trace** — Collect: a viral claim's exact wording, `within = "month"`. Do: order transcripts that repeat it by publish date and channel. Build: a propagation timeline for fact-checkers, citing public statements.
922. **Skill demand signal** — Collect: "learn Rust", "learn Go", "learn Kotlin" monthly. Do: compare new-video counts and views per day per language over time. Build: a skills heat index for career planners, labelled as interest, not jobs.
923. **Weekly list diff** — Collect: one keyword daily. Do: diff consecutive lists/ copies to find videos that entered or dropped out of the top. Build: a "new this week" changelog for a niche.
924. **Public figure quote bank** — Collect: interviews of a CEO via `title_must_contain` their name, `timestamps = true`. Do: extract direct quotes by subject with links to the second. Build: a searchable quote database for journalists.
925. **Domain expert Claude skill** — Collect: 300 videos on "Kubernetes troubleshooting". Do: map->reduce into knowledge/ files, then package them with a SKILL.md and search instructions. Build: a Claude skill that answers from the knowledge base with sources.
926. **Context pack builder** — Collect: one broad keyword with combined/ output. Do: re-split the combined Markdown by subtopic using Claude labels, cap each at your model's context. Build: ready-to-paste context packs per subtopic.
927. **Translation consistency check** — Collect: one topic in Spanish with and without `translate`. Do: compare key terms in machine translation against a human glossary. Build: a list of terms YouTube translation garbles, to fix before analysis.
928. **Repeat-content measurement** — Collect: "podcast clips" topic with heavy re-uploads. Do: count how many videos the tool marked as repeats versus originals per channel. Build: a stat on how much of a niche is recycled clips.
929. **Monthly niche data report** — Collect: 15 keywords all month. Do: compute top risers, new channels, total views per day and biggest themes from export. Build: a PDF data report a newsletter or agency can send clients.

[↑ Contents](#contents)

### No-code, automation & productivity tools

930. **n8n summary-to-Slack flow** — Collect: 10 keywords daily on `schedule_daily.bat`. Do: an n8n watch-folder trigger reads new combined/ files, sends them to Claude, posts the summary. Build: a Slack channel that gets a morning digest with zero clicks.
931. **Zapier to Google Sheets log** — Collect: daily brand keywords, `within = "today"`. Do: a Zapier folder trigger appends each new video_list.csv row to a Sheet. Build: a shared running log of every new mention with views per day.
932. **Make.com Airtable base** — Collect: research keywords with per-video .json output. Do: a Make scenario parses each .json and creates Airtable records with title, channel, link. Build: a filterable Airtable research base the team tags by hand.
933. **Notion reading queue** — Collect: learning keywords weekly. Do: import the `yt.py export` .csv into a Notion database with views per day and keyword as properties. Build: a prioritised "watch or read" queue with status columns.
934. **Obsidian video vault** — Collect: your favourite channels with `timestamps = true`. Do: drop the .md per video into a vault, add Dataview queries by channel and date. Build: a linked vault where every note jumps to the exact second.
935. **Excel Power Query watchlist** — Collect: daily lists/ for 5 keywords. Do: point Power Query at the lists/ folder to combine every dated file, refresh with one click. Build: an Excel pivot showing how each video's views grew.
936. **n8n node cookbook** — Collect: "n8n tutorial" `within = "month"`, `min_views = 500`. Do: extract each workflow built: trigger, nodes, purpose, timestamp. Build: a cookbook of n8n recipes to copy, each linked to the video that shows it.
937. **Small-business Zapier idea list** — Collect: "Zapier automation ideas" `within = "year"`. Do: extract each automation, the apps used and the time saved claimed. Build: a checklist of 30 automations a shop owner can pick from.
938. **Excel formula cheat sheet** — Collect: "Excel tips" from 5 Excel channels, `timestamps = true`. Do: list each formula shown with syntax and use case. Build: a one-page formula cheat sheet with links to the demo second.
939. **Notion template blueprint** — Collect: "Notion setup tour" `within = "year"`. Do: extract each database, its properties and relations as described. Build: a blueprint for your own workspace, combining the best structures.
940. **Obsidian plugin census** — Collect: "Obsidian workflow" `within = "year"`. Do: count plugins named across videos and note what each is used for. Build: a ranked plugin list with one-line reasons and install order.
941. **PKM method comparison** — Collect: "PARA method", "Zettelkasten", "Johnny Decimal". Do: compare setup effort, best user type and common failure from comments with `top_comments = 30`. Build: a comparison table to choose a system.
942. **30-day productivity experiment** — Collect: "time blocking", "GTD", "Pomodoro" `min_duration = 480`. Do: extract each method's rules and measurable claims. Build: a 30-day self-experiment plan with a daily tracking sheet.
943. **Role-specific automation backlog** — Collect: "real estate agent automation" `within = "year"`. Do: list every automation, tool and claimed benefit. Build: a backlog sorted by effort and impact for one agent's office.
944. **Daily quote email** — Collect: favourite thinkers' channels, `channel_within = "week"`. Do: n8n picks 3 strong quotes from new transcripts and emails them with links. Build: a Readwise-style morning email from your own sources.
945. **iPhone Shortcuts recipes** — Collect: "iPhone shortcuts" `within = "year"`, `max_duration = 900`. Do: extract each shortcut's actions in order. Build: a step-by-step recipe list you can rebuild on your phone.
946. **Apps Script snippet library** — Collect: "Google Sheets Apps Script" tutorials. Do: summarise each script's goal, triggers and steps (write your own code from it). Build: a library of tested snippets for Sheets automation.
947. **Power Automate office SOPs** — Collect: "Power Automate tutorial" `within = "year"`. Do: turn each flow into numbered steps with prerequisites. Build: SOPs that a Microsoft 365 office can follow without a consultant.
948. **Inbox rules playbook** — Collect: "inbox zero", "Gmail filters" `within = "year"`. Do: extract concrete rules, labels and filters people use. Build: a playbook of filters to set up in an afternoon.
949. **Task app comparison** — Collect: "Todoist vs TickTick vs Things" `within = "year"`. Do: tabulate features, prices said and complaints. Build: a comparison table with "best for" rows, prices marked to verify.
950. **Course to Obsidian Canvas** — Collect: a playlist course with `chapters = true`. Do: turn chapters into cards and dependencies into arrows. Build: an Obsidian Canvas map of the whole course to study from.
951. **Automation error fixes** — Collect: "n8n error", "Make.com error" `top_comments = 30`. Do: list errors people hit and the fixes given in videos and comments. Build: a troubleshooting doc ordered by how often each error appears.
952. **Telegram riser bot** — Collect: 15 keywords with `rising_views_per_day = 500`. Do: n8n reads the newest video_list.csv and sends the top 3 risers to a Telegram chat. Build: a bot that pings you when a topic starts moving.
953. **Automation service menu** — Collect: "sell automation services" `within = "year"`. Do: extract offers, pricing ranges said and client types. Build: a service menu draft, prices marked as creators' claims to test in your market.
954. **Student semester planner** — Collect: "Notion student planner" `within = "year"`. Do: extract layouts for classes, deadlines and grade tracking. Build: one Notion planner template that merges the best ideas.
955. **Daily-note auto-append** — Collect: your watchlist daily. Do: a script appends yesterday's new videos (title, channel, link) to today's Obsidian daily note. Build: a daily note that always shows what's new in your field.
956. **Deep work opinion map** — Collect: "deep work", "focus routine" `within = "year"`. Do: group advice by type and note what each creator says it fixes. Build: a map of opinions to try, not a prescription.
957. **ADHD tool strategies** — Collect: "ADHD productivity system" `top_comments = 40`. Do: list strategies and apps shared, with comment feedback. Build: a strategy map, labelled as lived experience to discuss with a clinician.
958. **Agency SOP library** — Collect: "how we run our agency ClickUp" `within = "year"`. Do: extract each process: intake, handoff, review. Build: editable SOP templates for a 5-person team.
959. **Project tool pick for an agency** — Collect: "ClickUp vs Asana vs Monday" `within = "year"`. Do: compare views, automations, limits and migration pain. Build: a decision matrix the team scores together.
960. **Notion formulas cheat sheet** — Collect: "Notion formulas 2.0" tutorials. Do: extract formulas with what they compute. Build: a copy-ready cheat sheet sorted by use: dates, progress bars, rollups.
961. **Excel dynamic arrays path** — Collect: "LAMBDA", "XLOOKUP", "dynamic arrays" from Excel channels. Do: order concepts by prerequisite. Build: a 2-week learning path with one practice file per day.
962. **Zapier to Make migration** — Collect: "Zapier vs Make" `within = "year"`. Do: map Zapier concepts to Make equivalents and list gotchas. Build: a migration guide with a checklist per Zap.
963. **Personal CRM in Notion** — Collect: "personal CRM Notion". Do: extract fields, reminder logic and review habits shown. Build: a template for keeping in touch with your own contacts (no scraping of other people).
964. **Weekly review checklist** — Collect: "GTD weekly review" `min_duration = 600`. Do: extract every step creators actually do. Build: a printable 20-minute weekly review checklist.
965. **Habit tracker designs** — Collect: "habit tracker Notion", "habit tracker Excel". Do: compare layouts and what users in `top_comments = 20` say kept them going. Build: a tracker template with the features people stuck with.
966. **Run the tool from n8n** — Collect: any keyword set. Do: an n8n Execute Command node runs yt.py, then a Claude node writes notes from new files. Build: a full map step running on a schedule without touching a terminal.
967. **Zettelkasten from notes/** — Collect: 100 videos on one theme. Do: have Claude split notes/ into atomic idea notes with backlinks between related ideas. Build: an Obsidian Zettelkasten seeded from your research.
968. **Capture workflow design** — Collect: "quick capture workflow", "voice notes to Notion". Do: compare capture tools and how notes get processed. Build: a one-page capture-to-review flow for your setup.
969. **Meeting bot comparison** — Collect: "Otter vs Fireflies vs Fathom" `within = "year"`. Do: compare accuracy claims, privacy notes and integrations. Build: a comparison table plus questions to ask IT before buying.
970. **Make.com error handling** — Collect: "Make.com error handling" tutorials. Do: extract patterns: retries, break, ignore, alerts. Build: a standard error-handling module to drop into every scenario.
971. **Copilot in Excel changelog** — Collect: "Copilot Excel" `within = "week"` weekly. Do: list newly shown features with the date first demoed. Build: a running changelog for a finance team's training lead.
972. **Invoice automation for freelancers** — Collect: "automate invoices" `within = "year"`. Do: extract stacks (form, sheet, invoice app, email) and steps. Build: a step-by-step setup plan for a solo freelancer.
973. **Automation idea queue** — Collect: "automation" with `rising_views_per_day = 300`, `max_views = 10000`. Do: extract each new idea from fast-rising small videos. Build: a weekly queue of fresh automation ideas to try.
974. **Launcher workflows** — Collect: "Raycast workflow", "Alfred workflow". Do: extract extensions and hotkeys shown. Build: a setup script list and hotkey map for a new Mac.
975. **Shortcut cheat sheets** — Collect: "Obsidian shortcuts", "Notion shortcuts" `max_duration = 900`. Do: list each shortcut and the task it speeds up. Build: a printable cheat sheet for your desk.
976. **Digital garden from knowledge/** — Collect: a hobby topic over 3 months. Do: turn knowledge/<topic>.md into short pages in your own words with source links. Build: a published Obsidian digital garden that cites creators.
977. **Teacher Google Workspace kit** — Collect: "Google Classroom tips" `within = "year"`. Do: extract time-saving tricks by task: grading, forms, sharing. Build: a staff training handout with links to each demo.
978. **Airtable formula reference** — Collect: "Airtable formulas" tutorials. Do: extract formulas with inputs and outputs. Build: a reference base inside Airtable with a worked example per formula.
979. **Retail stock alert flow** — Collect: "Shopify low stock automation". Do: extract the triggers and apps creators use. Build: a Zapier or Make plan for low-stock alerts to your phone.
980. **Calendar system design** — Collect: "calendar blocking", "Google Calendar setup" `within = "year"`. Do: extract colour codes, block types and review habits. Build: a calendar setup guide with a sample week.
981. **Spreadsheet dashboard build** — Collect: "Excel dashboard tutorial" `min_views = 5000`. Do: extract layout steps, chart choices and slicers used. Build: a dashboard plan for your own sales sheet.
982. **Productivity app news feed** — Collect: `only_channels` = Notion, Obsidian, Todoist official channels, `channel_within = "week"`. Do: summarise new features weekly. Build: a short "what changed" note for your team.
983. **No-code learning roadmap** — Collect: "no-code for beginners" `within = "year"`, `top_comments = 20`. Do: order skills by what beginners say confused them first. Build: a 6-week roadmap from spreadsheets to webhooks.

[↑ Contents](#contents)

### Hardware, electronics & making

984. **3D printer buying matrix** — Collect: "Bambu Lab vs Prusa vs Creality" `within = "year"`. Do: tabulate speed, enclosure, multi-colour, noise and complaints from `top_comments = 30`. Build: a buyer's matrix with prices marked to verify.
985. **Print-failure decision tree** — Collect: "stringing fix", "layer shift", "warping" `within = "year"`. Do: map each symptom to causes and fixes, ordered by how often creators cite them. Build: a printable troubleshooting decision tree.
986. **Filament settings table** — Collect: "PETG settings", "ASA printing", "TPU tips". Do: extract nozzle, bed, fan and speed values creators use. Build: a starting-point table, flagged to check against the maker's datasheet.
987. **Klipper setup SOP** — Collect: "Klipper input shaping", "pressure advance" `within = "year"`. Do: extract each calibration step in order with commands named. Build: a calibration SOP with links to the exact second of each demo.
988. **Fusion 360 curriculum** — Collect: 3 Fusion teaching channels, all videos, `chapters = true`. Do: order lessons by skill prerequisite. Build: a 12-week curriculum with one exercise per week and timestamped references.
989. **CAD shortcut sheet** — Collect: "Fusion 360 tips" `max_duration = 1200`. Do: list features and shortcuts shown with when to use each. Build: a desk cheat sheet for sketch, extrude, fillet, joints.
990. **Free CAD switch guide** — Collect: "FreeCAD vs Onshape vs Fusion" `within = "year"`. Do: compare licence terms said, file export, learning curve. Build: a switching guide for a hobbyist leaving paid CAD, licence terms to verify.
991. **Arduino project picker** — Collect: "Arduino project for beginners" `within = "year"`, `max_duration = 1200`. Do: extract parts, difficulty and skills taught. Build: a project picker sheet with a bill of materials per project.
992. **Raspberry Pi 5 project ranking** — Collect: "Raspberry Pi 5 projects" `within = "year"`. Do: score each by cost, time and usefulness from comments. Build: a ranked list for a weekend builder.
993. **ESP32 sensor cookbook** — Collect: "ESP32 temperature sensor", "ESP32 deep sleep". Do: extract wiring described, libraries and pitfalls. Build: a cookbook where each recipe says "check pinout against the datasheet".
994. **PC build checklist** — Collect: "PC build guide 2026" `top_comments = 40`. Do: extract build steps and the mistakes people admit in comments. Build: a step checklist with "most common mistake" warnings at each step.
995. **GPU value table** — Collect: "GPU review" `within = "month"`, monthly. Do: extract stated prices and frame rates with test game and resolution. Build: a dated value table, labelled as reviewers' numbers.
996. **Compatibility gotchas list** — Collect: "AM5 build problems", "RAM not detected" `top_comments = 30`. Do: list part pairings that caused trouble and the fix. Build: a pre-purchase compatibility checklist.
997. **FPV starter kit** — Collect: "FPV drone beginner" `within = "year"`. Do: extract recommended sims, radios, goggles and budget tiers. Build: a starter kit list plus questions to verify with your local aviation authority.
998. **Betaflight tuning notes** — Collect: "Betaflight PID tuning" `min_duration = 600`. Do: extract the tuning order and what each change fixed. Build: a tuning log template with step order and links to demos.
999. **ROS 2 roadmap** — Collect: "ROS 2 tutorial" `within = "year"`, `chapters = true`. Do: order topics from nodes to navigation. Build: a learning roadmap with a mini project per stage.
1000. **Robot arm build comparison** — Collect: "DIY robot arm" `max_views = 20000`. Do: compare servos vs steppers, printed parts, controller and cost. Build: a comparison table to pick a design to build.
1001. **Soldering technique card** — Collect: "how to solder" `min_views = 50000`. Do: extract technique steps, tip temps and fume safety notes. Build: a laminated bench card for a makerspace.
1002. **PCB design review checklist** — Collect: "KiCad tutorial", "PCB design mistakes". Do: extract rules on traces, grounding, decoupling and footprints. Build: a pre-order design review checklist for your boards.
1003. **DFM rules sheet** — Collect: "PCB manufacturing tips", "JLCPCB assembly". Do: extract clearance, drill and panel rules said. Build: a DFM rules sheet, to verify against your fab's own specs.
1004. **Home Assistant setup guide** — Collect: "Home Assistant beginner" `within = "year"`. Do: extract install path, first integrations and dashboard tips. Build: a weekend setup guide in order.
1005. **Keyboard switch matrix** — Collect: "switch comparison", "linear vs tactile" `within = "year"`. Do: extract sound and feel descriptions per switch. Build: a matrix to pick switches before ordering samples.
1006. **CNC router shortlist** — Collect: "hobby CNC router" `within = "year"`. Do: compare rigidity, work area, software and feeds and speeds mentioned. Build: a shortlist and a feeds notes sheet to test on scrap.
1007. **Laptop no-power flowchart** — Collect: "laptop won't turn on repair" from repair channels. Do: extract diagnostic steps in order, with any safety warnings. Build: a diagnostic flowchart for a repair cafe volunteer.
1008. **Retro restoration plan** — Collect: "Commodore 64 restoration", "recap" `channels` of retro repair creators. Do: extract common faults and parts replaced. Build: a restoration checklist for one machine.
1009. **Workshop jig library** — Collect: "shop jig ideas" `within = "any"`, `min_views = 10000`. Do: list each jig, what it solves and materials. Build: a jig library sorted by tool.
1010. **3D print shop plan** — Collect: "selling 3D prints" `within = "year"`. Do: extract what sells, pricing logic and licence warnings about others' models. Build: a business plan that only uses own or commercially licensed designs.
1011. **Teardown component database** — Collect: teardown channels, all videos. Do: extract chips, sensors and batteries named per device. Build: a searchable component database of what's inside common gadgets.
1012. **First oscilloscope guide** — Collect: "oscilloscope beginner", "best budget oscilloscope". Do: extract specs that matter and first measurements to try. Build: a buying guide plus a first-week practice plan.
1013. **LiPo safety card** — Collect: "LiPo battery safety" `min_views = 20000`. Do: extract storage, charging and disposal rules. Build: a safety card for an RC club, to cross-check with the battery maker.
1014. **DIY power station map** — Collect: "DIY solar generator" `within = "year"`. Do: compare parts lists and safety steps. Build: a map of builds plus questions for a licensed electrician before any mains work.
1015. **Makerspace class kit** — Collect: "intro to 3D printing class", "makerspace workshop". Do: extract lesson flow and common learner mistakes. Build: a 2-hour class plan with handouts.
1016. **Classroom robotics kits** — Collect: "STEM robot kit review" `within = "year"`. Do: compare age range, coding language, cost per student and durability. Build: a comparison table for a school purchasing teacher.
1017. **Cosplay armor workflow** — Collect: "EVA foam armor", "3D printed cosplay armor". Do: extract workflow, finishing steps and fit tips. Build: a build schedule working back from a convention date.
1018. **Print farm ops** — Collect: "3D print farm" `within = "year"`. Do: extract layout, maintenance and queue software. Build: an SOP for running 10 printers with a weekly maintenance sheet.
1019. **Firmware update monitor** — Collect: "Bambu firmware", "Prusa firmware" `within = "today"`, daily. Do: flag videos reporting new bugs or features. Build: a daily alert so you know before you update.
1020. **New board launches** — Collect: "new single board computer" `within = "week"`, weekly. Do: extract board names, specs said and price. Build: a weekly launch log for a maker newsletter.
1021. **Hidden-gem builds** — Collect: "DIY CNC build", "homemade robot" `max_views = 2000`. Do: summarise novel ideas small creators show. Build: an inspiration list of builds the algorithm misses.
1022. **Chinese printer mods** — Collect: "3D打印机 改装" with `languages = ["zh"]`, `translate`. Do: extract mods and parts. Build: an English summary of mods popular in Chinese maker videos, cited.
1023. **OpenSCAD pattern library** — Collect: "OpenSCAD tutorial" `within = "any"`. Do: summarise modelling techniques (write your own code). Build: a parametric pattern library: boxes, hinges, threads.
1024. **Fit tolerance test plan** — Collect: "3D print tolerances", "press fit clearance". Do: extract clearance values creators report. Build: a test-print plan to find your own printer's numbers.
1025. **Electronics flashcards** — Collect: "electronics basics" from teaching channels. Do: pull definitions and formulas: Ohm's law, dividers, pull-ups. Build: an Anki deck with a link to each explanation.
1026. **Microcontroller pick** — Collect: "RP2040 vs ESP32 vs STM32" `within = "year"`. Do: compare power, wireless, tooling and community. Build: a decision tree for picking a board per project.
1027. **Sensor selection guide** — Collect: "best temperature sensor", "humidity sensor comparison". Do: tabulate accuracy said, interface and price. Build: a sensor picker to confirm against datasheets.
1028. **Robotics team knowledge base** — Collect: "FRC robot reveal" `within = "year"`. Do: map->reduce into knowledge/ on drivetrains, intakes, climbers. Build: a team knowledge base for next season's design meetings.
1029. **Photogrammetry workflow** — Collect: "drone photogrammetry", "drone mapping software". Do: extract flight settings, overlap and processing steps. Build: a field-to-model SOP for a surveying hobbyist, rules to check locally.
1030. **3D scanner comparison** — Collect: "3D scanner review" `within = "year"`. Do: compare accuracy claims, object sizes and software. Build: a comparison table for reverse-engineering parts.
1031. **Resin printing safety SOP** — Collect: "resin printing safety", "resin ventilation". Do: extract PPE, ventilation and disposal steps. Build: a safety SOP to check against the resin's safety data sheet.
1032. **Homelab NAS build** — Collect: "DIY NAS build 2026" `within = "year"`. Do: compare cases, drives, OS choice and power draw said. Build: a parts list and setup plan for a family photo NAS.
1033. **Undervolting notes** — Collect: "GPU undervolt guide" `within = "year"`. Do: extract steps, tools and stability tests. Build: a step list with a risk note and a revert plan.
1034. **Appliance fault list** — Collect: "washing machine repair", "toaster repair" repair channels. Do: list common faults, signs and parts. Build: a repair cafe triage sheet with "unplug first" safety notes.
1035. **Ham radio first station** — Collect: "first HF station", "ham radio beginner" `within = "year"`. Do: extract gear, antenna options and licence steps mentioned. Build: a setup plan with licence rules to verify with your regulator.
1036. **Print help Claude skill** — Collect: 500 3D printing troubleshooting videos with `timestamps = true`. Do: map->reduce into knowledge/ by symptom. Build: a Claude skill that diagnoses a print photo description and cites videos.
1037. **Failure stories from comments** — Collect: "first PC build" `top_comments = 50`. Do: extract "my build failed because..." stories and group by cause. Build: a top-10 causes list for a beginner's guide.
1038. **BOM cost estimator** — Collect: "Arduino weather station", "ESP32 smart home" builds. Do: extract parts and quantities named. Build: a spreadsheet that totals a BOM with your own supplier prices.

[↑ Contents](#contents)

### Web design, UI/UX & graphic design

1039. **Landing page pattern library** — Collect: "landing page teardown" `within = "year"`. Do: extract section types, their order and why each works per creator. Build: a pattern library of hero, proof, pricing and FAQ blocks.
1040. **CRO test backlog** — Collect: "conversion rate optimization" `within = "year"`, `min_duration = 600`. Do: list each test idea and claimed lift. Build: an ICE-scored A/B backlog, claims treated as hypotheses to test.
1041. **Design token naming guide** — Collect: "design tokens", "design system Figma" `within = "year"`. Do: compare naming schemes and layering (primitive, semantic, component). Build: a token naming convention doc for your team.
1042. **Figma changelog** — Collect: `only_channels` = Figma, `channel_within = "week"`. Do: summarise each new feature and who it matters to. Build: a weekly changelog note for a design team's standup.
1043. **Site builder pick for a client** — Collect: "Framer vs Webflow vs WordPress" `within = "year"`. Do: compare CMS, hosting, editing for non-tech clients, cost said. Build: a client-facing comparison table with a recommendation.
1044. **Webflow CMS SOP** — Collect: "Webflow CMS tutorial" `chapters = true`. Do: extract collection setup, fields and dynamic pages in order. Build: an SOP a junior can follow, linked to each demo second.
1045. **Font pairing list** — Collect: "font pairing", "Google Fonts pairing" `within = "year"`. Do: extract pairs and the reasoning given. Build: a pairing list grouped by mood with licence notes to verify.
1046. **Brand discovery questionnaire** — Collect: "brand identity process" from 5 design studios' channels. Do: extract the questions they ask clients. Build: a client questionnaire and kickoff agenda.
1047. **Logo critique rubric** — Collect: "logo design critique" `top_comments = 20`. Do: extract criteria critics keep using: scalability, uniqueness, legibility. Build: a scoring rubric for reviewing logo drafts.
1048. **Usability test plan** — Collect: "usability testing", "user interview tips" `within = "year"`. Do: extract planning steps, sample sizes said and question mistakes. Build: a test plan template with a script.
1049. **Accessibility audit checklist** — Collect: "web accessibility", "WCAG 2.2" `within = "year"`. Do: extract checks: contrast, focus, alt text, motion. Build: an audit checklist with each item linked to the WCAG spec to verify.
1050. **Portfolio checklist** — Collect: "UX portfolio review" `top_comments = 30`. Do: list what reviewers praise and reject. Build: a checklist a junior uses before sending a portfolio.
1051. **Design interview question bank** — Collect: "product design interview" `within = "year"`. Do: extract questions and what interviewers say a good answer shows. Build: a practice question bank with answer outlines.
1052. **Palette workflow** — Collect: "color palette design", "color theory UI". Do: extract steps from base colour to scale to states. Build: a palette workflow with contrast checks at each step.
1053. **Micro-interaction idea library** — Collect: "Framer animation", "Rive tutorial" `within = "year"`. Do: list each interaction, trigger and purpose. Build: an idea library grouped by component: buttons, toggles, loaders.
1054. **Design roast lessons** — Collect: "website roast", "design roast" `within = "year"`. Do: count the mistakes called out most. Build: a top-20 mistakes list with a fix for each.
1055. **Pricing models for designers** — Collect: "how to price web design" `within = "year"`. Do: compare hourly, project and value pricing as creators describe them. Build: a map of pricing opinions with numbers to test locally.
1056. **Freelance onboarding SOP** — Collect: "client onboarding web designer". Do: extract steps: contract, deposit, assets, timeline. Build: an onboarding SOP with email templates written in your own words.
1057. **Figma plugin ranking** — Collect: "best Figma plugins" `within = "year"`. Do: count mentions and note what each does. Build: a ranked plugin list for a team's starter kit.
1058. **Auto layout and variables path** — Collect: "Figma auto layout", "Figma variables" `chapters = true`. Do: order concepts from basics to advanced. Build: a learning path with practice files and timestamps.
1059. **Dark mode rules** — Collect: "dark mode UI design" `within = "year"`. Do: extract rules on surfaces, contrast and saturation. Build: a dark mode checklist for your design system.
1060. **Mobile pattern sheet** — Collect: "iOS app design", "Material 3" `within = "year"`. Do: extract navigation, sheet and gesture patterns. Build: a pattern sheet with each item to check against Apple HIG or Material docs.
1061. **Dashboard design principles** — Collect: "dashboard UI design" `min_duration = 480`. Do: extract layout, hierarchy and chart choice advice. Build: a principles one-pager for a SaaS team's next dashboard.
1062. **Product page audit** — Collect: "ecommerce product page" `within = "year"`. Do: extract elements creators say matter: images, reviews, shipping info. Build: an audit template to score your shop's pages.
1063. **SaaS onboarding flows** — Collect: "SaaS onboarding UX" `within = "year"`. Do: extract flow types: checklists, tours, empty states, with examples. Build: a flow comparison and a proposal for your app.
1064. **Microcopy guide** — Collect: "UX writing", "microcopy" `within = "year"`. Do: extract rules for buttons, errors and empty states. Build: a microcopy style guide with before and after examples.
1065. **Design trend radar** — Collect: "web design trends" with `rising_views_per_day = 200`, `within = "month"`. Do: tag each trend as rising, peak or fading by month. Build: a trend radar to decide what to adopt.
1066. **AI design tool tracker** — Collect: "v0", "Lovable", "Figma Make" `within = "week"`, weekly. Do: note capabilities shown and limits users hit. Build: a weekly comparison table for an agency deciding what to adopt.
1067. **Japanese web design study** — Collect: "Webデザイン" with `languages = ["ja"]`, `translate`. Do: extract layout and typography habits that differ from Western sites. Build: a briefing with cited examples.
1068. **Small-designer ideas** — Collect: "web design process" `max_views = 3000`, `within = "month"`. Do: summarise unusual techniques. Build: a weekly list of fresh ideas from designers the algorithm misses.
1069. **Brand guidelines Claude skill** — Collect: "brand guidelines", "brand book" `within = "year"`. Do: map->reduce into knowledge/ on sections and rules. Build: a Claude skill that drafts a brand guideline outline from a client brief.
1070. **High school design syllabus** — Collect: "graphic design basics" from teaching channels. Do: order topics: contrast, alignment, type, colour, layout. Build: a 10-week syllabus with one project per unit.
1071. **Design app choice** — Collect: "Affinity vs Adobe vs Canva" `within = "year"`. Do: compare price said, print support and file compatibility. Build: a choice guide for a small business doing its own graphics.
1072. **Print prep checklist** — Collect: "print ready file", "bleed CMYK" `min_views = 10000`. Do: extract steps: bleed, colour mode, resolution, fonts. Build: a pre-press checklist, to confirm with your printer.
1073. **Packaging design brief** — Collect: "packaging design process" `within = "year"`. Do: extract stages: dieline, materials, shelf test. Build: a brief template for a startup's first product box.
1074. **Icon set guide** — Collect: "icon design tutorial" `within = "any"`. Do: extract grid, stroke and corner rules. Build: an icon spec sheet so a team's icons match.
1075. **Card sorting kit** — Collect: "information architecture", "card sorting". Do: extract methods, tools and analysis steps. Build: a card-sorting study kit for a site redesign.
1076. **Dev handoff checklist** — Collect: "Figma dev mode", "design handoff" `top_comments = 20`. Do: list what developers say they need and often miss. Build: a handoff checklist for designers.
1077. **CSS layout recipes** — Collect: "CSS grid layout", "container queries" `within = "year"`. Do: summarise each technique and when to use it (write your own code). Build: a layout recipe page for common sections.
1078. **Wireframe kit from teardowns** — Collect: "SaaS landing page breakdown" `within = "year"`. Do: extract the most common section order. Build: a low-fi Figma wireframe kit following that order.
1079. **Speed-aware design rules** — Collect: "Core Web Vitals design", "image optimization". Do: extract design choices that hurt or help load time. Build: a design checklist reviewed before handoff.
1080. **Heuristic site audit** — Collect: "Nielsen heuristics" `chapters = true`. Do: extract each heuristic with examples. Build: a scored heuristic audit sheet to run on your own site.
1081. **Agency positioning study** — Collect: `channels` of 10 design agencies, newest 30 each. Do: compare niches, offers and messaging. Build: a positioning map to find a gap for your studio.
1082. **Design-to-code prompts** — Collect: "Figma to code AI" `within = "month"`. Do: extract prompt patterns that gave clean output. Build: a prompt library for turning frames into components.
1083. **App UX friction list** — Collect: "[app name] review" `top_comments = 50`. Do: extract usability complaints from reviewers and commenters. Build: a ranked friction list for that app's product team.
1084. **Redesign principles** — Collect: "website redesign case study" `within = "year"`. Do: extract before/after changes and the reasons given. Build: a principles list for planning your own redesign.
1085. **Form design rules** — Collect: "form UX", "form design best practices". Do: extract rules on labels, errors, steps and inputs. Build: a form review checklist for sign-up and checkout.
1086. **Checkout UX audit** — Collect: "checkout UX", "cart abandonment" `within = "year"`. Do: extract fixes and claimed effects. Build: an audit sheet plus test ideas, claims marked to verify with your data.
1087. **Creator site patterns** — Collect: "personal website design" `within = "year"`. Do: extract sections people include and what they say drives contact. Build: a page plan for a freelancer's portfolio site.
1088. **Font licensing questions** — Collect: "font licensing explained". Do: list licence types and grey areas creators mention. Build: a question list to check with the foundry or a lawyer before shipping.
1089. **Daily inspiration feed** — Collect: "web design", "UI design" `within = "today"`, `min_views = 1000`, daily. Do: summarise each new video in one line. Build: a daily Slack post for a design team.
1090. **Template business plan** — Collect: "sell Framer templates", "Webflow templates income" `within = "year"`. Do: extract niches, pricing and marketplaces mentioned. Build: a plan for a first template, claims marked unverified.
1091. **Design review ritual** — Collect: "design critique process", "design ops". Do: extract formats, roles and feedback rules. Build: a weekly critique agenda and feedback guide.
1092. **HTML email design rules** — Collect: "email design", "HTML email" `within = "year"`. Do: extract width, font, dark mode and button rules. Build: a newsletter template checklist.
1093. **Webflow SEO setup** — Collect: "Webflow SEO" `within = "year"`. Do: extract setup steps: meta, sitemap, alt text, redirects. Build: a launch checklist for every Webflow site.

[↑ Contents](#contents)

## Creators and media

### YouTube creators & video production

1094. **Hook taxonomy** — Collect: your niche keywords, `within = "month"`, `min_views = 100000`, `timestamps = true`. Do: classify how each video's first 30 seconds opens (question, stakes, result-first). Build: hook taxonomy with paraphrased examples and links.
1095. **Breakout format finder** — Collect: niche keywords, `max_views = 50000`, `rising_views_per_day = 2000`, `within = "week"`. Do: ask what the fast risers share in topic, angle and length. Build: weekly list of formats a new channel could test.
1096. **Title structure ranking** — Collect: 300 videos per niche keyword, `within = "year"`, video_list.csv. Do: group titles by structure ("I tried X", "Why X") and compare median views per day. Build: spreadsheet of title templates ranked by views/day.
1097. **Own-channel pacing audit** — Collect: your channel via `channels`, `channel_max_videos = 30`, `chapters = true`. Do: measure setup vs payoff time per video and flag long intros. Build: per-video pacing report with fixes for the next script.
1098. **Unanswered-question backlog** — Collect: top niche videos with `top_comments = 50`, `within = "month"`. Do: extract viewer questions the videos left unanswered. Build: ranked backlog of video ideas, each with the comments behind it.
1099. **Niche viability check** — Collect: 8 candidate niche keywords, `within = "year"`, `min_views = 10000`, trends.html. Do: compare new-video supply against attention per keyword. Build: decision table marking each niche saturated, growing or underserved.
1100. **Personal scripting style guide** — Collect: your channel, `channel_min_views` set at your median. Do: contrast best vs worst videos on sentence length, open loops, CTA placement. Build: style guide plus a Claude skill that drafts scripts in it.
1101. **Title payoff timing** — Collect: top niche videos, `timestamps = true`. Do: find the second each video delivers what its title promises and compare with views/day. Build: "deliver the promise by minute X" rule sheet for your packaging.
1102. **Editing self-study course** — Collect: "DaVinci Resolve beginner", "Premiere Pro basics", `min_duration = 600`, `within = "year"`. Do: order topics from first cut to export. Build: 4-week beginner course with linked lessons and exercises.
1103. **Shorts cut-down SOP** — Collect: "shorts strategy", "long form to shorts", `include_shorts = true`. Do: extract structures creators recommend (text-first, loop endings). Build: SOP for turning each long video into three Shorts.
1104. **Algorithm claim tracker** — Collect: "YouTube algorithm update", `within = "week"`, daily runs. Do: separate claims quoting YouTube staff from speculation. Build: running FAQ of claims with sources and confidence labels.
1105. **Income mix planner** — Collect: "channel memberships", "YouTube affiliate income", "merch for YouTubers", `within = "year"`. Do: tabulate each revenue stream's requirements and creator-reported results. Build: income-mix comparison table.
1106. **Faceless channel reality check** — Collect: "faceless YouTube channel", `exclude_words = "guaranteed, passive income course"`. Do: list niches, tools and reported pitfalls. Build: honest pros/cons briefing before starting one.
1107. **Video essay beat sheets** — Collect: 5 video-essay `channels`, every video, `chapters = true`. Do: map act structure and how each argument is sequenced. Build: structure templates and a beat-sheet prompt for your next essay.
1108. **Gear consensus by budget** — Collect: "best camera for YouTube", "best YouTube microphone", `within = "month"`. Do: tally products recommended per price tier and the reasons given. Build: budget-tier gear table with linked justifications.
1109. **Livestream run-of-show** — Collect: 8 streamers' `channels`, `channel_tabs = "streams"`, `channel_max_videos = 10`. Do: summarise segment order, chat-interaction moments and lengths. Build: reusable livestream run-of-show template.
1110. **Cadence vs growth study** — Collect: 20 niche `channels`, all videos, then `yt.py export`. Do: compute upload frequency and views/day over time per channel. Build: spreadsheet chart testing whether cadence tracks views in your niche.
1111. **Collab scout** — Collect: adjacent-topic keywords, `max_views = 20000`, `within = "month"`. Do: find similar-sized channels and summarise their recent topics. Build: collab shortlist with a tailored pitch angle for each.
1112. **Agency prospect audit** — Collect: a prospect's channel, `channel_max_videos = 50`, `top_comments = 20`. Do: audit topic spread, pacing and what the audience keeps asking for. Build: pitch-deck outline of growth opportunities.
1113. **24-hour trend alert** — Collect: niche keywords, `within = "today"`, `rising_views_per_day = 5000`, scheduled daily. Do: flag topics spiking since yesterday. Build: daily shortlist of reactive video ideas with a publish-by date.
1114. **Pre-script fact list** — Collect: top 15 videos on your next topic, `timestamps = true`. Do: list factual claims and where creators contradict each other. Build: verify-before-scripting checklist with second-exact links.
1115. **CTA placement benchmark** — Collect: top niche videos with `sponsorblock` off so subscribe reminders stay. Do: find where and how creators ask for subscribes, likes, comments. Build: CTA placement guidelines with examples.
1116. **Search-intent content calendar** — Collect: related keywords finder on your seed topic. Do: cluster suggestions by intent (how-to, comparison, review). Build: 12-video content calendar, one video per cluster.
1117. **Media studies lesson** — Collect: "how to start a YouTube channel", `within = "year"`, `min_views = 50000`. Do: extract consensus steps and contested advice. Build: classroom lesson plan and quiz on how creator advice spreads.
1118. **Pacing complaint map** — Collect: niche videos with `top_comments = 100`. Do: find comments saying "get to the point" or citing skipped timestamps, and match them to transcript moments. Build: list of pacing mistakes to avoid.
1119. **Format outline skill** — Collect: 100 top videos in your format; map->reduce into `notes/` then `knowledge/format.md`. Do: distill the format's recurring beats. Build: Claude skill that outlines new scripts in that format.
1120. **Length sweet spot** — Collect: one topic keyword, `within = "year"`, then `yt.py export`. Do: bucket videos by duration and compare views/day per bucket. Build: chart and recommended length range for that topic.
1121. **Localisation priority** — Collect: your niche keywords in Spanish and Portuguese, `languages`, `translate` into English. Do: compare which subtopics are covered abroad vs at home. Build: report on which of your videos to dub first.
1122. **Channel trailer template** — Collect: "channel trailer", "welcome to my channel", `max_duration` short. Do: extract how trailers state who, what and why subscribe. Build: fill-in-the-blanks trailer script.
1123. **Solo creator workflow** — Collect: "YouTube burnout", "batch filming workflow", `within = "year"`. Do: summarise reported systems (batching, editors, schedules) and what failed. Build: weekly production SOP for a one-person channel.
1124. **Editor hiring kit** — Collect: "hiring a video editor YouTube", "YouTube editor rates". Do: extract rates mentioned, trial-task ideas and red flags. Build: hiring checklist and a paid test-edit brief.
1125. **Brand deal rate card** — Collect: "brand deal rates YouTube", "how much to charge sponsors", `within = "year"`. Do: compile pricing rules of thumb and their caveats. Build: draft rate card with ranges to sanity-check with peers.
1126. **Pivot decision tree** — Collect: "I changed my niche", "rebranding my channel". Do: compare outcomes and warning signs creators report. Build: decision tree for whether and how to pivot a stalled channel.
1127. **Thumbnail principles** — Collect: "thumbnail design tutorial", "Photoshop thumbnail", `within = "year"`. Do: extract principles (contrast, faces, word count) and conflicts. Build: thumbnail pre-publish checklist.
1128. **Policy changelog** — Collect: YouTube's official creator `channels`, `channel_within = "month"`, daily runs. Do: summarise each monetisation or policy announcement. Build: dated changelog with links to the exact second.
1129. **Analytics flashcards** — Collect: "YouTube analytics explained", "CTR and impressions". Do: extract definitions and the benchmarks creators claim. Build: Anki deck of analytics terms, benchmarks marked as opinions.
1130. **Fair use question list** — Collect: "fair use YouTube" from lawyer-run channels. Do: map the factors discussed and where lawyers disagree. Build: questions to take to a media lawyer before publishing commentary videos.
1131. **Documentary research dossier** — Collect: topic keywords, `within = "any"`, `min_duration = 1200`, `yt.py export`. Do: RAG over transcripts for every angle already covered. Build: dossier showing gaps your original documentary can fill.
1132. **Series fatigue check** — Collect: channels running series, `title_must_contain = "Episode"`. Do: compare views/day of episodes over time. Build: report on when recurring series gain or lose steam.
1133. **Edu explainer template** — Collect: 5 science-teaching `channels`, newest 40 each. Do: map explanation devices (analogy, worked example, recap). Build: instructional script template for education creators.
1134. **Pre-launch audience persona** — Collect: your audience's problem keywords with `top_comments = 100`. Do: cluster pain points voiced in comments. Build: audience persona doc and first 10 video topics.
1135. **Agency trend dashboard** — Collect: 30 client-niche keywords, daily schedule, trends.html. Do: weekly review of attention shifts and fastest risers. Build: client-facing trend dashboard with a short commentary.
1136. **Intro length benchmark** — Collect: top niche videos, `chapters = true`. Do: measure seconds until the first content chapter. Build: benchmark table of intro lengths for top performers vs average.
1137. **Vlog storytelling workbook** — Collect: 5 vloggers' `channels`, newest 30. Do: extract story devices (in medias res, callbacks, stakes reveals). Build: storytelling exercise workbook for vloggers.
1138. **Speaking habits report** — Collect: your channel, `remove_filler_words` off. Do: count fillers per minute and spot repeated phrases. Build: on-camera delivery report with targets for the next 5 videos.
1139. **Editor software comparison** — Collect: "DaVinci Resolve vs Premiere", "Final Cut vs", `within = "year"`. Do: tabulate pros, cons and price per use case. Build: comparison table to pick an editor.
1140. **Underserved query list** — Collect: related keywords finder on a seed, then each suggestion with `within = "month"`. Do: find queries with demand but few recent videos. Build: list of underserved searches to target.
1141. **Growth principles base** — Collect: long creator-strategy interviews, `min_duration = 3600`; map->reduce. Do: distill principles and who said them. Build: `knowledge/growth.md` with timestamped sources.
1142. **Creator economy newsletter** — Collect: "creator economy", "YouTube news", `within = "today"`, daily. Do: summarise and cite each story. Build: daily newsletter for creators, linking the videos.
1143. **Binge path planner** — Collect: your whole channel. Do: group videos into topic clusters and propose watch orders. Build: playlist and end-screen linking plan.
1144. **Pinned-reply answer bank** — Collect: your channel, `top_comments = 100`. Do: find repeated questions and use `yt.py find` to locate where you already answered. Build: FAQ with exact-second links for replies.
1145. **Shorts vs long-form test** — Collect: 10 similar `channels`, `channel_tabs` videos and shorts. Do: compare views/day per tab over a year. Build: report on whether Shorts seem to lift long-form for channels like yours.
1146. **Voiceover pace benchmark** — Collect: narration-led `channels`, newest 20. Do: compute words per minute from transcript length and duration. Build: pacing benchmark for your voiceover recordings.

[↑ Contents](#contents)

### Podcasting, audio & music production

1147. **Mix checklist** — Collect: "mixing vocals", "mix bus processing", `min_views = 50000`, `within = "year"`. Do: extract steps most engineers share vs disputed ones. Build: printable mix-session checklist.
1148. **Loudness target sheet** — Collect: "mastering LUFS streaming", "loudness normalization". Do: map stated targets and reasoning; flag contradictions. Build: loudness reference sheet to check against platform docs.
1149. **First DAW decision tree** — Collect: "Ableton vs FL Studio", "Logic vs Ableton", `within = "year"`. Do: compare by genre, workflow and price. Build: decision tree for beginners choosing a DAW.
1150. **Free plugin starter pack** — Collect: "best free plugins", "free VST", `within = "year"`. Do: tally mentions and stated uses. Build: ranked starter pack list by category (EQ, comp, reverb).
1151. **Music theory syllabus** — Collect: 3 theory educators' `channels`, all videos. Do: order concepts by prerequisite. Build: 12-week syllabus with linked lessons.
1152. **Genre recipe cards** — Collect: "how to make lo-fi beats", "techno kick tutorial", `timestamps = true`. Do: extract BPM, key, sound choices and arrangement. Build: one recipe card per genre.
1153. **Synth patch cheat sheets** — Collect: "Serum tutorial", "Vital sound design", `chapters = true`. Do: summarise patch steps by sound type. Build: indexed cheat sheets (bass, pad, pluck).
1154. **90-day podcast growth plan** — Collect: "podcast growth", "grow podcast audience", `within = "year"`. Do: separate tactics with reported results from generic advice. Build: 90-day experiment plan.
1155. **Guest prospect list** — Collect: 10 niche podcasts' `channels`, newest 50. Do: list recurring public guests and topics; find who appears across shows. Build: guest prospect list with outreach angles.
1156. **Video podcast studio** — Collect: "video podcast setup", "podcast studio on a budget". Do: compile gear lists by budget and layout tips. Build: shopping list and setup notes.
1157. **Episode show notes** — Collect: your newest episode via `channels`, `chapters = true`, `timestamps = true`. Do: summarise, chapter and pick key lines. Build: show notes and a companion blog post.
1158. **Clip picker** — Collect: your episodes with `timestamps = true`, `top_comments = 30`. Do: pick 5 self-contained moments, weighing what comments mention. Build: clip list with in/out times for Shorts.
1159. **Back catalogue search** — Collect: your podcast channel, every episode. Do: use `yt.py find` to search every past discussion of a topic. Build: "best of" compilation plan with exact-second links.
1160. **Ear training routine** — Collect: "ear training intervals", "relative pitch practice". Do: extract exercises and suggested progression. Build: daily 15-minute practice routine.
1161. **Songwriting knowledge base** — Collect: "songwriting process" interviews, `min_duration = 1800`; map->reduce. Do: distill techniques by songwriter. Build: `knowledge/songwriting.md` plus prompt cards.
1162. **Podcast mic comparison** — Collect: "best podcast microphone", "SM7B vs", `within = "year"`. Do: tabulate verdicts by room type and budget. Build: comparison table with reviewer links.
1163. **Room treatment SOP** — Collect: "acoustic treatment home studio", "bass traps placement". Do: extract placement rules and common myths. Build: step-by-step treatment plan for a small room.
1164. **Audio repair decision tree** — Collect: "iZotope RX dialogue repair", "remove background noise Audacity". Do: map fixes per problem (hum, reverb, clicks). Build: troubleshooting decision tree.
1165. **Release timeline** — Collect: "release music on Spotify strategy", "pre-save campaign". Do: extract steps and lead times. Build: release checklist counting back from release day.
1166. **Beat-selling model** — Collect: "selling beats online", `within = "year"`, `exclude_words = "course"`. Do: compare income claims with reported costs. Build: business model sheet with numbers to verify.
1167. **Sync licensing primer** — Collect: "sync licensing music" from working composers. Do: map how sync is described and which libraries are named. Build: library shortlist plus questions for a music lawyer.
1168. **Synth history lecture** — Collect: "history of the synthesizer", `min_duration = 900`. Do: build a timeline of instruments and people. Build: lecture notes and slide outline for a music tech class.
1169. **Gear news digest** — Collect: "new synth announced", "new audio interface", `within = "today"`, daily. Do: summarise announcements and prices. Build: daily gear news digest.
1170. **Narration setup** — Collect: "audiobook narration ACX", "home narration booth". Do: extract technical specs and workflow claims. Build: setup checklist to verify against ACX's own requirements.
1171. **Film scoring workflow** — Collect: 5 composer `channels`, newest 30. Do: extract approaches to spotting, themes and deliverables. Build: scoring workflow SOP.
1172. **Self-review rubric** — Collect: mix feedback `channel_tabs = "streams"` from 3 critique channels. Do: list problems critics hear most and their fixes. Build: rubric to score your own mixes.
1173. **Arrangement template** — Collect: "song breakdown" videos for your genre. Do: extract section lengths and energy changes. Build: arrangement template spreadsheet.
1174. **Host prep worksheet** — Collect: "how to interview people", interviewers on technique. Do: extract questioning techniques. Build: worksheet a host fills in before each episode.
1175. **Podcast revenue models** — Collect: "podcast sponsorship rates", "podcast Patreon", "podcast ads CPM". Do: tabulate models with reported numbers. Build: comparison table marked as claims to verify.
1176. **Type beat trend radar** — Collect: "type beat" keywords, `rising_views_per_day = 1000`, `within = "week"`. Do: see which artist styles are rising. Build: weekly list of styles to produce in.
1177. **Volunteer sound tech guide** — Collect: "church sound mixing", "FOH engineer tips". Do: extract the basics for small venues. Build: one-page training guide for volunteer sound techs.
1178. **DJ transition drills** — Collect: "DJ transitions tutorial", `chapters = true`. Do: order techniques by difficulty. Build: drill progression for a new DJ.
1179. **Instrument practice plan** — Collect: "guitar practice routine", "piano practice routine". Do: extract warmups, technique and repertoire blocks. Build: weekly practice plan per level.
1180. **Vocal chain table** — Collect: `title_must_contain = "vocal chain"` across genres. Do: tabulate plugin order and setting ranges. Build: starting-point chain table per genre.
1181. **Sample clearance questions** — Collect: "sample clearance explained", music lawyers' videos. Do: map opinions and grey areas. Build: question list for a music lawyer before releasing.
1182. **Game audio learning path** — Collect: "FMOD tutorial", "Wwise tutorial", "game audio". Do: order skills from basics to implementation. Build: learning path with linked lessons.
1183. **Foley reference** — Collect: "DIY foley sound effects", "foley artist". Do: extract which props make which sounds. Build: prop-to-sound reference table.
1184. **Podcast editing SOP** — Collect: "podcast editing workflow", "Descript editing". Do: extract steps and time estimates. Build: editor SOP with turnaround targets.
1185. **Music store staff bot** — Collect: 10 gear review `channels`, then `yt.py export`. Do: embed the .jsonl for RAG. Build: staff Q&A bot answering "what do reviewers say about X" with sources.
1186. **Producer habits base** — Collect: long producer interview `channels`; map->reduce. Do: distill working habits and studio rules. Build: `knowledge/producer-habits.md` with citations.
1187. **Chord progression dataset** — Collect: "chord progression explained", song analysis videos. Do: extract progressions and the songs cited. Build: CSV of progressions with example songs.
1188. **AI music tools briefing** — Collect: "AI music generator", "AI mastering", `within = "month"`. Do: map uses, quality opinions and ethics debates. Build: briefing for a label or collective.
1189. **Podcast launch checklist** — Collect: "how to start a podcast", `within = "year"`. Do: merge advice into ordered steps. Build: launch checklist from name to episode three.
1190. **Audio drama bible** — Collect: "audio drama production", "radio play sound design". Do: extract writing and production methods. Build: production bible template.
1191. **Show positioning memo** — Collect: top 5 shows in your niche, `channel_max_videos = 20`, `top_comments = 30`. Do: compare topics, lengths, praise and complaints. Build: positioning memo for your show.
1192. **School music unit** — Collect: "BandLab tutorial", "GarageBand for beginners". Do: pick age-appropriate steps. Build: 6-lesson production unit for middle school.
1193. **Remote guest guide** — Collect: "podcast mic technique", "record remote guest". Do: extract do's and don'ts. Build: one-page instructions sent to every guest.
1194. **Remote recording tools** — Collect: "Riverside vs Zencastr", "remote podcast recording". Do: tabulate quality, price and reliability claims. Build: comparison table.
1195. **Hearing health questions** — Collect: "hearing loss musicians", "musician ear plugs". Do: map advice creators give, as opinions only. Build: questions to ask an audiologist.
1196. **Non-English production tips** — Collect: Japanese and German mixing tutorials, `languages`, `translate`. Do: find techniques rarely covered in English. Build: digest of non-English tips.
1197. **Plugin deal monitor** — Collect: "plugin sale", "Black Friday plugins", `within = "today"`, daily. Do: extract deals and reviewer opinions. Build: daily deals shortlist matched to your wishlist.
1198. **Lyric workshop** — Collect: "how to write lyrics", songwriter lyric breakdowns. Do: extract exercises. Build: 4-session lyric-writing workshop.
1199. **Atmos primer** — Collect: "Dolby Atmos mixing", "spatial audio music", `within = "year"`. Do: explain setup options and workflow. Build: primer and glossary.
1200. **Album making-of timeline** — Collect: interviews with an album's artists and producers. Do: gather production anecdotes with dates. Build: fan-wiki-style timeline with citations.
1201. **Guest research brief** — Collect: a public guest's name, `within = "year"`. Do: summarise talking points they repeat on other shows. Build: prep doc with fresh questions that avoid repeats.

[↑ Contents](#contents)

### Writing, publishing & journalism

1202. **Craft lecture knowledge base** — Collect: university writing lecture series and author-craft `channels`; map->reduce. Do: distill plot, character and prose advice. Build: `knowledge/craft.md` organised by topic.
1203. **Structure framework table** — Collect: "Save the Cat", "three act structure", "hero's journey". Do: compare beats, strengths and critiques. Build: comparison table of story frameworks.
1204. **Query letter checklist** — Collect: "query letter", literary agents' `channels`. Do: extract dos, don'ts and common rejections. Build: query letter checklist.
1205. **Self-publishing budget** — Collect: "self publishing costs", "KDP income", `within = "year"`. Do: compare reported costs with income claims. Build: budget template with figures to verify.
1206. **Launch marketing plan** — Collect: "book marketing", "Amazon ads for authors", "BookTok for authors". Do: rank tactics by effort and reported results. Build: 90-day launch plan.
1207. **Trope demand table** — Collect: "[genre] book recommendations", `top_comments = 50`. Do: find tropes readers praise and complain about. Build: trope demand table for a genre novelist.
1208. **Newsletter growth list** — Collect: "Substack growth", "beehiiv growth", `within = "year"`. Do: extract tactics with reported subscriber numbers. Build: growth experiment list.
1209. **What YouTube said today** — Collect: your beat keywords, `within = "today"`, daily `combined/`. Do: summarise and cite the day's videos. Build: daily newsletter section with links to each source.
1210. **Viral claim worksheet** — Collect: claim keywords, `within = "week"`, `rising_views_per_day = 5000`, `timestamps = true`. Do: list exact claims with timestamps. Build: worksheet of claims to check against primary sources.
1211. **Agency beat log** — Collect: official agency and ministry `channels`, `channel_within = "today"`, daily. Do: summarise new public statements. Build: beat log with exact-second links.
1212. **Press conference quote sheet** — Collect: "press conference" plus the speaker, `within = "today"`, `timestamps = true`. Do: pull key quotes to confirm against the video. Build: quote sheet with links.
1213. **Candidate stance tracker** — Collect: candidate names, `within = "month"`, `timestamps = true`. Do: track stated positions over time. Build: stance table with exact-second sources.
1214. **Expert source list** — Collect: topic keywords, `min_duration = 1200`, conference talks. Do: list experts speaking publicly and their positions. Build: source list for interview outreach.
1215. **Non-fiction chapter notes** — Collect: lectures on your book's subject, `within = "any"`, `yt.py export`. Do: RAG per chapter question. Build: chapter research notes with citations to check.
1216. **Writing routine experiments** — Collect: "writing routine", author interviews. Do: extract routines and rationales. Build: 4-week experiment plan to test routines.
1217. **Dialogue workbook** — Collect: "writing dialogue", "subtext in dialogue". Do: extract techniques. Build: exercise workbook with one drill per technique.
1218. **Revision passes** — Collect: "self-editing a novel", "line editing". Do: order advice into separate passes. Build: multi-pass revision checklist.
1219. **Genre expectations sheet** — Collect: "romance tropes", "fantasy worldbuilding", "thriller pacing". Do: extract conventions readers expect. Build: genre expectations cheat sheet.
1220. **Small press briefing** — Collect: "publishing industry news", `within = "week"`. Do: summarise deals, trends and debates. Build: weekly briefing for a small press team.
1221. **Agent wishlist matcher** — Collect: "manuscript wishlist", agents' own `channels`. Do: summarise what each agent says they want. Build: agent-genre spreadsheet to research further.
1222. **Screenplay format check** — Collect: "screenplay format", screenwriter interviews. Do: extract formatting rules and structure advice. Build: formatting checklist and structure notes.
1223. **Essay writing unit** — Collect: "how to write an essay", "thesis statement". Do: pick clear explanations by grade level. Build: lesson plan and grading rubric.
1224. **Poetry forms deck** — Collect: "poetry forms explained", "sonnet villanelle". Do: extract rules and examples cited. Build: flashcard deck of forms.
1225. **Cover designer brief** — Collect: "book cover design [genre]", `within = "year"`. Do: extract current genre cover conventions. Build: brief for a cover designer.
1226. **Audiobook route choice** — Collect: "audiobook self publishing", "ACX vs Findaway". Do: compare routes, costs and royalty claims. Build: decision table with terms to verify.
1227. **Book Kickstarter plan** — Collect: "Kickstarter book campaign". Do: extract timelines, reward tiers and pitfalls. Build: campaign timeline template.
1228. **Data journalism path** — Collect: "data journalism tutorial", "Datawrapper", "spreadsheets for journalists". Do: order skills. Build: learning path for reporters.
1229. **Council meeting brief** — Collect: your city council's `channels`, `channel_within = "week"`, `timestamps = true`. Do: summarise decisions and debates. Build: weekly local-news brief with exact-second links.
1230. **Narrative spread study** — Collect: narrative keywords, `within = "month"`, `languages`, `translate`. Do: track how a narrative spreads across languages and dates. Build: dataset and timeline for a research paper.
1231. **Op-ed argument map** — Collect: debate videos and talks on your topic. Do: steelman each side. Build: argument map to write against before drafting an op-ed.
1232. **Foreign framing memo** — Collect: foreign news `channels`, `translate`. Do: compare framing of one event with domestic coverage. Build: framing comparison memo.
1233. **Historical setting bible** — Collect: lectures on your period, `min_duration = 1800`. Do: extract daily-life details and sources cited. Build: setting bible for a historical novelist.
1234. **Character research notes** — Collect: psychology lectures on your character's experience. Do: summarise how experts describe it. Build: character profile notes with sources.
1235. **Publication AI policy** — Collect: "AI writing authors", "AI in newsrooms", `within = "year"`. Do: map positions and arguments. Build: draft AI-use policy for a writers' group or outlet.
1236. **Freelance pitch kit** — Collect: "freelance writing rates", "pitching editors". Do: extract pitch structures and rate ranges. Build: pitch template and rate notes.
1237. **Earnings call tip sheet** — Collect: company `channels` posting earnings calls, `timestamps = true`. Do: extract forward-looking statements. Build: story tip sheet with quotes to verify.
1238. **MFA decision table** — Collect: "is an MFA worth it", "MFA vs no MFA". Do: tabulate arguments and costs mentioned. Build: pros/cons decision table.
1239. **Book club guide** — Collect: author interviews about one book. Do: extract themes and stated intentions. Build: discussion guide citing interviews.
1240. **Picture book submission** — Collect: "picture book publishing", "children's book agent". Do: extract steps and norms. Build: submission checklist.
1241. **Grammar deck** — Collect: grammar-teaching `channels`. Do: extract rules with examples. Build: Anki deck for students or ESL writers.
1242. **Explainer reader questions** — Collect: top explainers on your topic, `top_comments = 100`. Do: list questions readers still ask. Build: question list your explainer must answer.
1243. **Serial fiction platforms** — Collect: "Royal Road", "Wattpad", "Kindle Vella", `within = "year"`. Do: compare reach and payout claims. Build: platform comparison table.
1244. **AuthorTube content plan** — Collect: author `channels` with `max_views = 50000`. Do: find which author video types draw views. Build: 3-month content plan for an author channel.
1245. **Speech template** — Collect: "how to write a speech", speechwriter talks. Do: extract structures. Build: speech template for toasts, keynotes and eulogies.
1246. **Footage verification SOP** — Collect: "verifying viral footage", newsroom verification talks. Do: extract the verification workflow. Build: newsroom SOP for checking user-uploaded footage.
1247. **House style update** — Collect: "AP style changes", style editors' talks, `within = "year"`. Do: list changes discussed. Build: house style update memo to confirm against the guide.
1248. **Craft prompt deck** — Collect: author process interviews; map->reduce into `notes/`. Do: turn each insight into an exercise. Build: 100 writing prompts, each crediting its source.
1249. **Memoir workbook** — Collect: "how to write a memoir", memoirist interviews. Do: extract structures and ethics of writing about real people. Build: memoir outline workbook.
1250. **Book proposal template** — Collect: "nonfiction book proposal", editors' advice. Do: extract required sections. Build: proposal template.
1251. **Literary translation notes** — Collect: literary translators' talks, `min_duration = 1800`. Do: summarise process, rights and pay discussions. Build: briefing for a first-time translator.
1252. **KDP keyword list** — Collect: related keywords finder on your book's topic. Do: map how readers phrase searches. Build: KDP keyword and category list to test.
1253. **J-school pitching module** — Collect: "how to pitch a story editor", newsroom talks. Do: extract pitching methods. Build: course module with exercises.
1254. **Public figure profile file** — Collect: a public figure's interviews, `within = "any"`, `timestamps = true`. Do: build a timeline of public statements. Build: profile background file with citations.
1255. **Video report text versions** — Collect: your newsroom's `channels` as .srt and .md. Do: clean and edit transcripts. Build: captions and article versions of your own video reports.
1256. **Study explainer draft** — Collect: researchers' talks on a new study. Do: extract their explanations and caveats. Build: plain-language draft with points to confirm with the authors.

[↑ Contents](#contents)

### Photography, film & visual arts

1257. **Beginner photo course** — Collect: "exposure triangle", "composition rules", `min_views = 100000`. Do: order concepts with exercises. Build: 6-week beginner photography course.
1258. **Camera buying table** — Collect: "best mirrorless camera", `within = "month"`. Do: tally picks by budget and use. Build: comparison table with reviewer links.
1259. **Lens verdict sheet** — Collect: a lens name with `title_must_contain`, `within = "year"`. Do: summarise sharpness, autofocus and flaw claims. Build: verdict sheet before buying.
1260. **Grading node SOP** — Collect: "DaVinci Resolve color grading", `chapters = true`. Do: extract node structures and order. Build: grading SOP for a small post team.
1261. **Lightroom recipe cards** — Collect: "Lightroom landscape edit", "Lightroom portrait edit". Do: extract slider moves and their reasons. Build: recipe cards per photo type.
1262. **Wedding photo business kit** — Collect: "wedding photography pricing", "wedding shot list". Do: extract packages and must-have shots. Build: pricing sheet and shot list.
1263. **Cinematography technique DB** — Collect: cinematography breakdown `channels`, all videos. Do: extract techniques per film. Build: searchable technique database with links.
1264. **Short film budget** — Collect: "low budget short film", "micro budget filmmaking". Do: extract cost lines and savings. Build: budget template.
1265. **30-day drawing plan** — Collect: 3 drawing-instruction `channels`. Do: order fundamentals. Build: 30-day plan with daily drills.
1266. **Animation principles drills** — Collect: "12 principles of animation". Do: extract exercises per principle. Build: flashcards and practice drills.
1267. **Blender learning path** — Collect: "Blender tutorial beginner", `within = "year"`. Do: order topics and flag outdated-version tutorials. Build: current learning path.
1268. **Blender release digest** — Collect: "Blender new features", `within = "month"`. Do: summarise changes and workflow impact. Build: release digest for a studio.
1269. **Self-critique rubric** — Collect: art critique `channel_tabs = "streams"`. Do: list recurring critique points. Build: self-critique rubric.
1270. **Street photo law questions** — Collect: "street photography laws" for your country, `translate`. Do: map opinions and conflicts. Build: questions for a lawyer, nothing taken as advice.
1271. **Drone rules check** — Collect: "drone rules", `within = "year"`. Do: list rules creators cite by country. Build: checklist to verify with the aviation authority before flying.
1272. **Film study guide** — Collect: video essays on one film. Do: summarise themes and techniques discussed. Build: student study guide with citations.
1273. **Directing actors prep** — Collect: "directing actors tips", director interviews. Do: extract rehearsal and note-giving methods. Build: director prep sheet.
1274. **Lighting setup notes** — Collect: "portrait lighting setup", "one light portrait". Do: extract light positions and modifiers. Build: setup notes per look.
1275. **Festival submission plan** — Collect: "film festival strategy", "festival submission tips". Do: extract strategies and timelines. Build: submission calendar.
1276. **Stock photo reality check** — Collect: "stock photography earnings", `within = "year"`. Do: compare earnings claims with effort. Build: honest income model with figures to verify.
1277. **Art school AI policy** — Collect: "AI art artists", "AI image ethics", `within = "year"`. Do: map positions and arguments. Build: briefing for an art school's policy.
1278. **Procreate technique index** — Collect: "Procreate tutorial", `chapters = true`. Do: index techniques by goal. Build: technique index with exact-second links.
1279. **Watercolour supply list** — Collect: "best watercolor paper", "watercolor supplies beginner". Do: tally recommended supplies. Build: budget supply list.
1280. **Art history flashcards** — Collect: museum and art-history `channels`. Do: extract movements, dates and works. Build: timeline flashcard deck.
1281. **Exhibition visitor guide** — Collect: curator talks on an exhibition. Do: summarise key works and context. Build: visitor guide.
1282. **Character design checklist** — Collect: "character design process", artist process videos. Do: extract steps. Build: process checklist.
1283. **Compositing learning path** — Collect: "Nuke compositing", "After Effects compositing". Do: order skills. Build: learning path for VFX newcomers.
1284. **Photo contest checklist** — Collect: "photo contest critique", "winning photos". Do: extract judges' criteria. Build: entry checklist.
1285. **Astro night checklist** — Collect: "astrophotography settings", "Milky Way photography". Do: extract settings and planning steps. Build: night-shoot checklist.
1286. **Wildlife field code** — Collect: "wildlife photography ethics", "baiting wildlife". Do: summarise ethical positions. Build: field code of conduct.
1287. **Film stock table** — Collect: "Portra 400 review", "film stock comparison". Do: tabulate stocks by look and use. Build: film stock comparison table.
1288. **Production company onboarding** — Collect: "corporate video production workflow", `within = "year"`. Do: extract steps from brief to delivery. Build: client onboarding SOP.
1289. **Storyboard template** — Collect: "storyboarding tutorial", "storyboard artist". Do: extract conventions. Build: storyboard template and guide.
1290. **Editing philosophy base** — Collect: talks by film editors, `min_duration = 1800`; map->reduce. Do: distill principles of rhythm and cutting. Build: `knowledge/editing.md` with citations.
1291. **Anime pipeline overview** — Collect: Japanese animation process videos, `languages = "ja"`, `translate`. Do: map production stages. Build: pipeline overview.
1292. **Camera rumour log** — Collect: "camera rumors", `within = "today"`, daily. Do: log claims and later confirmations. Build: rumour log with confidence labels.
1293. **Mural proposal kit** — Collect: "mural pricing", "public art commission". Do: extract pricing and proposal structure. Build: proposal template.
1294. **Elementary art unit** — Collect: "art lesson elementary", "kids art project". Do: pick projects by age. Build: 6-week unit plan.
1295. **Photo editor comparison** — Collect: "Capture One vs Lightroom", `within = "year"`. Do: compare features, price and workflows. Build: comparison table.
1296. **Real estate shoot SOP** — Collect: "real estate photography", "HDR interiors". Do: extract shot order and settings. Build: shoot SOP.
1297. **Home product photo setup** — Collect: "product photography at home", "ecommerce photos". Do: extract setups by budget. Build: setup guide for a small shop.
1298. **Emerging artist discovery** — Collect: "speedpaint", "digital painting", `max_views = 10000`, `rising_views_per_day = 300`. Do: find rising small artists. Build: discovery list to follow and feature.
1299. **Art sales channel table** — Collect: "selling art online", "selling prints Etsy". Do: compare platforms. Build: sales channel comparison table.
1300. **Virtual production primer** — Collect: "Unreal Engine virtual production", `within = "year"`. Do: extract setups and costs. Build: primer for an indie studio.
1301. **3D capture tool table** — Collect: "Gaussian splatting", "photogrammetry", `within = "month"`. Do: compare tools and results. Build: comparison table.
1302. **Artist copyright questions** — Collect: "copyright for artists", lawyers' videos. Do: map positions and grey areas. Build: questions for an IP lawyer.
1303. **Colour theory exercises** — Collect: "color theory for artists". Do: extract concepts. Build: palette exercises and flashcards.
1304. **Film school Q&A bot** — Collect: cinematography `channels`, `yt.py export`. Do: embed the .jsonl. Build: student Q&A bot citing exact-second sources.
1305. **Commission price calculator** — Collect: "how to price art commissions". Do: extract formulas artists use. Build: pricing calculator spreadsheet.
1306. **Camera movement glossary** — Collect: "camera movements explained", `timestamps = true`. Do: define each move. Build: glossary with exact-second examples.
1307. **City photo trip list** — Collect: "photography spots [city]", `languages`, `translate`. Do: extract locations and best times. Build: location list for a photo trip.
1308. **Retouching SOP** — Collect: "frequency separation", "skin retouching Photoshop". Do: extract steps and restraint advice. Build: retouching SOP.
1309. **Webcomic workflow** — Collect: "how to make a webcomic", "manga making process". Do: extract stages. Build: production workflow.
1310. **Gear maintenance schedule** — Collect: "camera sensor cleaning", "lens care". Do: extract routines and warnings. Build: maintenance schedule.

[↑ Contents](#contents)

## Learning and research

### Education, teaching & self-study

1311. **Free degree-style syllabus** — Collect: university lecture playlists via `channels` for "intro to economics lecture". Do: order topics by prerequisite, flag gaps. Build: a 12-week self-study syllabus linking each lecture.
1312. **Course notes with second-links** — Collect: one course playlist, `chapters`, `timestamps`. Do: map->reduce a note per lecture into notes/, then knowledge/course.md. Build: searchable course notes that jump to the exact second.
1313. **Anki deck from lectures** — Collect: a lecture playlist, `remove_filler_words`. Do: pull definitions, formulas and key claims per lecture. Build: a cloze-flashcard CSV for Anki with the source timestamp on every card.
1314. **Lesson plan from top explainers** — Collect: "photosynthesis explained" `max_duration = 900`. Do: compare how explainers sequence the idea and which analogies they use. Build: a 45-minute lesson plan with hook, analogy and check-for-understanding.
1315. **Misconception catalogue** — Collect: "common algebra mistakes" `top_comments = 30`. Do: list misconceptions creators name plus confusions learners post. Build: a misconception-to-fix table for a maths department.
1316. **Homeschool week planner** — Collect: kids' science channels via `only_channels`, `max_duration = 1200`. Do: group by grade and topic, write discussion questions. Build: a printable homeschool week with video links and hands-on activities.
1317. **Best explainer per level** — Collect: "Fourier transform explained" `within = "any"`, `min_views = 100000`. Do: score clarity, assumed prerequisites, worked examples. Build: a table naming the best video for beginners, students and pros.
1318. **Study-technique evidence check** — Collect: "spaced repetition", "active recall" `top_comments = 20`. Do: split claims citing studies from anecdote; list studies named. Build: a claims-vs-evidence sheet to check against the research.
1319. **New free course radar** — Collect: "full course" `within = "week"`, `min_duration = 7200`, daily schedule. Do: summarise scope, level and prerequisites of each new long course. Build: a weekly newsletter of new free full-length courses.
1320. **Certification topic weighting** — Collect: "AWS Solutions Architect exam experience" `within = "month"`. Do: rank topics creators say appeared on recent exams. Build: a weighted study checklist with a mention-count column.
1321. **Socratic tutor skill** — Collect: a full course playlist, then `yt.py export`. Do: have Claude Code index concepts into knowledge/. Build: a Claude skill that quizzes the student Socratically and cites the lecture second.
1322. **Flipped-class pre-watch packs** — Collect: short explainers `max_duration = 480` per unit keyword. Do: write 3 comprehension questions and a "muddiest point" prompt per video. Build: a pre-class packet for each lesson.
1323. **Accessible class handouts** — Collect: the videos a teacher assigns, `strip_sound_tags`, .srt output. Do: tidy text for students who need reading support. Build: readable transcript handouts and caption files for in-class use.
1324. **Differentiated reading sheets** — Collect: one explainer per topic, `subtitles_only`. Do: re-explain the idea in original words at grade 4, 8 and 12 levels. Build: three-level reading sheets with vocab lists, citing the video.
1325. **Course glossary** — Collect: a whole lecture playlist. Do: extract every technical term with the lecturer's definition and first use. Build: an alphabetical glossary with timestamped links.
1326. **Prerequisite gap finder** — Collect: a course playlist plus "what to know before learning X". Do: list concepts lectures assume but never teach. Build: a "before you start" primer linking short catch-up videos.
1327. **Coding tutorial checklist** — Collect: "build a todo app React tutorial" `min_duration = 1800`, `chapters`. Do: extract each step, command and file changed. Build: a follow-along checklist with timestamps to rewatch when stuck.
1328. **Teacher PD one-pagers** — Collect: "formative assessment strategies" `within = "year"`. Do: pull concrete classroom strategies with grade level and setup. Build: a one-page PD brief per strategy for a staff meeting.
1329. **Ed-tech purchase matrix** — Collect: "Kahoot vs Quizizz", "best LMS for teachers" `within = "year"`. Do: tabulate pros, cons, price and privacy claims. Build: a decision matrix for a school committee with claims marked to verify.
1330. **Parent guide to new maths** — Collect: "common core math explained for parents". Do: summarise each method and why schools teach it. Build: a parent FAQ handout for the school newsletter.
1331. **Learner search map** — Collect: related keywords finder on "learn statistics". Do: cluster queries into beginner, intermediate, advanced. Build: a topic map of what learners actually search, in learning order.
1332. **Revision audio scripts** — Collect: unit review videos for a course. Do: condense each unit into a 5-minute two-voice dialogue with original examples. Build: revision scripts students record and replay.
1333. **Professor-by-topic picker** — Collect: "linear algebra lecture" from several universities via `only_channels`. Do: compare coverage, order and depth per topic. Build: a table of whose lecture to watch for each topic.
1334. **Worked-problem set** — Collect: "kinematics problem solving" `min_duration = 600`. Do: extract each worked problem's setup and solution steps. Build: a problem set with solution outlines linking to the video walkthrough.
1335. **Self-study recall log** — Collect: the playlist you study, daily run with `channel_max_videos = 2`. Do: after each lecture Claude asks 5 recall questions from notes/. Build: a progress log with scores and weak topics to revisit.
1336. **Tutorial FAQ supplement** — Collect: a popular tutorial with `top_comments = 50`. Do: cluster learner questions and answer each from the transcript. Build: an FAQ page to sit beside the course.
1337. **Apprentice trade study guide** — Collect: "electrician apprentice exam", "HVAC basics" `min_views = 20000`. Do: extract topics and safety rules as stated. Build: a study guide where every rule is flagged "check against the official code".
1338. **Board-exam priority tracker** — Collect: "USMLE Step 1 high yield" `within = "year"`. Do: rank topics by mention frequency as study-priority opinion, not clinical guidance. Build: a ranked topic spreadsheet.
1339. **Standards alignment sheet** — Collect: explainers for each learning-standard keyword. Do: match videos to the teacher's standards list and note coverage depth. Build: a standards-to-video alignment spreadsheet.
1340. **Missed-class digest** — Collect: a teacher's own channel, `channel_within = "week"`, `timestamps`. Do: summarise the week's lectures and homework mentioned. Build: a Friday email for absent students.
1341. **Instructor's course Q&A bot** — Collect: an instructor's own lecture videos, `yt.py export` jsonl. Do: embed into a RAG index. Build: a course bot that answers with links to the lecture second.
1342. **Lecture pacing chart** — Collect: a course playlist with `timestamps`. Do: measure words per minute and new terms per minute per lecture. Build: a chart flagging lectures to watch at slower speed.
1343. **Micro-lesson cards from Shorts** — Collect: "math trick" `include_shorts = true`, `max_duration = 60`. Do: verify each trick and explain why it works. Build: a daily micro-lesson card set with the reasoning added.
1344. **Study routine menu** — Collect: "how I study 10 hours a day", "pomodoro" `top_comments = 20`. Do: extract routines and what commenters say worked. Build: a routine menu with a one-week trial template.
1345. **College essay do/don't list** — Collect: "college essay tips", "admissions officer reacts" `within = "year"`. Do: list advice most creators agree on and where they clash. Build: a checklist labelled as creator opinion.
1346. **Test-format strategy check** — Collect: "digital SAT tips" `within = "year"`. Do: compare strategies and flag ones written for the old format. Build: a current-format strategy table with practice drills.
1347. **Teacher channel re-record list** — Collect: your own channel with `top_comments = 30`. Do: find concepts commenters found confusing. Build: a prioritised list of lessons to re-record or clarify.
1348. **Course creator gap finder** — Collect: "learn Excel" twice, high `min_views` vs `max_views = 5000`. Do: find subtopics people seek but popular videos skip. Build: an outline for an online course that fills the gap.
1349. **Cross-course concept index** — Collect: 5 machine-learning course playlists. Do: map each concept to where every course explains it. Build: an index of concept -> three timestamped explanations.
1350. **Kids' video vetting** — Collect: candidate kids' channels, `top_comments = 20`. Do: check language and topics against age guidelines. Build: an approved-video list for a family or classroom.
1351. **Field-trip worksheet** — Collect: "museum virtual tour" and topic documentaries `max_duration = 1800`. Do: extract facts and questions to ask on site. Build: a student scavenger-hunt worksheet.
1352. **Classroom demo planning cards** — Collect: "chemistry classroom demo" from education channels. Do: list materials, steps and stated precautions. Build: demo cards marked to check with the school safety officer.
1353. **Visual concept map** — Collect: one subject's lecture playlist. Do: extract concept dependencies as edges. Build: a JSON graph rendered as a clickable concept map for students.
1354. **ELL support sheets** — Collect: explainers with `translate = "es"`. Do: pair key English terms with Spanish glosses. Build: side-by-side vocabulary sheets for English-language learners.
1355. **Tutoring session script** — Collect: explainers on the topic a student struggles with. Do: write diagnostic questions that pinpoint the gap. Build: a 30-minute tutoring script with fallback explanations.
1356. **Staffroom AI briefing** — Collect: "AI in the classroom", "ChatGPT homework" `within = "week"`. Do: use `trends.html` to spot what teachers discuss most. Build: a weekly briefing on new practices and concerns.
1357. **School AI policy inputs** — Collect: "AI detectors teachers", "AI school policy" `top_comments = 20`. Do: map positions teachers, students and parents voice. Build: discussion questions for drafting a policy.
1358. **Textbook video companion** — Collect: videos per chapter title with `title_must_contain`. Do: pick the best two per chapter and note how each differs from the text. Build: a video companion guide.
1359. **Career-switch roadmap** — Collect: "how I became a data analyst self-taught" `within = "year"`. Do: extract resources, timelines and what they'd skip. Build: a 6-month learning roadmap with milestones.
1360. **Live-class stream index** — Collect: an instructor's `channel_tabs = "streams"`, `timestamps`. Do: detect topic changes in multi-hour sessions. Build: a topic index so students jump to each segment.
1361. **Unit cram sheet** — Collect: review videos for one unit. Do: compress to formulas, definitions and 10 likely questions. Build: a one-page cheat sheet per unit.
1362. **Teaching-technique playbook** — Collect: 3Blue1Brown, Khan Academy via `channels`. Do: analyse how they open, use analogies and recap. Build: a playbook of explanation techniques for new teachers.
1363. **Underrated tutor finder** — Collect: "calculus explained" `max_views = 10000`, `min_duration = 600`. Do: rank transcripts by explanation clarity. Build: a list of small tutors to recommend to students.
1364. **Student research starter pack** — Collect: related keywords for the project topic, `within = "year"`. Do: list subtopics, claims and sources creators cite. Build: a starter pack of sources to find and check in the library.

[↑ Contents](#contents)

### Language learning

1365. **Comprehensible input ladder** — Collect: "easy Spanish" `languages = ["es"]`, `subtitles_only`. Do: rate each transcript by word frequency and sentence length. Build: a graded watch list from A1 to B2.
1366. **Sentence-mining deck** — Collect: one native channel in your target language. Do: pull unknown words with the sentence they appear in. Build: an Anki CSV where each card links to the second you can hear it.
1367. **Grammar in the wild** — Collect: native German vlogs `languages = ["de"]`; `yt.py find "obwohl"`. Do: gather real sentences using the pattern. Build: a grammar sheet of 30 authentic examples linked to the second.
1368. **Hobby domain word list** — Collect: Japanese cooking videos `languages = ["ja"]`. Do: compute the most frequent words in that domain. Build: a top-500 vocabulary list for a cooking-loving learner.
1369. **Accent contrast table** — Collect: "British vs American accent", "Australian accent explained". Do: list the sound differences with example words. Build: a contrast table with practice word pairs.
1370. **Regional slang glossary** — Collect: "Mexican Spanish slang", "Argentinian Spanish" `within = "year"`. Do: catalogue regional words with usage notes. Build: a regional-variant glossary.
1371. **Listening worksheets** — Collect: native clips `max_duration = 300`. Do: write gap-fill and true/false items from the transcript. Build: listening worksheets with answer key and video link for a class.
1372. **Daily graded news** — Collect: "noticias" `within = "today"`, `languages = ["es"]`, daily schedule. Do: retell the day's news in simple Spanish with a glossary. Build: a daily B1 news digest.
1373. **Parallel reading texts** — Collect: target-language videos plus `translate = "en"` copies. Do: align original and translation line by line. Build: two-column study texts for personal use.
1374. **Method comparison** — Collect: "how I learned Japanese", "polyglot tips" `top_comments = 20`. Do: list methods, hours claimed and what commenters report. Build: a table to choose a study plan.
1375. **JLPT/DELE checklist** — Collect: "JLPT N3 grammar", "DELE B2 tips" `within = "year"`. Do: list grammar points and exam tactics. Build: a checklist mapped to each exam section.
1376. **Idiom cards from vlogs** — Collect: casual English vlogs `languages = ["en"]`. Do: find phrasal verbs and idioms in natural speech. Build: idiom cards with real context sentences and links.
1377. **Sound-natural filler sheet** — Collect: unscripted interviews with `remove_filler_words = false`. Do: catalogue fillers and discourse markers natives use. Build: a "sound natural" cheat sheet.
1378. **Glossed intensive reading** — Collect: a learner podcast channel. Do: Claude marks B1+ words and adds glosses. Build: glossed transcripts for private intensive-reading sessions.
1379. **Error-correction quiz** — Collect: "mistakes English learners make" `top_comments = 30`. Do: list errors with corrections. Build: a 50-item spot-the-error quiz.
1380. **Pronunciation sprint** — Collect: "French nasal vowels", "French r pronunciation". Do: extract minimal pairs and mouth-position tips. Build: a 10-day pronunciation drill plan.
1381. **Tutor session phrasebook** — Collect: target-language videos on "job interview". Do: extract useful phrases and questions. Build: a phrasebook to rehearse with an online tutor.
1382. **Level-locked chat partner** — Collect: native channels, `yt.py export`. Do: build a RAG of real phrases by level. Build: a Claude prompt that chats at your level using phrasing seen in transcripts.
1383. **Graded reader writer** — Collect: a native explainer on a topic. Do: retell it in original simple A2 text. Build: a short graded reader with glossary, citing the source video.
1384. **Authentic-materials bank** — Collect: `languages = ["fr"]`, `max_duration = 480`, theme keywords like "environnement". Do: rate level and classroom fit. Build: a bank sorted by CEFR level and theme.
1385. **Phrase-of-the-day for kids** — Collect: children's cartoons and songs in the target language `max_duration = 300`. Do: extract repeated phrases. Build: a parent's phrase-of-the-day calendar.
1386. **Relocation business glossary** — Collect: target-language business interviews. Do: extract workplace vocabulary and polite formulas. Build: an industry glossary for a professional moving abroad.
1387. **Machine translation critique** — Collect: a video with `translate = "en"`. Do: compare your own translation with YouTube's and note errors. Build: a translation practice log.
1388. **Sign language curriculum** — Collect: "ASL lesson" channels. Do: organise lessons by vocabulary theme (transcripts describe, not show, signs). Build: a curriculum outline linking each lesson.
1389. **Heritage speaker refresher** — Collect: target-language talks on formal topics. Do: list formal vocabulary heritage speakers often lack. Build: a heritage-learner study plan.
1390. **Immersion log** — Collect: chosen channels daily, `channel_max_videos = 3`. Do: log input minutes and new words per video. Build: a spreadsheet with an input-hours and words-learned curve.
1391. **False-friends list** — Collect: native videos in Portuguese. Do: list cognates and false friends with English. Build: a false-friends warning list with real example lines.
1392. **Textbook clip supplement** — Collect: native clips per textbook chapter theme. Do: pair each chapter with two clips. Build: a supplement map for a language course.
1393. **Speaking prompts from debates** — Collect: target-language opinion videos `top_comments = 20`. Do: turn the debated points into prompts. Build: a weekly speaking-practice prompt list.
1394. **Trending ESL lesson** — Collect: English videos `within = "week"`, `rising_views_per_day`. Do: build vocabulary and discussion around a viral topic. Build: a timely ESL lesson plan.
1395. **Realistic progress timeline** — Collect: "1 year learning Korean" `within = "year"`. Do: extract hours, methods and plateaus reported. Build: a realistic-expectations timeline for new learners.
1396. **App comparison table** — Collect: "Duolingo vs Babbel" `within = "year"`. Do: tabulate features and claims. Build: an app comparison table with claims to verify.
1397. **Tense priority list** — Collect: native Spanish vlogs; `yt.py find` for tense markers. Do: count tense usage in real speech. Build: a priority list of tenses to learn first.
1398. **Slang watch** — Collect: youth channels in target language `within = "month"`. Do: track new slang on `trends.html`. Build: a monthly "new slang" update for advanced learners.
1399. **Interpreter glossary** — Collect: conference talks on the event topic in both languages. Do: align terms across languages. Build: a bilingual glossary for an interpreting assignment.
1400. **Language teacher content plan** — Collect: language-teaching channels `top_comments = 30`. Do: find most-asked learner questions left unanswered. Build: a content calendar for a teacher's channel.
1401. **Dictation exercises** — Collect: slow native videos as .srt. Do: split into sentences with timings. Build: dictation drills where you type then check against the transcript.
1402. **Shadowing scripts** — Collect: native videos as .vtt with `timestamps`. Do: chunk into 5-second phrases. Build: a shadowing script with time codes to loop.
1403. **Culture notes unit** — Collect: "culture shock Japan", "living in Germany as a foreigner". Do: extract norms and etiquette. Build: culture notes for a language class unit.
1404. **Minority language directory** — Collect: `languages = ["cy"]`, "learn Welsh". Do: find what native content exists and at what level. Build: a resource directory for Welsh learners.
1405. **Spoken corpus for coursework** — Collect: thousands of target-language videos with proxies, `yt.py export`. Do: study word frequency and collocations. Build: a cited corpus for a linguistics project.
1406. **Unified grammar rule** — Collect: "ser vs estar explained" from several teachers. Do: compare rules and exceptions each gives. Build: one rule sheet with disagreements flagged.
1407. **Mnemonic library** — Collect: "kanji mnemonics", "German noun gender tricks". Do: collect and group memory strategies. Build: a mnemonic library by skill.
1408. **Travel phrase card** — Collect: "Italian phrases for travel" `within = "year"`. Do: dedupe to the 50 most-taught phrases. Build: a printable pocket card.
1409. **Channel speed ranking** — Collect: target-language channels with `timestamps`. Do: compute words per minute per channel. Build: a slowest-to-fastest channel ranking for graded listening.
1410. **Tutor homework pack** — Collect: one video the student enjoys. Do: generate vocab list, 5 questions and a writing prompt. Build: a ready homework pack.
1411. **Cross-cultural topic contrast** — Collect: one topic in three `languages`. Do: compare how each culture frames it. Build: an advanced discussion activity.
1412. **Korean register guide** — Collect: Korean videos on 존댓말 and honorifics. Do: extract formality levels with examples. Build: a register guide with when-to-use rules.
1413. **Language club newsletter** — Collect: language-learning channels `within = "week"`, `sponsorblock`. Do: summarise new methods and resources. Build: a weekly club newsletter.
1414. **Plateau decision tree** — Collect: "stuck at B1", "intermediate plateau" `top_comments = 30`. Do: map causes and remedies offered. Build: a decision tree to diagnose your plateau.
1415. **Song-meaning lesson notes** — Collect: "song meaning explained" in Spanish. Do: note vocab and grammar points discussed, no full lyrics. Build: music-based lesson notes.
1416. **Particle quiz** — Collect: "は vs が explained" plus native vlogs; `yt.py find`. Do: match rules to real usage. Build: a particle quiz built from real sentences.
1417. **90-day course calendar** — Collect: a language course playlist via `channels`. Do: split into 20-minute daily lessons with review days. Build: a 90-day study calendar.
1418. **CI teaching technique cards** — Collect: "TPRS", "comprehensible input teaching" `within = "year"`. Do: extract classroom techniques. Build: technique cards for language teachers.
1419. **Caption reliability check** — Collect: target-language videos with and without `subtitles_only`. Do: compare auto-caption errors. Build: notes on which channels have trustworthy captions for study.

[↑ Contents](#contents)

### Academic research & science

1420. **Conference digest** — Collect: a conference channel via `channels`, `channel_within = "month"`. Do: per talk note problem, method, result, limits. Build: a skim-friendly digest of the whole conference.
1421. **Lit-review seed list** — Collect: "base editing talk" `min_duration = 1200`. Do: extract papers and authors speakers cite. Build: a reading list to locate in databases.
1422. **Lab trend memo** — Collect: "protein design", "LLM reasoning" `within = "week"`, daily schedule. Do: read `trends.html` for rising subtopics. Build: a monthly trend memo for the lab.
1423. **Methods tutorial index** — Collect: "mixed effects model tutorial R" `chapters`. Do: map each method step to tutorial timestamps. Build: a methods help index for grad students.
1424. **Consensus vs speculation** — Collect: explainers on "dark matter" `min_views = 50000`. Do: sort claims into presented-as-consensus vs speculation. Build: a claims table to verify against review papers.
1425. **Pre-writing fact-check list** — Collect: viral science videos via `rising_views_per_day`. Do: list factual claims and cited sources. Build: a verification list for a science journalist.
1426. **Department seminar KB** — Collect: a department seminar channel, all videos. Do: map->reduce a note per seminar. Build: knowledge/department.md of who works on what.
1427. **Grant open-problems section** — Collect: keynotes by field leaders. Do: list open problems they name. Build: a draft "open questions" paragraph citing each talk.
1428. **PhD topic scouting** — Collect: "open problems in" plus field `within = "year"`. Do: cluster problems by how often named. Build: a topic shortlist with public labs to contact.
1429. **Study appraisal checklist** — Collect: "replication crisis", "p-hacking explained". Do: extract criteria for judging studies. Build: a checklist for reading papers.
1430. **Outreach style guide** — Collect: top science channels via `channels`. Do: analyse how they convey uncertainty and scale. Build: a sci-comm style guide for a lab.
1431. **Lab talk lay summaries** — Collect: your lab's own talks. Do: write plain-language summaries. Build: lab blog posts and press-office blurbs.
1432. **Expert disagreement map** — Collect: panels on "is string theory testable" `min_duration = 3600`. Do: map positions by speaker. Build: a debate map with timestamps.
1433. **Lab software SOP** — Collect: "ImageJ tutorial", "Python for neuroscience". Do: extract steps and settings. Build: an onboarding SOP for the lab's pipeline.
1434. **Reading-group shortlist** — Collect: paper-explainer channels `within = "week"`. Do: summarise each paper discussed. Build: a weekly shortlist for the reading group.
1435. **Journal club guide** — Collect: the author's talk on the paper. Do: list key figures, assumptions and open questions. Build: a discussion guide for journal club.
1436. **Public misconception FAQ** — Collect: big explainers with `top_comments = 50`. Do: catalogue lay misconceptions in comments. Build: an outreach FAQ answering them.
1437. **Reference manager pick** — Collect: "Zotero vs Mendeley", "Obsidian for research". Do: compare features and workflows. Build: a comparison table for a research group.
1438. **Peer-review template** — Collect: "how to review a paper" talks by editors. Do: extract reviewer checklists. Build: a review template for early-career reviewers.
1439. **Paper-writing checklist** — Collect: "how to write a scientific paper" lectures. Do: merge advice by section. Build: a section-by-section writing checklist.
1440. **JWST findings timeline** — Collect: "JWST new findings" `within = "month"`. Do: summarise results reported. Build: a timeline of announcements with papers to check.
1441. **Climate briefing layers** — Collect: climate scientists' talks `min_duration = 1800`. Do: separate measured data, model projections and opinion. Build: a layered briefing for policy staff.
1442. **Talk-to-paper dataset** — Collect: hundreds of talks, `yt.py export`. Do: extract each cited paper. Build: a dataset of which research gets discussed on YouTube.
1443. **Workshop speaker scouting** — Collect: field talks with `max_views = 2000`. Do: find early-career researchers with clear talks. Build: a speaker shortlist for a workshop.
1444. **Stats explainer audit** — Collect: "p-value explained", "Bayesian vs frequentist". Do: spot errors and oversimplifications. Build: an annotated watch list for a stats course.
1445. **Cross-field term glossary** — Collect: talks on "entropy" from physics, info theory and ecology. Do: compare usage. Build: a translation glossary for interdisciplinary teams.
1446. **Hype tracker** — Collect: `title_must_contain = "breakthrough"` `within = "month"`. Do: compare video claims with what the cited study states. Build: a hype-vs-finding tracker.
1447. **Defense mock questions** — Collect: "PhD defense questions", recorded defenses. Do: classify question types. Build: a mock-defense question bank.
1448. **Dataset release index** — Collect: ML talks; `yt.py find "we release"`. Do: list datasets and benchmarks announced. Build: an index of new datasets with talk links.
1449. **Science fair mentor list** — Collect: "science fair project ideas" by grade. Do: rate feasibility and the method each needs. Build: an idea list with method sketches.
1450. **Citizen science directory** — Collect: "citizen science project" `within = "year"`. Do: extract project, skill level and how to join. Build: a directory for hobbyists.
1451. **Feynman lectures study guide** — Collect: a classic physics lecture series. Do: note each lecture's key derivations. Build: a study guide with timestamps.
1452. **Scientist position timeline** — Collect: a public scientist's talks with `published_after`. Do: track how stated claims changed. Build: a timeline of their public positions.
1453. **Reproducible search appendix** — Collect: keyword sets; keep `lists/` dated copies. Do: document queries, filters and dates. Build: a methods appendix for a study of YouTube science content.
1454. **Framing content analysis** — Collect: thousands of vaccine and climate videos with proxies, `yt.py export`. Do: code framing per video. Build: an annotated dataset for communication research.
1455. **Predictions ledger** — Collect: long scientist interviews `min_duration = 5400`, `chapters`. Do: extract dated predictions. Build: a ledger to check when the dates arrive.
1456. **Microscope buying table** — Collect: "microscope review", vendor webinars. Do: compare specs and stated pros/cons. Build: a purchase comparison for a lab manager.
1457. **Workshop recap memo** — Collect: workshop `channel_tabs = "streams"`, `timestamps`. Do: summarise each session. Build: a recap memo for absent lab members.
1458. **Weekly science newsletter** — Collect: science channels `within = "week"`, `sponsorblock`. Do: pick and summarise top stories. Build: a weekly newsletter with source links.
1459. **Proof outline sheets** — Collect: "proof explained" for key theorems. Do: extract proof steps and key ideas. Build: proof outlines for a maths student.
1460. **Science ethics viewing guide** — Collect: "gene drive ethics", "AI alignment debate". Do: map arguments. Build: a viewing guide for an ethics-of-science seminar.
1461. **Fieldwork checklist** — Collect: "ethnography fieldwork tips", "qualitative coding". Do: merge practical advice. Build: a fieldwork prep checklist.
1462. **Institute outreach plan** — Collect: your institute's channel `top_comments = 30`. Do: find what the public asks most. Build: a next-year outreach content plan.
1463. **Grant application checklist** — Collect: "ERC grant interview tips" `within = "year"`. Do: extract advice. Build: a checklist to verify against official funder guidance.
1464. **Benchmark claims table** — Collect: "new AI model benchmark" `within = "week"`. Do: compare claimed scores across videos. Build: a claims table with original sources to check.
1465. **Presentation phrase bank** — Collect: conference talks in English. Do: extract phrases for framing, transitions and Q&A. Build: a phrase bank for non-native presenters.
1466. **3MT talk template** — Collect: "three minute thesis winner". Do: analyse structure and hooks. Build: a template for your own 3MT.
1467. **Hypothesis generator skill** — Collect: talks into knowledge/<topic>.md. Do: map known results. Build: a Claude skill that proposes testable hypotheses citing talks.
1468. **Q&A critique mining** — Collect: talks with Q&A `min_duration = 2700`. Do: extract audience questions and answers. Build: a list of critiques raised against a method.
1469. **Non-English talk digest** — Collect: Chinese and Japanese talks with `translate = "en"`. Do: summarise. Build: a digest of research presented outside English.
1470. **Observing calendar** — Collect: "meteor shower 2026", "eclipse" `within = "month"`. Do: extract dates and viewing tips. Build: an amateur astronomy calendar.
1471. **Nutrition claims audit** — Collect: "seed oils study" `top_comments = 20`. Do: list studies cited and opinions held. Build: papers to read and questions for a dietitian.
1472. **Correction timeline** — Collect: a viral claim keyword across `published_after` months. Do: see if later videos corrected it. Build: a correction timeline.
1473. **Exhibit label drafts** — Collect: explainers on a museum exhibit topic. Do: extract strongest analogies. Build: exhibit labels in original wording.
1474. **Lab-wide talk search** — Collect: all talks the lab follows into one `library.html`. Do: `yt.py find` across them. Build: a shared searchable archive.

[↑ Contents](#contents)

### History, philosophy, religion & the humanities

1475. **History course study guide** — Collect: an open university history playlist via `channels`. Do: note each lecture. Build: a study guide with a running timeline.
1476. **Event timeline CSV** — Collect: "French Revolution documentary" `min_duration = 1800`. Do: extract dated events. Build: a sortable timeline with source links.
1477. **Historiography table** — Collect: "causes of WWI" by several historians. Do: compare which causes each stresses. Build: a historiography comparison table.
1478. **Free-will argument tree** — Collect: "free will debate" `min_duration = 3600`. Do: map arguments and objections. Build: an argument tree diagram.
1479. **Interfaith comparison** — Collect: adherents of several faiths on "what happens after death". Do: summarise each view in its own terms. Build: a respectful comparison table.
1480. **Sermon discussion guide** — Collect: a church's own `channel_tabs = "streams"`. Do: summarise each sermon and scripture cited. Build: small-group discussion guides.
1481. **Artwork ID flashcards** — Collect: "Baroque art explained" from art-history channels. Do: list artworks and key features. Build: flashcards for an art-history exam.
1482. **Novel study guide** — Collect: "Moby Dick lecture analysis". Do: extract themes, symbols and interpretations. Build: a study guide that supports reading.
1483. **Primary source leads** — Collect: history channels' long videos. Do: list primary sources they quote. Build: a list to find in archives.
1484. **History myth sheet** — Collect: "history myths debunked" `top_comments = 20`. Do: list myths and sources cited. Build: a myth-vs-evidence classroom sheet.
1485. **Kant reading companion** — Collect: "Critique of Pure Reason lecture". Do: map lecture parts to book sections. Build: a chapter-by-chapter companion.
1486. **Ethics case packet** — Collect: "trolley problem", "ethics of AI" debates. Do: extract cases and positions. Build: a case-study packet for an ethics class.
1487. **Local heritage summary** — Collect: local history channels `max_views = 5000`. Do: extract places and dates. Build: a heritage summary for a historical society.
1488. **Genealogy workflow** — Collect: "how to search census records", genealogy tutorials. Do: extract steps per record type. Build: a family-research workflow.
1489. **Documentary framing worksheet** — Collect: documentaries on one contested event. Do: compare framing and omissions. Build: a media-literacy worksheet.
1490. **Iliad reading schedule** — Collect: "Iliad lectures". Do: pair lectures with books of the poem. Build: a 6-week reading schedule.
1491. **Book of Job across traditions** — Collect: scholars from Jewish and Christian traditions on Job. Do: compare readings. Build: study notes.
1492. **Philosophy for kids prompts** — Collect: "philosophy for children" videos. Do: extract questions. Build: discussion prompts for primary classes.
1493. **Essay prompt bank** — Collect: a history lecture series. Do: find debatable claims. Build: essay prompts for teachers.
1494. **Debate club drills** — Collect: famous public debates `min_duration = 3600`. Do: extract argument moves and rebuttals. Build: practice drills.
1495. **Museum visit guide** — Collect: "British Museum highlights". Do: extract objects and stories. Build: a visit route guide.
1496. **On-this-day calendar** — Collect: history channels `within = "week"`. Do: tag anniversaries mentioned. Build: weekly social posts for a history page.
1497. **Theology knowledge base** — Collect: a seminary's lecture channel. Do: map->reduce notes. Build: knowledge/theology.md searchable by doctrine.
1498. **Architecture glossary** — Collect: "Gothic cathedral architecture explained". Do: extract terms. Build: an illustrated-term glossary list.
1499. **BookTube canon list** — Collect: "classics recommendations" `top_comments = 30`. Do: rank books by mention count. Build: a reading list.
1500. **Pop-Stoicism check** — Collect: "stoicism" `within = "month"`. Do: compare popular claims with scholars' lectures. Build: a report on where they diverge.
1501. **Battle accounts compared** — Collect: "Battle of Cannae analysis". Do: compare numbers and tactics given. Build: a summary with disagreements flagged.
1502. **Foreign-language history** — Collect: Spanish history documentaries with `translate = "en"`. Do: summarise. Build: English notes on Spanish-language scholarship.
1503. **Socratic dialogue skill** — Collect: lectures on Plato. Do: map elenchus moves. Build: a Claude skill that runs a Socratic dialogue.
1504. **Jazz listening guide** — Collect: "history of jazz lecture". Do: extract eras and recordings named. Build: a listening guide.
1505. **Film class notes** — Collect: video essays on Kubrick. Do: extract themes and techniques. Build: film-studies notes.
1506. **Etymology cards** — Collect: etymology channels. Do: extract word origins. Build: word-origin flashcards.
1507. **Archaeology digest** — Collect: "archaeology discovery" `within = "week"`. Do: summarise finds. Build: a monthly digest with sources to verify.
1508. **Pseudo-history lesson** — Collect: "ancient aliens" and archaeologists' replies. Do: compare claims and evidence. Build: a critical-thinking lesson.
1509. **Testimony thematic index** — Collect: public veteran interviews from archive channels. Do: tag themes. Build: a thematic index with timestamps.
1510. **Science-religion debate map** — Collect: "science and religion debate". Do: map positions. Build: a debate map.
1511. **Philosophy glossary** — Collect: intro philosophy lectures. Do: extract terms and definitions. Build: a glossary for first-years.
1512. **Homeschool history cycle** — Collect: history channels `max_duration = 1200`. Do: sort by era. Build: a four-year chronological homeschool rotation.
1513. **Quote verifier** — Collect: "misattributed quotes". Do: list sourced vs unsourced quotes. Build: a quote-check list.
1514. **Aristotle on friendship essay** — Collect: lectures on Nicomachean Ethics. Do: link ideas to online friendship. Build: an essay outline.
1515. **Inclusive holiday notes** — Collect: practitioners explaining Diwali and Ramadan. Do: summarise customs. Build: school calendar notes.
1516. **Flood myth comparison** — Collect: "flood myths compared". Do: tabulate shared motifs. Build: a comparative-mythology table.
1517. **Justice seminar plan** — Collect: Michael Sandel "Justice" lectures. Do: extract cases. Build: a weekly seminar plan.
1518. **Poetry annotation guide** — Collect: "poem analysis" `max_duration = 900`. Do: extract devices discussed, no full poems. Build: an annotation guide.
1519. **Documentary watchlist** — Collect: history docs `min_views = 100000`, `min_duration = 2700`. Do: rate depth and sourcing. Build: a ranked watchlist.
1520. **Coverage-by-era dataset** — Collect: history channels, `yt.py export`. Do: tag era per video. Build: a chart of which eras YouTube covers.
1521. **Contemplative traditions table** — Collect: teachers from Zen, Christian and Sufi traditions. Do: compare practices. Build: a comparison table.
1522. **Holocaust lesson plan** — Collect: survivor testimonies from museum channels. Do: extract themes. Build: an age-appropriate lesson plan.
1523. **Propaganda analysis kit** — Collect: documentaries on WWII propaganda. Do: list techniques. Build: a media-literacy analysis kit.
1524. **Pop philosophy accuracy** — Collect: popular channels vs academic lectures on Nietzsche. Do: compare accuracy. Build: accuracy notes.
1525. **Daily reflection prompt** — Collect: philosophy Shorts `include_shorts = true`. Do: extract one idea each. Build: daily journaling prompts.
1526. **Walking tour script** — Collect: city history documentaries. Do: extract site stories. Build: a tour script in original words.
1527. **Civics study guide** — Collect: "Federalist Papers explained". Do: summarise each paper. Build: a civics guide.

[↑ Contents](#contents)

## Health, food, family and personal growth

### Health, fitness & wellbeing

1528. **Beginner strength program map** — Collect: "beginner strength program", "full body workout beginners", `within = "year"`, `min_duration = 600`. Do: tabulate sets, reps, frequency, progression per creator. Build: comparison table to review with a trainer.
1529. **Mobility drill index** — Collect: "hip mobility routine", "shoulder mobility", `timestamps = true`. Do: extract each drill name, cue and target area with the second it is demonstrated. Build: searchable drill index linking to the exact moment.
1530. **Sleep advice opinion map** — Collect: "sleep hygiene tips", "how to sleep better", sleep-researcher channels. Do: group claims (light, caffeine timing, temperature), mark which cite studies. Build: opinion map plus questions for a doctor.
1531. **Physician-channel claim log** — Collect: channels of doctor-run creators, `channel_within = "month"`. Do: list each health claim, whether a source is cited, and the speaker's stated certainty. Build: spreadsheet of claims to verify with a professional.
1532. **First 5K plan decoder** — Collect: "couch to 5k", "first 5k training plan". Do: compare weekly structure, run/walk ratios and rest days across plans. Build: side-by-side plan table and a question list for a running coach.
1533. **Marathon taper approaches** — Collect: "marathon taper", `top_comments = 20`, `within = "year"`. Do: compare taper length and volume cuts suggested; mine comments for runners' reported experiences. Build: one-page map of taper approaches.
1534. **Home gym buying guide** — Collect: "home gym setup", "adjustable dumbbells review", `sponsorblock`. Do: list products named, pros, cons, price ranges, space needs. Build: home-gym comparison spreadsheet.
1535. **PT exercise glossary** — Collect: channels of licensed physical therapists, `chapters = true`. Do: extract exercise names, body area and how they are described. Build: flashcard glossary to understand terms before an appointment.
1536. **Fitness myth checker** — Collect: "fitness myths", "spot reduction", "muscle confusion". Do: list each myth, the counter-argument and any study named. Build: myth-vs-evidence table with items still to verify.
1537. **Trainer client handouts** — Collect: "progressive overload explained", "RPE explained". Do: summarise the clearest plain-language explanations and analogies. Build: client handout series that cites the source videos.
1538. **Yoga sequence library** — Collect: "yoga flow for beginners", `min_duration = 1200`. Do: extract pose order, transitions and stated modifications per class. Build: teacher's sequence library sorted by length and level.
1539. **Pilates cue bank** — Collect: "pilates instructor cues", "pilates teacher training". Do: collect verbal cues per exercise and group by intent (alignment, breath, tempo). Build: printable instructor cue cards.
1540. **Wearable metrics explainer** — Collect: "HRV explained", "oura ring review", "whoop review". Do: compare how creators interpret HRV, readiness and sleep scores and what caveats they give. Build: plain explainer of what the numbers mean and don't.
1541. **Daily wellness fad radar** — Collect: "wellness trend", `within = "today"`, `rising_views_per_day = 2000`, `schedule_daily.bat`. Do: flag new fads gaining fast and note claims made. Build: daily brief of rising trends with skeptic notes.
1542. **Supplement claims map** — Collect: "supplement review", doctor and pharmacist channels. Do: list claimed benefits and evidence mentioned; omit all doses. Build: claims map and a question list to bring to a pharmacist or doctor.
1543. **Stretching debate summary** — Collect: "static stretching before running", "do you need to stretch". Do: summarise positions for and against with any research cited. Build: balanced one-page summary for a club newsletter.
1544. **Office ergonomics SOP** — Collect: "desk posture exercises", "ergonomic desk setup". Do: extract setup tips and micro-break routines creators agree on. Build: HR-ready office ergonomics SOP draft.
1545. **Staff wellbeing newsletter** — Collect: "workplace wellbeing", "stress at work", `within = "week"`. Do: pick three practical ideas per week that cite a source. Build: weekly internal newsletter with links to the videos.
1546. **Balance exercises for seniors** — Collect: "balance exercises for seniors", physiotherapist channels. Do: catalogue exercises and every safety note stated. Build: large-print sheet to review with a doctor before starting.
1547. **Postnatal fitness question list** — Collect: "postpartum exercise", pelvic-floor physio channels. Do: map suggested timelines and the signs they say need a professional. Build: question list for a postnatal check-up.
1548. **Climbing warm-up poster** — Collect: "climbing finger injury prevention", "hangboard warm up". Do: compile warm-up protocols and warning signs creators mention. Build: climbing gym warm-up poster draft.
1549. **Youth soccer drill bank** — Collect: "soccer conditioning drills kids", coach channels, `timestamps = true`. Do: extract drills with duration, equipment and age group. Build: season practice-plan bank for a volunteer coach.
1550. **Cycling zones cheat sheet** — Collect: "zone 2 training", "FTP test explained". Do: compare how each creator defines zones and tests; flag differences. Build: zones cheat sheet with disagreements marked.
1551. **Swim drill cards** — Collect: "freestyle technique drills", "swim drills", `timestamps = true`. Do: list each drill with its key cue and common fault. Build: waterproof lane-side card set.
1552. **Meditation style chooser** — Collect: "how to meditate", "body scan meditation", "loving kindness". Do: classify techniques by instructions, duration and goal. Build: beginner decision tree for picking a style.
1553. **Breathwork cautions map** — Collect: "breathwork for beginners", "box breathing". Do: extract techniques and every caution or contraindication creators mention. Build: map of methods with cautions to discuss with a professional.
1554. **Therapy modality explainer** — Collect: channels of licensed therapists, "CBT explained", "DBT explained". Do: summarise how each modality is described and when they say to seek help. Build: glossary to help someone choose questions for a therapist.
1555. **Health misinformation dataset** — Collect: "detox cleanse", "cure naturally", `include_description = true`. Do: code each claim by type, citation presence and product links. Build: `yt.py export` dataset for a research paper.
1556. **Affiliate disclosure audit** — Collect: top fitness channels, `include_description = true`, `channel_max_videos = 50`. Do: count affiliate links and brand mentions per video. Build: disclosure audit spreadsheet for a media-literacy study.
1557. **Group class format scouting** — Collect: "new group fitness class", "HIIT class ideas", `within = "month"`. Do: list formats, timings and equipment trending among instructors. Build: proposed new timetable for a gym owner.
1558. **Fitness app gap finder** — Collect: "fitness app review", `top_comments = 50`. Do: extract user complaints and wished-for features by app. Build: feature-gap list for a startup roadmap.
1559. **Recovery modalities table** — Collect: "cold plunge benefits", "sauna benefits", "compression boots". Do: map claims, cited studies and contradictions. Build: evidence-strength table marked "verify before trusting".
1560. **Thru-hike prep plan** — Collect: "thru hike training", "hiking training plan". Do: extract training progressions and pack-weight advice. Build: 12-week preparation checklist.
1561. **Calisthenics skill tree** — Collect: "muscle up progression", "handstand progression". Do: order the progression steps each creator teaches and merge them. Build: skill-tree diagram with video links per step.
1562. **Kettlebell form checklist** — Collect: "kettlebell swing mistakes", "kettlebell form". Do: list common errors and the fix each coach gives. Build: form-check checklist for coaches.
1563. **Credentialed small creators** — Collect: "physiotherapist explains", `max_views = 5000`, `include_description = true`. Do: find channels whose descriptions state credentials. Build: curated list of qualified, under-noticed creators.
1564. **Cross-country training cultures** — Collect: "entrenamiento de fuerza", "Krafttraining", `languages`, `translate`. Do: compare popular training styles and advice by country. Build: comparison briefing for a fitness journalist.
1565. **Health podcast knowledge base** — Collect: long-form health podcast channels, `min_duration = 3600`, `remove_filler_words`. Do: map -> reduce notes per episode. Build: `knowledge/<topic>.md` with timestamped sources.
1566. **Appointment prep questions** — Collect: "questions to ask your doctor", "what to ask at a checkup". Do: compile the questions creators recommend, grouped by visit type. Build: personal printable question list.
1567. **Pain science support deck** — Collect: "pain science explained", pain-researcher channels. Do: summarise concepts as described with the analogies used. Build: slide outline for a patient support group, reviewed by a clinician.
1568. **Teen strength training FAQ** — Collect: "youth strength training safety", coach and paediatric channels. Do: map age guidance and supervision points. Build: parent FAQ sheet to discuss with a paediatrician.
1569. **Warm-up generator skill** — Collect: "dynamic warm up", "warm up for sprinting", "warm up for lifting". Do: extract drills tagged by sport and time. Build: Claude skill that assembles a warm-up from sport and minutes available.
1570. **Trusted-channel Q&A bot** — Collect: a hand-picked set of credentialed channels, all videos. Do: `yt.py export` to .jsonl and embed. Build: RAG bot that answers with cited timestamps and a "check with a professional" note.
1571. **Step target myth check** — Collect: "10000 steps myth", "walking for health". Do: compare stated step targets and studies cited. Build: short myth-check article with sources.
1572. **Heat training safety list** — Collect: "running in heat", "heat acclimation". Do: extract precautions and warning signs mentioned. Build: summer safety checklist for a running club.
1573. **Busy-parent micro-workouts** — Collect: "10 minute workout no equipment", `max_duration = 900`. Do: extract routines with equipment and space needed. Build: weekly micro-workout calendar.
1574. **Exercise physiology lesson** — Collect: "VO2 max explained", "lactate threshold explained". Do: pick the clearest analogies and diagrams described. Build: lesson plan with clip timestamps for a PE teacher.
1575. **Fitness concept lifecycle** — Collect: "zone 2", "hybrid training", "Japanese walking", daily for months. Do: read `trends.html` to see which concepts rise and fade. Build: quarterly trend report for a fitness brand.
1576. **Program user-results dossier** — Collect: a popular program's channel, `top_comments = 100`. Do: summarise reported results, complaints and drop-off reasons. Build: pros/cons dossier from real users' comments.
1577. **Shift worker sleep guide** — Collect: "night shift sleep tips", "shift work sleep". Do: extract strategies and cautions creators give. Build: break-room guide for a nursing team plus questions for occupational health.
1578. **Screen eye-strain poster** — Collect: "eye strain computer", optometrist channels. Do: list suggestions like breaks and lighting, noting who says what. Build: workplace poster draft.
1579. **Tai chi class outline** — Collect: "tai chi for beginners", "qigong for seniors", `chapters = true`. Do: sequence forms and teaching cues. Build: 8-week community-centre class outline.
1580. **Gym anxiety onboarding** — Collect: "gym anxiety tips", "first time at the gym", `top_comments = 30`. Do: collect practical tips and beginners' worries. Build: first-week onboarding guide for a gym's new members.
1581. **Longevity figures' positions** — Collect: channels and interviews of public longevity researchers, `channel_within = "any"`. Do: track how their public statements change over time. Build: dated timeline of positions with links.
1582. **Cycle-syncing claims map** — Collect: "cycle syncing workouts", "menstrual cycle training". Do: map claims and how creators describe evidence quality. Build: balanced explainer with questions for a GP.

[↑ Contents](#contents)

### Food, cooking & drink

1583. **Knife skills drill sheet** — Collect: "knife skills basics", "how to dice an onion", `timestamps = true`. Do: list each cut with grip and safety cues. Build: practice drill sheet with links to the exact demo second.
1584. **Sourdough fault tree** — Collect: "sourdough troubleshooting", "dense sourdough", `top_comments = 30`. Do: map symptom -> likely cause -> suggested fix. Build: troubleshooting decision tree for home bakers.
1585. **Regional cuisine dossier** — Collect: "mole oaxaqueño", "cocina oaxaqueña", `languages = ["es"]`, `translate`. Do: summarise ingredients, techniques and regional variations. Build: cuisine dossier for a chef planning a menu.
1586. **Four-week meal prep plan** — Collect: "meal prep for the week", `within = "month"`. Do: extract recipes with prep time, storage life and reheating notes. Build: 4-week prep calendar with shopping lists.
1587. **Restaurant pre-opening checklist** — Collect: "opening a restaurant mistakes", restaurateur channels. Do: extract lessons and costly mistakes by stage. Build: pre-opening checklist ordered by timeline.
1588. **Food truck cost model** — Collect: "food truck startup costs", "food truck business". Do: extract every cost item and range mentioned. Build: cost spreadsheet template to fill with local quotes.
1589. **Brew recipe database** — Collect: "V60 recipe", "aeropress recipe", "chemex recipe". Do: extract dose, water, temperature, grind and time per recipe. Build: CSV of brew recipes sortable by method.
1590. **Espresso dial-in flowchart** — Collect: "dialing in espresso", "sour espresso fix". Do: map taste problems to adjustments creators recommend. Build: dial-in flowchart for a café bar.
1591. **Cocktail spec book** — Collect: bartender channels, "classic cocktail recipe". Do: extract specs, ratios, glassware and garnish; note variations by bartender. Build: house spec book.
1592. **Non-alcoholic menu draft** — Collect: "mocktail recipes", "non alcoholic cocktails", `within = "year"`. Do: shortlist drinks by prep effort and ingredient overlap. Build: NA drinks menu draft for a café.
1593. **Wine vocabulary flashcards** — Collect: sommelier channels, "wine tasting for beginners". Do: extract tasting terms with how they are explained. Build: flashcard deck for a beginner wine course.
1594. **Baking science FAQ** — Collect: "why cookies spread", "baking soda vs baking powder". Do: summarise cause-and-effect explanations. Build: FAQ handout for a baking class.
1595. **Lamination method table** — Collect: "croissant lamination", "puff pastry folds". Do: compare butter temperature, fold count and rest times. Build: method comparison table for a pastry student.
1596. **Kitchen food safety SOP** — Collect: "food safety for restaurants", "cooling food safely". Do: extract practices mentioned; mark each to check against local regulations. Build: kitchen SOP draft for review by an inspector.
1597. **Fermentation log** — Collect: "lacto fermentation", "fermenting vegetables". Do: extract salt ratios, temperatures and the safety signs creators describe. Build: fermentation log template with checkpoints.
1598. **Weekly viral recipe digest** — Collect: "viral recipe", `within = "week"`, `rising_views_per_day = 5000`. Do: list recipes gaining fast and the hook behind each. Build: weekly trend digest for a food blogger.
1599. **Grocery buy/skip list** — Collect: "trader joe's haul", "aldi finds", `top_comments = 20`. Do: tally products praised and panned by creators and commenters. Build: buy/skip shopping list.
1600. **Student budget cookbook outline** — Collect: "cheap meals for students", "budget meals". Do: extract dishes with cost, equipment and time. Build: outline for an original student cookbook, crediting inspirations.
1601. **Cookware comparison** — Collect: "best chef knife", "dutch oven review", `sponsorblock`. Do: list products, test methods and verdicts per reviewer. Build: cookware comparison spreadsheet.
1602. **Brisket cook-day timeline** — Collect: pitmaster channels, "brisket smoking". Do: compare pit temperature, wrap timing and rest. Build: hour-by-hour cook-day timeline.
1603. **City restaurant shortlist** — Collect: "best ramen Tokyo", "where to eat Tokyo", `within = "year"`. Do: list places mentioned, dishes ordered and neighbourhoods. Build: shortlist grouped by area for a trip.
1604. **Street food dish wishlist** — Collect: "Bangkok street food", `translate`, `languages = ["th"]`. Do: extract dish names, descriptions and where they were filmed. Build: dish wishlist with local names.
1605. **Menu engineering worksheet** — Collect: "menu engineering", "menu pricing restaurant". Do: summarise methods like star/plowhorse classification. Build: menu pricing worksheet for an owner.
1606. **Teen cooking course** — Collect: "cooking basics for beginners", "cooking for teens". Do: order skills from simplest to hardest. Build: 8-week school cooking course with clip timestamps.
1607. **Allergy substitution chart** — Collect: "egg substitute baking", "gluten free flour blend". Do: list swaps, ratios and stated results. Build: substitution chart, labelled to double-check for serious allergies.
1608. **Plant-based swap table** — Collect: "vegan protein recipes", "plant based swaps". Do: map common dishes to plant-based versions creators use. Build: swap table for a canteen menu.
1609. **Spice blend comparison** — Collect: "garam masala recipe", "ras el hanout recipe". Do: compare spice ratios across creators. Build: blend comparison chart with common core.
1610. **Food photo shot list** — Collect: "food photography lighting", "food styling tips". Do: extract setups, angles and props. Build: reusable shot list template.
1611. **Cookbook gap research** — Collect: "air fryer recipes", `top_comments = 50`. Do: find questions viewers ask that videos don't answer. Build: chapter outline gaps for a cookbook author.
1612. **Food cost calculator** — Collect: "restaurant food cost", "recipe costing". Do: extract formulas and target percentages mentioned. Build: food cost and yield spreadsheet.
1613. **Cottage bakery launch list** — Collect: "cottage food business", "home bakery business". Do: extract steps, permits and pricing tips; mark legal items to verify locally. Build: launch checklist.
1614. **Café open/close checklist** — Collect: "coffee shop owner day in the life", "cafe opening routine". Do: extract tasks by shift. Build: opening and closing checklists.
1615. **Latte art training module** — Collect: "latte art tutorial", `timestamps = true`. Do: order patterns by difficulty with key pour cues. Build: barista training module with clip links.
1616. **Gongfu tea card** — Collect: "gongfu tea brewing", "oolong brewing". Do: extract leaf ratio, temperature and steep times by tea type. Build: brewing parameter card.
1617. **Brew day checklist** — Collect: "all grain brewing", "homebrew mistakes". Do: list steps and common errors. Build: home beer brew day checklist.
1618. **Kids kitchen tasks by age** — Collect: "cooking with kids", "toddler cooking". Do: extract tasks suggested per age. Build: age-appropriate kitchen task list.
1619. **Canteen waste reduction** — Collect: "reduce food waste kitchen", "restaurant food waste". Do: list tactics and reported savings. Build: zero-waste guide for a workplace canteen.
1620. **Chef philosophy knowledge base** — Collect: chef interview podcast channels, `min_duration = 2400`. Do: map -> reduce notes on each chef's principles. Build: `knowledge/chefs.md` with timestamped quotes.
1621. **Japanese technique notes** — Collect: "出汁 取り方", "和食 基本", `translate`. Do: summarise techniques from Japanese-language creators. Build: English technique notes with links.
1622. **Pasta pairing matrix** — Collect: "fresh pasta shapes", "pasta sauce pairing". Do: extract which shape suits which sauce and why. Build: shape-by-sauce pairing matrix.
1623. **Sous vide time-temp chart** — Collect: "sous vide steak temperature", "sous vide chicken". Do: compile times and temperatures; flag where food-safety guidance should be checked. Build: chart with sources.
1624. **Holiday dinner schedule** — Collect: "thanksgiving dinner timeline", `within = "month"`. Do: extract make-ahead steps and oven sequencing. Build: day-of cooking schedule.
1625. **Catering scale-up guide** — Collect: "cooking for 100 people", "catering tips". Do: extract quantity rules and logistics advice. Build: scaling guide for an event caterer.
1626. **Pantry recipe bot** — Collect: favourite cooking channels, all videos. Do: `yt.py export` and embed transcripts. Build: bot that suggests dishes from what's in your fridge, linking to the source video.
1627. **Food channel content gaps** — Collect: "one pot dinner", `max_views = 10000`. Do: compare views per day against coverage. Build: content gap list for a new food creator.
1628. **Miso buyer's guide** — Collect: "types of miso", "how to use miso". Do: extract types, flavour notes and uses. Build: ingredient buyer's guide.
1629. **Ghost kitchen briefing** — Collect: "ghost kitchen", "delivery app fees restaurant". Do: summarise owners' reported economics and pitfalls. Build: pros/cons briefing for a restaurant group.
1630. **Front-of-house manual** — Collect: "server training tips", "front of house training". Do: extract service steps and recovery scripts. Build: FOH training manual.
1631. **Commenter recipe tweaks** — Collect: popular recipe videos, `top_comments = 50`. Do: extract tweaks commenters say improved the result. Build: annotated recipe with tweaks to test.
1632. **Beginner cheese making** — Collect: "beginner cheese making", "mozzarella at home". Do: list steps, equipment and failure points. Build: step checklist.
1633. **Mise en place template** — Collect: "mise en place", "line cook prep". Do: extract prep organisation methods. Build: prep list template for a small kitchen.
1634. **Chocolate tempering methods** — Collect: "tempering chocolate", "seed method". Do: compare methods and temperatures. Build: method comparison card.
1635. **Food myth table** — Collect: "is MSG bad", "searing seals in juices". Do: list myths, counter-arguments and tests creators ran. Build: myth vs evidence table.
1636. **Home roasting log** — Collect: "home coffee roasting", "first crack". Do: extract roast stages and timing cues. Build: roast log spreadsheet.
1637. **Restaurant trade daily brief** — Collect: "restaurant industry news", `within = "today"`, `schedule_daily.bat`. Do: summarise new stories and opinions. Build: daily briefing for a trade newsletter.

[↑ Contents](#contents)

### Parenting, family & relationships

1638. **Toddler sleep approaches** — Collect: "toddler sleep regression", paediatric channels. Do: compare approaches and stated pros and cons. Build: comparison sheet plus questions for a paediatrician.
1639. **Milestones timeline** — Collect: "baby milestones by month", paediatrician channels. Do: extract milestones and the points they say to ask a doctor. Build: month-by-month timeline, framed as general information.
1640. **School type comparison** — Collect: "montessori vs traditional school", "waldorf school". Do: compare philosophy, day structure and critiques. Build: comparison table for parents choosing schools.
1641. **Homeschool curriculum sheet** — Collect: "homeschool curriculum review", `top_comments = 20`. Do: extract cost, grade range and reported pros and cons. Build: curriculum comparison spreadsheet.
1642. **Family media plan** — Collect: "screen time for kids", "family media plan". Do: summarise positions and practical rules suggested. Build: family media plan draft to adapt.
1643. **Tantrum calm-down cards** — Collect: "toddler tantrums what to do", child psychologist channels. Do: extract phrases and steps recommended. Build: calm-down script cards for the fridge.
1644. **Teen conversation starters** — Collect: "how to talk to teenagers", "teen communication". Do: extract question styles that creators say work. Build: conversation-starter deck.
1645. **Potty training methods** — Collect: "potty training methods", "3 day potty training". Do: compare readiness signs and steps. Build: method comparison chart.
1646. **Low-pressure mealtimes** — Collect: "picky eater toddler", feeding therapist channels. Do: extract low-pressure strategies; avoid any restriction advice. Build: mealtime ideas list plus questions for a paediatrician.
1647. **Chore system by age** — Collect: "chore chart by age", "family command center". Do: list chores suggested per age and reward systems. Build: printable chore chart system.
1648. **New parent checklist** — Collect: "what I wish I knew before baby", `top_comments = 50`. Do: extract recurring lessons from creators and commenters. Build: new-parent prep checklist.
1649. **Baby gear comparison** — Collect: "best stroller", "car seat review", `sponsorblock`. Do: tabulate features and verdicts; mark safety ratings to verify officially. Build: gear comparison sheet.
1650. **Couples weekly check-in** — Collect: couples therapist channels, "relationship check in". Do: extract question sets and formats. Build: weekly check-in template.
1651. **Co-parenting handover kit** — Collect: "co-parenting tips", "co-parenting communication". Do: extract communication rules and handover practices. Build: handover checklist and message templates; legal questions for a lawyer.
1652. **Bilingual family plan** — Collect: "raising bilingual children", "one parent one language". Do: compare strategies and reported outcomes. Build: family language plan.
1653. **Parent evening workshop** — Collect: "growth mindset for kids", "praise effort". Do: summarise key ideas and activities. Build: slide outline for a teacher-led parent evening.
1654. **Early reading routine** — Collect: "teach child to read phonics", "reading with toddlers". Do: order the steps creators recommend. Build: 15-minute daily reading routine.
1655. **ADHD parenting strategy map** — Collect: clinician channels, "ADHD parenting strategies". Do: map strategies described, no diagnosis. Build: strategy map plus questions for a specialist.
1656. **Sibling rivalry scripts** — Collect: "sibling rivalry", "kids fighting what to do". Do: extract mediation steps and phrases. Build: parent script sheet.
1657. **Allowance system** — Collect: "teaching kids about money", "kids allowance". Do: compare allowance models by age. Build: allowance and savings system by age.
1658. **Toddler travel packing list** — Collect: "traveling with toddlers", "flying with a baby", `top_comments = 30`. Do: extract tips and must-pack items. Build: packing list and travel-day plan.
1659. **Aging parent care plan** — Collect: "caring for aging parents", "sandwich generation". Do: extract tasks, conversations and services mentioned. Build: family care-coordination checklist.
1660. **Explaining death to kids** — Collect: "explaining death to a child", child grief specialist channels. Do: extract age-appropriate language. Build: age-by-age language guide.
1661. **Foster care question list** — Collect: "foster parent training", "becoming a foster parent". Do: extract what creators wish they had asked. Build: question list for a fostering agency.
1662. **Daycare tour checklist** — Collect: "questions to ask daycare", "choosing childcare". Do: compile questions and red flags mentioned. Build: daycare tour checklist.
1663. **Family tech agreement** — Collect: "teens social media talk", "family tech rules". Do: extract rules and how parents negotiated them. Build: family tech agreement template.
1664. **PTA weekly newsletter** — Collect: "parenting tips", `within = "week"`, `min_views = 20000`. Do: pick three practical, sourced ideas. Build: weekly PTA newsletter with links.
1665. **Wedding planning timeline** — Collect: "wedding planning timeline", "wedding planning mistakes". Do: extract tasks by months-out. Build: wedding planning timeline.
1666. **First date advice map** — Collect: "first date tips", "dating advice", `top_comments = 30`. Do: map common advice and where creators disagree. Build: respectful opinion map.
1667. **Adult friendship plan** — Collect: "how to make friends as an adult". Do: extract concrete tactics and reported results. Build: 8-week friendship action plan.
1668. **Kids party planner** — Collect: "kids birthday party ideas", "party on a budget". Do: extract themes, games and timings. Build: party plan template.
1669. **Rainy day activity jar** — Collect: "rainy day activities for kids", "indoor activities toddlers". Do: list activities with materials and age. Build: activity jar cards.
1670. **Homework routine** — Collect: "how to help kids with homework", teacher channels. Do: extract routines and what not to do. Build: homework routine for the family.
1671. **College application timeline** — Collect: admissions officer channels, "college application tips". Do: extract tasks by grade and month. Build: parent timeline for applications.
1672. **Nanny house manual** — Collect: "nanny tips", "nanny share". Do: extract what nannies say families should document. Build: house manual template.
1673. **Parenting styles debate** — Collect: "gentle parenting criticism", "authoritative parenting". Do: summarise each side's arguments. Build: balanced map of styles.
1674. **Parenting content study** — Collect: "parenting tips", `within = "year"`, `yt.py export`. Do: code advice by topic and evidence cited, not children. Build: dataset for a research project.
1675. **Lactation question list** — Collect: lactation consultant channels, "breastfeeding tips". Do: extract common issues and when they say to get help. Build: question list for a lactation consultant.
1676. **Family meeting agenda** — Collect: "family meeting ideas", "family meetings with kids". Do: extract formats and roles. Build: family meeting agenda template.
1677. **Moving with kids plan** — Collect: "moving with kids", "new school transition". Do: extract transition tips by age. Build: moving transition plan.
1678. **Long-distance parent connection** — Collect: "long distance parenting", "deployed parent kids". Do: extract connection rituals. Build: list of ideas by age.
1679. **Grandparent boundaries guide** — Collect: "grandparents boundaries", "in-laws boundaries". Do: extract phrasing and approaches. Build: respectful conversation guide.
1680. **Teen driving practice log** — Collect: "teaching teen to drive", driving instructor channels. Do: order skills by stage. Build: practice log and skill checklist.
1681. **Summer learning plan** — Collect: "summer learning loss", "summer activities learning". Do: extract activities by age and subject. Build: summer learning plan.
1682. **Pregnancy appointment questions** — Collect: OB and midwife channels, "first trimester what to know". Do: compile suggested questions. Build: question list for a midwife visit.
1683. **Body safety talks by age** — Collect: "body safety for kids", child protection educator channels. Do: extract age-appropriate wording. Build: age guide for protective conversations.
1684. **Parenting book shortlist** — Collect: author interview videos, "parenting book author interview". Do: summarise each book's core ideas as told by the author. Build: reading shortlist.
1685. **Family budget sheet** — Collect: "family budget", "budget with kids". Do: extract categories and methods. Build: family budget spreadsheet.
1686. **Fair fight rules card** — Collect: "repair attempts relationship", "fighting fair couples". Do: extract rules couples therapists recommend. Build: fridge card of fair-fight rules.
1687. **IEP meeting prep binder** — Collect: "IEP meeting tips", special education advocate channels. Do: extract documents and questions to prepare; flag rights to verify locally. Build: meeting prep binder.
1688. **Home daycare business plan** — Collect: "starting a home daycare", "in home daycare". Do: extract costs, licensing steps and pitfalls. Build: business plan checklist.
1689. **Parenting course outline** — Collect: "parenting coach", `top_comments = 50`. Do: cluster the questions parents ask most. Build: FAQ-driven course outline for a parenting coach.
1690. **Teen mental health signs** — Collect: adolescent psychiatrist channels, "teen mental health signs". Do: list signs they mention and when to seek help. Build: parent guide with crisis resource links.
1691. **Blended family guide** — Collect: "stepparenting tips", "blended family". Do: extract common challenges and approaches. Build: blended family guide.
1692. **School system explainer** — Collect: "how US school system works", `translate`. Do: summarise grades, tests and options in a parent's language. Build: translated explainer for newcomer families.

[↑ Contents](#contents)

### Productivity, mental models & personal development

1693. **Habit framework comparison** — Collect: "how to build habits", "atomic habits summary". Do: compare frameworks and their steps. Build: comparison table of habit frameworks.
1694. **Second brain SOP** — Collect: "second brain", "zettelkasten". Do: extract setup steps and workflows. Build: personal knowledge system SOP.
1695. **Note app decision matrix** — Collect: "obsidian vs notion", `within = "year"`. Do: compare features and reported pain points. Build: decision matrix.
1696. **Deep work time blocks** — Collect: "deep work routine", "time blocking". Do: extract schedules creators follow. Build: weekly time-block template.
1697. **Pomodoro variants** — Collect: "pomodoro technique", "52 17 method". Do: compare intervals and claimed reasons. Build: timer presets to test.
1698. **Study plan with Anki** — Collect: "spaced repetition", "active recall". Do: extract methods and schedules. Build: study plan plus Anki deck template.
1699. **Speaking rehearsal checklist** — Collect: "public speaking tips", "stop saying um". Do: extract rehearsal techniques. Build: rehearsal checklist.
1700. **Talk opener library** — Collect: TED channel, `channel_max_videos = 200`, `chapters = true`. Do: analyse the first 60 seconds of each talk. Build: library of opener patterns.
1701. **Mental model flashcards** — Collect: "mental models", "inversion thinking". Do: extract models with examples given. Build: flashcard deck.
1702. **Decision journal template** — Collect: "decision journal", "how to make better decisions". Do: extract fields and review cadence. Build: decision journal template.
1703. **Team email SOP** — Collect: "inbox zero", "email management". Do: extract rules and filters. Build: team email handling SOP.
1704. **Meeting agenda template** — Collect: "how to run effective meetings". Do: extract agenda structures and rules. Build: meeting agenda template.
1705. **Realistic morning routine** — Collect: "morning routine", `top_comments = 50`. Do: compare creators' claims with commenters' realities. Build: realistic, adjustable routine.
1706. **Procrastination if-then plans** — Collect: "how to stop procrastinating". Do: extract tactics and triggers. Build: if-then plan sheet.
1707. **Phone setup for focus** — Collect: "dopamine detox", "phone minimalism". Do: map claims and practical settings. Build: phone setup guide plus claims to verify.
1708. **Speed reading claim check** — Collect: "speed reading", "speed reading myth". Do: compare claims with research cited. Build: claim vs evidence table.
1709. **Memory palace drills** — Collect: "memory palace", memory champion channels. Do: extract techniques and practice steps. Build: 14-day practice drills.
1710. **Annual goal worksheet** — Collect: "personal OKRs", "SMART goals". Do: compare goal-setting methods. Build: annual goal worksheet.
1711. **90-day journaling deck** — Collect: "journaling prompts", "reflective journaling". Do: collect and dedupe prompts by theme. Build: 90-day prompt deck.
1712. **Productivity fad tracker** — Collect: "productivity system", daily runs for a year. Do: use `trends.html` to see which methods rise and fade. Build: annual fad report.
1713. **Weekly planner Claude skill** — Collect: planning-method videos, `knowledge/planning.md`. Do: distil methods into steps. Build: Claude skill that runs your weekly plan with you.
1714. **Negotiation role-plays** — Collect: interviews with negotiation experts, "negotiation tactics". Do: extract tactics and example phrases. Build: role-play scripts for practice.
1715. **Clear writing checklist** — Collect: "how to write clearly", "writing tips". Do: extract rules and examples. Build: editing checklist.
1716. **Time tracking sheet** — Collect: "time tracking", "time audit". Do: extract categories and review methods. Build: time-tracking spreadsheet.
1717. **ADHD-friendly toolkit** — Collect: ADHD coach and clinician channels, "ADHD productivity". Do: list tools and tactics, not treatment. Build: toolkit with a note to discuss care with a professional.
1718. **Exam revision timetable** — Collect: "how to study for exams", "revision timetable". Do: extract scheduling rules. Build: revision timetable generator prompt.
1719. **Language method comparison** — Collect: polyglot channels, "how to learn a language". Do: compare methods and claims. Build: method comparison and starter plan.
1720. **Remote work policy ideas** — Collect: "remote work routine", "work from home productivity". Do: extract practices for teams. Build: WFH guideline draft.
1721. **Burnout opinion map** — Collect: "burnout recovery", psychologist channels. Do: map signs and approaches described. Build: map plus questions for a professional.
1722. **Author idea digest** — Collect: author interviews, "productivity book author". Do: summarise core ideas in their own words. Build: reading list with one-paragraph takeaways.
1723. **Slide design checklist** — Collect: "slide design tips", "presentation design". Do: extract rules and examples. Build: slide checklist.
1724. **Story structure template** — Collect: "storytelling techniques", "storytelling for presentations". Do: extract structures. Build: story template.
1725. **STAR answer worksheet** — Collect: "job interview answers", recruiter channels. Do: extract answer structures and mistakes. Build: STAR worksheet.
1726. **Bias checklist for teams** — Collect: "cognitive biases", "decision making biases". Do: extract biases and countermeasures. Build: pre-decision checklist.
1727. **Delegation matrix** — Collect: "how to delegate", "manager productivity". Do: extract delegation levels. Build: delegation matrix.
1728. **Daily planning prompt** — Collect: "daily planning routine", `within = "year"`. Do: distil common steps. Build: AI prompt that plans your day from your task list.
1729. **30-day declutter plan** — Collect: "declutter", "minimalism tips". Do: extract room-by-room steps. Build: 30-day plan.
1730. **File organisation SOP** — Collect: "file naming conventions", "organize computer files". Do: extract folder structures. Build: file organisation SOP.
1731. **Reading tracker** — Collect: "how to read more books". Do: extract habits and tracking methods. Build: reading tracker spreadsheet.
1732. **Coaching offer research** — Collect: "productivity coach", `top_comments = 100`. Do: cluster viewers' pain points. Build: coaching offer outline.
1733. **Study skills lesson** — Collect: "study skills for students", teacher channels. Do: extract activities. Build: classroom lesson plan.
1734. **Elevator pitch templates** — Collect: "elevator pitch examples". Do: extract structures. Build: pitch templates.
1735. **Motivation vs discipline debate** — Collect: "motivation vs discipline". Do: summarise each side. Build: debate summary.
1736. **Artists' creative routines** — Collect: "creative process", artist interview channels. Do: extract routines and rituals. Build: creative routine library.
1737. **30-day skill sprint** — Collect: "learn anything fast", "first 20 hours". Do: extract deconstruction steps. Build: 30-day skill sprint plan.
1738. **Feedback script** — Collect: "how to give feedback", "SBI feedback". Do: extract models and phrasing. Build: feedback script card.
1739. **Small talk cue cards** — Collect: "how to make small talk", "conversation skills". Do: extract openers and follow-ups. Build: cue cards.
1740. **Personal kanban setup** — Collect: "personal kanban", "trello for personal tasks". Do: extract column setups and WIP limits. Build: board setup guide.
1741. **Daily ideas digest** — Collect: a few chosen channels, `within = "today"`, `schedule_daily.bat`. Do: summarise one idea per video. Build: 5-minute daily digest.
1742. **Thinker quote index** — Collect: a long-form interview channel, all videos. Do: `yt.py find` for recurring themes. Build: quote index with links to the exact second.
1743. **Toastmasters table topics** — Collect: "table topics", "impromptu speaking". Do: extract prompt styles and frameworks. Build: prompt bank for a club.
1744. **Accountability group charter** — Collect: "accountability partner", "mastermind group". Do: extract formats and rules. Build: group charter.
1745. **Energy-based schedule** — Collect: "chronotype", "energy management". Do: map claims and suggested schedules. Build: energy-based weekly schedule to test.
1746. **Productivity advice dataset** — Collect: "productivity tips", `within = "year"`, `yt.py export`. Do: categorise advice by type and evidence. Build: research dataset.

[↑ Contents](#contents)

## Home, hobbies, sports and travel

### Home, DIY & vehicles

1747. **Used-car inspection checklist** — Collect: "<model year> common problems", "<model> buying guide", `min_views = 20000`, `top_comments = 30`. Do: list recurring faults by mileage and how owners spot them. Build: printable test-drive checklist.
1748. **Owner recall radar** — Collect: "<model> recall", "<model> TSB", `within = "week"`, daily schedule. Do: flag newly discussed faults and dealer fixes. Build: weekly owner digest, each item marked "check the official recall database".
1749. **Bathroom remodel SOP** — Collect: "bathroom remodel start to finish", "shower pan install", `min_duration = 1200`, `chapters`, `timestamps`. Do: merge pros' step order, cure times, tool lists. Build: day-by-day SOP linking each step to the exact second.
1750. **Tiling method disputes** — Collect: "thinset vs mastic", "liquid waterproofing vs membrane", `top_comments = 50`. Do: map where tilers disagree and the reasons each gives. Build: comparison table with a "check manufacturer spec" column.
1751. **Joinery flashcards** — Collect: 5 woodworking educator channels, `channel_max_videos = 100`. Do: extract each joint, its use, strength claims and tools needed. Build: Anki deck of joinery cards with timestamp links.
1752. **First-shop tool decision tree** — Collect: "best budget table saw", "track saw vs table saw", "garage workshop setup", `within = "year"`. Do: who recommends what for which space and budget. Build: decision tree for a beginner's first five tools.
1753. **EV winter range dataset** — Collect: "<EV> winter range test", "<EV> highway range test", `subtitles_only`. Do: pull stated temperature, speed, battery % and distance. Build: CSV via `yt.py export`, labelled as unverified creator-reported tests.
1754. **Home charger electrician questions** — Collect: "level 2 charger install", "EV charger panel upgrade". Do: list what installers say about panel capacity, permits, load management. Build: question sheet for a licensed electrician, not a DIY guide.
1755. **Motorcycle service log** — Collect: "<bike> valve adjustment", "<bike> major service", `chapters`. Do: extract intervals, parts and specs mentioned. Build: maintenance spreadsheet with every spec flagged "confirm in service manual".
1756. **Regional pest early warning** — Collect: "squash vine borer", "aphids <region>", `within = "week"`, `rising_views_per_day = 300`. Do: spot pests gardeners in your area suddenly discuss. Build: weekly pest alert for a community garden.
1757. **Zone sowing calendar** — Collect: channels of growers in your hardiness zone, `channel_within = "year"`. Do: extract what they sow and transplant relative to last frost. Build: month-by-month sowing calendar spreadsheet.
1758. **Backyard chickens course** — Collect: "backyard chickens beginner", "chicken coop build", `min_views = 50000`, `remove_filler_words`. Do: map -> reduce into coop, feed, predators, winter. Build: 6-module beginner course outline citing clips.
1759. **Roofing quote review** — Collect: "roof replacement cost", "what roofers won't tell you", `top_comments = 40`. Do: list line items, red flags and questions pros say to ask. Build: one-page quote review checklist for homeowners.
1760. **Handyman business SOPs** — Collect: channels of handyman business owners, `channel_max_videos = 80`. Do: extract pricing methods, intake calls, job-walk routines. Build: SOP binder plus a job pricing template for a new business.
1761. **DIY channel gap finder** — Collect: "<niche> DIY", `max_views = 5000`, `within = "month"`, `top_comments = 30`. Do: compare questions viewers ask with topics actually covered. Build: list of 30 underserved video ideas.
1762. **Paint problem helper** — Collect: "paint peeling", "brush marks cabinet paint", "paint sprayer tips". Do: map symptom -> cause -> fix as painters describe it. Build: Claude skill answering paint questions with timestamped sources.
1763. **Classic car restoration KB** — Collect: channels restoring <car>, `channel_max_videos = 200`. Do: map -> reduce rust spots, parts interchange, supplier mentions. Build: `knowledge/<car>.md` reference for a restoration club.
1764. **DIY vs shop job cards** — Collect: "<model> brake job", "<model> alternator replacement", `timestamps`. Do: extract tools, time taken, difficulty and gotchas. Build: job cards rating each repair DIY-friendly or shop-only.
1765. **OBD code cause ranking** — Collect: "P0420 <model>", "P0171 fix", "<code> diagnosis". Do: rank causes by how often mechanics name them, cheapest checks first. Build: code lookup table for your own car.
1766. **Smart home ecosystem matrix** — Collect: "Home Assistant vs", "Matter thread setup", `within = "month"`. Do: track which platforms creators recommend and recurring complaints. Build: comparison matrix refreshed monthly.
1767. **Heat pump claims map** — Collect: "heat pump install cost", "heat pump regret", `top_comments = 50`. Do: map claimed savings, climate caveats, regret reasons. Build: questions for an energy auditor plus claims to verify.
1768. **Solar owner outcomes sheet** — Collect: "solar panels 5 years later", "solar worth it", `min_duration = 600`, `include_description`. Do: extract stated cost, payback, problems, location. Build: spreadsheet of owner-reported outcomes.
1769. **Wood finish recipe cards** — Collect: "wipe-on poly", "hardwax oil", "french polish tutorial". Do: extract coats, dry times, sanding grits, application tools. Build: printable finish schedule cards for the shop wall.
1770. **Shop class safety briefing** — Collect: "table saw kickback explained", "woodshop safety", shop-teacher channels. Do: extract rules and common mistakes shown. Build: safety slides and a 15-question quiz for students.
1771. **Lawn care year plan** — Collect: "lawn care schedule <grass type>", 4 lawn creator channels. Do: extract monthly tasks by product type, not brand. Build: 12-month lawn calendar with soil-test reminder.
1772. **Tool brand watch** — Collect: "<brand> tool review", `within = "today"`, daily runs, `top_comments = 20`. Do: track complaints, praise and launches. Build: `trends.html`-backed brand briefing for a tool retailer's buyers.
1773. **Appliance triage tree** — Collect: "dishwasher not draining", "dryer not heating", `subtitles_only`. Do: map symptom -> checks -> likely part. Build: decision tree with "unplug first" and "gas: call a pro" stop points.
1774. **Tiny house budget template** — Collect: "tiny house build cost breakdown", `min_duration = 900`, `include_description`. Do: extract line items and totals. Build: budget template showing low/typical/high ranges.
1775. **Van build electrical review** — Collect: "van build electrical system", "lithium battery van". Do: list component choices and every safety warning creators give. Build: component table and a checklist for a qualified electrician to review.
1776. **Homestead water planner** — Collect: "rainwater harvesting system", "well pump install", "gravity water system". Do: compare designs, costs, maintenance. Build: planning worksheet for off-grid water.
1777. **Mobile detailing menu** — Collect: detailing business channels, "detailing packages pricing". Do: extract packages, minutes per job, pricing logic. Build: service menu and time-per-job sheet for a startup.
1778. **Charging network reliability** — Collect: "<network> charger broken", "EV road trip charging", `within = "week"`. Do: categorise failures by network and region. Build: monthly reliability briefing for a fleet manager.
1779. **Helmet comparison** — Collect: "<helmet> review", `exclude_words = "unboxing"`, `sponsorblock`. Do: extract fit, noise, venting claims. Build: comparison table noting which reviews say the product was supplied free.
1780. **Houseplant symptom bot** — Collect: "monstera yellow leaves", "fiddle leaf fig dropping leaves", "overwatering signs". Do: map symptom -> cause -> fix. Build: plant-care Claude skill for a garden centre counter.
1781. **Permaculture across climates** — Collect: permaculture educator channels plus non-English ones with `translate`. Do: compare how principles change by climate. Build: study guide with a climate-specific example per principle.
1782. **Foreign carpentry techniques** — Collect: "Holzverbindungen", "大工 継手", `translate`, `languages`. Do: extract techniques rarely covered in English. Build: annotated technique list with source links.
1783. **Home inspection decoder** — Collect: "home inspector explains", "home inspection red flags". Do: gloss terms and how serious inspectors say each is. Build: glossary and question list for a buyer's walk-through.
1784. **Basement waterproofing bids** — Collect: "basement waterproofing scam", "interior french drain", `top_comments = 40`. Do: map methods and disputes. Build: question set to compare three contractor bids.
1785. **Self-paced mechanic curriculum** — Collect: auto-tech educator channels, `channel_max_videos = 300`. Do: map -> reduce into a systems topic map. Build: ordered curriculum with timestamped lessons per system.
1786. **Dealer launch talking points** — Collect: "<new model> first drive", `within = "week"`, `min_views = 10000`. Do: summarise praise and criticism reviewers repeat. Build: sales-team briefing with honest answers to objections.
1787. **3D-printed repair parts** — Collect: "3D printed replacement part", "functional prints PETG vs ASA". Do: extract materials and settings creators use for durable parts. Build: material selection chart.
1788. **Deck planning sheet** — Collect: "deck footing", "deck joist spacing", "ledger board". Do: extract rules of thumb creators cite. Build: planning spreadsheet with a "verify with local code" column per item.
1789. **House binder QR index** — Collect: "replace toilet flapper", "faucet cartridge replace", `max_duration = 900`, `timestamps`. Do: pick the clearest short clip per job. Build: printed binder with QR codes to the exact second.
1790. **Hardware store aisle FAQs** — Collect: common DIY keywords, `top_comments = 50`. Do: extract the questions beginners ask most per category. Build: staff cheat sheets per aisle.
1791. **Garden trial log** — Collect: "no dig vs dig trial", "raised bed vs in ground". Do: extract each creator's setup and claimed results. Build: table of informal trials and a design for your own side-by-side test.
1792. **Canning safety cross-check** — Collect: "pressure canning beginner", `top_comments = 30`. Do: flag where creators deviate from tested guidelines. Build: checklist pointing to official tested recipes.
1793. **Ownership cost comparison** — Collect: "<model A> 150k miles", "<model B> ownership cost". Do: extract owner-reported repairs and costs. Build: total-cost comparison sheet for a family car choice.
1794. **Restoration video script template** — Collect: your channel and 6 rivals via `channels`. Do: analyse hooks and structure of the highest views-per-day videos. Build: script template for your next build series.
1795. **New homeowner first month** — Collect: "first things to do new house", "new homeowner mistakes". Do: merge and deduplicate tasks. Build: 30-day checklist ordered by urgency.
1796. **E-bike conversion parts list** — Collect: "ebike conversion kit", "hub vs mid drive". Do: compare kits, install difficulty, battery warnings. Build: parts list and pros/cons table.
1797. **Small engine repair guide** — Collect: "lawn mower won't start", "carburetor clean small engine", `subtitles_only`. Do: map common faults to fixes. Build: seasonal small-engine checklist for a landscaping crew.
1798. **Sharpening angle chart** — Collect: "sharpen chisel", "plane iron honing", "card scraper burr". Do: extract angles and stone grits recommended. Build: laminated sharpening reference chart.
1799. **Teardown failure report** — Collect: "<product> teardown", "<product> failed", `top_comments = 40`. Do: list failure modes and repair complaints. Build: product-improvement report for an R&D team.
1800. **Rental turnover SOP** — Collect: "rental turnover checklist", "landlord maintenance tips". Do: extract task order and time estimates. Build: unit-turnover SOP for a small property manager.
1801. **Personal DIY archive** — Collect: every DIY channel you follow, `schedule_daily.bat`. Do: `yt.py find "sill plate"` when a problem comes up. Build: searchable library of your trusted creators with links to the exact second.

[↑ Contents](#contents)

### Gaming & esports

1802. **Patch-day briefing** — Collect: "<game> patch <version>", `within = "today"`, `min_views = 5000`, `top_comments = 30`. Do: summarise which changes creators call buffs or nerfs and player reaction. Build: one-page patch briefing.
1803. **Tier list consensus** — Collect: "<game> tier list", `within = "week"`, `min_views = 10000`. Do: aggregate placements across creators. Build: consensus tier table with a disagreement score per pick.
1804. **Build card** — Collect: "<game> <class> build guide", `chapters`, `timestamps`. Do: extract gear, skill order and rotation. Build: one-page build card with links to each explanation.
1805. **Speedrun route doc** — Collect: top runners' channels, "<game> any% tutorial". Do: extract tricks, setups and frame windows mentioned. Build: route document with each trick linked to the exact second.
1806. **New speedrun tech watch** — Collect: "<game> new skip", "<game> new strat", `within = "week"`, `rising_views_per_day = 1000`. Do: flag newly shown techniques. Build: weekly alert for a speedrun community.
1807. **Postmortem lessons library** — Collect: "game postmortem", "what went wrong game dev", `min_duration = 1200`. Do: map -> reduce causes of success and failure. Build: `knowledge/postmortems.md` and a risk checklist for your project.
1808. **Indie genre opportunity** — Collect: "devlog", `max_views = 10000`, `within = "month"`. Do: find genres and hooks gaining views per day. Build: genre opportunity report for a solo developer.
1809. **Steam launch timeline** — Collect: "steam wishlist marketing", "steam next fest results". Do: extract tactics and stated wishlist numbers. Build: launch-countdown checklist from 12 months out.
1810. **Public VOD scouting dossier** — Collect: tournament org channels, `channel_tabs = "streams"`, "<team> vs". Do: summarise casters' and analysts' remarks on team tendencies. Build: opponent dossier from public matches.
1811. **Caster storyline sheet** — Collect: "<player> interview", "<team> roster change", `within = "month"`. Do: extract rivalries, comebacks, quotes. Build: caster prep sheet with timestamped quote sources.
1812. **What to stream this week** — Collect: game names, `rising_views_per_day = 2000`, `within = "week"`. Do: spot rising games before saturation. Build: weekly shortlist for a small streamer.
1813. **Board game teach script** — Collect: "how to play <game>", `max_duration = 1800`. Do: compare how teachers order rules and what they skip. Build: 5-minute teach script for game night.
1814. **Board game recommender** — Collect: 6 board game reviewer channels, `channel_max_videos = 300`. Do: extract player count, weight, comparisons. Build: Claude skill that suggests games for a group.
1815. **Accessibility matrix** — Collect: "<game> accessibility review", "colorblind mode <game>". Do: extract options reviewers praise or miss. Build: feature matrix for disabled players.
1816. **Parents' game brief** — Collect: "<game> parents guide", "<game> review". Do: summarise content, spending, chat and safety settings. Build: one-page brief for parents.
1817. **Lore timeline** — Collect: lore channels, `channel_max_videos = 200`. Do: map -> reduce events in order, noting where creators disagree. Build: lore timeline citing videos for a fan wiki.
1818. **Fighting game matchup notes** — Collect: "<character> guide", "<character> matchup". Do: extract punishes and habits pros warn about. Build: matchup notes per character.
1819. **Chess opening plan** — Collect: "<opening> explained", chess educator channels. Do: extract main lines, plans and traps. Build: repertoire study plan with timestamped lessons.
1820. **Player feedback report** — Collect: "<your game> review", `within = "week"`, `top_comments = 50`. Do: cluster praise and complaints. Build: weekly feedback report for the dev team.
1821. **Community bug triage** — Collect: "<game> bug", "<game> glitch", `within = "today"`, `timestamps`. Do: deduplicate reported bugs. Build: QA triage list linking to footage.
1822. **Settings by GPU tier** — Collect: "best settings <game>", `within = "month"`. Do: extract recommended settings per hardware tier. Build: settings table for a PC gaming forum.
1823. **Sponsor mention report** — Collect: tournament broadcasts, `channel_tabs = "streams"`. Do: use keyword mentions to count brand references. Build: sponsor exposure summary for an esports marketing team.
1824. **Live-service economy reference** — Collect: "gacha monetization explained", "battle pass design". Do: extract design patterns and criticism. Build: design reference doc for a monetisation review.
1825. **Level design module** — Collect: "level design breakdown", `min_duration = 900`. Do: extract principles with examples. Build: course module with clips for a game design class.
1826. **Mod roundup newsletter** — Collect: "<game> mods", `within = "week"`, `min_views = 2000`. Do: summarise standout mods. Build: weekly mod newsletter.
1827. **Rank-up self-review checklist** — Collect: "<game> coaching VOD review". Do: extract recurring mistakes coaches point out by rank. Build: checklist players use to review their own replays.
1828. **Tournament recap** — Collect: tournament channels, `channel_within = "week"`. Do: summarise results, upsets, storylines. Build: recap newsletter for a regional scene.
1829. **Developer quote bank** — Collect: "<studio> developer interview". Do: extract quotes on design decisions with `timestamps`. Build: cited quote bank for a journalist.
1830. **Foreign scene digest** — Collect: Korean and Chinese esports channels, `translate`, `languages`. Do: summarise news missing from English coverage. Build: weekly English digest.
1831. **Stream clip finder** — Collect: your channel, `channel_tabs = "streams"`. Do: `yt.py find` hype words and funny moments. Build: clip list with exact-second links for your editor.
1832. **GM prep checklist** — Collect: "GM tips", "session prep tabletop". Do: extract prep routines and encounter ideas. Build: session prep checklist and idea bank.
1833. **House rules doc** — Collect: "<rule> explained D&D", "<rule> ruling". Do: map how popular GMs interpret contested rules. Build: house rules document for your table.
1834. **VR comfort ratings** — Collect: "<VR game> review", "motion sickness VR". Do: extract comfort options and reviewer reports. Build: comfort table for new VR owners.
1835. **Trailer fact check** — Collect: "<game> trailer breakdown". Do: separate confirmed features from speculation. Build: confirmed-vs-rumoured list.
1836. **Pre-launch risk memo** — Collect: "<game> beta impressions", `top_comments = 50`. Do: extract concerns and their frequency. Build: launch risk memo for a publisher.
1837. **Gaming channel concept** — Collect: niche keywords, `max_views = 5000`, `top_comments = 30`. Do: find unmet questions. Build: channel concept with first 10 video ideas.
1838. **Draft trend sheet** — Collect: "<game> draft analysis", `within = "week"`. Do: extract picks and bans casters discuss. Build: spreadsheet for a team analyst.
1839. **Deck archetype table** — Collect: "<TCG> deck tech", `within = "month"`. Do: extract archetypes, key cards, matchups claimed. Build: archetype table for a card shop.
1840. **Minecraft lesson plans** — Collect: "Minecraft education lesson", "teaching with games". Do: extract activities and learning goals. Build: lesson plans for teachers.
1841. **Game-based learning claims** — Collect: game-based learning talks, `min_duration = 1200`. Do: list claims and cited studies. Build: annotated list of claims to check against papers.
1842. **Game audio glossary** — Collect: "game audio design", "adaptive music explained". Do: extract techniques and terms. Build: glossary for a sound design student.
1843. **Achievement checklist** — Collect: "<game> all achievements", `chapters`, `timestamps`. Do: extract missable items and order. Build: checklist with links to each clip.
1844. **Pro interview dataset** — Collect: pro player interview channels, `channel_max_videos = 500`. Do: `yt.py export` to .jsonl. Build: searchable RAG dataset of public quotes.
1845. **Budget PC part picks** — Collect: "gaming PC build <budget>", `within = "month"`. Do: extract parts recommended per budget. Build: part list table by price tier.
1846. **Localization issue report** — Collect: non-English reviews of your game, `languages`, `translate`. Do: extract translation complaints. Build: localization issue report.
1847. **Narrative structure templates** — Collect: "writing for games", "branching narrative". Do: extract structures writers use. Build: story templates for a narrative designer.
1848. **Strategy cheat sheet** — Collect: "<4X game> beginner strategy". Do: extract openings and common mistakes. Build: cheat sheet for new players.
1849. **Org content benchmarks** — Collect: rival esports org channels. Do: compare formats by views per day. Build: content benchmark report for an org's media team.
1850. **Marathon couch commentary** — Collect: past runs of games on a marathon schedule. Do: extract trivia and trick names per game. Build: commentary notes per run.
1851. **Game history syllabus** — Collect: game history documentary channels, `min_duration = 1200`. Do: map -> reduce eras and turning points. Build: semester syllabus with viewing list.
1852. **UGC creator economy** — Collect: "Roblox game monetization", "UEFN creator earnings". Do: extract tactics and stated earnings. Build: tactics list with claims marked unverified.
1853. **Discord moderation guidelines** — Collect: "<game> toxicity", "community moderation tips". Do: extract common problems and policies. Build: moderation guideline draft.
1854. **Esports org onboarding pack** — Collect: "<game> fundamentals", "<game> callouts", `min_views = 20000`, `chapters`. Do: extract map callouts, comms rules, role duties. Build: onboarding pack and quiz for new academy-team players.
1855. **What to play next** — Collect: trusted reviewers via `only_channels`. Do: profile your taste from games you loved. Build: Claude skill recommending your next game.

[↑ Contents](#contents)

### Sports, coaching & outdoors

1856. **Youth soccer drill cards** — Collect: "U10 soccer drills", "small sided games kids", `max_duration = 900`, `timestamps`. Do: extract setup, player count, coaching points. Build: drill cards grouped by skill with links to each demo.
1857. **Practice plan generator** — Collect: 6 basketball coaching channels, `channel_max_videos = 200`. Do: map -> reduce into a drill knowledge base tagged by skill and age. Build: Claude skill that writes a 90-minute practice plan on request.
1858. **Public match scouting report** — Collect: "<team> tactical analysis", "<team> pressing", `within = "month"`. Do: summarise shape, build-up and set-piece habits analysts describe. Build: pre-match scouting report from public coverage.
1859. **Tactics glossary for new fans** — Collect: "football tactics explained", "inverted full back explained", `max_duration = 900`. Do: extract each term with one example. Build: plain-English glossary for a supporters' club newsletter.
1860. **Transfer rumour log** — Collect: "<club> transfer news", `within = "today"`, daily runs. Do: log each rumour with channel, date and claimed source. Build: rumour spreadsheet with every row marked unconfirmed until official.
1861. **Strength program comparison** — Collect: "beginner strength program", "5x5 vs PPL", `min_views = 50000`. Do: compare structure, frequency and progression. Build: comparison table to discuss with a qualified coach, not a prescription.
1862. **Running injury opinion map** — Collect: "shin splints runners", "runner's knee", `top_comments = 30`. Do: map what creators suggest and where they disagree. Build: question list to take to a physiotherapist.
1863. **Marathon plan comparison** — Collect: "marathon training plan", "sub 4 marathon plan", `min_duration = 600`. Do: compare weekly mileage, long-run caps, taper length. Build: side-by-side plan table for a running club.
1864. **Trail conditions brief** — Collect: "<trail> hike", `within = "week"`, `top_comments = 20`. Do: extract remarks on snow, water sources, washouts and closures. Build: conditions brief marked "confirm with the ranger station".
1865. **Thru-hike gear weight sheet** — Collect: "PCT gear list", "ultralight gear list", `within = "year"`. Do: extract items, stated weights, what hikers regretted carrying. Build: gear spreadsheet with total base weight.
1866. **Seasonal fishing calendar** — Collect: channels of anglers on <lake>, `channel_within = "year"`. Do: extract lures, depths and techniques by month. Build: month-by-month technique calendar.
1867. **Fly pattern recipe cards** — Collect: "<fly> tying tutorial", `chapters`. Do: extract hook size, thread, materials and step order. Build: printable recipe cards for a fly-tying class.
1868. **Climbing movement flashcards** — Collect: 4 climbing coach channels, `channel_max_videos = 150`. Do: extract each technique and its key cue. Build: Anki deck with timestamp links to the demos.
1869. **Bouldering training block** — Collect: "bouldering training plan", "hangboard beginner". Do: compare protocols and every injury caution given. Build: 8-week training block draft to review with a coach.
1870. **Bike fit pre-check** — Collect: "bike fit explained", "saddle height knee pain". Do: extract measurements and symptom-adjustment pairs. Build: checklist and notes to bring to a professional fitter.
1871. **Bike shop mechanic training** — Collect: "road bike maintenance", "tubeless setup", `max_duration = 900`, `subtitles_only`. Do: extract job steps and common errors. Build: training SOPs for junior shop mechanics.
1872. **Referee scenario quiz** — Collect: "referee explains handball", "offside decision explained". Do: extract incidents and the rule applied. Build: scenario quiz for referee trainees with clip links.
1873. **Broadcaster prep notes** — Collect: "<team> preview", "<player> form", `within = "week"`. Do: extract storylines, stats quoted and talking points. Build: commentary prep notes for a local radio commentator.
1874. **Golf fault-to-drill table** — Collect: "fix slice", "golf early extension drill", `max_duration = 1200`. Do: map fault -> cause -> drill as coaches teach it. Build: range-session table for a weekend golfer.
1875. **Tennis pro pattern notes** — Collect: "<player> tactics analysis", "<player> serve breakdown". Do: extract serve and rally patterns analysts note. Build: pattern notes a club player can copy in practice.
1876. **Coaching philosophy module** — Collect: long-form coach interviews, `min_duration = 1800`, `remove_filler_words`. Do: extract philosophies on feedback, culture and selection. Build: discussion module for a coaching certification course.
1877. **Fantasy lineup notes** — Collect: "<sport> injury news", "<sport> lineup news", `within = "today"`, daily runs. Do: extract role and injury updates per player. Build: daily lineup notes, cross-checked against official team reports.
1878. **Recovery claims check** — Collect: "cold plunge benefits", "recovery science", `min_views = 100000`. Do: list each claim and any study creators cite. Build: table of claims to check against published research.
1879. **Avalanche course prep** — Collect: "avalanche safety basics", "avalanche rescue practice". Do: extract concepts and open questions. Build: question list for a certified avalanche course, explicitly not a substitute.
1880. **Backcountry menu** — Collect: "backpacking meals", "trail food calories per ounce". Do: extract meals, weights and calories claimed. Build: 5-day menu with packing weight per day.
1881. **Wild camping rule list** — Collect: "wild camping <country>", local-language keywords, `translate`. Do: extract rules creators state. Build: list of rules to confirm with local authorities before a trip.
1882. **Surf forecast reading guide** — Collect: "how to read surf forecast", "swell period explained". Do: extract swell, wind and tide rules of thumb. Build: one-page guide for beginner surfers.
1883. **Sea kayak trip plan** — Collect: "sea kayak trip planning", "kayak rescue practice". Do: extract gear, tide planning and safety steps. Build: trip checklist and float plan template.
1884. **Ski instructor progression** — Collect: "ski lesson beginner", "parallel turn drill", `channels` of ski schools. Do: extract skill order and cues. Build: progression ladder an instructor uses to plan lessons.
1885. **Club social media plan** — Collect: 10 amateur and pro club channels. Do: compare formats by views per day. Build: 3-month content plan for a grassroots club.
1886. **Athlete quote dataset** — Collect: "<athlete> press conference", `channel_max_videos = 300`. Do: `yt.py export` to .jsonl for search. Build: dataset of public quotes with dates for a sports writer.
1887. **Women's sport coverage tracker** — Collect: "<league> highlights", "<league> analysis", daily runs. Do: track new videos and attention in `trends.html`. Build: monthly coverage report for an advocacy group.
1888. **Sabermetrics study guide** — Collect: "sabermetrics explained", "WAR explained". Do: extract each stat, its formula idea, its limits. Build: study guide for a sports analytics student.
1889. **Volunteer onboarding SOP** — Collect: "running a grassroots club", "youth sports volunteer". Do: extract roles, duties and common pitfalls. Build: onboarding SOP for new club volunteers.
1890. **PE unit plans** — Collect: "PE lesson ideas", "PE games middle school". Do: extract activities by age and equipment. Build: 6-week unit plans for a PE teacher.
1891. **BJJ technique tree** — Collect: BJJ instructor channels, `channel_max_videos = 250`. Do: map positions -> techniques -> counters. Build: technique tree for a gym's curriculum wall.
1892. **Running shoe comparison** — Collect: "<shoe> review", `sponsorblock`, `exclude_words = "unboxing"`. Do: extract fit, stack, durability claims. Build: comparison table noting which reviewers say shoes were supplied.
1893. **Birding field sheet** — Collect: "<species> ID tips", "<species> call". Do: extract field marks, habitat and look-alikes. Build: pocket field sheet for a beginner birding walk.
1894. **National park permit questions** — Collect: "<park> permit tips", `within = "year"`. Do: extract stated reservation and permit rules. Build: list to verify with the park service.
1895. **Sailing manoeuvre cards** — Collect: "tacking explained", "man overboard drill". Do: extract crew steps and calls. Build: drill cards for a sailing school.
1896. **Swim drill progression** — Collect: "freestyle drills", "catch drill swimming". Do: extract drills and cues by level. Build: 6-week progression for a masters squad.
1897. **Lower-league prospect watch** — Collect: "<league> prospect", `max_views = 5000`. Do: extract players small analysts rate and why. Build: public-athlete watch list for a scout to follow up with film.
1898. **Press conference themes** — Collect: "<coach> press conference", `channel_within = "month"`. Do: track recurring themes and wording. Build: themes tracker for a beat reporter.
1899. **Rule change explainer** — Collect: "<sport> new rules", `within = "month"`. Do: extract changes and predicted effects. Build: one-pager for parents and players.
1900. **Outdoor gear trend report** — Collect: "<category> gear review", `within = "month"`, `rising_views_per_day = 500`. Do: extract items gaining attention. Build: buying-trends report for an outdoor retailer.
1901. **Map and compass practice** — Collect: "map and compass", "navigation skills hiking". Do: extract exercises and common mistakes. Build: practice plan for a scout troop.
1902. **Race course recon** — Collect: "<race> course recon", "<race> race report". Do: extract notes per section: climbs, aid stations, surprises. Build: course notes by mile.
1903. **Pre-performance routine** — Collect: "sports psychology routine", "pre-game routine". Do: map techniques coaches recommend. Build: worksheet an athlete fills in with their own routine.
1904. **Crag beta notes** — Collect: "<crag> beta", "<route name>". Do: extract beta per route and conditions mentioned. Build: beta notes to pair with the local guidebook.
1905. **Gravel event calendar** — Collect: "gravel race", "<region> gravel event", `within = "year"`. Do: extract events, dates, distances, terrain. Build: season calendar for a cycling club.
1906. **MTB skills progression** — Collect: "mtb skills", "mtb cornering", `max_duration = 1200`. Do: extract skills by level with drills. Build: progression card for a youth MTB program.
1907. **Parent communication handbook** — Collect: "youth coach parents", "sideline behavior". Do: extract communication tips and policies. Build: parent handbook for a youth team.
1908. **Underreported story leads** — Collect: "<sport> news", `max_views = 2000`, `within = "week"`. Do: find topics small creators cover that mainstream media do not. Build: story lead list for a journalist.
1909. **Personal coaching archive** — Collect: your favourite coaches' channels, `schedule_daily.bat`. Do: `yt.py find "first touch"` when planning sessions. Build: searchable archive with links to the exact second.
1910. **Climb pacing cheat sheet** — Collect: "climb pacing cycling", "power on climbs". Do: extract pacing advice and examples. Build: cheat sheet for a club sportive.

[↑ Contents](#contents)

### Travel, culture & lifestyle

1911. **Destination itinerary draft** — Collect: "<city> travel guide", "<city> 3 days", `within = "year"`, `top_comments = 30`. Do: extract must-sees, skips and timing tips. Build: day-by-day itinerary draft with clip links.
1912. **Tourist trap list** — Collect: "<city> tourist traps", "<city> mistakes to avoid", `top_comments = 40`. Do: extract traps and what creators do instead. Build: avoid list with an alternative for each.
1913. **Points strategy map** — Collect: "<program> points strategy", "award flight sweet spots", `within = "month"`. Do: map tactics creators describe. Build: list of strategies to verify against current program terms, not financial advice.
1914. **Entry rule change watch** — Collect: "<country> visa", "<country> entry requirements", `within = "week"`, daily runs. Do: flag claimed rule changes. Build: weekly list of items to confirm on the official government site.
1915. **Relocation city matrix** — Collect: "living in <city> pros and cons", `min_duration = 600`, `top_comments = 30`. Do: extract cost, climate, transport, culture claims. Build: weighted comparison matrix for a family move.
1916. **Cost-of-living ranges** — Collect: "cost of living <city>", "monthly budget <city>", `within = "year"`. Do: extract stated rent, groceries, transport figures. Build: budget sheet with low/typical/high ranges, labelled anecdotal.
1917. **Survival phrase sheet** — Collect: "<language> travel phrases", `max_duration = 1200`. Do: extract phrases, pronunciation tips and politeness rules. Build: one-page phrase sheet for a first trip.
1918. **Local-language insider list** — Collect: keywords for <city> in the local language, `languages`, `translate`. Do: extract places locals recommend. Build: insider list of spots missing from English guides.
1919. **Nomad base shortlist** — Collect: "digital nomad <city>", "nomad visa <country>", `within = "year"`. Do: compare internet, coworking, community and visa claims. Build: shortlist with every visa item marked "verify officially".
1920. **Carry-on packing checklist** — Collect: "carry-on packing list", "<climate> packing list", `min_views = 20000`. Do: merge and deduplicate items, note what travellers regret. Build: printable checklist per trip type.
1921. **Travel agent destination brief** — Collect: "<destination> travel guide", `min_views = 20000`, `include_description`. Do: summarise highlights, seasons, pitfalls. Build: one-page brief agents use when selling the destination.
1922. **Hotel shortlist comparison** — Collect: "<hotel> review", "<hotel> room tour", `top_comments = 20`. Do: extract room, noise, location and service remarks. Build: comparison table for three candidate hotels.
1923. **Street food clip map** — Collect: "<city> street food", `timestamps`. Do: extract dishes, stall names and neighbourhoods mentioned. Build: food list grouped by area with links to the exact second.
1924. **Festival year calendar** — Collect: "<country> festivals", "<city> events", `within = "year"`. Do: extract festivals and months. Build: trip-timing calendar with dates to confirm on official sites.
1925. **Accessible travel notes** — Collect: "wheelchair travel <city>", "accessible travel <country>". Do: extract barriers, step-free routes, workarounds. Build: accessibility notes for a disabled traveller's trip.
1926. **Family trip with kids** — Collect: "<city> with kids", "toddler flight tips". Do: extract kid-friendly stops, nap-friendly timing, logistics. Build: family itinerary with backup rainy-day options.
1927. **Boutique buyer trend report** — Collect: "fashion trends", "<season> must haves", `within = "week"`, `rising_views_per_day = 2000`. Do: extract items gaining attention. Build: weekly trend report for a boutique's buyers.
1928. **Capsule wardrobe builder** — Collect: "capsule wardrobe", "minimalist wardrobe", `min_views = 50000`. Do: extract core pieces and combination rules. Build: checklist plus outfit matrix for a 30-piece wardrobe.
1929. **Sustainability claim table** — Collect: "<brand> sustainable", "greenwashing fashion", `top_comments = 30`. Do: extract claims brands and reviewers make. Build: table of claims to verify against certifications.
1930. **Sneaker release calendar** — Collect: "sneaker release", "upcoming drops", `within = "week"`, daily runs. Do: extract models and claimed dates. Build: rolling release calendar for a sneaker shop's social team.
1931. **Watch collector reference** — Collect: 5 watch collector channels, `channel_max_videos = 200`. Do: map -> reduce references, movements, buying tips. Build: `knowledge/watches.md` reference guide.
1932. **Coin grading glossary** — Collect: "coin grading explained", "coin errors to look for". Do: extract terms and grading cues. Build: glossary flashcards for a new collector.
1933. **Thrift resale cheat sheet** — Collect: "thrift flip", "what sells on resale", `within = "month"`. Do: extract brands and item types resellers say move fast. Build: pocket sourcing cheat sheet.
1934. **Fake-spotting checklist** — Collect: "how to spot fake <item>", "real vs fake <item>". Do: extract the tells collectors point to. Build: authentication checklist, with a note to confirm high-value items with an expert.
1935. **Dog breed shortlist** — Collect: "<breed> pros and cons", "<breed> owner experience", `top_comments = 30`. Do: extract energy, grooming, temperament claims. Build: comparison table for a family choosing a breed.
1936. **Puppy training plan** — Collect: dog trainer channels, "puppy training first week". Do: extract skills in order and session lengths. Build: 8-week week-by-week training plan.
1937. **Vet visit question list** — Collect: "<pet> health problems", "<breed> common issues". Do: map what creators say and where they disagree. Build: question list for the vet, not a diagnosis.
1938. **Cat behaviour FAQ** — Collect: "cat behavior explained", "why does my cat". Do: extract behaviours and explanations offered. Build: FAQ for a shelter's adoption pack.
1939. **Aquarium cycling SOP** — Collect: "fishless cycle", "aquarium nitrogen cycle", `subtitles_only`. Do: extract steps and test targets. Build: step-by-step setup SOP for a new tank.
1940. **Reptile husbandry checklist** — Collect: "<reptile> care guide", "<reptile> enclosure setup". Do: extract temperatures, lighting, diet claims. Build: checklist marked "confirm with an exotics vet".
1941. **Business etiquette brief** — Collect: "<country> business etiquette", "<country> culture shock". Do: extract dos, don'ts and meeting norms. Build: briefing card for a sales team's first visit.
1942. **Airport survival notes** — Collect: "<airport> tips", "<airport> layover", `within = "year"`. Do: extract security, transit and lounge tips. Build: one-page layover guide.
1943. **Travel channel gap finder** — Collect: "<destination> travel", `max_views = 3000`, `top_comments = 30`. Do: find questions viewers ask that videos skip. Build: 20 video ideas for a travel creator.
1944. **Cruise line comparison** — Collect: "<cruise line> review", "<ship> honest review". Do: extract food, cabin, crowd and fee remarks. Build: comparison table for a first cruise.
1945. **Road trip stop planner** — Collect: "<route> road trip", `min_duration = 900`, `chapters`. Do: extract stops, distances, overnight towns. Build: stop-by-stop route plan.
1946. **Neighbourhood safety cross-check** — Collect: "<city> safety", "<city> areas to avoid". Do: map what creators claim about areas. Build: list to cross-check against official travel advisories.
1947. **Skincare opinion map** — Collect: "skincare routine", "<ingredient> explained", `min_views = 50000`. Do: map claims and disagreements. Build: questions to ask a dermatologist, not a routine prescription.
1948. **Interior style brief** — Collect: "<style> interior design", "<style> living room". Do: extract materials, colours, furniture rules. Build: style brief and shopping list for a room refresh.
1949. **Destination wedding plan** — Collect: "destination wedding planning", "<country> wedding legal". Do: extract timelines and pitfalls. Build: planning checklist with legal items to verify.
1950. **Coffee tasting guide** — Collect: "coffee tasting", "coffee cupping explained". Do: extract flavour terms and brew variables. Build: tasting sheet for a café's staff training.
1951. **Wine region tasting plan** — Collect: "<region> wine", "<region> winery tour". Do: extract wineries, styles, booking tips. Build: two-day tasting itinerary.
1952. **Short-let guest FAQ** — Collect: "airbnb host tips", "guest complaints airbnb", `top_comments = 40`. Do: extract what guests expect and complain about. Build: guest FAQ and check-in guide.
1953. **Pet relocation checklist** — Collect: "moving abroad with dog", "<country> pet import". Do: extract steps and timelines. Build: checklist to confirm with the destination's official rules.
1954. **Rail pass comparison** — Collect: "rail pass worth it", "<country> train travel". Do: compare passes vs point-to-point claims. Build: comparison table for an interrail route.
1955. **Budget travel dataset** — Collect: "daily budget <country>", "how much I spent <country>". Do: `yt.py export` stated figures. Build: CSV of creator-reported daily spend by country.
1956. **Weekly lifestyle newsletter** — Collect: 10 lifestyle creators via `only_channels`, `within = "week"`, `sponsorblock`. Do: summarise standout ideas. Build: weekly newsletter with links, summarised not republished.
1957. **Cultural studies corpus** — Collect: "<subculture>", `languages`, `channel_within = "year"`. Do: `yt.py export` for coding and analysis. Build: research corpus with metadata for a cultural studies thesis.
1958. **Graded listening list** — Collect: "<language> for learners", "slow <language>", `subtitles_only`. Do: rank videos by speed and vocabulary. Build: graded listening list from beginner to advanced.
1959. **Fragrance notes guide** — Collect: "fragrance review", "<perfume> review". Do: extract notes, longevity and comparisons. Build: guide of scents grouped by family.
1960. **Vinyl pressing guide** — Collect: "<album> pressing comparison", "vinyl collecting tips". Do: extract which pressings collectors rate and why. Build: pressing guide for a record shop.
1961. **Pet product opportunity report** — Collect: "pet product review", "<product> fail", `top_comments = 50`. Do: cluster owner complaints. Build: product opportunity report for a pet startup.
1962. **Travel memoir from your vlogs** — Collect: your own channel, `channel_max_videos = 500`, `timestamps`. Do: extract places, dates and moments per trip. Build: travel memoir outline with links back to each moment.
1963. **Retirement destination comparison** — Collect: "retire in <country>", "retiree <city>". Do: compare healthcare access, cost, visas as stated. Build: comparison table with items to check with professionals.

[↑ Contents](#contents)

## Work, society and industry

### Careers, jobs, HR & management

1964. **Role interview question bank** — Collect: "<role> interview questions", "<role> interview prep", `within = "year"`, `min_views = 5000`. Do: extract each question asked, group by type, note what good answers cover. Build: a question bank with STAR prompts.
1965. **Salary-talk reality map** — Collect: "<job title> salary", "how much I make as a <job>", `within = "year"`, `top_comments = 30`. Do: tabulate stated pay by city, seniority and year. Build: a pay-range sheet to check against official wage data.
1966. **Negotiation script kit** — Collect: "salary negotiation", "counter offer email" from recruiter channels, `remove_filler_words`. Do: pull exact phrasings and the objections they answer. Build: a fill-in negotiation script plus replies to 5 common pushbacks.
1967. **Daily layoff briefing** — Collect: "layoffs", "hiring freeze", `within = "today"`, `schedule_daily.bat`. Do: log companies, sectors and numbers mentioned plus sources cited. Build: a daily brief where each claim is tagged "verify before sharing".
1968. **Résumé review prompt** — Collect: "resume mistakes recruiter", "ATS resume", `within = "year"`, `top_comments = 20`. Do: list do/don't rules and where recruiters disagree. Build: a checklist and a Claude prompt that scores a CV against it.
1969. **Pre-interview employer brief** — Collect: "working at <company>", "day in the life <company>", `title_must_contain = "<company>"`. Do: summarise hours, teams, perks and complaints with `timestamps`. Build: a one-page brief plus questions to ask.
1970. **Leadership-principles flashcards** — Collect: "Amazon leadership principles interview", "behavioral interview examples", `subtitles_only`. Do: pair each principle with example stories and follow-ups. Build: Anki flashcards for nightly drill.
1971. **First-time manager course** — Collect: 8 management-coach channels, `channel_max_videos = 50`. Do: map -> reduce into `knowledge/management.md` (1:1s, feedback, delegation). Build: a 6-week self-study course with weekly exercises.
1972. **1:1 agenda rotation** — Collect: "one on one meeting questions", "skip level meeting". Do: harvest questions by goal (morale, growth, blockers, career). Build: a spreadsheet that rotates fresh 1:1 questions each week.
1973. **Return-to-office debate brief** — Collect: "return to office", "remote work policy", `within = "month"`, `top_comments = 30`. Do: list exec and worker arguments; tally comment themes. Build: a pros/cons brief for an HR policy meeting.
1974. **Structured interview scorecard** — Collect: "how to interview candidates", "structured interview", "hiring manager mistakes". Do: extract criteria and red flags per competency. Build: a scorecard with 1–5 behavioural anchors.
1975. **Tool onboarding SOP** — Collect: a vendor's public tutorial playlist via `channels`, `chapters`, `timestamps`. Do: turn the steps into ordered tasks for a new hire. Build: an onboarding SOP that links to the exact second of each demo.
1976. **Apprenticeship vs college tree** — Collect: "apprenticeship vs college", "is trade school worth it", `top_comments = 20`. Do: compare costs, earnings claims and time; mark figures to verify. Build: a decision tree for a school counselor.
1977. **Job-market mood chart** — Collect: "job market", "is anyone hiring", "<field> jobs", daily runs. Do: read attention per keyword in `trends.html`; summarise mood shifts weekly. Build: a weekly mood chart with three representative quotes.
1978. **What actually landed offers** — Collect: "how I got a job as", `max_views = 10000`, `within = "month"`. Do: count which tactics people credit (referrals, portfolios, cold email). Build: a ranked tactics table with example links.
1979. **LinkedIn profile audit** — Collect: "LinkedIn profile tips", "LinkedIn headline examples", `within = "year"`. Do: list concrete edits and algorithm claims, noting contradictions. Build: a before/after profile checklist.
1980. **Performance review phrase bank** — Collect: "performance review tips for managers", "self evaluation examples". Do: extract phrasings for strengths, gaps and goals. Build: a phrase bank by competency plus a self-review template.
1981. **Hard-conversation playbook** — Collect: "how to fire someone", "giving negative feedback", "PIP meeting" from HR channels. Do: extract steps and scripts; flag legal points for HR review. Build: a manager playbook for difficult talks.
1982. **Training video quiz bank** — Collect: a vendor's training playlist, `chapters`, `timestamps`. Do: write 10 questions per chapter with the answer's second-exact link. Build: an importable quiz bank for the company LMS.
1983. **Gen Z workplace research memo** — Collect: "Gen Z at work", "quiet quitting", `include_shorts`, `top_comments = 50`. Do: code themes and compare creator vs commenter views. Build: a research memo for an HR team.
1984. **Interview loop comparison** — Collect: "<company> software engineer interview experience" for 10 firms, `title_must_contain`. Do: list rounds, problem types and timelines reported. Build: a comparison table of interview loops.
1985. **Freelance rate calculator** — Collect: "freelance rates <skill>", "how much to charge as a freelancer", `max_views = 50000`. Do: extract quoted rates and pricing methods. Build: a rate calculator spreadsheet with method notes.
1986. **Team burnout check-in** — Collect: "burnout signs at work", "manager preventing burnout". Do: list warning signs and team practices mentioned, framed as opinion, not clinical guidance. Build: a monthly anonymous team pulse survey.
1987. **Employer-brand gap report** — Collect: competitor careers channels via `channels`, `channel_tabs` videos/shorts, `channel_within = "year"`. Do: compare culture and benefit claims and views per day. Build: an employer-branding gap report.
1988. **Leadership talk club pack** — Collect: "leadership keynote", `min_duration = 1200`, `min_views = 100000`. Do: summarise each talk's core idea and write discussion questions. Build: a monthly leadership discussion club pack.
1989. **Job title glossary** — Collect: "what does a <title> do" for 30 titles. Do: define daily tasks, tools and entry routes per title. Build: a glossary plus a titles-vs-skills matrix for career changers.
1990. **Certification payoff table** — Collect: "is <cert> worth it", "PMP worth it", `within = "year"`. Do: tabulate claimed cost, study hours, salary effect and disagreements. Build: a cert comparison table with a "verify" column.
1991. **Mock interview Claude skill** — Collect: "<role> mock interview", `min_duration = 900`. Do: build a knowledge base of questions, follow-ups and rubrics. Build: a Claude skill that runs mock interviews and scores answers.
1992. **HR change watchlist** — Collect: "HR trends", "pay transparency law", `within = "month"`. Do: list topics HR creators flag as changing and the jurisdictions named. Build: a list of items to confirm with employment counsel.
1993. **AI hiring tools debate** — Collect: "AI resume screening", "AI interview software", `top_comments = 30`. Do: map arguments from vendors, recruiters and candidates. Build: a balanced brief for a talent team choosing tools.
1994. **Remote team rituals menu** — Collect: "remote team building", "async standup", `max_views = 20000`. Do: list rituals with tools, cadence and pitfalls. Build: a menu of 30 rituals with setup steps.
1995. **Internship application calendar** — Collect: "summer internship timeline", "internship recruiting season", `within = "year"`. Do: extract deadlines mentioned by industry. Build: a month-by-month calendar for a student careers club.
1996. **Why-I-quit retention checklist** — Collect: "why I quit my job", `include_shorts`, `within = "month"`. Do: categorise reasons people give for leaving. Build: a retention-risk checklist managers review quarterly.
1997. **Business English phrasebook** — Collect: "business English meetings", "email phrases English", `subtitles_only`. Do: extract phrases for agreeing, pushing back, updates. Build: flashcards for non-native professionals.
1998. **Weekly manager digest** — Collect: 10 management channels, `channel_within = "week"`, scheduled runs. Do: summarise new ideas and practical tips. Build: an internal weekly management digest with links.
1999. **Job ad rewriter** — Collect: "how to write a job description", "inclusive job ads". Do: extract structure and wording do's and don'ts. Build: a JD template plus a Claude prompt that rewrites draft ads.
2000. **Career-gap comeback kit** — Collect: "career gap resume", "returning to work after kids". Do: collect ways people explain gaps in CVs and interviews. Build: script snippets and a return-to-work checklist.
2001. **Sales role-play cards** — Collect: "cold call role play", "objection handling", `min_duration = 600`. Do: extract objections with suggested rebuttals. Build: role-play cards for weekly sales team training.
2002. **Call-centre de-escalation module** — Collect: "customer service de-escalation", "call center training". Do: turn advice into ordered steps and sample lines. Build: a training module with scenario quizzes.
2003. **Four-day week evidence list** — Collect: "four day work week trial", `within = "year"`. Do: list studies cited, outcomes claimed and who claimed them. Build: a citation list to verify before writing a proposal.
2004. **Career-coach content gaps** — Collect: "career advice", `rising_views_per_day = 2000`, `within = "week"`. Do: find angles taking off and ones nobody covers well. Build: a content calendar for a career coach.
2005. **Design portfolio self-audit** — Collect: "UX portfolio review", "portfolio critique", `min_duration = 600`. Do: list critique points that recur across reviewers. Build: a portfolio self-audit checklist.
2006. **OKR writing worksheet** — Collect: "OKR examples", "how to set OKRs". Do: extract good and bad examples with reasons. Build: a worksheet teams fill in at quarterly planning.
2007. **Relocation question list** — Collect: "moving to Germany for work", "work visa jobs", `translate`. Do: list steps creators describe, marked to verify with official sources. Build: questions for an immigration advisor.
2008. **CEO leadership comparison** — Collect: "<CEO name> interview" for 8 public CEOs, `min_duration = 1800`. Do: extract stated views on hiring and culture. Build: a comparison table of public leadership philosophies with `timestamps`.
2009. **Networking CRM template** — Collect: "networking tips introvert", "coffee chat questions". Do: extract opening lines and follow-up timing. Build: a networking tracker spreadsheet with scripts.
2010. **Case interview packs** — Collect: "case interview example", "consulting case walkthrough", `min_duration = 1200`. Do: extract frameworks and solution paths. Build: practice case packs with outline solutions.
2011. **Job scam red flags** — Collect: "job scam", "fake recruiter", `within = "month"`. Do: list red flags people report. Build: a candidate safety checklist for a university careers centre.
2012. **In-demand skills chart** — Collect: "skills employers want", "<field> skills in demand", `within = "year"`. Do: count skill mentions across transcripts. Build: a ranked skills chart for a bootcamp's curriculum planning.
2013. **Neurodiversity awareness guide** — Collect: "ADHD at work", "autism workplace accommodations". Do: list accommodations people describe as lived experience, not advice. Build: a manager awareness guide with questions for HR.
2014. **Answer examples via find** — Collect: all past interview-prep runs. Do: `yt.py find "tell me about yourself"` and compare answers. Build: a curated sheet of example answers with second-exact links.
2015. **Shift scheduling rules** — Collect: "restaurant manager scheduling", "shift scheduling tips". Do: extract rules of thumb on coverage, fairness, swaps. Build: a scheduling checklist for frontline managers.
2016. **Promotion brag document** — Collect: "how to get promoted", "promotion packet". Do: extract the evidence types managers say matter. Build: a brag-document template to update monthly.
2017. **Cross-country remote work brief** — Collect: "Homeoffice", "télétravail", "リモートワーク", `translate = "en"`. Do: compare remote-work debates by country. Build: an international HR comparison brief.

[↑ Contents](#contents)

### Law, policy, government & civic life

2018. **Bill hearing explainer** — Collect: "<bill name> hearing", official channels via `only_channels`, `min_duration = 1800`, `timestamps`. Do: summarise each witness and member's points. Build: a neutral bill explainer with quote links.
2019. **Policy issue map** — Collect: "<policy> debate", "<policy> pros and cons", `within = "year"`. Do: list each side's strongest arguments and evidence cited. Build: an issue map for a newsroom explainer.
2020. **Court case brief** — Collect: "<case name> oral argument", "<case> explained". Do: summarise the justices' questions, each side's arguments and commentator views. Build: an informational case brief for students.
2021. **Official promise tracker** — Collect: official government `channels`, `channel_within = "week"`, daily runs. Do: log commitments and announcements with dates. Build: a promise tracker spreadsheet with links.
2022. **Debate positions table** — Collect: candidate debates, `title_must_contain = "debate"`, `timestamps`. Do: extract each candidate's stated position by issue. Build: a side-by-side positions table, no endorsements.
2023. **Civics unit** — Collect: "how a bill becomes law", "separation of powers explained", `subtitles_only`. Do: build a knowledge base by concept. Build: a 4-week high-school civics unit with quizzes.
2024. **City council digest** — Collect: the city's channel, `channel_tabs = streams`, `min_duration = 3600`. Do: summarise agenda items, votes and public comment themes. Build: a weekly plain-language digest for residents.
2025. **Proposed rule comment prep** — Collect: "<agency> proposed rule", `within = "month"`. Do: list what stakeholders say changes and sections they cite. Build: a reading guide for the official docket before commenting.
2026. **Tenant rights questions** — Collect: "tenant rights <state>", "eviction process <state>". Do: compile claims, each tagged "verify with statute or legal aid". Build: a question list for a legal aid clinic visit.
2027. **Viral claim queue** — Collect: "<policy topic>", `rising_views_per_day = 5000`, `within = "today"`. Do: list factual claims with second-exact links. Build: a prioritised fact-check queue for a newsroom.
2028. **Health systems compared** — Collect: "healthcare system <country>" for 6 countries, `translate`. Do: compare how locals describe access, cost and waits. Build: a comparison table for a policy seminar.
2029. **Testimony dataset** — Collect: a year of hearing playlists, then `yt.py export`. Do: tag speakers, roles and topics in the .jsonl. Build: a dataset for researchers studying expert testimony.
2030. **Legal terms flashcards** — Collect: "legal terms explained", "what is habeas corpus", `max_duration = 900`. Do: extract plain-language definitions with examples. Build: flashcards for law-curious beginners.
2031. **Business formation questions** — Collect: "LLC vs sole proprietorship", "business license <state>". Do: compile steps creators describe, marked to verify. Build: a question list for an accountant or attorney.
2032. **Think-tank agenda watch** — Collect: think-tank channels across the spectrum via `channels`, `channel_within = "week"`. Do: note which topics each emphasises. Build: a balanced weekly policy agenda watch.
2033. **Ballot measure sheet** — Collect: "Proposition <n>", "<state> ballot measure", `within = "month"`. Do: summarise yes and no arguments and backers named. Build: a neutral explainer linking the official measure text.
2034. **Jury duty FAQ** — Collect: "jury duty what to expect", "jury selection explained", `max_views = 50000`. Do: extract the process and common surprises. Build: a first-timer FAQ checked against the court's website.
2035. **Model UN research notes** — Collect: "<issue> UN speech", UN channels, `translate`. Do: extract each country's stated position. Build: delegate research notes for a position paper.
2036. **Budget hearing explainer** — Collect: "<city> budget hearing", "budget explained". Do: list where officials say money goes and changes year on year. Build: an infographic outline with figures to verify.
2037. **Advocacy framing analysis** — Collect: advocacy channels on all sides of an issue via `channels`. Do: compare frames, vocabulary and appeals. Build: a framing analysis report for a communications class.
2038. **Amendment history lectures** — Collect: "<amendment> history", `min_duration = 900`, `within = "any"`. Do: build a chronology of cases and debates. Build: a timeline plus lecture notes.
2039. **School board comment tally** — Collect: the district's channel, `channel_tabs = streams`. Do: categorise public comment topics per meeting. Build: a themed tally for a parent-teacher association.
2040. **Ruling reaction roundup** — Collect: "<ruling> reaction", `within = "today"`, `top_comments = 30`. Do: summarise legal commentators' and public reactions. Build: a next-day explainer of what changed and what's disputed.
2041. **Floor speech archive** — Collect: "<legislator> floor speech", `within = "any"`. Do: extract the rationale given per vote or bill. Build: a searchable archive with `timestamps` for journalists.
2042. **Privacy law landscape** — Collect: "GDPR explained", "state privacy law", "EU AI Act". Do: compare requirements as creators describe them. Build: a comparison table a product team verifies with counsel.
2043. **Civic tech idea list** — Collect: "civic tech", "open government data". Do: list problems, tools and datasets mentioned. Build: a hackathon project list with data sources.
2044. **Debate evidence cards** — Collect: the season's resolution topic, `min_duration = 600`, `timestamps`. Do: extract quotable claims with the source each speaker cites. Build: evidence cards to check against originals.
2045. **Civic action how-to** — Collect: "how to call your representative", "testify at city council". Do: extract steps, scripts and timing tips. Build: a step-by-step civic participation guide.
2046. **Benefits application friction** — Collect: "<program> application experience", `max_views = 20000`. Do: catalogue friction points applicants report. Build: a usability issue list for a government digital service team.
2047. **Foreign parliament brief** — Collect: a foreign parliament's channel, `translate = "en"`, `channel_within = "week"`. Do: summarise sessions and votes. Build: an English weekly brief for analysts.
2048. **Political rhetoric lesson** — Collect: "inaugural address", `within = "any"`, `min_duration = 600`. Do: compare themes and rhetorical devices across eras. Build: a lesson plan on political speech.
2049. **Law firm education plan** — Collect: "<law topic> explained", `rising_views_per_day`, `top_comments = 50`. Do: find questions and misconceptions the public raises. Build: a content plan for public-education videos.
2050. **Citizenship test cards** — Collect: "US citizenship test questions", "civics test 100 questions", `subtitles_only`. Do: pair each question with the explanation given. Build: study flashcards checked against the official list.
2051. **Zoning reform brief** — Collect: "zoning reform", "housing affordability debate". Do: map arguments and city examples cited. Build: a briefing for a neighbourhood association meeting.
2052. **Press briefing Q&A log** — Collect: an agency's channel, `channel_tabs = streams`, daily runs. Do: extract each question and the answer given. Build: a daily Q&A table with second-exact links.
2053. **Stakeholder role-play game** — Collect: "<policy> explained" from varied viewpoints. Do: build stakeholder profiles with stated goals and arguments. Build: a classroom role-play game with cards.
2054. **Climate talks tracker** — Collect: "COP climate negotiations", `within = "week"`, `translate`. Do: log statements by delegation. Build: a negotiation positions tracker.
2055. **Vote counting explainer** — Collect: "how votes are counted", "election audit explained". Do: describe the process steps creators show. Build: a civics-class explainer that links official election office pages.
2056. **Small claims prep** — Collect: "small claims court tips", "how to file small claims". Do: extract steps and preparation tips. Build: a checklist plus questions for the court's self-help centre.
2057. **Session bill watchlist** — Collect: "<state> legislative session", `within = "week"`. Do: rank bills by attention in `trends.html`. Build: a priority bill watchlist for an advocacy coalition.
2058. **Newcomer civic guide** — Collect: civic explainers in residents' languages, `translate`. Do: extract the basics newcomers ask about (IDs, councils, services). Build: a simplified civic guide for a resettlement agency.
2059. **Campaign ad message dataset** — Collect: "campaign ad", `max_duration = 120`, `include_shorts`, `within = "month"`. Do: tag themes and claims per ad. Build: a dataset for political communication researchers.
2060. **Think-tank report summaries** — Collect: report launch events, `min_duration = 1800`. Do: summarise findings and critics' responses. Build: one-page summaries for a legislative staffer.
2061. **Bar exam outlines** — Collect: "bar exam contracts", "<subject> law lecture", `min_duration = 1800`. Do: extract rules and exceptions. Build: outlines and flashcards to verify against casebooks.
2062. **Records request toolkit** — Collect: "FOIA request tutorial", "public records request". Do: extract steps, wording and follow-up tips. Build: a request template plus a tracking sheet.
2063. **Discourse timeline** — Collect: "<policy>", `within = "any"`, `published_after` per year. Do: describe how arguments shifted year by year. Build: a timeline of shifts with dated quotes.
2064. **Hearing search answers** — Collect: a year of committee hearings. Do: `yt.py find "<term>"` to see who said what. Build: answers to reporters' questions with links to the exact second.
2065. **Policy research assistant** — Collect: hearings and explainers; map -> reduce into `knowledge/`. Do: let Claude Code answer via `CLAUDE.md`. Build: an assistant that answers policy questions with citations.
2066. **50-state comparison** — Collect: "<issue> <state>" with `[[keyword_settings]]` per state. Do: compare approaches states take. Build: a 50-state table to verify against statutes.
2067. **Disaster aid guide** — Collect: "FEMA assistance how to apply", `within = "month"`. Do: extract steps and documents mentioned. Build: a community-centre handout linking official pages to verify.
2068. **Youth council playbook** — Collect: "youth council", "student government ideas". Do: extract structures, projects and pitfalls. Build: a playbook for a new municipal youth council.
2069. **Town hall concern taxonomy** — Collect: policy explainers, `top_comments = 100`. Do: categorise commenter concerns, noting they aren't representative. Build: a concerns taxonomy for a town hall agenda.
2070. **Witness FAQ** — Collect: "what to expect testifying in court", "being a witness". Do: extract process and etiquette tips. Build: a witness FAQ to review with the victim-witness office.
2071. **Balanced policy newsletter** — Collect: 15 explainer channels across the spectrum, weekly runs. Do: summarise how each side framed the week's issues. Build: a newsletter with labelled framing sections.
2072. **AI regulation tracker** — Collect: "AI regulation", "AI executive order", `within = "week"`, `title_must_contain = "AI"`. Do: log announced measures by jurisdiction. Build: a dated tracker to verify against official texts.

[↑ Contents](#contents)

### Nonprofits, community, local business & causes

2073. **Donor ask script** — Collect: "nonprofit fundraising tips", "how to ask for donations". Do: extract ask structures and phrasings. Build: a donor call script plus three appeal email templates.
2074. **Grant proposal template** — Collect: "grant writing tips", "grant proposal example", `min_duration = 900`. Do: section-by-section advice and reviewer pet peeves. Build: a proposal template with a pre-submit checklist.
2075. **Volunteer orientation SOP** — Collect: "volunteer orientation", "volunteer management". Do: extract onboarding steps and retention tips. Build: an orientation SOP and handbook outline.
2076. **Neighbourhood news digest** — Collect: local TV station `channels`, `channel_within = "today"`, `schedule_daily.bat`. Do: summarise stories by area. Build: a daily neighbourhood email newsletter.
2077. **Café competitor review** — Collect: "best coffee <city>", `max_views = 20000`, `top_comments = 20`. Do: list what reviewers praise and complain about nearby. Build: an improvement list for a café owner.
2078. **Menu pricing sheet** — Collect: "menu engineering", "restaurant food cost". Do: extract costing formulas and layout tips. Build: a menu pricing spreadsheet for an independent restaurant.
2079. **Green small business plan** — Collect: "sustainable packaging small business", "zero waste business". Do: list actions with costs and savings claimed. Build: an action plan ranked by cost and effort.
2080. **Charity due diligence** — Collect: "<charity> review", "how to evaluate a charity". Do: note claims about impact and overhead to check against filings. Build: a donor's due-diligence question list.
2081. **Community garden start-up** — Collect: "start a community garden", `max_views = 30000`. Do: extract steps, budgets and land-use pitfalls. Build: a launch plan with budget template.
2082. **Mutual aid organiser guide** — Collect: "mutual aid how to start", "mutual aid network". Do: extract structures, tools and burnout warnings. Build: an organiser's starter guide.
2083. **Fundraiser idea matrix** — Collect: "charity fundraiser ideas", `include_shorts`, `within = "year"`. Do: score ideas by cost, effort and money raised claims. Build: an idea matrix for a PTA.
2084. **Peer nonprofit video audit** — Collect: peer nonprofits via `channels`, `channel_within = "year"`. Do: compare formats by views per day. Build: a content strategy memo for the comms team.
2085. **Board member training** — Collect: "nonprofit board responsibilities", "board meeting tips". Do: summarise duties and good practices. Build: a new-board-member training deck outline.
2086. **Shop-local campaign** — Collect: "small business saturday ideas", "shop local campaign". Do: extract tactics and timing. Build: a campaign calendar for a chamber of commerce.
2087. **Market vendor checklist** — Collect: "farmers market vendor tips", `max_views = 50000`. Do: extract display, pricing and setup lessons. Build: a market-day packing and setup checklist.
2088. **Donor stewardship calendar** — Collect: "donor retention", "thank donors ideas". Do: extract touchpoints and timing. Build: a 12-month stewardship calendar.
2089. **Logic model builder** — Collect: "theory of change", "nonprofit impact measurement". Do: extract frameworks and indicator examples. Build: a logic model template with an indicator list.
2090. **Resident concerns brief** — Collect: "<town> <issue>", `within = "week"`, `max_views = 5000`. Do: summarise what residents are posting about. Build: a weekly concerns brief for a community organisation.
2091. **Disaster volunteer readiness** — Collect: "disaster relief volunteer", "Red Cross volunteer training". Do: extract roles, training and kit lists. Build: a volunteer readiness checklist.
2092. **Pantry distribution SOP** — Collect: "food pantry distribution", "food bank operations". Do: extract flow, stations and roles. Build: a distribution-day SOP with staffing chart.
2093. **Local podcast guest prep** — Collect: local owners' interviews, `max_views = 2000`. Do: summarise each owner's story and talking points. Build: guest prep sheets for a hometown podcast.
2094. **Cause message testing** — Collect: "<cause> awareness", `top_comments = 50`. Do: compare which messages draw supportive vs sceptical comments. Build: a message matrix for the next campaign.
2095. **Town history timeline** — Collect: "<town> history", `within = "any"`. Do: extract dated events and people with sources mentioned. Build: a timeline for a historical society exhibit.
2096. **Teen volunteer recruitment** — Collect: "volunteering for teens", "volunteer hours college application". Do: find what motivates teens. Build: recruitment flyer copy and a parent FAQ.
2097. **Humanitarian digest** — Collect: NGO channels via `channels`, `channel_within = "month"`, `translate`. Do: summarise field updates by region. Build: a monthly humanitarian situation digest.
2098. **Local climate proposals** — Collect: "city climate action plan", "community solar". Do: list initiatives with examples and costs cited. Build: a proposal shortlist for a green group.
2099. **Repair café runbook** — Collect: "repair cafe how to start", "fix it clinic". Do: extract roles, tools and liability notes. Build: an event-day runbook.
2100. **Owner Q&A skill** — Collect: small business advice channels; map -> reduce into `knowledge/`. Do: answer owner questions with links, flagging tax and legal items for pros. Build: a Claude skill for a business association.
2101. **Franchise questions** — Collect: "buying a franchise review", "franchise regrets". Do: list cost and support claims to check in the disclosure document. Build: questions for franchisors and current owners.
2102. **Nonprofit CRM comparison** — Collect: "CRM for nonprofits", "Bloomerang vs", `within = "year"`. Do: extract features, prices and complaints. Build: a comparison table for a small charity.
2103. **Weekend events list** — Collect: "<city> events this weekend", `within = "week"`. Do: pull event names, dates and places. Build: a weekly events list for a community Facebook group.
2104. **Petition campaign toolkit** — Collect: "how to organize a petition", "community organizing". Do: extract tactics and timelines. Build: an advocacy toolkit for a tenants' group.
2105. **Charity shop pricing guide** — Collect: "thrift store pricing", "charity shop volunteer". Do: extract pricing rules and sorting flows. Build: a pricing guide for volunteers.
2106. **Impact story template** — Collect: "nonprofit storytelling", "beneficiary story video". Do: extract story structures and consent practices. Build: a story collection form for the annual report.
2107. **Sponsorship tier sheet** — Collect: "corporate sponsorship nonprofit", "sponsorship deck". Do: extract tiers and benefits offered. Build: a sponsor deck outline with a tier sheet.
2108. **Main street case studies** — Collect: "main street revitalization", "downtown vacancies". Do: summarise towns' tactics and results claimed. Build: a case study list for a business improvement district.
2109. **Adoption event playbook** — Collect: "shelter adoption event", "foster program tips". Do: extract promotion and logistics tips. Build: an adoption-event playbook for an animal shelter.
2110. **Venue accessibility audit** — Collect: "accessible small business tips", "wheelchair accessibility review". Do: list barriers people describe. Build: an audit checklist, not a legal compliance opinion.
2111. **Library program calendar** — Collect: "library program ideas", "library makerspace". Do: extract programs with costs and audiences. Build: a season programme calendar.
2112. **Greenwashing red flags** — Collect: "greenwashing examples", "<brand> sustainability claims". Do: compare brand claims with critiques. Build: a red-flags checklist for an ethical shopping group.
2113. **Church livestream setup** — Collect: "church livestream setup", "small church audio". Do: extract gear lists and settings. Build: an AV setup guide for volunteers.
2114. **Gala run-of-show** — Collect: "gala planning", "charity auction tips". Do: extract timings and roles. Build: a minute-by-minute run-of-show.
2115. **Local service price benchmark** — Collect: "dog grooming prices <city>", `max_views = 10000`. Do: extract price points mentioned. Build: a local pricing benchmark for a new groomer.
2116. **Co-op formation checklist** — Collect: "how to start a co-op", "worker cooperative". Do: extract formation steps and governance models. Build: a checklist to review with a co-op advisor.
2117. **Hyperlocal creator directory** — Collect: "<city>", `max_views = 3000`, `within = "month"`. Do: list channels covering the area and their topics. Build: a directory for local partnership outreach.
2118. **Cleanup event kit** — Collect: "beach cleanup organize", "litter pick event". Do: extract logistics and safety tips. Build: an event kit with a safety checklist.
2119. **B Corp readiness** — Collect: "B Corp certification", "carbon footprint small business". Do: extract steps, costs and effort claimed. Build: a readiness checklist for a small firm.
2120. **Shop shorts plan** — Collect: "small business TikTok ideas", `include_shorts`, `rising_views_per_day = 1000`. Do: find formats rising this week. Build: a 30-day short-video plan.
2121. **Social enterprise models** — Collect: "social enterprise examples", "buy one give one". Do: compare revenue and impact models. Build: a model comparison table for founders.
2122. **Neighbourhood meeting kit** — Collect: "run a neighborhood association meeting", "Robert's rules explained". Do: extract agenda and procedure basics. Build: an agenda template and rules cheat sheet.
2123. **Campaign timing calendar** — Collect: "<cause>" keywords on daily runs. Do: spot attention spikes in `trends.html`. Build: a calendar showing when to time campaign pushes.
2124. **Immigrant community needs** — Collect: videos by local immigrant creators in their languages, `translate = "en"`. Do: summarise needs and concerns raised. Build: a needs summary for a social service provider.

[↑ Contents](#contents)

### Industries & trades

2125. **Estimating template** — Collect: "construction estimating tutorial", "material takeoff". Do: extract steps and markup rules. Build: an estimating checklist and spreadsheet template.
2126. **Electrician exam cards** — Collect: "journeyman electrician exam", "NEC code explained". Do: extract rules and calculations. Build: flashcards to verify against the current code book.
2127. **Plumbing fault tree** — Collect: "plumber explains <problem>", `min_views = 20000`. Do: map symptom -> cause -> fix sequences. Build: a troubleshooting decision tree for apprentices.
2128. **5S audit sheet** — Collect: "lean manufacturing", "5S", "kaizen examples". Do: extract audit criteria and examples. Build: a scored 5S audit sheet for the shop floor.
2129. **CNC setup checklist** — Collect: "CNC machining tips", machinist `channels`. Do: extract setup steps and claims to test. Build: a machine setup checklist plus a test log.
2130. **Cattle market log** — Collect: "cattle market report", `within = "today"`, daily runs. Do: log commentary on prices and drivers. Build: a daily market commentary log for a ranch.
2131. **Crop disease field guide** — Collect: "<crop> disease identification", `min_duration = 300`. Do: extract symptoms and look-alikes. Build: a field guide to confirm with the extension service.
2132. **Freight market brief** — Collect: "freight market update", "trucking rates", `within = "week"`. Do: summarise rate and capacity commentary. Build: a weekly brief for a small carrier.
2133. **Forklift safety quiz** — Collect: "forklift safety", "warehouse picking tips". Do: extract procedures and hazards. Build: a warehouse SOP and safety quiz.
2134. **Energy earnings table** — Collect: "<oil company> earnings call", `min_duration = 1800`. Do: extract guidance on output, capex and prices. Build: a quarterly comparison table.
2135. **Solar install checklist** — Collect: "solar panel installation", "solar install mistakes". Do: extract steps and common errors. Build: an install checklist for a new crew.
2136. **A&P study guide** — Collect: "A&P mechanic", "aircraft inspection". Do: extract topics and procedures. Build: a study guide checked against official handbooks.
2137. **Checkride oral bank** — Collect: "private pilot checkride", "oral exam". Do: extract examiner questions. Build: an oral question bank to review with an instructor.
2138. **Patient flow ideas** — Collect: "hospital patient flow", "ED throughput". Do: extract interventions and results claimed. Build: an improvement list for an operations committee.
2139. **SBAR handoff template** — Collect: "nurse report sheet", "SBAR handoff". Do: extract structures. Build: a handoff template to check with unit policy.
2140. **Front desk SOP** — Collect: "hotel front desk training", "check-in process". Do: extract steps and scripts. Build: a front desk SOP for a boutique hotel.
2141. **Auto industry brief** — Collect: "EV sales", "<automaker> earnings", `within = "week"`. Do: summarise sales, pricing and plant news. Build: a weekly auto industry brief.
2142. **Fault-code notes** — Collect: "<car model> P0300 diagnosis", `min_duration = 600`. Do: extract tests and fixes per code. Build: diagnostic notes for a repair shop.
2143. **HVAC sizing questions** — Collect: "Manual J explained", "HVAC sizing". Do: extract sizing principles and mistakes. Build: questions homeowners can ask a contractor.
2144. **6G weld test plan** — Collect: "welding certification test", "6G pipe weld". Do: extract technique tips and fail reasons. Build: a practice plan for the certification test.
2145. **Port disruption alerts** — Collect: "port congestion", "shipping rates", daily runs. Do: flag new disruptions. Build: an alert digest for an importer.
2146. **Toolbox talk scripts** — Collect: "toolbox talk", "fall protection". Do: extract hazards and controls. Build: 52 weekly toolbox talk scripts for a contractor.
2147. **Contractor bid template** — Collect: "how to bid jobs contractor", "contractor pricing". Do: extract pricing methods. Build: a bid template for a remodeling firm.
2148. **Kitchen prep system** — Collect: "kitchen line setup", "prep list". Do: extract par and station systems. Build: a prep list system for a restaurant kitchen.
2149. **Precision ag comparison** — Collect: "precision agriculture", "farm drones", `within = "year"`. Do: extract costs and payback claims. Build: a tech comparison table for a farm.
2150. **Calving season checklist** — Collect: "calving season tips", `max_views = 50000`. Do: extract prep and warning signs. Build: a calving checklist to review with a vet.
2151. **CDL pre-trip script** — Collect: "CDL pre-trip inspection". Do: extract inspection order and wording. Build: a memorisation script and checklist.
2152. **Energy tech opinion map** — Collect: "grid storage", "small modular reactor", `min_duration = 1200`. Do: map experts' claims on cost and timelines. Build: a technology opinion map.
2153. **Lineworker glossary** — Collect: "lineman training", "power line work". Do: extract terms and equipment. Build: a glossary for apprentices.
2154. **Trade show product list** — Collect: "IMTS", "Hannover Messe", `translate`, `within = "month"`. Do: extract new products shown. Build: a product list for a buyer.
2155. **Equipment buyer table** — Collect: "<excavator model> review", "<tractor> problems", `top_comments = 30`. Do: extract issues owners report. Build: a buyer's comparison table.
2156. **Trim technique library** — Collect: "finish carpentry tips", "trim install". Do: extract techniques with `timestamps`. Build: a technique library for a crew.
2157. **Cabin comparison table** — Collect: "<airline> business class review", `min_views = 10000`. Do: extract seat and service details. Build: a comparison table for a travel manager.
2158. **Medical billing module** — Collect: "medical billing training", "denial management". Do: extract workflows and denial causes. Build: a training module for billing staff.
2159. **PLC exercise course** — Collect: "PLC programming tutorial", "ladder logic". Do: extract exercises. Build: a practice exercise course for maintenance techs.
2160. **ISO 9001 audit prep** — Collect: "ISO 9001 audit", "internal audit". Do: extract evidence auditors ask for. Build: an audit prep checklist.
2161. **Roof inspection report** — Collect: "roof inspection", "hail damage". Do: extract inspection points. Build: a report template for a roofing company.
2162. **Hotel pricing playbook** — Collect: "hotel revenue management", "dynamic pricing hotel". Do: extract pricing rules. Build: a revenue management playbook.
2163. **Trades shortage report** — Collect: "skilled trades shortage", `within = "year"`. Do: summarise causes and fixes argued. Build: a report for a workforce board.
2164. **Fleet PM schedule** — Collect: "fleet maintenance tips", "telematics". Do: extract service intervals and practices. Build: a preventive maintenance schedule.
2165. **Code change summary** — Collect: "IRC code changes", "building code update", `within = "year"`. Do: extract changes discussed. Build: a summary to verify with the official code.
2166. **Part 107 business notes** — Collect: "Part 107", "drone inspection business". Do: extract test topics and pricing. Build: study notes and a business plan outline.
2167. **HACCP worksheet** — Collect: "HACCP plan", "food safety audit". Do: extract hazards and control points. Build: a HACCP worksheet to review with a food safety pro.
2168. **Operator training drills** — Collect: "excavator operator tips", `max_views = 50000`. Do: extract skills and drills. Build: operator training drills for a new hire.
2169. **Regenerative trial plan** — Collect: "regenerative agriculture results", `max_views = 50000`. Do: extract yield and cost claims. Build: a trial plan to test on a field plot.
2170. **Courier route SOP** — Collect: "last mile delivery", "route optimization". Do: extract routing practices. Build: a route-planning SOP for a small courier.
2171. **Plumber channel plan** — Collect: trade channels, `rising_views_per_day = 500`, `within = "month"`. Do: find formats that grow. Build: a content plan for a plumbing company's channel.
2172. **Hospital PAR levels** — Collect: "hospital supply chain", "PAR levels". Do: extract stocking methods. Build: a PAR level SOP for a unit.
2173. **Punch list kit** — Collect: "construction punch list", "CPM schedule". Do: extract closeout steps. Build: a punch list template and weekly meeting agenda.
2174. **Service advisor scripts** — Collect: "service advisor training", "car dealership service". Do: extract scripts. Build: training scripts for a dealership.
2175. **Energy audit checklist** — Collect: "home energy audit", "blower door test". Do: extract steps and findings. Build: an auditor checklist.
2176. **PdM rollout plan** — Collect: "vibration analysis", "predictive maintenance". Do: extract tools and phases. Build: a predictive maintenance rollout plan.
2177. **CRM case studies** — Collect: "NTSB report explained", "accident analysis", `min_duration = 900`. Do: extract causal factors. Build: crew resource management case studies.
2178. **Overseas factory notes** — Collect: Japanese and German factory tours, `translate = "en"`. Do: extract practices. Build: best-practice notes for a plant manager.
2179. **Trade school curriculum** — Collect: trade `channels`, `channel_max_videos = 200`; map -> reduce. Do: organise by skill. Build: a semester curriculum with video segment links.

[↑ Contents](#contents)
