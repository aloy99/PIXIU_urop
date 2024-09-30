def no_prompt(ctx):
    return ctx

def finma_prompt(ctx):
    return f'Human: \n{ctx}\n\nAssistant: \n'

def cot_prompt(ctx):
    return f"{ctx} Let's think step by step."

MODEL_PROMPT_MAP = {
    "no_prompt": no_prompt,
    "finma_prompt": finma_prompt,
    "cot_prompt": cot_prompt
}