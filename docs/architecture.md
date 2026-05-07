# `Detection face` Architecture

## Repository Layout

```text
detection_face/
├── .gitignore
├── .python-version
├── .pre-commit-config.yaml
├── pyproject.toml
├── uv.lock
├── README.md
│
├── configs/
│   ├── global.yaml              # shared: artifacts_dir, log_level, device
├── data/
│   ├── raw/
│   ├── processed/
│   ├── samples/
│   └── known_faces/             # per-person subfolders with .npy embeddings
│
├── docs/
│   ├── report_template.md
│   ├── data_flow.md
│   ├── api_contracts.md
│   └── architecture.md
│
├── notebooks/
│   └── 01_eda.ipynb
├── artifacts/
│   ├── models/
│   └── runs/
│       └── version_1/
│           ├── logs/
│           │   └── inference.log
│           ├── predictions/
│               └── json/
│           ├── diagram/
│               └── pipeline.mmd
├── src/
│   └── detection_face/
│       ├── py.typed
│       ├── composition.py
│       ├── domain/
│       │   ├── entities/
│       │   │   ├── image.py
│       │   │   ├── camera_health_result.py
│       │   └── ports/
│       │       └── black_frame_checker.py
│       ├── application/           # use cases orchestrate ports + domain
│       │   ├── gateways/
│       │   │   ├── image_source.py
│       │   │   ├── prediction_writer.py
│       │   │   └── run_logger.py
│       │   ├── use_cases/
│       │   │   ├── check_camera_health.py
│       │   └── pipeline/
│       │       ├── analyze_photo_graph.py
│       │       └── analyze_photo_pipeline.py
│       ├── infrastructure/
│       │   ├── config/
│       │   │   └── yaml_loader.py
│       │   ├── io/
│       │   │   └── image_reader.py
│       │   ├── storage/
│       │   │   └── filesystem_prediction_writer.py
│       │   ├── logging/
│       │   │   └── filesystem_run_logger.py
│       │   └── models/
│       │       └── camera_health/
│       │           └── black_frame.py
│       └── entrypoints/
│           └── cli/
│               ├── __main__.py
│               └── analyze.py
└── tests/
    ├── conftest.py
    ├── unit/
    │   ├── domain/
    │   ├── application/
    │   │   └── test_check_camera_health.py
    │   └── infrastructure/
    └── integration/
        └── test_analyze_photo_pipeline.py
