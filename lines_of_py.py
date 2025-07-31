#!/usr/bin/env python3
import os
import fnmatch
import argparse

COLOR_RESET = "\033[0m"
COLOR_GREEN = "\033[32m"
COLOR_CYAN = "\033[36m"
COLOR_YELLOW = "\033[33m"

def find_files(path, exclude_dirs, exts):
    files_list = []
    for root, dirs, files in os.walk(path):
        dirs[:] = [d for d in dirs if not any(ex in d.lower() for ex in exclude_dirs)]
        for ext in exts:
            for fname in fnmatch.filter(files, f"*.{ext}"):
                files_list.append(os.path.join(root, fname))
    return files_list

def count_lines(files, ignore_duplicates=False, verbose=False, verbose_all=False):
    total_lines = 0
    seen_lines = set()
    raw_counts = {}
    filtered_counts = {}

    for idx, filepath in enumerate(files, start=1):
        raw_count = 0
        filt_count = 0
        try:
            with open(filepath, encoding='utf-8', errors='ignore') as f:
                for line in f:
                    raw_count += 1
                    if ignore_duplicates:
                        if line not in seen_lines:
                            seen_lines.add(line)
                            total_lines += 1
                            filt_count += 1
                    else:
                        total_lines += 1
                        filt_count += 1
        except Exception:
            continue

        raw_counts[filepath] = raw_count
        filtered_counts[filepath] = filt_count

        if verbose_all:
            print(f"{COLOR_CYAN}[{idx}/{len(files)}] Processed:{COLOR_RESET} {filepath}")
        elif verbose and idx % 100 == 0:
            print(f"{COLOR_CYAN}[{idx}/{len(files)}] Processed:{COLOR_RESET} {filepath}")

    return total_lines, raw_counts, filtered_counts

def shorten_path(path, max_len=40):
    if len(path) <= max_len:
        return path
    parts = path.split(os.sep)
    for i in range(len(parts)):
        candidate = os.sep.join(['...'] + parts[i:])
        if len(candidate) <= max_len:
            return candidate
    return path[-max_len:]

def generate_histogram(counts, limit=10, max_bar_len=40, max_path_len=40):
    max_count = max(counts.values(), default=0)
    hist_lines = []
    for filepath, count in sorted(counts.items(), key=lambda x: x[1], reverse=True)[:limit]:
        bar_len = int((count / max_count) * max_bar_len) if max_count > 0 else 0
        bar = '█' * bar_len
        display = shorten_path(filepath, max_path_len)
        hist_lines.append(f"{display:40} | {bar} {count}")
    return hist_lines

def main():
    parser = argparse.ArgumentParser(description="Count lines of code with extras.")
    parser.add_argument("path", nargs="?", default=os.path.expanduser("~"),
                        help="Root directory to scan (default: home directory).")
    parser.add_argument("--exclude", default="anaconda,miniconda,envs,site-packages,"
                        ".ipynb_checkpoints,downloads,.config,.local,.steam",
                        help="Comma-separated list of directory names to exclude.")
    parser.add_argument("--ignore-duplicates", action="store_true",
                        help="Exclude repeated identical lines from the total count.")
    parser.add_argument("--verbose", action="store_true",
                        help="Print progress every 100 files.")
    parser.add_argument("--verbose-all", action="store_true",
                        help="Print progress for every file.")
    parser.add_argument("--estimate-hours", type=int, default=50,
                        help="LOC per hour rate for time estimation (default: 50).")
    parser.add_argument("--top-files", type=int, default=0,
                        help="Show top N files by raw line count.")
    parser.add_argument("--hist-limit", type=int, default=10,
                        help="Number of entries in histogram (default: 10).")
    parser.add_argument("--ext", default="py",
                        help="Comma-separated list of file extensions to include.")
    parser.add_argument("--report", metavar="FILE",
                        help="Write a markdown report to FILE.")
    args = parser.parse_args()

    exclude_dirs = [d.strip().lower() for d in args.exclude.split(",")]
    exts = [e.strip().lower() for e in args.ext.split(",")]

    print(f"{COLOR_YELLOW}Scanning for files...{COLOR_RESET}")
    files = find_files(args.path, exclude_dirs, exts)
    print(f"{COLOR_GREEN}Found {len(files)} files to process.{COLOR_RESET}")

    print(f"{COLOR_YELLOW}Counting lines...{COLOR_RESET}")
    total, raw_counts, filtered_counts = count_lines(
        files,
        ignore_duplicates=args.ignore_duplicates,
        verbose=args.verbose,
        verbose_all=args.verbose_all
    )

    print(f"\n{COLOR_GREEN}Total lines counted: {total}{COLOR_RESET}")
    hours = total / args.estimate_hours if args.estimate_hours > 0 else 0
    print(f"{COLOR_CYAN}Estimated time: {hours:.1f} hours (at {args.estimate_hours} LOC/hr){COLOR_RESET}")

    if args.top_files > 0:
        print(f"\n{COLOR_YELLOW}Top {args.top_files} files by raw lines:{COLOR_RESET}")
        for filepath, count in sorted(raw_counts.items(), key=lambda x: x[1], reverse=True)[:args.top_files]:
            print(f"{shorten_path(filepath, 60):60} {count}")

    print(f"\n{COLOR_YELLOW}Histogram of top {args.hist_limit} files by raw lines:{COLOR_RESET}")
    for line in generate_histogram(raw_counts, limit=args.hist_limit):
        print(line)

    if args.report:
        with open(args.report, "w", encoding="utf-8") as rpt:
            rpt.write(f"# lines-of-py Report\n\n")
            rpt.write(f"- Total lines: **{total}**\n")
            rpt.write(f"- Estimated hours (@{args.estimate_hours} LOC/hr): **{hours:.1f}**\n\n")
            if args.top_files > 0:
                rpt.write(f"## Top {args.top_files} files\n")
                for filepath, count in sorted(raw_counts.items(), key=lambda x: x[1], reverse=True)[:args.top_files]:
                    rpt.write(f"- {filepath}: {count}\n")
                rpt.write("\n")
            rpt.write(f"## Histogram (top {args.hist_limit} files by raw lines)\n```\n")
            rpt.write("\n".join(generate_histogram(raw_counts, limit=args.hist_limit)))
            rpt.write("\n```\n")
        print(f"{COLOR_GREEN}Report written to {args.report}{COLOR_RESET}")

if __name__ == "__main__":
    main()
