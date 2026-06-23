from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from .schemas import (
    AuthBootstrapRequest,
    AuthBootstrapResponse,
    LicenseResponse,
    WorkspaceCreateRequest,
    WorkspaceRecord,
)


class ControlPlaneStore:
    def __init__(self) -> None:
        self._workspaces: dict[str, WorkspaceRecord] = {}

    def bootstrap(self, payload: AuthBootstrapRequest) -> AuthBootstrapResponse:
        return AuthBootstrapResponse(
            access_token=f"dev_{uuid4().hex}",
            token_type="bearer",
            user_id=payload.user_hint or f"user_{uuid4().hex[:8]}",
            workspace_sync_enabled=False,
        )

    def license_for_current_user(self) -> LicenseResponse:
        return LicenseResponse(
            plan="local_dev",
            status="active",
            seats=1,
            features=["local_vault", "workspace_notes", "control_plane_stub"],
        )

    def list_workspaces(self) -> list[WorkspaceRecord]:
        return sorted(
            self._workspaces.values(),
            key=lambda workspace: workspace.created_at,
            reverse=True,
        )

    def create_workspace(self, payload: WorkspaceCreateRequest) -> WorkspaceRecord:
        now = datetime.now(timezone.utc)
        workspace = WorkspaceRecord(
            id=f"ws_{uuid4().hex[:10]}",
            name=payload.name,
            note=payload.note,
            created_at=now,
            updated_at=now,
        )
        self._workspaces[workspace.id] = workspace
        return workspace
