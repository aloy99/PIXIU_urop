faireval_path='/home/shadeform/faireval'
export PYTHONPATH="$faireval_path/src:$faireval_path/src/financial-evaluation:$faireval_path/src/metrics/BARTScore"
echo $PYTHONPATH
export CUDA_VISIBLE_DEVICES="0"

declare -a tasks=("flare_fpb" "flare_fiqasa" "flare_finqa" "flare_convfinqa" "flare_sm_bigdata" "flare_sm_acl" "flare_sm_cikm" "flare_ner" "flare_headlines")

now="$(date +'%Y-%m-%d-%T')"
start=$(date +%s)

for TASK in "${tasks[@]}"
do
    python3 src/eval.py \
        --model hf-causal-vllm \
        --tasks $TASK \
        --model_args use_accelerate=True,pretrained=AdaptLLM/finance-chat,tokenizer=AdaptLLM/finance-chat,use_fast=False \
        --no_cache \
        --batch_size 256 \
        --num_fewshot 0  >> output_"$now".log
done

end=$(date +%s)
seconds=$(echo "$end - $start" | bc)
echo $seconds' sec'
awk -v t=$seconds 'BEGIN{t=int(t*1000); printf "%d:%02d:%02d\n", t/3600000, t/60000%60, t/1000%60}' >> output_"$now".log