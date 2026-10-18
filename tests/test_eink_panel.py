"""Offline golden snapshot tests for displays/eink-panel.yaml using syrupy."""

from __future__ import annotations

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
PREVIEW_CONFIG = REPO_ROOT / "displays" / "packages" / "eink-panel-preview.yaml"


@pytest.fixture
def snapshot_png(snapshot: SnapshotAssertion) -> SnapshotAssertion:
    """Return a syrupy snapshot fixture configured to store PNG files."""
    return snapshot.use_extension(PNGImageSnapshotExtension)


@pytest.fixture(scope="session")
def eink_panel_program() -> Path:
    """Compile the host snapshot binary for eink-panel once per test session."""
    cmd = [sys.executable, "-m", "esphome", "compile", str(PREVIEW_CONFIG)]
    subprocess.run(cmd, cwd=REPO_ROOT, check=True)

    program = (
        PREVIEW_CONFIG.parent
        / ".esphome"
        / "build"
        / "eink-panel-preview"
        / ".pioenvs"
        / "eink-panel-preview"
        / "program"
    )
    assert program.exists(), f"Compiled host binary not found at {program}"
    return program


def render_eink_panel_png(program: Path, tmp_path: Path) -> bytes:
    """Run the compiled host binary and return the rendered e-paper PNG bytes."""
    env = os.environ.copy()
    env["ESPHOME_SNAPSHOT_DIR"] = str(tmp_path)

    subprocess.run([str(program)], cwd=REPO_ROOT, env=env, check=True)

    bmp_path = tmp_path / "eink-panel-preview.bmp"
    assert bmp_path.exists(), f"Snapshot BMP was not created at {bmp_path}"

    with Image.open(bmp_path) as img:
        # Invert RGB so COLOR_ON renders as black ink on white paper like Waveshare 7.5inV2
        eink_img = ImageOps.invert(img.convert("RGB"))
        buf = io.BytesIO()
        eink_img.save(buf, format="PNG")
        return buf.getvalue()


def test_eink_panel_default_render(
    eink_panel_program: Path,
    tmp_path: Path,
    snapshot_png: SnapshotAssertion,
) -> None:
    """Verify eink-panel rendering against the syrupy PNG snapshot."""
    assert render_eink_panel_png(eink_panel_program, tmp_path) == snapshot_png
