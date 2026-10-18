"""Shared pytest fixtures for ESPHome display snapshot tests."""

from __future__ import annotations

from collections.abc import Callable
import io
import os
from pathlib import Path
import subprocess
import sys

from PIL import Image, ImageOps
import pytest
from syrupy.assertion import SnapshotAssertion
from syrupy.extensions.image import PNGImageSnapshotExtension

REPO_ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture
def snapshot_png(snapshot: SnapshotAssertion) -> SnapshotAssertion:
    """Return a syrupy snapshot fixture configured to store PNG files."""
    return snapshot.use_extension(PNGImageSnapshotExtension)


@pytest.fixture(scope="session")
def compile_preview() -> Callable[[Path | str], Path]:
    """Session-scoped compiler cache for ESPHome host preview configurations."""
    compiled: dict[Path, Path] = {}

    def _compile(config_file: Path | str) -> Path:
        config_path = (REPO_ROOT / config_file).resolve()
        if config_path not in compiled:
            cmd = [sys.executable, "-m", "esphome", "compile", str(config_path)]
            subprocess.run(cmd, cwd=REPO_ROOT, check=True)
            name = config_path.stem
            program = (
                config_path.parent
                / ".esphome"
                / "build"
                / name
                / ".pioenvs"
                / name
                / "program"
            )
            assert program.exists(), f"Compiled host binary not found at {program}"
            compiled[config_path] = program
        return compiled[config_path]

    return _compile


@pytest.fixture
def render_display_png(
    compile_preview: Callable[[Path | str], Path],
    tmp_path: Path,
) -> Callable[[Path | str], bytes]:
    """Compile and run an ESPHome host preview config and return inverted e-paper PNG bytes."""

    def _render(config_file: Path | str) -> bytes:
        program = compile_preview(config_file)
        env = os.environ.copy()
        env["ESPHOME_SNAPSHOT_DIR"] = str(tmp_path)
        env["TZ"] = "UTC"

        subprocess.run([str(program)], cwd=REPO_ROOT, env=env, check=True)

        bmp_files = list(tmp_path.glob("*.bmp"))
        assert len(bmp_files) == 1, f"Expected 1 BMP snapshot in {tmp_path}, found {bmp_files}"

        with Image.open(bmp_files[0]) as img:
            # Invert RGB so COLOR_ON renders as black ink on white paper
            eink_img = ImageOps.invert(img.convert("RGB"))
            buf = io.BytesIO()
            eink_img.save(buf, format="PNG")
            return buf.getvalue()

    return _render
