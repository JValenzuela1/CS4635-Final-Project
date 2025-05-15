# VTMOP Optimization Study

This repository contains a small-scale study and implementation of multi-objective optimization using [VTMOP](https://github.com/ParkinsonLab/vtmop), a Fortran-based tool for solving vector optimization problems. The focus is on analyzing the performance of VTMOP across different problem types, objective counts, and budget settings.

## Project Structure

- **`src/`**  
  Contains all Fortran source files from VTMOP, along with a Jupyter notebook (`vtmop_analysis.ipynb`) that demonstrates:
  - Compilation and execution of the tool for a specific configuration (e.g., `p=2`, budget = 1000)
  - Data parsing using a Python script (`analyze_results.py`)
  - Visualization and summary of output

- **`results/`**  
  Contains the full results of running VTMOP across different problem types and configurations. It includes:
  - Two subfolders: `f(c)` (a convex problem) and `DTLZ2` (a standard nonconvex test problem)
  - PNG plots summarizing solution quality, root-mean-square error (RMSE), and triangulation
  - Summary tables in `.txt` format for each objective count (`p=2`, `p=3`, `p=4`)

## About VTMOP

VTMOP is a Fortran 2008 package containing a robust, portable solver and a flexible framework for solving MOPs. Designed for efficiency and scalability to an arbitrary number of objectives, VTMOP attempts to generate uniformly spaced points on a (possibly nonconvex) Pareto front with minimal cost function evaluations. The driver subroutine is VTMOP_SOLVE, which can be run both serially and with parallel function evaluations. Minimal subsets of dependencies such as VTDIRECT, QNSTOP, SHEPPACK, DELAUNAYSPARSE, SLATEC, LAPACK, and BLAS are also provided. Comments at the top of each subroutine document their usage, and examples demonstrating the driver's usage are given in src/sample.f90.

All VTMOP-related source code in this repository is directly credited to the Tyler H Chang and remains under their original license. No modifications were made to the algorithm itself; rather, the wrapper and analysis scripts were developed externally to facilitate testing and interpretation of results.

For more information about VTMOP, refer to their [GitHub repository](https://github.com/vtopt/VTMOP).

## Purpose

The purpose of this project was to:

- Understand and replicate a multi-objective optimization algorithm implemented in Fortran
- Analyze how solution accuracy and model behavior change with different objective counts and budget allocations
- Develop simple tooling to automate analysis and visualization from VTMOP output

## Reproducibility

The Jupyter notebook in `src/` includes all steps needed to compile, run, and analyze results for a specific configuration. Due to long runtimes, only one configuration is executed directly in the notebook (`p=2`, budget = 1000). Precomputed results for all configurations are located in the `results/` folder.

## Requirements

- GCC or GFortran (supporting OpenMP and legacy standards)
- Python 3.x (for data parsing and visualization)
- Jupyter Notebook (optional, for interactive execution)
