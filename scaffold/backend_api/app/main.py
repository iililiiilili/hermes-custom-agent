from __future__ import annotations

from datetime import date, datetime, timezone
from uuid import uuid4

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .control_plane import ControlPlaneStore
from .saju_engine import build_saju_preview
from .schemas import (
    AuthBootstrapRequest,
    AuthBootstrapResponse,
    BirthProfileInput,
    DailyFortuneResponse,
    DeleteMeRequest,
    DeleteMeResponse,
    FortunePreviewResponse,
    FreeCard,
    LicenseResponse,
    SessionBootstrapRequest,
    SessionBootstrapResponse,
    ShareCardRequest,
    ShareCardResponse,
    UnlockCard,
    UnlockRequest,
    UnlockResponse,
    WorkspaceCreateRequest,
    WorkspaceRecord,
)

app = FastAPI(title="sajuwonhae-api", version="0.1.0")
control_plane_store = ControlPlaneStore()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "sajuwonhae-api"}


@app.post("/v1/auth/bootstrap", response_model=AuthBootstrapResponse)
def auth_bootstrap(payload: AuthBootstrapRequest) -> AuthBootstrapResponse:
    return control_plane_store.bootstrap(payload)


@app.get("/v1/licenses/me", response_model=LicenseResponse)
def license_me() -> LicenseResponse:
    return control_plane_store.license_for_current_user()


@app.get("/v1/workspaces", response_model=list[WorkspaceRecord])
def list_workspaces() -> list[WorkspaceRecord]:
    return control_plane_store.list_workspaces()


@app.post("/v1/workspaces", response_model=WorkspaceRecord, status_code=201)
def create_workspace(payload: WorkspaceCreateRequest) -> WorkspaceRecord:
    return control_plane_store.create_workspace(payload)


@app.post("/v1/session/bootstrap", response_model=SessionBootstrapResponse)
def session_bootstrap(payload: SessionBootstrapRequest) -> SessionBootstrapResponse:
    return SessionBootstrapResponse(
        anonymous_user_id=f"anu_{uuid4().hex[:8]}",
        server_time=datetime.now(timezone.utc),
        policy_version="2026-06-22",
        feature_flags={
            "share_cards": True,
            "reward_unlocks": True,
            "daily_fortune": True,
        },
    )


@app.post("/v1/saju/preview", response_model=FortunePreviewResponse)
def saju_preview(payload: BirthProfileInput) -> FortunePreviewResponse:
    preview = build_saju_preview(
        profile_id=f"pro_{uuid4().hex[:8]}",
        name=payload.name,
        calendar_type=payload.calendar_type,
        birth_date=payload.birth_date,
        birth_time=payload.birth_time,
        birth_time_known=payload.birth_time_known,
        is_leap_month=payload.is_leap_month,
        gender=payload.gender,
    )

    return FortunePreviewResponse(
        profile_id=preview.profile_id,
        year_pillar=preview.year_pillar,
        month_pillar=preview.month_pillar,
        day_pillar=preview.day_pillar,
        hour_pillar=preview.hour_pillar,
        chart_line=preview.chart_line,
        element_summary=", ".join(
            f"{key} {value}%" for key, value in preview.five_elements.items()
        ),
        five_elements=preview.five_elements,
        overall_score=preview.overall_score,
        mascot_mood=preview.mascot_mood,
        summary_title=preview.summary_title,
        summary_body=preview.summary_body,
        details=preview.details,
        caution=preview.caution,
        lucky_tip=preview.lucky_tip,
        free_cards=[FreeCard(**card) for card in preview.free_cards],
        locked_cards=preview.locked_cards,
    )


@app.post("/v1/fortune/cards/unlock", response_model=UnlockResponse)
def unlock_card(payload: UnlockRequest) -> UnlockResponse:
    if not payload.reward_event_id:
        raise HTTPException(status_code=400, detail="reward_event_id is required")

    card = UnlockCard(
        card_key=payload.card_key,
        title=payload.card_key.replace("_", " ").title(),
        score=72,
        mascot_mood="steady",
        summary="Unlocked local preview card.",
        details=["This is a development stub.", "Replace with paid card logic later."],
        share_line="Local preview unlocked.",
    )
    return UnlockResponse(unlocked=True, card=card)


@app.get("/v1/fortune/daily", response_model=DailyFortuneResponse)
def daily_fortune(profile_id: str, anonymous_user_id: str) -> DailyFortuneResponse:
    return DailyFortuneResponse(
        date=date.today(),
        mascot_mood="steady",
        headline="Local daily preview",
        body="A lightweight local-first daily fortune stub.",
        scores={"love": 50, "money": 50},
    )


@app.post("/v1/share/cards", response_model=ShareCardResponse)
def create_share_card(payload: ShareCardRequest) -> ShareCardResponse:
    return ShareCardResponse(
        share_card_id=f"share_{uuid4().hex[:8]}",
        title="Local share card",
        subtitle=payload.source_card_key,
        line="Generated from the local development API.",
        scores={"love": 50, "money": 50},
    )


@app.delete("/v1/user/me", response_model=DeleteMeResponse)
def delete_me(payload: DeleteMeRequest) -> DeleteMeResponse:
    return DeleteMeResponse(deleted=True, deleted_at=datetime.now(timezone.utc))
