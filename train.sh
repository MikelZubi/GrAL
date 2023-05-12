

source ~/inguruneak/GRAL/bin/activate

echo "Entrenamentuaren hasiera"

for dir in MEE_BIO_REDUCED2/*/
do
    language=$(basename "$dir")
    echo "$language"
    
    python run_ner.py \
        --model_name_or_path xlm-roberta-base \
        --do_train \
        --do_eval \
        --do_predict \
        --seed 85 \
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

python testEus.py 85

echo "Bukatuta"