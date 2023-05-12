#!/bin/bash
#SBATCH --job-name=TEST_ARG
#SBATCH --cpus-per-task=1
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem=4GB
#SBATCH --gres=gpu:1
#SBATCH --output=./SLURM/LOG/irteeraTestArg.log
#SBATCH --error=./SLURM/ERRORE/erroreTestArg.err

source ~/inguruneak/GRAL/bin/activate

echo "Test-ak ejekutatzen"

srun python testRed.py
srun python testAllRed.py
srun python testCrossRed.py english
srun python testCrossRed.py euskera
srun python testCrossRed.py hindi
srun python testCrossRed.py japanese
srun python testCrossRed.py korean
srun python testCrossRed.py polish
srun python testCrossRed.py portuguese
srun python testCrossRed.py spanish
srun python testCrossRed.py turkish

echo "Bukatuta"