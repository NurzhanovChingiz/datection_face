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

## Graph export

The pipeline execution uses LangGraph internally for deterministic stage orchestration.

To save the generated Mermaid graph diagram for a run:

```bash
uv run python -m detection_face.entrypoints.cli --save-graph data/samples/image.jpg
```

The diagram is written to:

```text
artifacts/runs/version_<N>/diagram/pipeline.mmd
```

You can open the `.mmd` file in any Mermaid-compatible renderer.

## Configuration

YAML files in `configs/`:

- `global.yaml` — `artifacts_dir`, `log_level`
- `camera_health.yaml` — `black_threshold`, `blur_threshold`.

## Lint

```bash
uv run pre-commit run --all-files
```
