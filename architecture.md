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
├── report_template.md
├── architecture.md
├── architecture.png (optional visual diagram)
├── configs/
│   ├── default.yaml
│   └── camera_health.yaml
├── data/
│   ├── raw/
│   ├── processed/
│   └── samples/
├── notebooks/
│   └── 01_eda.ipynb
├── artifacts/
│   ├── models/
│   └── runs/
│       └── <model_version>/<run_id>/
│           ├── config.yaml
│           ├── metadata.json
│           ├── logs/
│           │   ├── inference.log
│           │   └── errors.log
│           ├── predictions/
│           │   ├── images/
│           │   └── json/
│           ├── metrics/
│           │   ├── metrics.json
│           │   └── benchmark.csv
│           └── errors/
│               ├── failed_images/
│               └── debug_crops/
├── src/
│   └── detection_face/
│       ├── py.typed
│       ├── composition.py
│       ├── domain/
│       │   ├── entities/
│       │   │   ├── image.py
│       │   │   ├── camera_health_result.py
│       │   │   ├── bbox_face.py
│       │   └── services/
│       │       └── ports/
│       │           └── black_frame_checker.py
│       ├── application/
│       │   ├── gateways/
│       │   │   ├── image_source.py
│       │   │   ├── prediction_writer.py
│       │   │   └── run_logger.py
│       │   ├── use_cases/
│       │   │   └── check_camera_health.py
│       │   └── pipeline/
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
│       ├── entrypoints/
│       │   ├── cli/
│       │   │   ├── __main__.py
│       │   │   └── analyze.py
│       │   └── api/
│       │       ├── main.py
│       │       └── routers/
│       │           └── analyze.py
├── tests/
│   ├── conftest.py
│   ├── unit/
│   │   ├── domain/
│   │   ├── application/
│   │   │   └── test_check_camera_health.py
│   └── infrastructure/
│       └── integration/
│           └── test_analyze_photo_pipeline.py
└── docker/
    ├── Dockerfile
    └── docker-compose.yaml