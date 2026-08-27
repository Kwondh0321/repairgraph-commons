# RepairGraph Commons

[한국어](README.md) | English

RepairGraph Commons defines an open symptom–cause–part–procedure knowledge-graph format with validation and deterministic search tools.

## Install and run

```bash
git clone https://github.com/Kwondh0321/repairgraph-commons.git
cd repairgraph-commons
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
python -m pip install .
repairgraph validate data/example.graph.json
repairgraph query data/example.graph.json "laptop will not charge"
```

Node types are `device`, `symptom`, `cause`, `part`, `procedure`, and `safety`. Validation rejects duplicate IDs, unknown endpoints, unsupported types, invalid confidence values, malformed alias/tag arrays, and procedures without a source citation.

Diagnostic rankings are suggestions based on graph edges, not professional repair or electrical-safety advice. Always consult device-specific service and safety documentation.

## Contributing data

Submit small, sourced changes with tests. Do not copy copyrighted service manuals or add uncertain compatibility claims. See [CONTRIBUTING.md](CONTRIBUTING.md).

The code is MIT licensed. Example graph data in `data/` is CC-BY-4.0.
