# 사주원해? Project Kit

작성 기준일: 2026-06-22

이 폴더는 `사주원해?`를 실제 출시 가능한 프로젝트로 옮기기 위한 첫 번째 기준 문서 묶음입니다.

## 포함 파일

- `PRODUCT_BRIEF.md`: 제품 방향, 타깃, 핵심 기능, 광고 구조
- `TECH_ARCHITECTURE.md`: Flutter + FastAPI + Supabase 기반 기술 설계
- `API_SPEC.md`: 앱과 서버가 주고받을 API 초안
- `AI_PROMPT_DESIGN.md`: AI 해석 생성 규칙과 프롬프트 설계
- `ROADMAP.md`: MVP 개발 순서와 단계별 목표
- `packs/`: 직업군별 pack 정의와 공통 계약
- `scaffold/`: 아주 얇은 시작용 코드 뼈대

## 지금 바로 쓰는 순서

1. `PRODUCT_BRIEF.md`로 범위 고정
2. `TECH_ARCHITECTURE.md`로 구현 방식 고정
3. `packs/`로 직업군별 문구/규칙/데이터 경계 고정
4. `API_SPEC.md` 기준으로 Flutter와 백엔드 병렬 개발
5. `AI_PROMPT_DESIGN.md` 기준으로 해석 품질 튜닝
6. `ROADMAP.md` 기준으로 실제 일정 진행

## 정책 메모

아래 내용은 2026-06-22 기준 공식 문서를 확인해 반영했습니다.

- Google Play User Data 정책:
  [https://support.google.com/googleplay/android-developer/answer/10144311](https://support.google.com/googleplay/android-developer/answer/10144311)
- AdMob 보상형 광고 정책:
  [https://support.google.com/admob/answer/7313578](https://support.google.com/admob/answer/7313578)
- OpenAI API 문서:
  [https://developers.openai.com/api/docs](https://developers.openai.com/api/docs)
- OpenAI latest model 안내:
  [https://developers.openai.com/api/docs/guides/latest-model](https://developers.openai.com/api/docs/guides/latest-model)
