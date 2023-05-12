#!/bin/bash
#SBATCH --job-name=TRAIN_ARG_RED
#SBATCH --cpus-per-task=1
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem=8GB
#SBATCH --gres=gpu:2
#SBATCH --output=./SLURM/LOG/irteeraTrainArg.log
#SBATCH --error=./SLURM/ERRORE/erroreTrainArg.err

source ~/inguruneak/GRAL/bin/activate

echo "Entrenamentuaren hasiera"

for dir in MEE_BIO/*/
do
    language=$(basename "$dir")
    echo "$language"
    srun python run_ner.py \
        --model_name_or_path xlm-roberta-base \
        --do_train \
        --do_eval \
        --do_predict \
        --evaluation_strategy steps \
        --per_device_train_batch_size 16 \
        --per_device_eval_batch_size 16 \
        --num_train_epochs 16.0 \
        --weight_decay 0.001 \
        --metric_for_best_model f1 \
        --load_best_model_at_end True \
        --save_strategy steps \
        --eval_steps 500 \
        --train_file MEE_BIO_REDUCED/$language/train.json \
        --label_column_name labels \
        --validation_file MEE_BIO_REDUCED/$language/test.json \
        --test_file MEE_BIO_REDUCED/$language/test.json \
        --output_dir Models_REDUCED/$language/entity \
        --overwrite_output_dir \
    
    rm -rf Models_REDUCED/$language/entity/checkpoint-*/
    
    srun python run_ner.py \
        --model_name_or_path xlm-roberta-base \
        --do_train \
        --do_eval \
        --do_predict \
        --evaluation_strategy epoch \
        --per_device_train_batch_size 16 \
        --per_device_eval_batch_size 16 \
        --num_train_epochs 32.0 \
        --weight_decay 0.001 \
        --metric_for_best_model f1 \
        --load_best_model_at_end True \
        --save_strategy epoch \
        --train_file MEE_BIO_REDUCED/$language/train.json \
        --label_column_name triggers \
        --validation_file MEE_BIO_REDUCED/$language/dev.json \
        --test_file MEE_BIO_REDUCED/$language/test.json \
        --output_dir Models_REDUCED/$language/triggers \
        --overwrite_output_dir \

    rm -rf Models_REDUCED/$language/triggers/checkpoint-*/
    
    srun python run_ner.py \
        --model_name_or_path xlm-roberta-base \
        --do_train \
        --do_eval \
        --do_predict \
        --evaluation_strategy epoch \
        --per_device_train_batch_size 16 \
        --per_device_eval_batch_size 16 \
        --num_train_epochs 80.0 \
        --weight_decay 0.001 \
        --metric_for_best_model f1 \
        --load_best_model_at_end True \
        --save_strategy epoch \
        --train_file MEE_BIO_REDUCED/$language/train_arg.json \
        --label_column_name arguments \
        --validation_file MEE_BIO_REDUCED/$language/dev_arg.json \
        --test_file MEE_BIO_REDUCED/$language/test_arg.json \
        --output_dir Models_REDUCED/$language/arguments \
        --overwrite_output_dir \

    rm -rf Models_REDUCED/$language/arguments/checkpoint-*/
    

    

done
echo "Test-ak ejekutatzen"

srun python testRed.py
srun python testAllRed.py
srun python testCrossRed.py english
srun python testCrossRed.py hindi
srun python testCrossRed.py euskera
srun python testCrossRed.py japanese
srun python testCrossRed.py korean
srun python testCrossRed.py polish
srun python testCrossRed.py portuguese
srun python testCrossRed.py spanish
srun python testCrossRed.py turkish

echo "Bukatuta"