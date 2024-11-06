pixiu_path='/home/shadeform/PIXIU_urop'
export PYTHONPATH="$pixiu_path/src:$pixiu_path/src/financial-evaluation:$pixiu_path/src/metrics/BARTScore"
echo $PYTHONPATH
export CUDA_VISIBLE_DEVICES="0"

export OPENAI_API_SECRET_KEY=YOUR_KEY_HERE

declare -a tasks=("faireval_fpb" "faireval_fiqasa" "faireval_finqa" "faireval_convfinqa" "faireval_sm_bigdata" "faireval_sm_acl" "faireval_sm_cikm" "faireval_ner" "faireval_headlines")

now="$(date +'%Y-%m-%d-%T')"
start=$(date +%s)

for TASK in "${tasks[@]}"
do
    python3 src/eval.py \
        --model gpt-4o-2024-08-06\
        --tasks $TASK \
        --no_cache \
        --num_fewshot 0 \
        --faireval_repeat_per_prompt  >> output_"$now".log
done

end=$(date +%s)
seconds=$(echo "$end - $start" | bc)
echo $seconds' sec'
awk -v t=$seconds 'BEGIN{t=int(t*1000); printf "%d:%02d:%02d\n", t/3600000, t/60000%60, t/1000%60}' >> output_"$now".log