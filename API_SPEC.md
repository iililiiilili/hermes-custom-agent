# 사주원해? API Spec v0

작성 기준일: 2026-06-22

## 1. 공통 규칙

- Base URL: `/v1`
- 인증:
  초기에는 `anonymous_user_id` 기반
- 응답 형식:
  JSON
- 날짜 기준:
  `Asia/Seoul`

## 2. 세션

### `POST /v1/session/bootstrap`

익명 사용자를 시작한다.

```json
{
  "device_fingerprint": "optional-client-generated-string",
  "app_version": "0.1.0",
  "platform": "android"
}
```

```json
{
  "anonymous_user_id": "anu_123",
  "server_time": "2026-06-22T10:00:00+09:00",
  "policy_version": "2026-06-22",
  "feature_flags": {
    "share_cards": true,
    "reward_unlocks": true
  }
}
```

## 3. 사주 입력

### `POST /v1/saju/preview`

무료 결과를 생성한다.

```json
{
  "anonymous_user_id": "anu_123",
  "calendar_type": "solar",
  "birth_date": "1996-08-21",
  "birth_time": "07:30",
  "birth_time_known": true,
  "is_leap_month": false,
  "gender": "female"
}
```

```json
{
  "profile_id": "pro_123",
  "day_pillar": "정유",
  "five_elements": {
    "wood": 22,
    "fire": 28,
    "earth": 18,
    "metal": 16,
    "water": 16
  },
  "mascot_mood": "lucky",
  "summary_title": "불빛처럼 선명한 감각형",
  "summary_body": "감각이 빠르고 반응이 예민한 편이에요.",
  "free_cards": [
    {
      "card_key": "love_preview",
      "title": "연애운",
      "score": 82,
      "body": "말을 아끼면 매력이 더 선명해져요."
    },
    {
      "card_key": "money_preview",
      "title": "금전운",
      "score": 76,
      "body": "오늘은 작은 지출을 한 번 더 살펴보면 좋아요."
    }
  ],
  "locked_cards": [
    "personality_deep",
    "career",
    "yearly",
    "daily_detail"
  ]
}
```

## 4. 잠긴 카드 조회

### `POST /v1/fortune/cards/unlock`

광고 완료 이후 잠긴 카드를 연다.

```json
{
  "anonymous_user_id": "anu_123",
  "profile_id": "pro_123",
  "card_key": "career",
  "reward_event_id": "reward_abc123"
}
```

```json
{
  "unlocked": true,
  "card": {
    "card_key": "career",
    "title": "직업운",
    "score": 71,
    "mascot_mood": "steady",
    "summary": "혼자 밀어붙이기보다 조율형 역할이 빛나요.",
    "details": [
      "실무 감각이 빠른 편이에요.",
      "의사결정 전에 맥락을 읽는 능력이 강해요."
    ],
    "share_line": "오늘은 앞장보다 조율이 복이 되는 날."
  }
}
```

### 실패 예시

```json
{
  "unlocked": false,
  "error_code": "REWARD_NOT_VERIFIED",
  "message": "광고 보상 확인이 완료되지 않았어요."
}
```

## 5. 오늘운 상세

### `GET /v1/fortune/daily?profile_id=pro_123&anonymous_user_id=anu_123`

오늘 기준 방울이 상태와 요약을 가져온다.

```json
{
  "date": "2026-06-22",
  "mascot_mood": "rough",
  "headline": "무리수 금지",
  "body": "조용히 지나가면 그게 제일 큰 복이에요.",
  "scores": {
    "love": 41,
    "money": 38
  }
}
```

## 6. 공유 카드

### `POST /v1/share/cards`

공유용 텍스트 메타데이터를 생성한다.

```json
{
  "anonymous_user_id": "anu_123",
  "profile_id": "pro_123",
  "source_card_key": "love_preview"
}
```

```json
{
  "share_card_id": "share_123",
  "title": "나는 정유일주, 방울이도 인정한 상승세",
  "subtitle": "오늘 운빨 상승",
  "line": "오늘은 방울 소리만 들어도 일이 풀리는 쪽.",
  "scores": {
    "love": 82,
    "money": 76
  }
}
```

## 7. 사용자 데이터 삭제

### `DELETE /v1/user/me`

익명 사용자의 서버 저장 데이터를 삭제한다.

```json
{
  "anonymous_user_id": "anu_123"
}
```

```json
{
  "deleted": true,
  "deleted_at": "2026-06-22T11:20:00+09:00"
}
```

## 8. 운영용

### `GET /health`

```json
{
  "status": "ok",
  "service": "sajuwonhae-api"
}
```

## 9. 서버 내부 규칙

- `profile_id`는 입력값 해시 기반으로 재사용 가능
- 광고 보상 없이는 잠긴 카드 생성 금지
- 무료 카드 결과도 캐시한다
- 같은 날 같은 카드 재요청 시 기존 스냅샷 우선 반환
