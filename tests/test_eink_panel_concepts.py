"""Golden PNG snapshot tests for the full 24-concept e-ink panel tournament gallery."""

from __future__ import annotations

import io
from pathlib import Path
import sys
from typing import Any

from PIL import Image
import pytest
from syrupy.assertion import SnapshotAssertion

sys.path.insert(0, str(Path(__file__).resolve().parent))
from concepts import (
    tournament_balanced,
    tournament_wild_finals,
    tournament_wild_r1,
)

CONCEPT_RENDERERS: list[tuple[str, Any, str]] = [
    # 6 Wild & Balanced Championship Finalists
    ("wf_01_architectural_cutaway", tournament_wild_finals, "render_wf_01"),
    ("wf_02_solari_split_flap", tournament_wild_finals, "render_wf_02"),
    ("wf_03_rp1_halftone_meteogram", tournament_wild_finals, "render_wf_03"),
    ("wf_04_editorial_broadsheet", tournament_wild_finals, "render_wf_04"),
    ("wf_05_macos_1984_desktop", tournament_wild_finals, "render_wf_05"),
    ("wf_06_casio_field_chrono", tournament_wild_finals, "render_wf_06"),
    # 8 Balanced Grid & Split Concepts
    ("bal_01_rp1_balanced_v2", tournament_balanced, "render_bal_01"),
    ("bal_02_weather_station_3tier", tournament_balanced, "render_bal_02"),
    ("bal_03_executive_quadrant", tournament_balanced, "render_bal_03"),
    ("bal_04_bento_8card_grid", tournament_balanced, "render_bal_04"),
    ("bal_05_swiss_newspaper", tournament_balanced, "render_bal_05"),
    ("bal_06_dark_telemetry_deck", tournament_balanced, "render_bal_06"),
    ("bal_07_nordic_4column", tournament_balanced, "render_bal_07"),
    ("bal_08_right_black_anchor", tournament_balanced, "render_bal_08"),
    # 10 Wild Departure Round 1 Concepts
    ("w1_01_solari_board", tournament_wild_r1, "render_w1_01"),
    ("w1_02_york_dispatch_broadsheet", tournament_wild_r1, "render_w1_02"),
    ("w1_03_house_blueprint_r1", tournament_wild_r1, "render_w1_03"),
    ("w1_04_macos_system1_r1", tournament_wild_r1, "render_w1_04"),
    ("w1_05_casio_gshock_r1", tournament_wild_r1, "render_w1_05"),
    ("w1_06_unix_tmux_terminal", tournament_wild_r1, "render_w1_06"),
    ("w1_07_yrno_meteogram_r1", tournament_wild_r1, "render_w1_07"),
    ("w1_08_star_trek_lcars", tournament_wild_r1, "render_w1_08"),
    ("w1_09_jr_shinkansen_consist", tournament_wild_r1, "render_w1_09"),
    ("w1_10_bauhaus_constructivist", tournament_wild_r1, "render_w1_10"),
]


def _make_concept_test(concept_id: str, module: Any, func_name: str) -> Any:
    def _test(
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
        snapshot_png: SnapshotAssertion,
    ) -> None:
        monkeypatch.setattr(module, "OUT_DIR", str(tmp_path))
        render_fn = getattr(module, func_name)
        render_fn()
        short_prefix = "_".join(concept_id.split("_")[:2])
        out_file = tmp_path / f"{short_prefix}.png"
        assert out_file.exists(), f"Expected rendered concept at {out_file}"
        with Image.open(out_file) as img:
            buf = io.BytesIO()
            img.convert("RGB").save(buf, format="PNG")
            assert buf.getvalue() == snapshot_png

    _test.__name__ = f"test_concept_{concept_id}"
    _test.__qualname__ = f"test_concept_{concept_id}"
    return _test


for _cid, _mod, _fn in CONCEPT_RENDERERS:
    globals()[f"test_concept_{_cid}"] = _make_concept_test(_cid, _mod, _fn)
