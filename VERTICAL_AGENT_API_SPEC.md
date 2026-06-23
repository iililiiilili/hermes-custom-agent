# Vertical Agent Platform API Spec v0

작성 기준일: 2026-06-22

## 1. 설계 원칙

이 API는 **local-first + cloud control plane** 구조를 전제로 한다.

### 원칙
- 민감한 업무 데이터는 기본적으로 로컬에 저장한다.
- 서버는 로그인, 라이선스, 좌석, 결제, 모델 라우팅만 담당한다.
- LLM 요청에는 필요한 최소 정보만 보낸다.
- 비개발자 기본 플로우는 API 키 입력이 없다.
- 사무실 공유 방지를 위해 기기/좌석 검증을 둔다.

---

## 2. 공통 규칙

- Base URL: `/v1`
- 응답 형식: JSON
- 날짜 기준: `Asia/Seoul`
- 인증: 기본적으로 `access_token` + `device_id`
- 민감 파일 업로드는 기본적으로 비활성, 사용자가 명시적으로 허용해야 함

### 공통 헤더 예시
```http
Authorization: Bearer <access_token>
X-Device-Id: <device_id>
X-App-Version: 0.1.0
X-Platform: windows
```

---

## 3. 인증 / 라이선스

### `POST /v1/auth/bootstrap`
앱 최초 실행 또는 재설치 시 초기 부트스트랩을 수행한다.

#### Request
```json
{
  "install_id": "inst_123",
  "device_fingerprint": "dfp_123",
  "app_version": "0.1.0",
  "platform": "windows"
}
```

#### Response
```json
{
  "anonymous_user_id": "anu_123",
  "device_id": "dev_123",
  "server_time": "2026-06-22T10:00:00+09:00",
  "policy_version": "2026-06-22",
  "feature_flags": {
    "local_vault": true,
    "license_check": true,
    "sync_backup": false
  }
}
```

### `POST /v1/auth/login`
로그인한다.

#### Request
```json
{
  "email": "user@example.com",
  "password": "••••••••",
  "device_id": "dev_123"
}
```

#### Response
```json
{
  "access_token": "atk_123",
  "refresh_token": "rtk_123",
  "user_id": "usr_123",
  "account_type": "pro",
  "seat_limit": 2,
  "subscription_status": "active"
}
```

### `POST /v1/auth/refresh`
액세스 토큰을 갱신한다.

### `POST /v1/auth/logout`
현재 기기의 세션을 종료한다.

---

## 4. 좌석 / 기기 관리

### `GET /v1/licenses/me`
현재 계정의 라이선스 상태를 확인한다.

#### Response
```json
{
  "plan": "pro",
  "status": "active",
  "seat_limit": 2,
  "active_devices": 1,
  "renewal_at": "2026-07-22T00:00:00+09:00"
}
```

### `POST /v1/licenses/devices/register`
기기를 등록한다.

#### Request
```json
{
  "device_id": "dev_123",
  "device_fingerprint": "dfp_123",
  "device_name": "OFFICE-PC-01"
}
```

### `POST /v1/licenses/devices/release`
기기 사용권을 반납한다.

### `GET /v1/licenses/devices`
등록된 기기 목록을 조회한다.

---

## 5. 직군 / pack

### `GET /v1/packs`
이 계정에서 사용할 수 있는 직군 pack 목록을 반환한다.

#### Response
```json
{
  "packs": [
    {
      "pack_id": "acct_pack",
      "name": "세무사 / 회계사 pack",
      "version": "1.0.0",
      "status": "enabled"
    },
    {
      "pack_id": "law_pack",
      "name": "변호사 pack",
      "version": "1.0.0",
      "status": "disabled"
    }
  ]
}
```

### `GET /v1/packs/{pack_id}`
팩 상세 메타데이터를 가져온다.

#### Response
```json
{
  "pack_id": "acct_pack",
  "name": "세무사 / 회계사 pack",
  "system_prompt_version": "2026-06-22",
  "allowed_tools": ["summary", "checklist", "draft", "file_sort"],
  "default_tasks": ["receipt_check", "monthly_summary", "client_reply_draft"]
}
```

---

## 6. 로컬 vault / 동기화

### `POST /v1/sync/manifest`
로컬 변경분을 서버와 맞추기 위한 매니페스트를 요청한다.

#### Request
```json
{
  "device_id": "dev_123",
  "last_sync_at": "2026-06-22T09:00:00+09:00",
  "local_revision": 42
}
```

#### Response
```json
{
  "server_revision": 43,
  "push_allowed": true,
  "pull_allowed": true,
  "conflicts": []
}
```

### `POST /v1/sync/push`
선택적으로 암호화된 로컬 변경사항을 업로드한다.

#### Request
```json
{
  "device_id": "dev_123",
  "bundle": "encrypted_blob_here"
}
```

### `POST /v1/sync/pull`
선택적으로 서버에 저장된 암호화 백업을 내려받는다.

### `POST /v1/sync/resolve`
충돌 해결 결과를 기록한다.

---

## 7. 문서 / 작업

> 기본 원칙상 원문 문서는 로컬 보관이 우선이다. 서버 API는 메타데이터 위주로만 다룬다.

### `POST /v1/workspaces`
로컬 워크스페이스 메타를 등록한다.

#### Request
```json
{
  "workspace_name": "kim-tax-office",
  "pack_id": "acct_pack"
}
```

### `GET /v1/workspaces`
워크스페이스 목록을 조회한다.

### `POST /v1/tasks/preview`
작업 실행 전 미리보기를 만든다.

#### Request
```json
{
  "workspace_id": "ws_123",
  "task_type": "client_reply_draft",
  "input_summary": "고객이 증빙 누락 여부를 물어봄",
  "local_doc_refs": ["doc_1", "doc_2"]
}
```

#### Response
```json
{
  "task_preview_id": "tp_123",
  "estimated_cost": 0.0021,
  "estimated_latency_ms": 1200,
  "requires_llm": true,
  "redaction_needed": false
}
```

### `POST /v1/tasks/run`
작업을 실행한다.

#### Request
```json
{
  "task_preview_id": "tp_123",
  "workspace_id": "ws_123",
  "task_type": "client_reply_draft",
  "model_policy": "balanced"
}
```

#### Response
```json
{
  "task_run_id": "tr_123",
  "status": "completed",
  "output_summary": "누락 자료 확인 요청 초안",
  "output_ref": "local://drafts/tr_123.md"
}
```

### `GET /v1/tasks/{task_run_id}`
작업 상태를 조회한다.

---

## 8. 파일 업로드

### `POST /v1/files/presign`
선택적으로 서버 저장이 필요한 파일에 대해 업로드 정보를 만든다.

#### Request
```json
{
  "workspace_id": "ws_123",
  "purpose": "backup",
  "file_name": "backup.zip"
}
```

#### Response
```json
{
  "upload_url": "https://...",
  "expires_at": "2026-06-22T12:00:00+09:00"
}
```

### `POST /v1/files/commit`
업로드 완료를 서버에 알린다.

> 기본 운영은 로컬 저장이므로, 이 엔드포인트는 선택적 백업에만 사용한다.

---

## 9. LLM 라우팅

### `POST /v1/model/route`
작업에 적합한 모델/공급자를 선택한다.

#### Request
```json
{
  "task_type": "summary",
  "input_size": 3200,
  "requires_reasoning": false,
  "sensitivity": "high"
}
```

#### Response
```json
{
  "provider": "openrouter",
  "model": "anthropic/claude-3-haiku",
  "routing_mode": "cheap_first",
  "fallback": ["openai/gpt-5-mini"],
  "cache_allowed": true
}
```

### `POST /v1/llm/run`
LLM 호출을 실행한다.

#### Request
```json
{
  "workspace_id": "ws_123",
  "task_type": "client_reply_draft",
  "prompt": "고객에게 누락 증빙을 안내하는 짧은 메일 초안",
  "redacted_context": "...",
  "model_policy": "cheap_first"
}
```

#### Response
```json
{
  "llm_run_id": "llm_123",
  "provider": "openrouter",
  "model": "anthropic/claude-3-haiku",
  "cost_estimate": 0.0012,
  "output": "안녕하세요..."
}
```

---

## 10. 사용량 / 과금

### `GET /v1/usage/me`
사용량 요약을 조회한다.

#### Response
```json
{
  "period": "2026-06",
  "llm_requests": 128,
  "documents_processed": 34,
  "seat_count": 2,
  "soft_limit_hit": false
}
```

### `POST /v1/usage/event`
내부 사용량 이벤트를 기록한다.

#### Request
```json
{
  "event_type": "llm_request",
  "workspace_id": "ws_123",
  "model": "anthropic/claude-3-haiku",
  "cost_usd": 0.0012
}
```

---

## 11. 사용자 삭제 / 보안

### `DELETE /v1/user/me`
서버에 저장된 계정/라이선스/메타데이터를 삭제한다.

#### Request
```json
{
  "user_id": "usr_123"
}
```

#### Response
```json
{
  "deleted": true,
  "deleted_at": "2026-06-22T11:20:00+09:00"
}
```

### `POST /v1/security/app-lock`
앱 잠금 상태를 서버에 동기화한다.

### `POST /v1/security/device-challenge`
새 기기에서 재인증이 필요할 때 챌린지를 발급한다.

---

## 12. 운영 / 헬스체크

### `GET /health`
시스템 상태 확인

#### Response
```json
{
  "status": "ok",
  "service": "vertical-agent-api"
}
```

### `GET /ready`
의존성 준비 여부 확인

---

## 13. 에러 형식

모든 에러는 다음 형식을 따른다.

```json
{
  "error_code": "LICENSE_EXPIRED",
  "message": "구독이 만료되었습니다.",
  "retryable": false
}
```

### 자주 쓰는 에러 코드
- `AUTH_REQUIRED`
- `INVALID_DEVICE`
- `LICENSE_EXPIRED`
- `SEAT_LIMIT_EXCEEDED`
- `SYNC_CONFLICT`
- `LLM_PROVIDER_DOWN`
- `REDACTION_REQUIRED`
- `TASK_NOT_FOUND`

---

## 14. 서버 내부 규칙

- 민감 문서는 서버에 원문 저장하지 않는다.
- 작업 실행 전 로컬 캐시를 먼저 조회한다.
- 동일 입력/동일 pack/동일 날짜 요청은 캐시 우선이다.
- 보안 민감 작업은 사용자 확인을 다시 받는다.
- 같은 기기에서 과도한 반복 요청은 soft cap을 적용한다.

---

## 15. MVP 우선순위

### 먼저 만들 것
- auth/bootstrap
- login/refresh
- license 조회
- seat/device register
- pack 목록
- task preview/run
- usage 조회
- local-first sync manifest

### 나중에 만들 것
- 파일 presign
- push/pull 백업
- 충돌 해결
- 앱 잠금
- 관리자 콘솔

---

## 16. 결론

이 API는 **서버가 모든 것을 저장하는 구조가 아니라**, 로컬 데스크톱을 중심으로 둔 **컨트롤 플레인 API**다.

즉:
- **문서/메모/초안 = 로컬**
- **인증/라이선스/좌석/결제 = 서버**
- **LLM 호출 = 필요한 최소 정보만 서버 통해 전송**

이 구조가 회계사, 세무사, 변호사 같은 민감 업종에 가장 잘 맞는다.
