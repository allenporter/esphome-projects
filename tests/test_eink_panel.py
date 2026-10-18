"""Offline golden snapshot tests for displays/eink-panel.yaml."""

from __future__ import annotations

from collections.abc import Callable

from syrupy.assertion import SnapshotAssertion


def test_eink_panel_default_render(
    render_display_png: Callable[[str], bytes],
    snapshot_png: SnapshotAssertion,
) -> None:
    """Verify eink-panel rendering against the syrupy PNG snapshot."""
    assert render_display_png("eink-panel-preview") == snapshot_png
