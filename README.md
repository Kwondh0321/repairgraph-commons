# RepairGraph Commons

한국어 | [English](README.en.md) | [변경 기록 / Changelog](CHANGELOG.md)

RepairGraph Commons는 증상–원인–부품–수리 절차를 연결하는 공개 지식 그래프 형식과 검증·검색 도구입니다. 코드는 재사용 가능하게 분리하고 예제 그래프 데이터는 공개 라이선스로 제공합니다.

## 설치 및 사용

```bash
git clone https://github.com/Kwondh0321/repairgraph-commons.git
cd repairgraph-commons
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
python -m pip install .
repairgraph validate data/example.graph.json
repairgraph query data/example.graph.json "노트북 충전 안됨"
```

노드 유형은 `device`, `symptom`, `cause`, `part`, `procedure`, `safety`이며, 절차 노드는 반드시 출처를 포함해야 합니다. 검증기는 중복 ID, 없는 노드 참조, 지원하지 않는 유형, 잘못된 신뢰도, 출처 없는 절차를 거부합니다.

진단 순위는 공개 그래프 관계를 바탕으로 한 제안일 뿐 전문 수리·전기 안전 조언이 아닙니다. 기기별 서비스 문서와 안전 지침을 반드시 확인하세요.

## 데이터 기여

작고 출처가 분명한 변경과 테스트를 함께 제출해 주세요. 저작권이 있는 서비스 매뉴얼을 복사하거나 불확실한 호환성 정보를 추가하지 마세요.

코드는 MIT, `data/` 예제 그래프는 CC-BY-4.0입니다.
