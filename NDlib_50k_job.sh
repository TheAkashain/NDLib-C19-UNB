#!/bin/bash
#SBATCH --time=05:00:00
#SBATCH --account=def-watmough
#SBATCH --mem=50000M
#SBATCH --cpu-per-task=32
#SBATCH --job-name=C19-50k-test1
#SBATCH --mail-type=ALL
#SBATCH --mail-user=gnosewo1@unb.ca
python 'P0-Phase Model Simulation.py'
