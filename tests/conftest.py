"""Shared pytest fixtures for ESPHome display snapshot tests."""

from __future__ import annotations

from collections.abc import Callable
import io
import os
from pathlib import Path
import subprocess
import sys
import tempfile

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
) -> Callable[..., bytes]:
    """Compile and run an ESPHome host preview config and return PNG bytes."""

    def _render(config_file: Path | str, *, invert: bool = True) -> bytes:
        program = compile_preview(config_file)
        with tempfile.TemporaryDirectory(dir=tmp_path) as snapshot_dir:
            env = os.environ.copy()
            env["ESPHOME_SNAPSHOT_DIR"] = snapshot_dir
            env["TZ"] = "UTC"

            subprocess.run([str(program)], cwd=REPO_ROOT, env=env, check=True)

            bmp_files = list(Path(snapshot_dir).glob("*.bmp"))
            assert len(bmp_files) == 1, (
                f"Expected 1 BMP snapshot in {snapshot_dir}, found {bmp_files}"
            )

            with Image.open(bmp_files[0]) as img:
                rgb_img = img.convert("RGB")
                if invert:
                    # Invert RGB so COLOR_ON renders as black ink on white paper
                    rgb_img = ImageOps.invert(rgb_img)
                buf = io.BytesIO()
                rgb_img.save(buf, format="PNG")
                return buf.getvalue()

    return _render
