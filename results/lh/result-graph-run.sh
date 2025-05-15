#!/bin/bash
#SBATCH --mem=16g
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=4
#SBATCH --partition=cpu
#SBATCH --account=bbrx-delta-cpu
#SBATCH --job-name=running-vtmop
#SBATCH --output=vtmop_%j.log
#SBATCH --error=vtmop_%j.err
#SBATCH --time=01:00:00

# Change to the directory where the job was submitted
cd $SLURM_SUBMIT_DIR

# Run the analysis Python script
python3 analyze_results.py
