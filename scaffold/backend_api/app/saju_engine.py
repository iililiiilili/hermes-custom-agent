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

STEM_YIN_YANG = {
    "갑": "yang",
    "을": "yin",
    "병": "yang",
    "정": "yin",
    "무": "yang",
    "기": "yin",
    "경": "yang",
    "신": "yin",
    "임": "yang",
    "계": "yin",
}

DAY_MASTER_PROFILES = {
    "갑": {"label": "큰 나무형", "love": "기준이 분명하고, 상대의 태도가 흔들리면 바로 느껴지는 타입이에요.", "money": "한 번에 크게 보기보다 장기적으로 쌓는 감각이 좋아요.", "career": "정리, 기획, 책임감이 필요한 역할에서 힘이 나요.", "caution": "고집이 세지면 주변 조언을 놓치기 쉬워요.", "tip": "오늘은 일단 방향을 정하고 나서 디테일을 잡는 게 좋아요."},
    "을": {"label": "덩굴풀형", "love": "분위기와 말의 온도가 잘 맞아야 마음이 열려요.", "money": "부드럽지만 꾸준한 관리가 재물운을 살려요.", "career": "조율, 상담, 미감, 커뮤니케이션이 강점이에요.", "caution": "주변 기류에 너무 오래 흔들리면 피곤해져요.", "tip": "오늘은 한 사람에게 집중해서 말하는 게 유리해요."},
    "병": {"label": "태양형", "love": "호감 표현이 빠르고, 반응이 오면 바로 살아나요.", "money": "보이는 성과가 있을 때 집중력이 높아져요.", "career": "발표, 리딩, 노출, 추진이 있는 일이 잘 맞아요.", "caution": "속도가 과하면 주변이 따라오지 못할 수 있어요.", "tip": "오늘은 먼저 분위기를 밝히는 쪽이 이득이에요."},
    "정": {"label": "촛불형", "love": "섬세한 배려가 빛나는 타입이라 작은 말이 크게 남아요.", "money": "정리된 루틴과 예산이 운을 안정적으로 받쳐줘요.", "career": "서비스, 기록, 감각, 디테일이 필요한 분야에 강해요.", "caution": "감정이 쌓이면 속으로 끓고 겉으로는 드러내지 않기 쉬워요.", "tip": "오늘은 느슨한 약속보다 선명한 일정이 좋아요."},
    "무": {"label": "산형", "love": "쉽게 흔들리지 않지만, 한 번 마음 열면 오래 가요.", "money": "버티는 힘이 좋아서 고정 수입 관리에 강점이 있어요.", "career": "기반, 운영, 책임, 조직 관리에서 존재감이 커져요.", "caution": "너무 버티기만 하면 변화 타이밍을 놓칠 수 있어요.", "tip": "오늘은 이미 하던 것의 기반을 한 번 더 다져보세요."},
    "기": {"label": "밭형", "love": "상대의 편안함을 먼저 살피는 다정한 타입이에요.", "money": "자잘한 지출 정리와 흐름 관리에서 강해요.", "career": "지원, 운영, 문서, 실무 정리에서 장점이 살아나요.", "caution": "챙길 것이 많아지면 내 페이스를 잃기 쉬워요.", "tip": "오늘은 작은 누락부터 잡으면 전체가 편해져요."},
    "경": {"label": "칼형", "love": "호불호가 분명하고, 선이 맞을 때 관계가 단단해져요.", "money": "판단이 빠르고 손익이 보이면 과감해질 수 있어요.", "career": "결단, 구조화, 룰 설정, 실행에서 힘이 나요.", "caution": "말이 직선적으로 나가면 오해를 살 수 있어요.", "tip": "오늘은 한 번 자르고, 한 번 더 다듬어 말하세요."},
    "신": {"label": "보석형", "love": "예민하지만 세련된 감각이 통하면 매력적으로 보여요.", "money": "작은 차이와 품질 구분에 강해서 선별력이 좋아요.", "career": "편집, 검토, 감정, 정밀함이 필요한 일에 적합해요.", "caution": "기준이 높아지면 스스로도 피곤해질 수 있어요.", "tip": "오늘은 작은 퀄리티 체크가 큰 차이를 만들어요."},
    "임": {"label": "큰물형", "love": "흐름을 읽는 감각이 좋아서 공감이 빠르게 이어져요.", "money": "판단보다 흐름을 넓게 보는 쪽이 유리해요.", "career": "확장, 연결, 이동, 정보 수집에서 강점이 있어요.", "caution": "생각이 많아지면 실행이 늦어질 수 있어요.", "tip": "오늘은 일단 시작하고 보면서 조정하는 게 좋아요."},
    "계": {"label": "비형", "love": "감정의 결이 섬세해서 사소한 분위기도 잘 읽어요.", "money": "숫자보다 맥락을 읽는 감각이 좋아요.", "career": "관찰, 분석, 후방 지원, 정리에서 장점이 있어요.", "caution": "조용히 쌓인 피로가 한꺼번에 올라올 수 있어요.", "tip": "오늘은 깊게 보기보다 가볍게 정리하는 게 맞아요."},
}

BRANCH_TRAITS = {
    "자": {"season": "겨울", "tone": "집중", "keyword": "시작 전의 준비"},
    "축": {"season": "겨울 끝", "tone": "축적", "keyword": "버티며 쌓기"},
    "인": {"season": "초봄", "tone": "기동", "keyword": "움직임의 시작"},
    "묘": {"season": "봄", "tone": "확장", "keyword": "퍼지는 기운"},
    "진": {"season": "봄 끝", "tone": "정리", "keyword": "방향 전환"},
    "사": {"season": "초여름", "tone": "집중", "keyword": "관심이 모이는 때"},
    "오": {"season": "여름", "tone": "발산", "keyword": "드러내기"},
    "미": {"season": "여름 끝", "tone": "완충", "keyword": "정리와 배려"},
    "신": {"season": "초가을", "tone": "선별", "keyword": "고르는 힘"},
    "유": {"season": "가을", "tone": "정리", "keyword": "마무리와 다듬기"},
    "술": {"season": "가을 끝", "tone": "보호", "keyword": "경계 세우기"},
    "해": {"season": "겨울 초입", "tone": "확장", "keyword": "흐름을 넓히기"},
}

TEN_GOD_LABELS = {
    "비견": "동료·자기주장",
    "겁재": "경쟁·돌파",
    "식신": "생산·표현",
    "상관": "재능·변화",
    "편재": "기회·확장",
    "정재": "관리·안정",
    "편관": "압박·규율",
    "정관": "책임·신뢰",
    "편인": "직감·보호",
    "정인": "학습·회복",
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


def _is_yang(stem: str) -> bool:
    return STEM_YIN_YANG.get(stem, "yang") == "yang"


def _ten_god(day_stem: str, other_stem: str) -> str:
    day_element = STEM_ELEMENT.get(day_stem)
    other_element = STEM_ELEMENT.get(other_stem)
    if not day_element or not other_element:
        return "정인"

    day_yang = _is_yang(day_stem)
    other_yang = _is_yang(other_stem)
    same_polarity = day_yang == other_yang

    if day_element == other_element:
        return "비견" if same_polarity else "겁재"

    generates = {"wood": "fire", "fire": "earth", "earth": "metal", "metal": "water", "water": "wood"}
    controls = {"wood": "earth", "fire": "metal", "earth": "water", "metal": "wood", "water": "fire"}

    if generates[day_element] == other_element:
        return "식신" if same_polarity else "상관"
    if controls[day_element] == other_element:
        return "편재" if same_polarity else "정재"
    if controls[other_element] == day_element:
        return "편관" if same_polarity else "정관"
    if generates[other_element] == day_element:
        return "편인" if same_polarity else "정인"
    return "정인"


def _daily_fortune_score(
    *,
    user_day_stem: str,
    user_day_element: str,
    user_month_branch: str,
    today_day_stem: str,
    today_day_element: str,
    today_month_branch: str,
    time_known: bool,
) -> int:
    generates = {"wood": "fire", "fire": "earth", "earth": "metal", "metal": "water", "water": "wood"}
    controls = {"wood": "earth", "fire": "metal", "earth": "water", "metal": "wood", "water": "fire"}
    weekday_bias = [0, 1, 2, 1, 0, -1, -2][date.today().weekday()]

    score = 50 + weekday_bias
    if user_day_element == today_day_element:
        score += 12
    elif generates[user_day_element] == today_day_element:
        score += 8
    elif generates[today_day_element] == user_day_element:
        score += 5
    elif controls[user_day_element] == today_day_element:
        score -= 8
    elif controls[today_day_element] == user_day_element:
        score -= 6

    if user_month_branch == today_month_branch:
        score += 6
    if _is_yang(user_day_stem) == _is_yang(today_day_stem):
        score += 2
    if time_known:
        score += 2
    else:
        score -= 2

    return max(1, min(100, score))


def _name_rhythm(name: str) -> tuple[int, str]:
    compact = "".join(ch for ch in name if not ch.isspace())
    length = len(compact)
    if length <= 2:
        return length, "짧고 선명한 이름"
    if length == 3:
        return length, "리듬이 자연스러운 이름"
    return length, "조금 길지만 안정감 있는 이름"


def _score_from_elements(elements: dict[str, int], day_element: str, time_known: bool) -> int:
    max_value = max(elements.values())
    min_value = min(elements.values())
    spread = max_value - min_value
    avg = sum(elements.values()) / len(elements)
    balance = 58 - int(spread * 0.45) - int(abs(max_value - avg) * 0.2)
    balance += DAY_STEM_ELEMENT_BONUS.get(day_element, 0) // 3
    if time_known:
        balance += 2
    else:
        balance -= 3
    return max(1, min(100, balance))


def _build_texts(
    score: int,
    dominant_element: str,
    day_pillar: str,
    time_known: bool,
    name: str,
    day_stem: str,
    month_branch: str,
    dominant_ten_god: str,
) -> tuple[str, str, list[str], str, str]:
    day_profile = DAY_MASTER_PROFILES.get(day_stem, DAY_MASTER_PROFILES["갑"])
    branch_trait = BRANCH_TRAITS.get(month_branch, BRANCH_TRAITS["자"])
    ten_god_label = TEN_GOD_LABELS.get(dominant_ten_god, dominant_ten_god)
    prefix = f"{name}님, " if name else ""
    if score >= 74:
        title = f"{prefix}{day_pillar} · {day_profile['label']} 대길형"
        summary = f"{prefix}{day_pillar}의 결이 선명해요. {branch_trait['season']} 기운과 맞물려 반응이 빠르고, 먼저 움직인 쪽이 이득을 봐요."
        details = [
            f"{day_profile['career']}",
            f"십신 축에서는 {dominant_ten_god} 기운이 두드러져 {ten_god_label} 흐름이 보여요.",
            f"{branch_trait['keyword']} 성향이 살아 있어 {branch_trait['tone']} 감각이 잘 맞아요.",
            f"{day_profile['tip']}",
        ]
        caution = f"기세가 좋아도 {day_profile['caution']}"
        lucky_tip = f"오늘의 행운 포인트: {branch_trait['tone']}을 살리는 행동"
    elif score >= 50:
        title = f"{prefix}{day_pillar} · {day_profile['label']} 안정형"
        summary = f"{prefix}{day_pillar}를 중심으로 흐름이 고르게 잡혀 있어요. 서두르기보다 정리해두면 더 편해져요."
        details = [
            f"{day_profile['love']}",
            f"{day_profile['money']}",
            f"{branch_trait['tone']}한 월지 흐름이라 {branch_trait['keyword']}이 중요해요.",
            f"{day_profile['tip']}",
        ]
        caution = f"루틴이 흔들리면 운도 같이 흔들릴 수 있어요. {day_profile['caution']}"
        lucky_tip = f"오늘의 행운 포인트: {branch_trait['keyword']} 점검"
    else:
        title = f"{prefix}{day_pillar} · {day_profile['label']} 조절형"
        summary = f"{prefix}{day_pillar}가 예민하게 작동해요. 무리하기보다 속도를 낮추면 훨씬 편해져요."
        details = [
            f"{day_profile['love']}",
            f"{day_profile['money']}",
            f"{day_profile['career']}",
            f"{day_profile['tip']}",
        ]
        caution = f"무리수, 즉흥 결제, 과한 약속은 피하는 게 좋아요. {day_profile['caution']}"
        lucky_tip = f"오늘의 행운 포인트: {branch_trait['tone']}으로 정리하기"

    if not time_known:
        details.append("시간 미상이라 시주는 생략하고, 년·월·일주 중심으로 봤어요.")
    details.insert(0, f"{name}님의 이름과 생년월일 흐름을 함께 묶어 읽었어요.")
    details.insert(1, f"이름 호흡은 '{name}' 기준 {_name_rhythm(name)[0]}글자라 {_name_rhythm(name)[1]}로 보여요.")
    details.insert(2, f"{day_pillar} 일간은 {day_profile['label']}로 읽혀서, 관계/일/돈의 반응 속도가 함께 달라져요.")

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
    day_stem = day_pillar[0]
    month_branch = month_pillar[1]

    today = date.today()
    today_saju = calculate_saju(
        today.year,
        today.month,
        today.day,
        12,
        0,
        utc_offset=9,
        use_solar_time=False,
        early_zi_time=True,
    )
    today_day_pillar = _to_korean_pillar(str(today_saju["day_pillar"]))
    today_month_pillar = _to_korean_pillar(str(today_saju["month_pillar"]))
    today_day_stem = today_day_pillar[0]
    today_day_element = STEM_ELEMENT.get(today_day_stem, "earth")
    today_month_branch = today_month_pillar[1]
    day_element = STEM_ELEMENT.get(day_stem, "earth")
    element_weights = _weighted_element_counts([
        (year_pillar, 0.9),
        (month_pillar, 1.1),
        (day_pillar, 1.6),
        (hour_pillar, 0.9 if time_known else 0.0),
    ])
    normalized_elements = _normalize_counts(element_weights)
    dominant_element = max(normalized_elements, key=normalized_elements.get)

    overall_score = _daily_fortune_score(
        user_day_stem=day_stem,
        user_day_element=day_element,
        user_month_branch=month_branch,
        today_day_stem=today_day_stem,
        today_day_element=today_day_element,
        today_month_branch=today_month_branch,
        time_known=time_known,
    )
    mood = _determine_mood(overall_score)

    ten_god_counts: dict[str, int] = {key: 0 for key in TEN_GOD_LABELS}
    for stem in [str(saju["year_stem"]), str(saju["month_stem"]), str(saju["hour_stem"]) if time_known else None]:
        if stem:
            ten_god_counts[_ten_god(day_stem, stem)] += 1
    dominant_ten_god = max(ten_god_counts, key=ten_god_counts.get)

    title, summary_body, details, caution, lucky_tip = _build_texts(
        overall_score, dominant_element, day_pillar, time_known, name, day_stem, month_branch, dominant_ten_god
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

    day_profile = DAY_MASTER_PROFILES.get(day_stem, DAY_MASTER_PROFILES["갑"])
    free_cards = [
        {
            "card_key": "love_preview",
            "title": "연애운",
            "score": love_score,
            "body": day_profile["love"],
        },
        {
            "card_key": "money_preview",
            "title": "금전운",
            "score": money_score,
            "body": day_profile["money"],
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
