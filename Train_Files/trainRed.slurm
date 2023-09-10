#!/bin/bash
#SBATCH --job-name=TRAIN_ARG_RED3
#SBATCH --cpus-per-task=1
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem=8GB
#SBATCH --gres=gpu:2
#SBATCH --output=./SLURM/LOG/irteeraTrainArg3.log
#SBATCH --error=./SLURM/ERRORE/erroreTrainArg3.err

source ~/inguruneak/GRAL/bin/activate

echo "Entrenamentuaren hasiera"

crossL=("japanese")
for lang in ${crossL[@]}; do
    bash trainRed.sh $lang
done