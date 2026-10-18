"""Offline golden snapshot tests for displays/eink-frame.yaml."""

from __future__ import annotations

from collections.abc import Callable

from syrupy.assertion import SnapshotAssertion


def test_eink_frame_default_render(
    render_display_png: Callable[[str], bytes],
    snapshot_png: SnapshotAssertion,
) -> None:
    """Verify eink-frame rendering against the syrupy PNG snapshot."""
    assert render_display_png("eink-frame-preview") == snapshot_png
