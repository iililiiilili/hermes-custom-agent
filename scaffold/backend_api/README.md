# Backend API Scaffold

FastAPI 기반 사주원해? 서버 뼈대입니다. 이 백엔드는 현재 로컬 개발용 control plane 역할만 합니다.

## 실행

기본 실행 진입점은 `python -m app`입니다. 이 엔트리포인트는 Android 에뮬레이터/실기기에서 앱이 접근할 수 있도록 `0.0.0.0`에 바인딩합니다.

```bash
python -m app
```

필요하면 호스트와 포트를 오버라이드할 수 있습니다.

```bash
SAJU_API_HOST=0.0.0.0 SAJU_API_PORT=8000 python -m app
```

## 현재 포함된 엔드포인트

- `GET /health`
- `POST /v1/session/bootstrap`
- `POST /v1/saju/preview`
- `POST /v1/fortune/cards/unlock`
- `GET /v1/fortune/daily`
- `POST /v1/share/cards`
- `DELETE /v1/user/me`

## 다음 단계

1. 사주 계산 엔진 붙이기
2. AdMob 보상 검증 서버 연결
3. OpenAI Responses API 연결
4. Supabase 저장소 연결
