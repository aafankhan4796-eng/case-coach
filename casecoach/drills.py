"""Mental-maths drills of the kind used in consulting case interviews.

Every generator takes a random.Random so drills are reproducible in tests.
"""

import random
import re
from dataclasses import dataclass
from typing import Callable, Optional


@dataclass
class Drill:
    kind: str
    question: str
    answer: float
    unit: str = ""          # shown after the answer, e.g. "%" or "€"
    tolerance: float = 0.01  # relative tolerance when checking
    tip: str = ""


def percent_of(rng: random.Random) -> Drill:
    p = rng.choice([5, 10, 15, 20, 25, 30, 35, 40, 45, 60, 75])
    n = rng.randrange(40, 1000, 20)
    return Drill("Percent of", f"What is {p}% of {n:,}?", p * n / 100,
                 tip="Build from 10%: 15% = 10% + half of 10%.")


def percent_change(rng: random.Random) -> Drill:
    old = rng.randrange(40, 300, 10)
    pct = rng.choice([-40, -30, -25, -20, -15, -10, -5, 5, 10, 15, 20, 25, 30, 40, 50, 60])
    while (old * pct) % 100:
        old += 10
    new = old + old * pct // 100
    return Drill("% change", f"Costs went from €{old}k to €{new}k. What is the % change?", pct, "%",
                 tip="(new − old) ÷ old. Always divide by the starting value.")


def multiply(rng: random.Random) -> Drill:
    a = rng.choice([12, 15, 18, 24, 25, 35, 45, 48, 75, 120, 250])
    b = rng.choice([40, 60, 80, 300, 400, 600, 1_200, 2_500, 8_000])
    return Drill("Multiplication", f"{a} × {b:,} = ?", a * b,
                 tip="Split the zeros off first: 45 × 600 = 45 × 6 × 100.")


def revenue(rng: random.Random) -> Drill:
    cafes = rng.choice([40, 80, 120, 150, 200])
    cups = rng.choice([250, 300, 400, 500])
    price = rng.choice([3.0, 3.5, 4.0, 4.5])
    total = cafes * cups * price
    return Drill("Revenue", f"{cafes} cafés each sell {cups} coffees a day at €{price:.2f}. "
                 "What is the total daily revenue in €?", total, "€",
                 tip="Volume × price. Multiply the easy numbers first.")


def breakeven(rng: random.Random) -> Drill:
    margin = rng.choice([0.5, 0.8, 1.2, 1.5, 2.0, 2.5, 4.0])
    units = rng.choice([200_000, 250_000, 400_000, 500_000, 750_000, 1_000_000])
    var_cost = rng.choice([0.8, 1.0, 1.3, 2.0])
    price = var_cost + margin
    fixed = margin * units
    return Drill("Breakeven", f"Fixed costs are €{fixed:,.0f}. Price is €{price:.2f} and variable cost "
                 f"€{var_cost:.2f} per unit. How many units to break even?", units, "units",
                 tip="Breakeven units = fixed costs ÷ (price − variable cost).")


def doubling(rng: random.Random) -> Drill:
    g = rng.choice([4, 6, 8, 9, 12, 18])
    return Drill("Growth", f"Revenue grows {g}% a year. Roughly how many years until it doubles?",
                 72 / g, "years", tolerance=0.15, tip="Rule of 72: years to double ≈ 72 ÷ growth rate.")


def market_share(rng: random.Random) -> Drill:
    market = rng.choice([200, 400, 600, 800, 1_200])
    share = rng.choice([2, 4, 5, 8, 12, 15])
    return Drill("Market share", f"The market is worth €{market}m. A company holds {share}%. "
                 "What is its revenue in €m?", market * share / 100, "€m",
                 tip="Share × market size. 5% = half of 10%.")


GENERATORS: dict[str, Callable[[random.Random], Drill]] = {
    "Percent of": percent_of,
    "% change": percent_change,
    "Multiplication": multiply,
    "Revenue": revenue,
    "Breakeven": breakeven,
    "Growth": doubling,
    "Market share": market_share,
}


def make_drill(rng: random.Random, kinds: Optional[list[str]] = None) -> Drill:
    kinds = kinds or list(GENERATORS)
    return GENERATORS[rng.choice(kinds)](rng)


_SUFFIX = {"k": 1e3, "m": 1e6, "bn": 1e9, "b": 1e9}


def parse_number(text: str) -> Optional[float]:
    """Read answers like '36', '15%', '-20 %', '1,400', '€1.4k', '42m'. Returns None if unreadable."""
    t = text.strip().lower().replace("€", "").replace(" ", "").replace("%", "")
    t = re.sub(r"(units|years|yrs)$", "", t)
    m = re.fullmatch(r"([-+]?[\d,]*\.?\d+)(bn|b|k|m)?", t)
    if not m:
        return None
    value = float(m.group(1).replace(",", ""))
    return value * _SUFFIX.get(m.group(2) or "", 1)


def check(drill: Drill, text: str) -> Optional[bool]:
    """True/False for a readable answer, None if it couldn't be read."""
    value = parse_number(text)
    if value is None:
        return None
    if drill.answer == 0:
        return abs(value) < 1e-9
    return abs(value - drill.answer) <= abs(drill.answer) * drill.tolerance


def fmt(value: float, unit: str = "") -> str:
    if unit == "%":
        return f"{value:g}%"
    if unit in ("€", "€m"):
        return f"€{value:,.2f}".rstrip("0").rstrip(".") + ("m" if unit == "€m" else "")
    if unit == "years":
        return f"about {value:.0f} years"
    return f"{value:,.0f}" + (f" {unit}" if unit else "")
