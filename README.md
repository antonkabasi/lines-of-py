# lines-of-py

A simple CLI tool to count all your Python (supports other extensions!) lines of code—and help you estimate the “time invested” in Python over the years.

> **Why?**  
> I wondered: how many hours have I actually spent coding in Python during my PhD as an experimental physicist? 

> Counting lines of code is a rough estimate for time spent. This tool lets you scan your folders, see progress as it runs, and gradually refine what to include or exclude using the CLI. In a few iterations you can really nail down the actual number.  

> It also supports counting only unique lines to avoid counting repeated boilerplate, generating reports, top-file histograms, and time estimates.

> Counts files ending in .py by default, but you can scan other extensions (js, sh, etc.) via --ext.
---

## Installation

1. **Clone the repo**  
   ```bash
   git clone https://github.com/antonkabasi/lines-of-py.git
   cd lines-of-py
   ```
2. **Make executable** (very optional)  
   ```bash
   chmod +x lines_of_py.py
   ```

---

## Usage

```bash
python lines_of_py.py [PATH] [OPTIONS]
```

- **PATH**  
  Directory to scan. Defaults to your home folder (`$HOME` or `%USERPROFILE%`depending on OS).

### Options

| Flag                     | Description                                                          |
|--------------------------|----------------------------------------------------------------------|
| `--exclude "a,b,c"`      | Skip folders/subfolders matching any of these names(comma-separated).|
| `--ext "py,js,sh"`       | File extensions to include (default: `py`).                          |
| `--ignore-duplicates`    | Count only unique lines across all files.                            |
| `--verbose`              | Print progress every 100 files.                                      |
| `--verbose-all`          | Print progress for every single file (useful when narrowing down     | 
|                          | unwanted scan                                                        |
| `--estimate-hours N`     | LOC per hour rate for time estimation (default: 50).                 |
| `--top-files N`          | Show the top N files by raw line count.                              |
| `--hist-limit N`         | Number of entries in the ASCII histogram (default: 10).              |
| `--report FILE.md`       | Write a Markdown report (totals, estimates, top-files, histogram)    |
|                          | to `FILE.md`.                                                        |
| `-h`, `--help`           | Show help message and exit.                                          |



## Suggested Workflow

1. **Initial run**  
   ```bash
   python lines_of_py.py --verbose
   ```
   See total LOC and which folders were scanned.

2. **Exclude noise**  
   Spot unwanted paths in the verbose log (e.g. `Downloads`, `OneDrive`, `site-packages`) and rerun:
   ```bash
   python lines_of_py.py ~ --exclude "Downloads,OneDrive,site-packages" --verbose
   ```

3. **Refine**  
   Repeat adding excludes until only your projects remain (~100–200 files).

4. **Deep scan**  
   ```bash
   python lines_of_py.py --exclude "Downloads,OneDrive,site-packages,other-noise" --verbose-all
   ```
   Inspect every file and update your exclude list.

5. **Compare duplicates**  
   ```bash
   python lines_of_py.py --ignore-duplicates
   ```
   See unique vs. total LOC to notice how much time you spend writing boilerplate.

6. **Top files & histogram**  
   ```bash
   python lines_of_py.py --top-files 20 --hist-limit 20
   python lines_of_py.py --report report.md
   ```
   Identify your largest scripts and generate a full report.

7. **Enjoy your estimate**  
   ```
   Estimated time = Total LOC ÷ LOC_per_hour
   ```

---

## Examples

```bash
# Scan projects only, show every file, estimate at 50 LOC/hr
python lines_of_py.py \
  --report report.md \
  --hist-limit 20 \
  --ext "py" \
  --verbose \
  --estimate-hours 80 \
  --top-files 5
```
## Example report:

```markdown
# lines-of-py Report

- Total lines: **34802**
- Estimated hours (@50 LOC/hr): **696.0**

## Top 5 files
- /home/anton/anton-github-site/conf.py: 1415
- /home/anton/pdfcompare/pdf_diff_with_metadata.py: 516
- /home/anton/pdfcompare/pdf_compare_Backup.py: 427
- /home/anton/measurements-sqlite/good stuff/calculations/calculate thermal conductivity from db.py: 421
- /home/anton/measurements-sqlite/good stuff/make db/1 add measurements from all subfolders.py: 408

## Histogram (top 20 files by raw lines)
/home/anton/anton-github-site/conf.py    | ████████████████████████████████████████ 1415
.../pdfcompare/pdf_diff_with_metadata.py | ██████████████ 516
.../pdfcompare/pdf_compare_Backup.py     | ████████████ 427
alculate thermal conductivity from db.py | ███████████ 421
 add measurements from all subfolders.py | ███████████ 408
ot all thermal conductivities from db.py | ███████████ 399
.../library_3omega.py                    | ██████████ 381
.../library_3omega.py                    | ██████████ 381
.../10_fine_solver.py                    | ██████████ 379
.../10_steady_state_solver.py            | █████████ 348
v3omega pairs by temperature plotting.py | █████████ 343
.../9_fine_solver.py                     | █████████ 343
/home/anton/heat-solver/9_fine_solver.py | █████████ 343
.../9_rough_solver.py                    | █████████ 342
.../anton/heat-solver/9_rough_solver.py  | █████████ 342
d/v3omega pairs by temperature export.py | █████████ 334
.../10_rough_solver.py                   | █████████ 334
 add measurements from all subfolders.py | █████████ 321
nt_CN_adaptive_step_until_convergence.py | ████████ 303
_solver_2d_optimized_rectangle_source.py | ████████ 302
```


## License

This project is licensed under the [MIT License].  
