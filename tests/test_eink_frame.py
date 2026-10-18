"""Offline golden snapshot tests for displays/eink-frame.yaml."""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

from syrupy.assertion import SnapshotAssertion


def test_eink_frame_default_render(
    render_display_png: Callable[[Path | str], bytes],
    snapshot_png: SnapshotAssertion,
) -> None:
    """Verify eink-frame rendering against the syrupy PNG snapshot."""
    assert render_display_png("tests/eink-frame-preview.yaml") == snapshot_png
