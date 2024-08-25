pixiu_path='/home/shadeform/PIXIU'
export PYTHONPATH="$pixiu_path/src:$pixiu_path/src/financial-evaluation:$pixiu_path/src/metrics/BARTScore"
echo $PYTHONPATH
export CUDA_VISIBLE_DEVICES="0"

declare -a tasks=("faireval_fpb" "faireval_fiqasa" "faireval_finqa" "faireval_convfinqa")

now="$(date +'%Y-%m-%d-%T')"
start=$(date +%s)

for TASK in "${tasks[@]}"
do
    python3 src/eval.py \
        --model hf-causal-vllm \
        --tasks $TASK \
        --model_args use_accelerate=True,pretrained=meta-llama/Llama-2-7b-chat-hf,tokenizer=meta-llama/Llama-2-7b-chat-hf,use_fast=False \
        --no_cache \
        --batch_size 8 \
        --num_fewshot 0  >> output_"$now".log
done

end=$(date +%s)
seconds=$(echo "$end - $start" | bc)
echo $seconds' sec'
awk -v t=$seconds 'BEGIN{t=int(t*1000); printf "%d:%02d:%02d\n", t/3600000, t/60000%60, t/1000%60}' >> output_"$now".log