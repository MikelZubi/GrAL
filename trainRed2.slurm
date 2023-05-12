#!/bin/bash
#SBATCH --job-name=TRAIN_ARG_RED2
#SBATCH --cpus-per-task=1
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem=8GB
#SBATCH --gres=gpu:2
#SBATCH --output=./SLURM/LOG/irteeraTrainArg2.log
#SBATCH --error=./SLURM/ERRORE/erroreTrainArg2.err

source ~/inguruneak/GRAL/bin/activate

echo "Entrenamentuaren hasiera"

for dir in MEE_BIO_REDUCED2/*/
do
    language=$(basename "$dir")
    echo "$language"
    srun python run_ner.py \
        --model_name_or_path xlm-roberta-base \
        --do_train \
        --do_eval \
        --do_predict \
        --seed 44 \
        --evaluation_strategy epoch \
        --per_device_train_batch_size 16 \
        --per_device_eval_batch_size 16 \
        --num_train_epochs 64.0 \
        --weight_decay 0.001 \
        --metric_for_best_model f1 \
        --load_best_model_at_end True \
        --save_strategy epoch \
        --train_file MEE_BIO_REDUCED2/$language/entities/train.json \
        --label_column_name labels \
        --validation_file Eus/dev.json \
        --test_file Eus/test.json \
        --output_dir Models_REDUCED2/$language/entity \
        --overwrite_output_dir \
    
    rm -rf Models_REDUCED2/$language/entity/checkpoint-*/
    
    srun python run_ner.py \
        --model_name_or_path xlm-roberta-base \
        --do_train \
        --do_eval \
        --do_predict \
        --seed 44 \
        --evaluation_strategy epoch \
        --per_device_train_batch_size 16 \
        --per_device_eval_batch_size 16 \
        --num_train_epochs 64.0 \
        --weight_decay 0.001 \
        --metric_for_best_model f1 \
        --load_best_model_at_end True \
        --save_strategy epoch \
        --train_file MEE_BIO_REDUCED2/$language/triggers/train.json \
        --label_column_name triggers \
        --validation_file Eus/dev.json \
        --test_file Eus/test.json \
        --output_dir Models_REDUCED2/$language/triggers \
        --overwrite_output_dir \

    rm -rf Models_REDUCED2/$language/triggers/checkpoint-*/
    
    srun python run_ner.py \
        --model_name_or_path xlm-roberta-base \
        --do_train \
        --do_eval \
        --do_predict \
        --seed 44 \
        --evaluation_strategy epoch \
        --per_device_train_batch_size 16 \
        --per_device_eval_batch_size 16 \
        --num_train_epochs 64.0 \
        --weight_decay 0.001 \
        --metric_for_best_model f1 \
        --load_best_model_at_end True \
        --save_strategy epoch \
        --train_file MEE_BIO_REDUCED2/$language/arguments/train.json \
        --label_column_name arguments \
        --validation_file Eus/dev_arg.json \
        --test_file Eus/test_arg.json \
        --output_dir Models_REDUCED2/$language/arguments \
        --overwrite_output_dir \

    rm -rf Models_REDUCED2/$language/arguments/checkpoint-*/
    

    

done
echo "Test-ak ejekutatzen"

srun python testEus.py 44

echo "Bukatuta"