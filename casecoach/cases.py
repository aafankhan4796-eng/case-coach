"""Practice cases. All companies and figures are fictional and written for practice.

Each case is a list of steps. A step asks one question, may show an exhibit (a small table)
and has a model answer that is revealed after the candidate has tried.
"""

CASES = [
    {
        "id": "freshbrew",
        "title": "FreshBrew Coffee",
        "type": "Profitability",
        "difficulty": "Beginner",
        "minutes": 25,
        "prompt": (
            "Your client is FreshBrew, a coffee chain with 120 cafés across the Netherlands. "
            "Revenue has been flat at about €60 million a year, but over the last two years profit has "
            "fallen by 30%. The CEO wants to know why profit has fallen and what FreshBrew should do "
            "to restore it."
        ),
        "clarifying": (
            "Revenue: flat at €60m in both years. Profit: €6.0m two years ago, €4.2m now. "
            "Goal: get back to €6m within 12 months. Number of cafés and opening hours unchanged. "
            "Competitors' prices have risen by about 5%."
        ),
        "steps": [
            {
                "question": "How would you structure this problem? Walk through the areas you would investigate.",
                "model_answer": (
                    "Profit = revenue − costs. Revenue is flat, so start with costs, but check revenue mix too.\n\n"
                    "1. Costs: split into fixed (rent, staff, overheads) and variable (coffee, milk, packaging). "
                    "Which line grew, and is it price (e.g. wage or bean prices) or volume (more hours, more waste)?\n"
                    "2. Revenue: flat in total, but check price vs volume and product mix; flat revenue could hide "
                    "fewer customers paying more.\n"
                    "3. Market: are competitors seeing the same cost pressure, and how did they respond?\n"
                    "4. Solutions: pricing, cost efficiency, portfolio (underperforming cafés)."
                ),
            },
            {
                "question": "Here is FreshBrew's cost base. What stands out?",
                "exhibit": {
                    "columns": ["Cost line", "Two years ago (€m)", "Now (€m)"],
                    "rows": [
                        ["Staff", 18.0, 19.5],
                        ["Rent", 12.0, 12.2],
                        ["Coffee, milk, food", 15.0, 15.1],
                        ["Other overheads", 9.0, 9.0],
                        ["Total costs", 54.0, 55.8],
                    ],
                },
                "model_answer": (
                    "Total costs rose €1.8m (54.0 → 55.8), exactly the profit drop (6.0 → 4.2).\n\n"
                    "Staff explains €1.5m of the €1.8m, about 83%. Staff costs grew 8.3% (1.5 ÷ 18). "
                    "Rent (+€0.2m) and ingredients (+€0.1m) are small. So the next question is why staff costs rose: "
                    "more hours worked, or a higher cost per hour?"
                ),
            },
            {
                "question": "Staff hours worked were 750,000 in both years. What does that tell you, and what was the cost per hour?",
                "model_answer": (
                    "Hours are flat, so the increase is all rate, not volume.\n\n"
                    "Cost per hour: €18.0m ÷ 750k = €24 two years ago; €19.5m ÷ 750k = €26 now, +8.3%. "
                    "Likely causes: minimum wage and collective agreement increases plus higher employer costs. "
                    "This is a market-wide pressure, not bad management, which supports a pricing response."
                ),
            },
            {
                "question": "Brainstorm: what could FreshBrew do to restore profit to €6m?",
                "model_answer": (
                    "Revenue levers: raise prices (competitors are already up ~5%), upsell food and larger sizes, "
                    "loyalty app to raise visit frequency, extend high-margin products.\n\n"
                    "Cost levers: smarter scheduling to match staff to footfall, self-order kiosks or app ordering "
                    "at peak times, renegotiate rent at lease renewal, close or reformat loss-making cafés.\n\n"
                    "Prioritise by size, speed and risk: pricing is fastest and largest; scheduling is next."
                ),
            },
            {
                "question": "The average ticket is €4.00. If volume stays the same, what price increase recovers the €1.8m?",
                "model_answer": (
                    "€1.8m ÷ €60m = 3% price increase. €4.00 × 1.03 = €4.12, about 12 cents per ticket.\n\n"
                    "With competitors up ~5%, a 3% increase is unlikely to lose many customers. "
                    "Even if volume fell 1%, the price rise still recovers most of the gap."
                ),
            },
            {
                "question": "The CEO walks in. Give your recommendation in under a minute.",
                "model_answer": (
                    "\"FreshBrew should raise prices by about 3% and tighten staff scheduling.\n\n"
                    "Profit fell €1.8m because staff cost per hour rose 8.3% from wage increases, while hours stayed flat. "
                    "A 3% price rise, 12 cents on a €4 coffee, recovers the full €1.8m, and competitors have already "
                    "raised prices by about 5%, so the risk to volume is low. Matching staff hours to footfall "
                    "protects against further wage increases.\n\n"
                    "Risks: customer reaction, so test in a few cafés first. Next steps: price test in 10 cafés for "
                    "4 weeks, scheduling pilot, review loss-making cafés.\""
                ),
            },
        ],
    },
    {
        "id": "velonova",
        "title": "VeloNova enters Germany",
        "type": "Market entry",
        "difficulty": "Intermediate",
        "minutes": 30,
        "prompt": (
            "VeloNova is a Dutch maker of premium e-bikes with €40m in revenue, almost all in the Netherlands. "
            "Growth at home is slowing, and the board is considering entering Germany. "
            "Should VeloNova enter the German market?"
        ),
        "clarifying": (
            "Goal: at least €40m extra revenue and a positive operating profit by year 3. "
            "Entry would be through its own showrooms in large cities plus online sales. "
            "VeloNova's bikes average €3,500, positioned in the premium segment."
        ),
        "steps": [
            {
                "question": "How would you structure this decision?",
                "model_answer": (
                    "1. Market attractiveness: size and growth of German e-bikes, especially premium.\n"
                    "2. Competition: who leads premium, how fragmented, brand loyalty.\n"
                    "3. VeloNova's ability to win: brand, product edge, distribution, service network.\n"
                    "4. Economics: revenue potential, costs of entry, profit and payback vs the goal.\n"
                    "5. Entry mode and risks: own showrooms vs dealers vs partnership."
                ),
            },
            {
                "question": "Use these assumptions to estimate VeloNova's year-3 revenue in Germany.",
                "exhibit": {
                    "columns": ["Assumption", "Value"],
                    "rows": [
                        ["German e-bikes sold per year", "2,000,000"],
                        ["Premium segment (over €3,000), share of units", "30%"],
                        ["VeloNova target share of premium by year 3", "2%"],
                        ["Average selling price", "€3,500"],
                    ],
                },
                "model_answer": (
                    "Premium units: 2,000,000 × 30% = 600,000.\n"
                    "VeloNova units: 600,000 × 2% = 12,000 bikes.\n"
                    "Revenue: 12,000 × €3,500 = €42m.\n\n"
                    "That just clears the €40m goal, so the case depends on whether 2% share is realistic."
                ),
            },
            {
                "question": "Contribution margin is 25% of revenue. Showrooms, staff and marketing in Germany cost €6m a year. Upfront investment is €12m. Does it meet the profit goal, and what is the payback?",
                "model_answer": (
                    "Contribution: €42m × 25% = €10.5m.\n"
                    "Operating profit: €10.5m − €6m = €4.5m a year by year 3, so it meets the profit goal.\n"
                    "Payback on year-3 run-rate: €12m ÷ €4.5m ≈ 2.7 years (longer in reality, since years 1 and 2 ramp up)."
                ),
            },
            {
                "question": "What are the biggest risks, and how would you reduce them?",
                "model_answer": (
                    "Share risk: strong German premium brands and loyal dealer networks; 2% may take longer. "
                    "Mitigate with a city-by-city rollout and dealer partnerships alongside showrooms.\n\n"
                    "Service risk: e-bike buyers want local repairs; partner with service chains.\n"
                    "Price risk: discounting by competitors; protect with a clear product edge.\n"
                    "Execution risk: management stretched across two markets; hire a German country lead."
                ),
            },
            {
                "question": "Give your recommendation to the board.",
                "model_answer": (
                    "\"Enter Germany, but in phases.\n\n"
                    "The premium segment is about 600,000 bikes a year; 2% share gives about €42m revenue and €4.5m "
                    "operating profit by year 3, meeting the board's goals with a payback of roughly three years. "
                    "The key risk is reaching 2% share against established brands, so start in 3 or 4 large cities "
                    "with showrooms plus dealer partners, and expand only if share targets are hit after 12 months.\""
                ),
            },
        ],
    },
    {
        "id": "amsterdam-coffee",
        "title": "Coffees sold in Amsterdam",
        "type": "Market sizing",
        "difficulty": "Beginner",
        "minutes": 10,
        "prompt": "Estimate how many cups of coffee are sold each day in cafés, kiosks and restaurants in Amsterdam.",
        "clarifying": (
            "Include coffee bought out of home only, not coffee made at home or in offices. "
            "Population about 930,000. Visitors and commuters count."
        ),
        "steps": [
            {
                "question": "Lay out your approach before doing any maths.",
                "model_answer": (
                    "Top-down, by people: residents who drink coffee × cups per day × share bought out of home, "
                    "then add visitors and commuters.\n\n"
                    "State each assumption, round to easy numbers, and sanity-check the answer at the end "
                    "(e.g. against the number of cafés)."
                ),
            },
            {
                "question": "Now estimate it. Say your assumptions out loud.",
                "model_answer": (
                    "One reasonable estimate (assumptions, not facts):\n\n"
                    "Adults: 930k × ~80% ≈ 750k.\n"
                    "Coffee drinkers: 750k × ~70% ≈ 525k.\n"
                    "Cups per drinker per day: ~2.5 → about 1.3m cups.\n"
                    "Bought out of home: ~25% → about 330k cups.\n"
                    "Visitors and commuters: add ~25% → about 410k cups a day.\n\n"
                    "Sanity check: if Amsterdam has roughly 2,000 places selling coffee, that is about 200 cups each "
                    "a day, which feels plausible. Answer: roughly 400,000 cups a day."
                ),
            },
        ],
    },
    {
        "id": "lumo",
        "title": "Lumo oat drink launch",
        "type": "Pricing and breakeven",
        "difficulty": "Intermediate",
        "minutes": 20,
        "prompt": (
            "Lumo, a Dutch plant-based drinks brand, is launching a new barista oat drink for cafés and supermarkets. "
            "The CEO asks: how many units must we sell to break even, and is the price right?"
        ),
        "clarifying": (
            "Planned shelf price €2.50 per litre carton. Variable cost €1.30 per carton. "
            "Launch fixed costs (marketing, listings, production line) €1.2m in year 1. "
            "Lumo's current oat drink sells 2 million cartons a year."
        ),
        "steps": [
            {
                "question": "What is the breakeven volume?",
                "model_answer": (
                    "Contribution per carton: €2.50 − €1.30 = €1.20.\n"
                    "Breakeven: €1.2m ÷ €1.20 = 1,000,000 cartons, half of what the current oat drink sells. "
                    "That is ambitious for a year-one launch."
                ),
            },
            {
                "question": "Competing barista oat drinks sell at €2.90. What happens to breakeven at a €2.90 price?",
                "model_answer": (
                    "Contribution: €2.90 − €1.30 = €1.60.\n"
                    "Breakeven: €1.2m ÷ €1.60 = 750,000 cartons, 25% fewer.\n\n"
                    "If Lumo's quality matches competitors, pricing at €2.90 (or close to it) lowers the risk a lot. "
                    "€2.50 only makes sense if a low price is needed to win listings."
                ),
            },
            {
                "question": "Give the CEO your recommendation.",
                "model_answer": (
                    "\"Price closer to €2.90, in line with competing barista products.\n\n"
                    "At €2.50 we need 1 million cartons to break even, half our current oat drink's volume; at €2.90 "
                    "we need 750,000. Barista buyers care about foaming quality more than a few cents, so we should "
                    "compete on quality, not price. Next steps: test price with 3 café chains and confirm "
                    "supermarket listing fees before launch.\""
                ),
            },
        ],
    },
]

FRAMEWORKS = {
    "Profitability": (
        "Profit = Revenue − Costs\n"
        "• Revenue = Price × Volume (customers × frequency); check mix\n"
        "• Costs = Fixed (rent, staff, overheads) + Variable (materials, packaging, delivery)\n"
        "• Ask: company-specific or market-wide? Price or volume driver?"
    ),
    "Market entry": (
        "1. Market: size, growth, profitability\n"
        "2. Competition: concentration, share, barriers\n"
        "3. Company: capabilities, brand, fit\n"
        "4. Economics: revenue, costs, investment, payback\n"
        "5. Entry mode: build, partner, buy; risks"
    ),
    "Market sizing": (
        "Top-down: population → segment → usage → price\n"
        "Bottom-up: outlets × sales per outlet\n"
        "Round to easy numbers, state assumptions, sanity-check the result"
    ),
    "Pricing": (
        "Cost-based: unit cost + margin (a floor)\n"
        "Competitor-based: where substitutes sit\n"
        "Value-based: what the customer is willing to pay (a ceiling)\n"
        "Breakeven = fixed costs ÷ (price − variable cost)"
    ),
    "M&A": (
        "1. Strategic rationale: why buy, why this target\n"
        "2. Target: market, position, financials\n"
        "3. Synergies: revenue and cost\n"
        "4. Price and returns vs standalone value\n"
        "5. Risks: integration, culture, financing"
    ),
    "Recommendation": (
        "Answer first → 2–3 supporting reasons with numbers → risks → next steps.\n"
        "Speak to the CEO, not the interviewer. Under one minute."
    ),
}
