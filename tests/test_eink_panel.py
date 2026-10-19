"""Offline golden snapshot tests for displays/eink-panel.yaml and its modular themes."""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

import pytest
from syrupy.assertion import SnapshotAssertion

EINK_PANEL_THEMES = [
    ("wf01_cutaway", "tests/eink-panel-wf01-preview.yaml"),
    ("wf02_splitflap", "tests/eink-panel-wf02-preview.yaml"),
    ("wf03_meteogram", "tests/eink-panel-wf03-preview.yaml"),
    ("wf04_broadsheet", "tests/eink-panel-wf04-preview.yaml"),
    ("wf05_macos1984", "tests/eink-panel-wf05-preview.yaml"),
    ("wf06_fieldchrono", "tests/eink-panel-wf06-preview.yaml"),
    ("bal01_rp1_v2", "tests/eink-panel-bal01-preview.yaml"),
]


def test_eink_panel_default_render(
    render_display_png: Callable[[Path | str], bytes],
    snapshot_png: SnapshotAssertion,
) -> None:
    """Verify active eink-panel rendering against the syrupy PNG snapshot."""
    assert render_display_png("tests/eink-panel-preview.yaml") == snapshot_png


@pytest.mark.parametrize(
    ("theme_id", "preview_config"),
    EINK_PANEL_THEMES,
    ids=[theme_id for theme_id, _ in EINK_PANEL_THEMES],
)
def test_eink_panel_themes(
    theme_id: str,
    preview_config: str,
    render_display_png: Callable[[Path | str], bytes],
    snapshot_png: SnapshotAssertion,
) -> None:
    """Verify each modular ESPHome eink-panel theme package against its golden PNG snapshot."""
    assert render_display_png(preview_config) == snapshot_png
