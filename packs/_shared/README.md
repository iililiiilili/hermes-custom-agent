# Shared Pack Contract

이 폴더는 모든 vertical pack이 공유하는 계약을 정의합니다.

## 공통 입력

- 사용자 프로필
- 업무 대상 문서/메모
- 날짜/마감/우선순위
- 선택된 vertical pack
- 출력 톤 설정

## 공통 출력

- 한 줄 요약
- 위험 신호
- 다음 행동 1~3개
- 필요한 누락 항목
- 공유/보고용 짧은 문구

## 공통 금지

- pack 없이 직업별 판단을 섣불리 말하지 않는다.
- core는 직업 용어를 직접 생성하지 않는다.
- 민감정보는 가능한 한 local-first로 다룬다.

## 설계 노트

이 계약은 나중에 JSON Schema, Pydantic model, 또는 SQLite metadata table로 옮기기 쉽도록 간단하게 유지한다.
