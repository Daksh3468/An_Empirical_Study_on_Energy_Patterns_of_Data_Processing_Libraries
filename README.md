# Are Newer Library Versions Greener?
### An Empirical Study on Energy Patterns of Data Processing Libraries

This repository contains the full experimental infrastructure, raw measurements, and analysis pipeline for an empirical study on the energy consumption and execution time of four Python dataframe libraries — **Pandas**, **Polars**, **Dask**, and **Vaex** — across multiple versions, six benchmark datasets, and 19 dataframe operations spanning I/O, missing-data handling, row/column manipulation, and statistical aggregation.

Energy is measured at the hardware level using **PyJoules** (Intel RAPL), and results are validated with a non-parametric statistical pipeline (Shapiro–Wilk, Friedman, Wilcoxon signed-rank, Mann–Whitney U, Cliff's Delta).

---

## Repository Structure

```
.
├── Code/                              # Benchmark drivers, analysis scripts, notebook
│   ├── measure_<dataset>_<library>.py     # Energy measurement scripts (one per dataset × library)
│   ├── measure_water_dask_perf.py         # Auxiliary Dask perf-timing variant for Water Potability
│   ├── clear_cache_util.py                # Filesystem/CPU-cache clearing utility used before each run
│   ├── pandas.sh / polar.sh / dask.sh /   # Driver shell scripts: system prep + sequential
│   │   vaex.sh / census.sh                # execution of measurement scripts
│   ├── analysis.py                        # Per-tag outlier removal + energy/time summarization
│   ├── compute_p.py                       # Wilcoxon rank-sum p-value computation between variants
│   └── summary_generator_green_energy.ipynb   # Full statistical pipeline + all paper figures/tables
│
├── datasets/                           # Benchmark datasets (CSV + JSON) and prep utilities
│   ├── adult.csv / adult.json
│   ├── bank.csv / bank.json
│   ├── drugs.csv / drugs.json
│   ├── exam_score.csv / exam_score.json
│   ├── water_potability.csv / water_potability.json
│   ├── csv_to_json.py, importCsv.py, jsonToNdjson.py,   # Dataset conversion / preprocessing helpers
│   │   json_count.py, jsoncompress.py
│   └── (USCensus1990.csv / USCensus1990.json — see note below)
│
└── Results/                             # All raw measurements, statistical outputs, and figures
    ├── Pandas/Pandas_v<version>/Pandas_v<version>_itr(10|20|30)/*.csv
    ├── Polars/Polars_v<version>/...
    ├── Dask/Dask_v<version>/...
    ├── Vaex/Vaex_v<version>/...
    ├── summary_results/summary_<Library>/         # Per-tag mean/median/std summaries
    ├── Statistical_Analysis_Results/               # Shapiro, Friedman, Wilcoxon, Cliff's Delta workbooks
    ├── output_tables/, output_tables_1/            # Consolidated CSV/LaTeX tables used in the paper
    └── figures/                                    # All generated PNG/PDF figures
```

Library versions and their raw-data folder names:

| Library | Versions covered |
|---|---|
| Pandas | `v1.0.0`, `v2.0.0`, `v2.2.3` |
| Polars | `v0.20.0`, `v1.0.0`, `v1.31.0` |
| Dask   | `v2022.1.0`, `v2024.8.0`, `v2025.1.0` |
| Vaex   | `v4.13.0`, `v4.15.0`, `v4.17.0` |

Each version was benchmarked at three independent iteration settings — `itr(10)`, `itr(20)`, `itr(30)` — treated as separate measurement campaigns.

---

## US Census 1990 Dataset

> **Due to GitHub's file size limitations, the US Census 1990 dataset files are not included in this repository.**
>
> Download the dataset from the [UCI Machine Learning Repository](https://archive.ics.uci.edu/dataset/116/us+census+data+1990), and place the prepared files inside the `datasets/` directory as:
>
> ```
> datasets/USCensus1990.csv
> datasets/USCensus1990.json
> ```
>
> These exact filenames are hard-coded into `measure_census_pandas.py`, `measure_census_dask.py`, `measure_census_polars.py`, and `measure_census_vaex.py`. The `datasets/importCsv.py` and `datasets/import json.py` scripts can be used to subsample the full census file down to the row count used in the study (1,700,000 rows) before conversion. `datasets/csv_to_json.py` converts a prepared CSV into the matching JSON file.
>
> All other datasets (Adult, Bank Marketing, Drug Review, Student Exam Scores, Water Potability) are already included in `datasets/`.

---

## Reproducing the Experiments

### 1. Hardware and OS requirements

Energy measurement relies on **Intel RAPL** counters via PyJoules, so this must be run on:

- An **Intel CPU** with RAPL support (`/sys/devices/system/cpu/cpu*/cpufreq` and `/sys/devices/system/cpu/intel_pstate` present).
- **Linux** (the original study used Ubuntu 22.04.5 LTS). RAPL access via PyJoules is not available on Windows/macOS or on AMD/ARM processors.
- `sudo` privileges — cache clearing, CPU governor changes, and Turbo Boost toggling all require root.

### 2. Software environment

There is one measurement script per `(dataset, library)` pair, and the library **version** is pinned via whichever environment that script is executed in — the version string is baked into each script's output filename (e.g. `pandas_adult_v1.0.0_itr(30).csv`). To reproduce a specific library version, create an isolated environment per version and install accordingly, e.g.:

```bash
python3 -m venv venv-pandas-1.0.0
source venv-pandas-1.0.0/bin/activate
pip install pandas==1.0.0 pyJoules
```

Repeat for each version of each library you want to reproduce (`pandas==2.0.0`, `pandas==2.2.3`, `polars==0.20.0`, `polars==1.0.0`, `polars==1.31.0`, `dask[dataframe]==2022.1.0`, `dask[dataframe]==2024.8.0`, `dask[dataframe]==2025.1.0`, `vaex==4.13.0`, `vaex==4.15.0`, `vaex==4.17.0`). Note the Python interpreter constraints used in the study: Pandas v1.0.0 requires Python 3.7–3.8; all other library versions were run on Python 3.10.

Core packages needed in every environment:

```bash
pip install pyJoules pandas
```

plus the target library (`polars`, `dask[dataframe]`, or `vaex`) at the pinned version. No `requirements.txt` is bundled — dependencies must be installed per version as above.

### 3. System preparation (per run)

Each driver shell script (`pandas.sh`, `polar.sh`, `dask.sh`, `vaex.sh`, `census.sh`) performs the same system-isolation steps used in the paper before launching any measurement:

```bash
sync
echo 3 | sudo tee /proc/sys/vm/drop_caches         # drop filesystem caches
echo performance | sudo tee .../scaling_governor    # fix CPU governor
echo 1 | sudo tee .../intel_pstate/no_turbo         # disable Turbo Boost
```

`clear_cache_util.py`'s `clear_caches()` repeats a version of this before every individual benchmark operation inside each measurement script. For faithful reproduction, also disable networking, background services, and OS notifications, and keep ambient temperature stable, as described in the paper's methodology.

### 4. Running a benchmark

From inside `Code/`, with the appropriate versioned environment activated:

```bash
cd Code
sudo python measure_adult_pandas.py
```

This runs all 19 operations (I/O, missing-data, row/column, aggregation) on the Adult dataset for the number of iterations hard-coded in the script (default loop is `for i in range(30)`, i.e. `itr(30)`), sleeping 30 seconds between operations for thermal stabilization, and writes a PyJoules CSV such as `pandas_adult_v1.0.0_itr(30).csv` to the current directory.

To run every dataset for a given library sequentially (as done in the study), use the matching driver script:

```bash
cd Code
sudo bash pandas.sh   # runs adult, bank, exam, drug, water for Pandas
sudo bash polar.sh    # runs bank, exam, drug, water for Polars
sudo bash dask.sh     # runs bank, exam, drug, water for Dask
sudo bash vaex.sh     # runs bank, exam, drug, water for Vaex
```

The **US Census 1990** dataset is handled separately (it is far larger and was run as repeated single invocations, one `RUN` per Dask/Pandas/Polars/Vaex census script):

```bash
cd Code
sudo bash census.sh   # repeatedly invokes measure_census_dask.py with an incrementing run id
```

For Pandas/Polars/Vaex on Census, invoke the corresponding `measure_census_<library>.py` script directly the same way.

Before switching to the next library version, edit the `CSVHandler(...)` filename string near the top of the script (or install the new version into a fresh venv and rerun) so output files don't overwrite each other, and re-run the corresponding `.sh` script to repeat the same protocol for `itr(10)`, `itr(20)`, and `itr(30)` by adjusting the iteration loop count in the script.

Each run produces a semicolon-delimited CSV with columns:

```
timestamp;tag;duration;package_0;dram_0;core_0;uncore_0
```

where `tag` identifies the operation (`load_csv`, `groupby`, `mean`, …), `duration` is execution time in seconds, and `package_0`/`dram_0` are CPU package and DRAM energy in microjoules.

### 5. Summarizing and analyzing results

All summarization, statistical testing, and figure/table generation for this study have already been completed. Every figure and table reported in the paper was produced from `Code/summary_generator_green_energy.ipynb`, which contains the full pipeline: IQR/MAD-based outlier filtering, Shapiro–Wilk normality testing, the Friedman omnibus test, Wilcoxon signed-rank pairwise tests with Mann–Whitney U fallback, Cliff's Delta effect sizes, and Spearman energy–time correlation.

The outputs of this pipeline are already included in this repository and do not need to be regenerated:

- `Results/summary_results/summary_<Library>/` — per-tag mean/median/std summaries
- `Results/Statistical_Analysis_Results/` — Shapiro, Friedman, Wilcoxon, and Cliff's Delta result workbooks
- `Results/output_tables/`, `Results/output_tables_1/` — consolidated CSV/LaTeX tables (`table_I`–`table_IV`)
- `Results/figures/` — every generated PNG/PDF figure (`fig01`–`fig24`, `figure2`–`figure6`, etc.)

If you collect new raw measurements (Step 4) and want to extend or rerun the analysis, place the new CSVs into `Results/<Library>/<Library>_v<version>/<Library>_v<version>_itr(<N>)/`, matching the existing folder convention, then rerun the relevant cells of `Code/summary_generator_green_energy.ipynb` against that folder. Note the notebook was originally developed on Google Colab and defaults to Google Drive paths (e.g. `ROOT_DIR = Path("/content/drive/MyDrive/Green energy/daksh_results")`), so `ROOT_DIR`/`OUTPUT_DIR` at the top of each cell would need to be pointed at your local `Results/` directory instead.

`Code/analysis.py` (per-file MAD-based outlier removal/summary) and `Code/compute_p.py` (pairwise Wilcoxon rank-sum p-values) are lighter-weight standalone scripts kept in the repo for ad-hoc checks on individual CSVs, but they are not required to reproduce the paper's results — the notebook supersedes both.

### 6. Required Python packages for analysis

The analysis scripts and notebook (separate from the measurement environments above) need:

```bash
pip install pandas numpy scipy matplotlib seaborn openpyxl
```

---

## Benchmark Operations

| Category | Operations |
|---|---|
| I/O | `load_csv`, `load_json`, `save_csv`, `save_json` |
| Missing-data | `isna`, `dropna`, `fillna`, `replace` |
| Row/Column | `drop`, `groupby`, `merge`, `sort`, `concat` (`concat_dataframes`) |
| Aggregation | `count`, `sum`, `mean`, `min`, `max`, `unique` |

## Datasets

| Dataset | Rows | Size class | Source |
|---|---|---|---|
| Water Potability | 3,276 | Small | Kaggle |
| Student Exam Scores | 30,641 | Small | Kaggle |
| Adult | 48,842 | Small | UCI |
| Bank Marketing | 45,211 | Medium | Kaggle |
| Drug Review | 161,297 | Medium | UCI |
| US Census 1990 | 2,458,285 | Large | UCI (not bundled — see above) |

## Citation

If you use this repository, please cite the accompanying paper, *"Are Newer Library Versions Greener? An Empirical Study on Energy Patterns of Data Processing Libraries."*
