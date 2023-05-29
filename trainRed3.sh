cross=$1
seeds=(16 44 85)
python translateRed3.py $cross

for seed in ${seeds[@]}; do
    echo $seed
    for dir in MEE_BIO_REDUCED3/*/
    do
        language=$(basename "$dir")
        echo "$language"
        srun python run_ner.py \
            --model_name_or_path xlm-roberta-base \
            --do_train \
            --do_eval \
            --do_predict \
            --seed $seed \
            --evaluation_strategy epoch \
            --per_device_train_batch_size 16 \
            --per_device_eval_batch_size 16 \
            --num_train_epochs 64.0 \
            --weight_decay 0.001 \
            --metric_for_best_model f1 \
            --load_best_model_at_end True \
            --save_strategy epoch \
            --train_file MEE_BIO_REDUCED3/$language/entities/train.json \
            --label_column_name labels \
            --validation_file MEE_BIO/$cross/dev.json \
            --test_file MEE_BIO/$cross/test.json \
            --output_dir Models_REDUCED3/$language/entity \
            --overwrite_output_dir \
        
        rm -rf Models_REDUCED3/$language/entity/checkpoint-*/
        
        srun python run_ner.py \
            --model_name_or_path xlm-roberta-base \
            --do_train \
            --do_eval \
            --do_predict \
            --seed $seed \
            --evaluation_strategy epoch \
            --per_device_train_batch_size 16 \
            --per_device_eval_batch_size 16 \
            --num_train_epochs 64.0 \
            --weight_decay 0.001 \
            --metric_for_best_model f1 \
            --load_best_model_at_end True \
            --save_strategy epoch \
            --train_file MEE_BIO_REDUCED3/$language/triggers/train.json \
            --label_column_name triggers \
            --validation_file MEE_BIO/$cross/dev.json \
            --test_file MEE_BIO/$cross/test.json \
            --output_dir Models_REDUCED3/$language/triggers \
            --overwrite_output_dir \

        rm -rf Models_REDUCED3/$language/triggers/checkpoint-*/
        
        srun python run_ner.py \
            --model_name_or_path xlm-roberta-base \
            --do_train \
            --do_eval \
            --do_predict \
            --seed $seed \
            --evaluation_strategy epoch \
            --per_device_train_batch_size 16 \
            --per_device_eval_batch_size 16 \
            --num_train_epochs 64.0 \
            --weight_decay 0.001 \
            --metric_for_best_model f1 \
            --load_best_model_at_end True \
            --save_strategy epoch \
            --train_file MEE_BIO_REDUCED3/$language/arguments/train.json \
            --label_column_name arguments \
            --validation_file MEE_BIO/$cross/dev_arg.json \
            --test_file MEE_BIO/$cross/test_arg.json \
            --output_dir Models_REDUCED3/$language/arguments \
            --overwrite_output_dir \

        rm -rf Models_REDUCED3/$language/arguments/checkpoint-*/
        

        

    done
    echo "Test-ak ejekutatzen"

    srun python testRed3.py $cross $seed

    echo "Bukatuta"
done

