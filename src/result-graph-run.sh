#!/bin/bash
#SBATCH --mem=16g
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=4    
#SBATCH --partition=cpu     
#SBATCH --account=bbrx-delta-cpu
#SBATCH --job-name=analyze-results
#SBATCH --output=../log/analyze_results_%j.log
#SBATCH --error=../error/analyze_results_%j.err
#SBATCH --time=01:00:00

# Change directory to the location where your analysis script is
cd /u/jvalenzuela/final-project/src

# Activate your environment (if you have one)
# conda activate my_env

# Run the Python analysis script
python3 analyze_results.py ../results/ > ../results/analysis_output.txt
