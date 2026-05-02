# detection_face

Photo analysis pipeline: camera health (black image, blur).
## Quick start

```bash
uv sync
uv run python -m detection_face.entrypoints.cli data/samples/image.jpg
```

The CLI defaults to `analyze`; this is equivalent:

```bash
uv run python -m detection_face.entrypoints.cli analyze data/samples/image.jpg
```

Multiple images are supported:

```bash
uv run python -m detection_face.entrypoints.cli data/samples/images/99/*
```

```
## Configuration

YAML files in `configs/`:

- `global.yaml` — `artifacts_dir`, `log_level`
- `camera_health.yaml` — `black_threshold`, `blur_threshold`.

## Lint

```bash
uv run pre-commit run --all-files
```
