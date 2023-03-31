

#eval "$(conda shell.bash hook)"
#conda activate ~/a2t_env

source ~/inguruneak/GRAL/bin/activate


for dir in MEE_BIO/*/
do
    language=$(basename "$dir")
    echo "$language"
    python run_ner.py \
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
        --train_file MEE_BIO/$language/train.json \
        --label_column_name labels \
        --validation_file MEE_BIO/$language/dev.json \
        --test_file MEE_BIO/$language/test.json \
        --output_dir Models/$language/entity \
        --overwrite_output_dir \
    
    rm -rf Models/$language/entity/checkpoint-*/
    
    python run_ner.py \
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
        --train_file MEE_BIO/$language/train.json \
        --label_column_name triggers \
        --validation_file MEE_BIO/$language/dev.json \
        --test_file MEE_BIO/$language/test.json \
        --output_dir Models/$language/triggers \
        --overwrite_output_dir \

    rm -rf Models/$language/triggers/checkpoint-*/
    
    python run_ner.py \
        --model_name_or_path xlm-roberta-base \
        --do_train \
        --do_eval \
        --do_predict \
        --evaluation_strategy epoch \
        --per_device_train_batch_size 16 \
        --per_device_eval_batch_size 16 \
        --num_train_epochs 64.0 \
        --weight_decay 0.001 \
        --metric_for_best_model f1 \
        --load_best_model_at_end True \
        --save_strategy epoch \
        --train_file MEE_BIO/$language/train_arg.json \
        --label_column_name arguments \
        --validation_file MEE_BIO/$language/dev_arg.json \
        --test_file MEE_BIO/$language/test_arg.json \
        --output_dir Models/$language/arguments \
        --overwrite_output_dir \

    rm -rf Models/$language/arguments/checkpoint-*/
    

    

done
echo "Test-a ejekutatzen"

python test.py
python testAll.py

echo "Bukatuta"