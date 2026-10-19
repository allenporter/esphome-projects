# E-Ink Panel (`800×480`) Theme & Concept Gallery

This directory contains the 7 championship **native ESPHome C++ display themes** for [`displays/eink-panel.yaml`](../../eink-panel.yaml), along with golden PNG snapshots generated via ESPHome's `host` platform (`pytest`) in [`tests/__snapshots__/`](../../../tests/__snapshots__/).

To switch the active layout on `eink-panel`, update the single `!include` line in [`displays/packages/eink-panel-display.yaml`](../eink-panel-display.yaml).

---

## 1. Native ESPHome C++ Themes (`displays/packages/themes/*.yaml`)

### WF-03: R-P1 Split-Contrast × Yr.no Halftone Meteogram *(Active Default)*
- **Package**: [`eink-panel-wf03-meteogram.yaml`](eink-panel-wf03-meteogram.yaml)
- **Fonts**: `Montserrat Black`, `Gotham Rounded Bold/Book`, `Space Mono Bold`, `Material Design Icons`

![WF-03: R-P1 Split-Contrast × Halftone Meteogram](../../../tests/__snapshots__/test_eink_panel/test_eink_panel_themes%5Bwf03_meteogram%5D.png)

---

### WF-01: Architectural Property Cutaway × Meteogram Sky
- **Package**: [`eink-panel-wf01-cutaway.yaml`](eink-panel-wf01-cutaway.yaml)
- **Fonts**: `Bebas Neue`, `Share Tech Mono`, `Montserrat Black`, `Gotham Rounded`

![WF-01: Architectural Property Cutaway](../../../tests/__snapshots__/test_eink_panel/test_eink_panel_themes%5Bwf01_cutaway%5D.png)

---

### WF-02: Solari Split-Flap × JR Express Departure Board
- **Package**: [`eink-panel-wf02-splitflap.yaml`](eink-panel-wf02-splitflap.yaml)
- **Fonts**: `Bebas Neue`, `Share Tech Mono`, `Gotham Rounded Book`

![WF-02: Solari Split-Flap Departure Board](../../../tests/__snapshots__/test_eink_panel/test_eink_panel_themes%5Bwf02_splitflap%5D.png)

---

### WF-04: The Woodgreen Editorial Broadsheet & Almanac
- **Package**: [`eink-panel-wf04-broadsheet.yaml`](eink-panel-wf04-broadsheet.yaml)
- **Fonts**: `DM Serif Display` (Regular & Italic), `Bebas Neue`, `Gotham Rounded Bold`

![WF-04: Editorial Broadsheet & Almanac](../../../tests/__snapshots__/test_eink_panel/test_eink_panel_themes%5Bwf04_broadsheet%5D.png)

---

### WF-05: 1984 Apple Macintosh System 1 / HyperCard Desktop v2
- **Package**: [`eink-panel-wf05-macos1984.yaml`](eink-panel-wf05-macos1984.yaml)
- **Fonts**: `Silkscreen` (Bold & Regular), `VT323`

![WF-05: 1984 Apple Macintosh Desktop](../../../tests/__snapshots__/test_eink_panel/test_eink_panel_themes%5Bwf05_macos1984%5D.png)

---

### WF-06: Casio G-Shock × Teenage Engineering Field Chrono v2
- **Package**: [`eink-panel-wf06-fieldchrono.yaml`](eink-panel-wf06-fieldchrono.yaml)
- **Fonts**: `Chakra Petch` (Bold & Regular)

![WF-06: Casio G-Shock × Teenage Engineering Field Chrono](../../../tests/__snapshots__/test_eink_panel/test_eink_panel_themes%5Bwf06_fieldchrono%5D.png)

---

### BAL-01: R-P1 Balanced v2 (5 Hourly Columns + White RH% Pills)
- **Package**: [`eink-panel-bal01-rp1-v2.yaml`](eink-panel-bal01-rp1-v2.yaml)
- **Fonts**: `Montserrat Black`, `Gotham Rounded Bold/Book`

![BAL-01: R-P1 Balanced v2](../../../tests/__snapshots__/test_eink_panel/test_eink_panel_themes%5Bbal01_rp1_v2%5D.png)

---

## 2. Full Tournament Concept Gallery (`tests/__snapshots__/test_eink_panel_concepts/`)

### Wild Round 1 Departures (`W1-01` .. `W1-10`)

| Concept | Preview |
| :--- | :--- |
| **W1-01: Solari Split-Flap Board** | ![W1-01](../../../tests/__snapshots__/test_eink_panel_concepts/test_eink_panel_concept_gallery%5Bw1_01_solari_board%5D.png) |
| **W1-02: The Woodgreen Dispatch Broadsheet** | ![W1-02](../../../tests/__snapshots__/test_eink_panel_concepts/test_eink_panel_concept_gallery%5Bw1_02_york_dispatch_broadsheet%5D.png) |
| **W1-03: Architectural Blueprint Cutaway** | ![W1-03](../../../tests/__snapshots__/test_eink_panel_concepts/test_eink_panel_concept_gallery%5Bw1_03_house_blueprint_r1%5D.png) |
| **W1-04: 1984 Macintosh System 1 Desktop** | ![W1-04](../../../tests/__snapshots__/test_eink_panel_concepts/test_eink_panel_concept_gallery%5Bw1_04_macos_system1_r1%5D.png) |
| **W1-05: Casio G-Shock Field Watch** | ![W1-05](../../../tests/__snapshots__/test_eink_panel_concepts/test_eink_panel_concept_gallery%5Bw1_05_casio_gshock_r1%5D.png) |
| **W1-06: UNIX `tmux` / `btop` Terminal** | ![W1-06](../../../tests/__snapshots__/test_eink_panel_concepts/test_eink_panel_concept_gallery%5Bw1_06_unix_tmux_terminal%5D.png) |
| **W1-07: Yr.no Full-Width Halftone Meteogram** | ![W1-07](../../../tests/__snapshots__/test_eink_panel_concepts/test_eink_panel_concept_gallery%5Bw1_07_yrno_meteogram_r1%5D.png) |
| **W1-08: Star Trek LCARS Biocomputer** | ![W1-08](../../../tests/__snapshots__/test_eink_panel_concepts/test_eink_panel_concept_gallery%5Bw1_08_star_trek_lcars%5D.png) |
| **W1-09: JR Shinkansen 6-Car Train Consist** | ![W1-09](../../../tests/__snapshots__/test_eink_panel_concepts/test_eink_panel_concept_gallery%5Bw1_09_jr_shinkansen_consist%5D.png) |
| **W1-10: Bauhaus / Constructivist Poster** | ![W1-10](../../../tests/__snapshots__/test_eink_panel_concepts/test_eink_panel_concept_gallery%5Bw1_10_bauhaus_constructivist%5D.png) |

---

### Balanced Grid & Split Explorations (`BAL-01` .. `BAL-08`)

| Concept | Preview |
| :--- | :--- |
| **BAL-01: R-P1 Balanced v2** | ![BAL-01](../../../tests/__snapshots__/test_eink_panel_concepts/test_eink_panel_concept_gallery%5Bbal_01_rp1_balanced_v2%5D.png) |
| **BAL-02: Weather Station 3-Tier** | ![BAL-02](../../../tests/__snapshots__/test_eink_panel_concepts/test_eink_panel_concept_gallery%5Bbal_02_weather_station_3tier%5D.png) |
| **BAL-03: Executive 4-Quadrant Grid** | ![BAL-03](../../../tests/__snapshots__/test_eink_panel_concepts/test_eink_panel_concept_gallery%5Bbal_03_executive_quadrant%5D.png) |
| **BAL-04: 8-Card Bento Grid** | ![BAL-04](../../../tests/__snapshots__/test_eink_panel_concepts/test_eink_panel_concept_gallery%5Bbal_04_bento_8card_grid%5D.png) |
| **BAL-05: Swiss Newspaper Broadsheet** | ![BAL-05](../../../tests/__snapshots__/test_eink_panel_concepts/test_eink_panel_concept_gallery%5Bbal_05_swiss_newspaper%5D.png) |
| **BAL-06: Dark Telemetry Deck** | ![BAL-06](../../../tests/__snapshots__/test_eink_panel_concepts/test_eink_panel_concept_gallery%5Bbal_06_dark_telemetry_deck%5D.png) |
| **BAL-07: Nordic 4-Column Vertical** | ![BAL-07](../../../tests/__snapshots__/test_eink_panel_concepts/test_eink_panel_concept_gallery%5Bbal_07_nordic_4column%5D.png) |
| **BAL-08: Right Black Anchor** | ![BAL-08](../../../tests/__snapshots__/test_eink_panel_concepts/test_eink_panel_concept_gallery%5Bbal_08_right_black_anchor%5D.png) |
