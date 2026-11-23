import random
import re

import pytest

from casecoach.cases import CASES, FRAMEWORKS
from casecoach.coach import system_prompt
from casecoach.drills import GENERATORS, Drill, check, fmt, make_drill, parse_number


@pytest.mark.parametrize("text,value", [("36", 36), ("15%", 15), ("-20 %", -20), ("1,400", 1400),
                                        ("€1.4k", 1400), ("42m", 42e6), ("9 years", 9), ("abc", None)])
def test_parse_number(text, value):
    assert parse_number(text) == value


@pytest.mark.parametrize("kind", list(GENERATORS))
def test_generators_are_self_consistent(kind):
    rng = random.Random(7)
    for _ in range(200):
        d = GENERATORS[kind](rng)
        assert d.question and d.tip
        assert check(d, str(d.answer)) is True


def test_percent_change_divides_by_old_value():
    rng = random.Random(1)
    for _ in range(200):
        d = GENERATORS["% change"](rng)
        old, new = map(float, re.findall(r"€(\d+)k", d.question))
        assert d.answer == pytest.approx((new - old) / old * 100)


def test_check_tolerance_and_unreadable():
    d = Drill("x", "q", 36)
    assert check(d, "36") and check(d, "36.2") and not check(d, "35")
    assert check(d, "thirty-six") is None


def test_make_drill_respects_kinds():
    rng = random.Random(3)
    assert {make_drill(rng, ["Breakeven"]).kind for _ in range(20)} == {"Breakeven"}


def test_fmt():
    assert fmt(1400, "€") == "€1,400" and fmt(15, "%") == "15%" and fmt(9, "years") == "about 9 years"


def test_cases_are_complete():
    ids = [c["id"] for c in CASES]
    assert len(ids) == len(set(ids))
    for c in CASES:
        assert c["prompt"] and c["clarifying"] and c["steps"]
        for s in c["steps"]:
            assert s["question"] and s["model_answer"]
            if "exhibit" in s:
                assert all(len(r) == len(s["exhibit"]["columns"]) for r in s["exhibit"]["rows"])


def test_freshbrew_numbers_add_up():
    ex = CASES[0]["steps"][1]["exhibit"]["rows"]
    then, now = sum(r[1] for r in ex[:-1]), sum(r[2] for r in ex[:-1])
    assert (then, now) == (ex[-1][1], ex[-1][2])
    assert round(now - then, 1) == round(6.0 - 4.2, 1)


def test_system_prompt_keeps_answers_private():
    p = system_prompt(CASES[0])
    assert "never reveal" in p and CASES[0]["title"] in p
    assert "Recommendation" in FRAMEWORKS
