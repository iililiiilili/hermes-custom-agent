from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Literal

try:
    from sajupy import calculate_saju, lunar_to_solar
except ModuleNotFoundError:
    _STEMS = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
    _BRANCHES = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]

    def _pillar_from_index(index: int) -> str:
        return f"{_STEMS[index % len(_STEMS)]}{_BRANCHES[index % len(_BRANCHES)]}"

    def lunar_to_solar(
        year: int,
        month: int,
        day: int,
        is_leap_month: bool,
    ) -> dict[str, str]:
        del is_leap_month
        return {"solar_date": date(year, month, day).isoformat()}

    def calculate_saju(
        year: int,
        month: int,
        day: int,
        hour: int,
        minute: int,
        utc_offset: int,
        use_solar_time: bool,
        early_zi_time: bool,
    ) -> dict[str, str]:
        del minute, utc_offset, use_solar_time, early_zi_time
        base_date = date(year, month, day)
        day_index = base_date.toordinal() % 60
        year_index = (year - 4) % 60
        month_index = (year * 12 + month - 1) % 60
        hour_index = ((hour % 24) // 2) % 12
        return {
            "year_pillar": _pillar_from_index(year_index),
            "month_pillar": _pillar_from_index(month_index),
            "day_pillar": _pillar_from_index(day_index),
            "hour_pillar": _pillar_from_index(day_index + hour_index),
        }



CalendarType = Literal["solar", "lunar"]
GenderType = Literal["female", "male", "other"]
MascotMood = Literal["lucky", "steady", "rough"]

STEM_MAP = {
    "甲": "갑",
    "乙": "을",
    "丙": "병",
    "丁": "정",
    "戊": "무",
    "己": "기",
    "庚": "경",
    "辛": "신",
    "壬": "임",
    "癸": "계",
}

BRANCH_MAP = {
    "子": "자",
    "丑": "축",
    "寅": "인",
    "卯": "묘",
    "辰": "진",
    "巳": "사",
    "午": "오",
    "未": "미",
    "申": "신",
    "酉": "유",
    "戌": "술",
    "亥": "해",
}

STEM_ELEMENT = {
    "갑": "wood",
    "을": "wood",
    "병": "fire",
    "정": "fire",
    "무": "earth",
    "기": "earth",
    "경": "metal",
    "신": "metal",
    "임": "water",
    "계": "water",
}

BRANCH_ELEMENT = {
    "자": "water",
    "축": "earth",
    "인": "wood",
    "묘": "wood",
    "진": "earth",
    "사": "fire",
    "오": "fire",
    "미": "earth",
    "신": "metal",
    "유": "metal",
    "술": "earth",
    "해": "water",
}

ELEMENT_LABELS = {
    "wood": "목",
    "fire": "화",
    "earth": "토",
    "metal": "금",
    "water": "수",
}

DAY_STEM_ELEMENT_BONUS = {
    "wood": 4,
    "fire": 5,
    "earth": 4,
    "metal": 5,
    "water": 4,
}


@dataclass(frozen=True)
class SajuPreviewData:
    profile_id: str
    year_pillar: str
    month_pillar: str
    day_pillar: str
    hour_pillar: str | None
    chart_line: str
    element_summary: str
    five_elements: dict[str, int]
    overall_score: int
    mascot_mood: MascotMood
    summary_title: str
    summary_body: str
    details: list[str]
    caution: str
    lucky_tip: str
    free_cards: list[dict[str, object]]
    locked_cards: list[str]


def _to_korean_pillar(raw_pillar: str) -> str:
    if len(raw_pillar) != 2:
        return raw_pillar
    stem, branch = raw_pillar[0], raw_pillar[1]
    return f"{STEM_MAP.get(stem, stem)}{BRANCH_MAP.get(branch, branch)}"


def _parse_birth_time(birth_time: str | None, birth_time_known: bool) -> tuple[int, int, bool]:
    if not birth_time_known or not birth_time:
        return 12, 0, False

    hour_str, minute_str = birth_time.split(":", 1)
    return int(hour_str), int(minute_str), True


def _solar_birth_date(calendar_type: CalendarType, birth_date: date, is_leap_month: bool) -> date:
    if calendar_type == "solar":
        return birth_date

    converted = lunar_to_solar(birth_date.year, birth_date.month, birth_date.day, is_leap_month)
    return date.fromisoformat(converted["solar_date"])


def _weighted_element_counts(pillars: list[tuple[str | None, float]]) -> dict[str, float]:
    counts = {key: 0.0 for key in ELEMENT_LABELS}
    for pillar, weight in pillars:
        if not pillar:
            continue
        stem = pillar[0]
        branch = pillar[1]
        stem_element = STEM_ELEMENT.get(stem)
        branch_element = BRANCH_ELEMENT.get(branch)
        if stem_element:
            counts[stem_element] += weight * 0.55
        if branch_element:
            counts[branch_element] += weight * 0.45
    return counts


def _normalize_counts(counts: dict[str, float]) -> dict[str, int]:
    total = sum(counts.values()) or 1.0
    return {key: int(round(value / total * 100)) for key, value in counts.items()}


def _determine_mood(score: int) -> MascotMood:
    if score >= 74:
        return "lucky"
    if score >= 50:
        return "steady"
    return "rough"


def _score_from_elements(elements: dict[str, int], day_element: str, time_known: bool) -> int:
    max_value = max(elements.values())
    min_value = min(elements.values())
    spread = max_value - min_value
    avg = sum(elements.values()) / len(elements)
    balance = 96 - int(spread * 1.25) - int(abs(max_value - avg) * 0.7)
    balance += DAY_STEM_ELEMENT_BONUS.get(day_element, 0)
    if time_known:
        balance += 3
    else:
        balance -= 4
    return max(1, min(100, balance))


def _build_texts(score: int, dominant_element: str, day_pillar: str, time_known: bool, name: str) -> tuple[str, str, list[str], str, str]:
    element_label = ELEMENT_LABELS[dominant_element]
    prefix = f"{name}님, " if name else ""
    if score >= 74:
        title = f"{prefix}{element_label} 기운이 크게 트이는 대길형"
        summary = f"{prefix}{day_pillar}의 결이 선명해요. 오늘은 시작과 응답이 빨라서, 먼저 움직인 쪽이 이득을 봐요."
        details = [
            "바로 결정한 일보다, 먼저 말문을 열어보는 쪽이 유리해요.",
            f"{element_label} 기운이 살아 있어 감각적인 선택이 잘 맞아요.",
            "작은 시도가 예상보다 큰 반응으로 돌아올 수 있어요.",
        ]
        caution = "기세가 좋아도 말은 한 번만 더 다듬어서 보내요."
        lucky_tip = "오늘의 행운 포인트: 먼저 연락하기"
    elif score >= 50:
        title = f"{prefix}{element_label} 기운이 안정적으로 받쳐주는 날"
        summary = f"{prefix}{day_pillar}를 중심으로 흐름이 고르게 잡혀 있어요. 서두르기보다 정리해두면 더 편해져요."
        details = [
            "기본 루틴을 지키면 전체 흐름이 안정돼요.",
            "중요한 말은 짧고 분명하게 전하는 게 좋아요.",
            "지출이나 일정은 한 번 더 체크하면 손해가 줄어요.",
        ]
        caution = "루틴이 흔들리면 운도 같이 흔들릴 수 있어요."
        lucky_tip = "오늘의 행운 포인트: 중간 점검"
    else:
        title = f"{prefix}{element_label} 기운이 부족해서 조절이 필요한 날"
        summary = f"{prefix}{day_pillar}가 예민하게 작동해요. 무리하기보다 속도를 낮추면 훨씬 편해져요."
        details = [
            "급하게 결론 내리기보다 한 박자 쉬어가는 게 좋아요.",
            "피곤하면 일정 하나는 미뤄도 괜찮아요.",
            "오늘은 완벽보다 무난이 복이에요.",
        ]
        caution = "무리수, 즉흥 결제, 과한 약속은 피하는 게 좋아요."
        lucky_tip = "오늘의 행운 포인트: 속도 낮추기"

    if not time_known:
        details.append("시간 미상이라 시주는 생략하고, 년·월·일주 중심으로 봤어요.")
    details.insert(0, f"{name}님의 이름과 생년월일 흐름을 함께 묶어 읽었어요.")

    return title, summary, details, caution, lucky_tip


def build_saju_preview(
    *,
    profile_id: str,
    name: str,
    calendar_type: CalendarType,
    birth_date: date,
    birth_time: str | None,
    birth_time_known: bool,
    is_leap_month: bool,
    gender: GenderType,
) -> SajuPreviewData:
    solar_date = _solar_birth_date(calendar_type, birth_date, is_leap_month)
    hour, minute, time_known = _parse_birth_time(birth_time, birth_time_known)

    saju = calculate_saju(
        solar_date.year,
        solar_date.month,
        solar_date.day,
        hour,
        minute,
        utc_offset=9,
        use_solar_time=False,
        early_zi_time=True,
    )

    year_pillar = _to_korean_pillar(str(saju["year_pillar"]))
    month_pillar = _to_korean_pillar(str(saju["month_pillar"]))
    day_pillar = _to_korean_pillar(str(saju["day_pillar"]))
    hour_pillar_raw = str(saju["hour_pillar"]) if time_known else None
    hour_pillar = _to_korean_pillar(hour_pillar_raw) if hour_pillar_raw else None

    pillars_for_balance = [
        (year_pillar, 0.9),
        (month_pillar, 1.1),
        (day_pillar, 1.6),
        (hour_pillar, 0.9 if time_known else 0.0),
    ]
    element_weights = _weighted_element_counts(pillars_for_balance)
    normalized_elements = _normalize_counts(element_weights)
    dominant_element = max(normalized_elements, key=normalized_elements.get)
    day_element = STEM_ELEMENT.get(day_pillar[0], "earth")
    overall_score = _score_from_elements(normalized_elements, day_element, time_known)
    mood = _determine_mood(overall_score)

    title, summary_body, details, caution, lucky_tip = _build_texts(
        overall_score, dominant_element, day_pillar, time_known, name
    )

    chart_parts = [year_pillar, month_pillar, day_pillar]
    if hour_pillar:
        chart_parts.append(hour_pillar)
    else:
        chart_parts.append("시간 미상")
    chart_line = " · ".join(chart_parts)

    element_summary = " · ".join(f"{ELEMENT_LABELS[key]} {value}%" for key, value in normalized_elements.items())

    love_score = max(1, min(100, overall_score + (5 if dominant_element in {"wood", "fire"} else -2)))
    money_score = max(1, min(100, overall_score + (5 if dominant_element in {"earth", "metal"} else -2)))

    free_cards = [
        {
            "card_key": "love_preview",
            "title": "연애운",
            "score": love_score,
            "body": "대화 리듬이 잘 맞으면 호감이 더 빨리 살아나요.",
        },
        {
            "card_key": "money_preview",
            "title": "금전운",
            "score": money_score,
            "body": "작은 지출을 한 번 더 보면 마음이 편해져요.",
        },
    ]

    return SajuPreviewData(
        profile_id=profile_id,
        year_pillar=year_pillar,
        month_pillar=month_pillar,
        day_pillar=day_pillar,
        hour_pillar=hour_pillar,
        chart_line=chart_line,
        element_summary=element_summary,
        five_elements=normalized_elements,
        overall_score=overall_score,
        mascot_mood=mood,
        summary_title=title,
        summary_body=summary_body,
        details=details,
        caution=caution,
        lucky_tip=lucky_tip,
        free_cards=free_cards,
        locked_cards=["personality_deep", "career", "yearly", "daily_detail"],
    )
