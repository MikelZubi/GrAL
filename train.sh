
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
        --num_train_epochs 4.0 \
        --weight_decay 0.001 \
        --load_best_model_at_end True \
        --save_strategy steps \
        --eval_steps 500 \
        --train_file MEE_BIO/$language/train.json \
        --label_column_name labels \
        --validation_file MEE_BIO/$language/dev.json \
        --test_file MEE_BIO/$language/test.json \
        --output_dir Models/$language/entity \
        --overwrite_output_dir \
    
    python run_ner.py \
        --model_name_or_path xlm-roberta-base \
        --do_train \
        --do_eval \
        --do_predict \
        --evaluation_strategy steps \
        --num_train_epochs 4.0 \
        --weight_decay 0.001 \
        --load_best_model_at_end True \
        --save_strategy steps \
        --eval_steps 500 \
        --train_file MEE_BIO/$language/train.json \
        --label_column_name triggers \
        --validation_file MEE_BIO/$language/dev.json \
        --test_file MEE_BIO/$language/test.json \
        --output_dir Models/$language/triggers \
        --overwrite_output_dir \
    
    python run_ner.py \
        --model_name_or_path xlm-roberta-base \
        --do_train \
        --do_eval \
        --do_predict \
        --evaluation_strategy steps \
        --num_train_epochs 4.0 \
        --weight_decay 0.001 \
        --load_best_model_at_end True \
        --save_strategy steps \
        --eval_steps 500 \
        --train_file MEE_BIO/$language/train_arg.json \
        --label_column_name arguments \
        --validation_file MEE_BIO/$language/dev_arg.json \
        --test_file MEE_BIO/$language/test_arg.json \
        --output_dir Models/$language/arguments \
        --overwrite_output_dir \
    

done
echo "Bukatuta"