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
PACKAGES_DIR = REPO_ROOT / "displays" / "packages"


@pytest.fixture
def snapshot_png(snapshot: SnapshotAssertion) -> SnapshotAssertion:
    """Return a syrupy snapshot fixture configured to store PNG files."""
    return snapshot.use_extension(PNGImageSnapshotExtension)


@pytest.fixture(scope="session")
def compile_preview() -> Callable[[str], Path]:
    """Session-scoped compiler cache for ESPHome host preview configurations."""
    compiled: dict[str, Path] = {}

    def _compile(preview_name: str) -> Path:
        if preview_name not in compiled:
            config_path = PACKAGES_DIR / f"{preview_name}.yaml"
            cmd = [sys.executable, "-m", "esphome", "compile", str(config_path)]
            subprocess.run(cmd, cwd=REPO_ROOT, check=True)
            program = (
                PACKAGES_DIR
                / ".esphome"
                / "build"
                / preview_name
                / ".pioenvs"
                / preview_name
                / "program"
            )
            assert program.exists(), f"Compiled host binary not found at {program}"
            compiled[preview_name] = program
        return compiled[preview_name]

    return _compile


@pytest.fixture
def render_display_png(
    compile_preview: Callable[[str], Path],
    tmp_path: Path,
) -> Callable[[str], bytes]:
    """Compile and run an ESPHome host preview config and return inverted e-paper PNG bytes."""

    def _render(preview_name: str) -> bytes:
        program = compile_preview(preview_name)
        env = os.environ.copy()
        env["ESPHOME_SNAPSHOT_DIR"] = str(tmp_path)
        env["TZ"] = "UTC"

        subprocess.run([str(program)], cwd=REPO_ROOT, env=env, check=True)

        bmp_path = tmp_path / f"{preview_name}.bmp"
        assert bmp_path.exists(), f"Snapshot BMP was not created at {bmp_path}"

        with Image.open(bmp_path) as img:
            # Invert RGB so COLOR_ON renders as black ink on white paper
            eink_img = ImageOps.invert(img.convert("RGB"))
            buf = io.BytesIO()
            eink_img.save(buf, format="PNG")
            return buf.getvalue()

    return _render
