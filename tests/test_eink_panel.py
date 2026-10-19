"""Offline golden snapshot tests for displays/eink-panel.yaml and its modular themes."""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

from syrupy.assertion import SnapshotAssertion


def test_eink_panel_default_render(
    render_display_png: Callable[[Path | str], bytes],
    snapshot_png: SnapshotAssertion,
) -> None:
    """Verify active eink-panel rendering against the syrupy PNG snapshot."""
    assert render_display_png("tests/eink-panel-preview.yaml") == snapshot_png


def test_eink_panel_theme_wf01_cutaway(
    render_display_png: Callable[[Path | str], bytes],
    snapshot_png: SnapshotAssertion,
) -> None:
    """Verify WF-01 Architectural Cutaway theme package against its golden PNG snapshot."""
    assert render_display_png("tests/eink-panel-wf01-preview.yaml") == snapshot_png


def test_eink_panel_theme_wf02_splitflap(
    render_display_png: Callable[[Path | str], bytes],
    snapshot_png: SnapshotAssertion,
) -> None:
    """Verify WF-02 Solari Split-Flap theme package against its golden PNG snapshot."""
    assert render_display_png("tests/eink-panel-wf02-preview.yaml") == snapshot_png


def test_eink_panel_theme_wf03_meteogram(
    render_display_png: Callable[[Path | str], bytes],
    snapshot_png: SnapshotAssertion,
) -> None:
    """Verify WF-03 R-P1 x Halftone Meteogram theme package against its golden PNG snapshot."""
    assert render_display_png("tests/eink-panel-wf03-preview.yaml") == snapshot_png


def test_eink_panel_theme_wf04_broadsheet(
    render_display_png: Callable[[Path | str], bytes],
    snapshot_png: SnapshotAssertion,
) -> None:
    """Verify WF-04 Editorial Broadsheet theme package against its golden PNG snapshot."""
    assert render_display_png("tests/eink-panel-wf04-preview.yaml") == snapshot_png


def test_eink_panel_theme_wf05_macos1984(
    render_display_png: Callable[[Path | str], bytes],
    snapshot_png: SnapshotAssertion,
) -> None:
    """Verify WF-05 1984 Macintosh Desktop theme package against its golden PNG snapshot."""
    assert render_display_png("tests/eink-panel-wf05-preview.yaml") == snapshot_png


def test_eink_panel_theme_wf06_fieldchrono(
    render_display_png: Callable[[Path | str], bytes],
    snapshot_png: SnapshotAssertion,
) -> None:
    """Verify WF-06 Casio Field Chrono theme package against its golden PNG snapshot."""
    assert render_display_png("tests/eink-panel-wf06-preview.yaml") == snapshot_png


def test_eink_panel_theme_bal01_rp1_v2(
    render_display_png: Callable[[Path | str], bytes],
    snapshot_png: SnapshotAssertion,
) -> None:
    """Verify BAL-01 R-P1 Balanced v2 theme package against its golden PNG snapshot."""
    assert render_display_png("tests/eink-panel-bal01-preview.yaml") == snapshot_png
