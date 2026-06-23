from __future__ import annotations

from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, Field

CalendarType = Literal["solar", "lunar"]
GenderType = Literal["female", "male", "other"]
MascotMood = Literal["lucky", "steady", "rough"]
CardKey = Literal[
    "love_preview",
    "money_preview",
    "personality_deep",
    "career",
    "yearly",
    "daily_detail",
    "monthly_flow",
]


class SessionBootstrapRequest(BaseModel):
    device_fingerprint: str | None = None
    app_version: str
    platform: str = Field(default="android")


class SessionBootstrapResponse(BaseModel):
    anonymous_user_id: str
    server_time: datetime
    policy_version: str
    feature_flags: dict[str, bool]


class AuthBootstrapRequest(BaseModel):
    device_id: str | None = None
    user_hint: str | None = None
    platform: str = "local"


class AuthBootstrapResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: str
    workspace_sync_enabled: bool = False


class LicenseResponse(BaseModel):
    plan: str
    status: str
    seats: int
    features: list[str]


class WorkspaceCreateRequest(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    note: str = Field(default="", max_length=4000)


class WorkspaceRecord(BaseModel):
    id: str
    name: str
    note: str
    created_at: datetime
    updated_at: datetime


class BirthProfileInput(BaseModel):
    anonymous_user_id: str
    name: str = Field(min_length=1, max_length=50)
    calendar_type: CalendarType
    birth_date: date
    birth_time: str | None = None
    birth_time_known: bool = True
    is_leap_month: bool = False
    gender: GenderType


class FreeCard(BaseModel):
    card_key: CardKey
    title: str
    score: int = Field(ge=0, le=100)
    body: str


class FortunePreviewResponse(BaseModel):
    profile_id: str
    year_pillar: str
    month_pillar: str
    day_pillar: str
    hour_pillar: str | None = None
    chart_line: str
    element_summary: str
    five_elements: dict[str, int]
    overall_score: int = Field(ge=0, le=100)
    mascot_mood: MascotMood
    summary_title: str
    summary_body: str
    details: list[str]
    caution: str
    lucky_tip: str
    free_cards: list[FreeCard]
    locked_cards: list[CardKey]


class UnlockRequest(BaseModel):
    anonymous_user_id: str
    profile_id: str
    card_key: CardKey
    reward_event_id: str


class UnlockCard(BaseModel):
    card_key: CardKey
    title: str
    score: int = Field(ge=0, le=100)
    mascot_mood: MascotMood
    summary: str
    details: list[str]
    share_line: str


class UnlockResponse(BaseModel):
    unlocked: bool
    card: UnlockCard | None = None
    error_code: str | None = None
    message: str | None = None


class DailyFortuneResponse(BaseModel):
    date: date
    mascot_mood: MascotMood
    headline: str
    body: str
    scores: dict[str, int]


class ShareCardRequest(BaseModel):
    anonymous_user_id: str
    profile_id: str
    source_card_key: CardKey


class ShareCardResponse(BaseModel):
    share_card_id: str
    title: str
    subtitle: str
    line: str
    scores: dict[str, int]


class DeleteMeRequest(BaseModel):
    anonymous_user_id: str


class DeleteMeResponse(BaseModel):
    deleted: bool
    deleted_at: datetime
