# Packs Overview

이 폴더는 공통 코어와 직업군별 해석/문구/규칙을 분리하기 위한 영역입니다.

## 원칙

- `core`는 로그인, 저장, 모델 호출, 공통 안전장치만 담당한다.
- `pack`은 직업별 언어, 템플릿, 체크리스트, 데이터 스키마, 금지 규칙을 담당한다.
- 같은 입력이라도 pack에 따라 해석의 우선순위와 표현을 다르게 가져간다.

## 현재 초기 pack

- `accounting`: 회계/세무/장부/증빙/마감
- `legal`: 변호/사건/문서/기한/증거

## 다음 확장 방식

새 직업군이 생기면 아래만 추가한다.

1. `packs/<vertical>/README.md`
2. `packs/<vertical>/rules.md`
3. `packs/<vertical>/templates.md`
4. `packs/<vertical>/data_model.md`

이렇게 하면 core는 덜 흔들리고, 직업별 경험만 계속 두껍게 만들 수 있다.
