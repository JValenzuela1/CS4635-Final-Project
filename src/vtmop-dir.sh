#!/bin/bash
#SBATCH --mem=16g
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=4    
#SBATCH --partition=cpu     
#SBATCH --account=bbrx-delta-cpu
#SBATCH --job-name=running-vtmop
#SBATCH --output=../log/vtmop_%j.log
#SBATCH --error=../error/vtmop_%j.err
#SBATCH --time=02:00:00

cd /u/jvalenzuela/final-project/src

# conda run -n my_env gfortran -O3 -fopenmp shared_modules.f90 blas.f lapack.f slatec.f qnstop.f90 \
# sVTdirect.f90 bVTdirect.f90 delsparse.f90 linear_shepard.f90 vtmop.f90 \
# vtmop_func.f90 samples.f90 -o samples

# gfortran -std=legacy -O2 -fopenmp shared_modules.f90 blas.f lapack.f slatec.f \
# qnstop.f90 sVTdirect.f90 bVTdirect.f90 delsparse.f90 \
# linear_shepard.f90 vtmop.f90 vtmop_func.f90 samples.f90 -o samples

# ./samples > samples_out.txt

# for p in 2 3 4; do
#   # Map to appropriate .f90 file
#   f="samples_p${p}.f90"

#   # Compile each version
#   gfortran -std=legacy -O2 -fopenmp shared_modules.f90 blas.f lapack.f slatec.f \
#   qnstop.f90 sVTdirect.f90 bVTdirect.f90 delsparse.f90 \
#   linear_shepard.f90 vtmop.f90 vtmop_func.f90 $f -o samples_p${p}

#   for budget in 1000 1500 2000; do
#     echo "Running P=$p, Budget=$budget"
#     ./samples_p${p} > ../results_out/out_p${p}_b${budget}.txt
#     wait

#     python3 analyze_results.py results_out/out_p${p}_b${budget}.txt $p >> summary_direct.csv
#   done
# done

for p in 2 3 4; do
    for budget in 1000 1500 2000; do
        filename="samples_p${p}_${budget}.f90"
        
        # Check if the file exists before submitting the job
        if [ -f "$filename" ]; then
            echo "Running $filename"
            
            # Compile the Fortran program
              gfortran -std=legacy -O2 -fopenmp shared_modules.f90 blas.f lapack.f slatec.f \
              qnstop.f90 sVTdirect.f90 bVTdirect.f90 delsparse.f90 \
              linear_shepard.f90 vtmop.f90 vtmop_func.f90 $filename -o samples_p${p}_${budget}

            # Run the compiled program
            srun ./samples_p${p}_${budget}
        else
            echo "File $filename does not exist."
        fi
    done
done