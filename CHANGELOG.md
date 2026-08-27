# 변경 기록 / Changelog

이 프로젝트는 [Keep a Changelog](https://keepachangelog.com/)의 구조와 [Semantic Versioning](https://semver.org/) 원칙을 따릅니다.

## [Unreleased]

### 한국어

- 빈 ID·레이블, 잘못된 별칭·태그, 형식이 잘못된 절차 출처를 거부합니다.
- 불리언을 신뢰도 숫자로 인정하지 않고 검색 결과 한도를 검증합니다.
- 검증 오류를 한국어 사용자에게 자연스러운 메시지로 제공합니다.
- 스키마 유효성이 실제 수리 안전성을 보장하지 않는다는 경계를 명시했습니다.

### English

- Rejects empty identifiers or labels, malformed aliases and tags, and invalid procedure sources.
- Prevents booleans from being accepted as confidence numbers and validates result limits.
- Provides clear localized validation messages.
- States that schema validity does not establish the physical safety of a repair procedure.

### 검증 / Validation

- 4 regression tests, Ruff checks, clean wheel build and install, validate/query examples, malformed-graph failure, and GitHub Actions.

[Unreleased]: https://github.com/Kwondh0321/repairgraph-commons/compare/v0.1.0...HEAD
