<p align="center" width="100%">
<img src="https://i.postimg.cc/xTpWgq3L/pixiu-logo.png"  width="100%" height="100%">
</p>



<div>
<div align="left">
    <a target='_blank'>Qianqian Xie<sup>1</sup></span>&emsp;
    <a target='_blank'>Weiguang Han<sup>1</sup></span>&emsp;
    <a target='_blank'>Xiao Zhang<sup>2</sup></a>&emsp;
    <a target='_blank'>Duanyu Feng<sup>3</sup></a>&emsp;
    <a target='_blank'>Yongfu Dai<sup>3</sup></a>&emsp;
    <a target='_blank'>Yanzhao Lai<sup>4</sup></a>&emsp;
    <a target='_blank'>Min Peng<sup>1</sup></a>&emsp;
    <a href='https://warrington.ufl.edu/directory/person/12693/' target='_blank'>Alejandro Lopez-Lira<sup>5</sup></a>&emsp;
    <a href='https://jimin.chancefocus.com/' target='_blank'>Jimin Huang*<sup>,6</sup></a>
</div>
<div>
<div align="left">
    <sup>1</sup>Wuhan University&emsp;
    <sup>2</sup>Sun Yat-Sen University&emsp;
    <sup>3</sup>Sichuan University&emsp;
    <sup>4</sup>Southwest Jiaotong University&emsp;
    <sup>5</sup>University of Florida&emsp;
  <sup>6</sup>ChanceFocus AMC.
</div>
<div align="left">
    <img src='https://i.postimg.cc/CLtkBwz7/57-EDDD9-FB0-DF712-F3-AB627163-C2-1-EF15655-13-FCA.png' alt='Wuhan University Logo' height='100px'>&emsp;
    <img src='https://i.postimg.cc/C1XnZNK1/Sun-Yat-sen-University-Logo.png' alt='Sun Yat-Sen University Logo' height='100px'>&emsp;
    <img src='https://i.postimg.cc/NjKhDkGY/DFAF986-CCD6529-E52-D7830-F180-D-C37-C7-DEE-4340.png' alt='Sichuan University Logo' height='100px'>&emsp;
    <img src='https://i.postimg.cc/k5WpYj0r/SWJTULogo.png' alt='Southwest Jiaotong University Logo' height='100px'>&emsp;
    <img src='https://i.postimg.cc/XY1s2RHD/University-of-Florida-Logo-1536x864.jpg' alt='University of Florida Logo' height='100px'>&emsp;
    <img src='https://i.postimg.cc/xTsgsrqN/logo11.png' alt='ChanceFocus AMC Logo' height='100px'>
</div>

  

-----------------

![](https://img.shields.io/badge/pixiu-v0.1-gold)
![](https://black.readthedocs.io/en/stable/_static/license.svg)

[Pixiu Paper](https://arxiv.org/abs/2306.05443) | [FLARE Leaderboard](https://huggingface.co/spaces/ChanceFocus/FLARE)

**Checkpoints:** 
- [FinMA v0.1 (NLP 7B version)](https://huggingface.co/ChanceFocus/finma-7b-nlp)
- [FinMA v0.1 (Full 7B version)](https://huggingface.co/ChanceFocus/finma-7b-full)


## Update
**[2023-07-04]**
1. Enhanced our Financial tasks portfolio by incorporating tasks from the [GT Fintech Lab Zero-shot Finance dataset](https://github.com/gtfintechlab/zero-shot-finance) (FOMC and Finer Ord) and adding credit scoring benchmark datasets (German and Australian).
2. Updated our leaderboard, featuring the latest benchmarks and models such as GPT-4, Llama-7B, Bloomz-7B, and Falcon-7B.


**[2023-06-26]**
1. Introduced a new automated evaluation for FLARE based on the [lm_eval framework](https://github.com/EleutherAI/lm-evaluation-harness).
2. Added new Huggingface datasets for FLARE, such as [flare_ner](https://huggingface.co/datasets/ChanceFocus/flare-ner).


**[2023-06-19]**
1. Publicly release [FinMA-7B-full](https://huggingface.co/ChanceFocus/finma-7b-full) (full version).
2. Added Falcon-7B fine-tuned results on FLARE.
3. Updated usage instructions in both the README and the Hugging Face model card.

**[2023-06-11]**
1. Check our arxiv [paper](https://arxiv.org/abs/2306.05443)!
2. Publicly release FinMA v0.1 (NLP 7B version)
3. All model results of FLARE can be found on our [leaderboard](https://huggingface.co/spaces/ChanceFocus/FLARE)!

## Overview

The advancement of Natural Language Processing (NLP) and machine learning (ML) techniques in financial technology (FinTech) has enabled a diverse set of capabilities from predicting stock price movements to advanced financial analytics. However, to effectively understand the complex financial language and concepts, domain-specific LLMs are necessary.

Despite prior efforts, there is a lack of open-source financial LLMs and benchmarks to evaluate them. Additionally, these models are not fine-tuned to follow natural language instructions, limiting their performance in downstream financial tasks.

To address these gaps, we introduce PIXIU, providing:

1. Open-source LLMs tailored for finance called **FinMA**, by fine-tuning LLaMA with the dataset constructed in PIXIU.
2. Large-scale, high-quality multi-task and multi-modal financial instruction tuning data **FIT**.
3. Holistic financial evaluation benchmarks **FLARE** for assessing financial LLMs.

## Key Features

- **Open resources**: PIXIU openly provides the financial LLM, instruction tuning data, and datasets included in the evaluation benchmark to encourage open research and transparency.
  
- **Multi-task**: The instruction tuning data in PIXIU cover a diverse set of financial tasks, including four financial NLP tasks and one financial prediction task.

- **Multi-modality**: PIXIU's instruction tuning data consist of multi-modality financial data, including time series data from the stock movement prediction task. It covers various types of financial texts, including reports, news articles, tweets, and regulatory filings.
  
- **Diversity**: Unlike previous benchmarks focusing mainly on financial NLP tasks, PIXIU's evaluation benchmark includes critical financial prediction tasks aligned with real-world scenarios, making it more challenging.

## Building PIXIU

To construct the multi-task and multi-modal instruction data, we collected publicly available training data from diverse tasks. We wrote task-specific instructions for each task and assembled these with data samples to create a large-scale instruction tuning data.

Using this dataset, we conducted multi-task instruction tuning on LLaMA to create FinMA, a domain-specific LLM.

We built the Financial Language Understanding and Prediction Evaluation Benchmark (FLARE), covering 4 financial NLP tasks with 6 datasets, and 1 financial prediction tasks with 3 datasets. This benchmark allows us to compare the performance of our model with BloombergGPT and general domain LLMs such as ChatGPT and GPT-4.

## Structure of Repository

The repository is organized as follows:

1. **Models**: Contains the FinMA model fine-tuned on our dataset.
2. **Instruction Tuning Data**: Multi-task and multi-modal instruction data FIT for financial tasks.
3. **Evaluation Benchmark**: FLARE for evaluating financial LLMs.

## FinMA v0.1: Financial Large Language Model

We are pleased to introduce the first version of FinMA, including three models FinMA-7B, FinMA-7B-full, FinMA-30B, fine-tuned on LLaMA 7B and LLaMA-30B. FinMA-7B and FinMA-30B are trained with the NLP instruction data, while FinMA-7B-full is trained with the full instruction data from FIT covering both NLP and prediction tasks. 

FinMA v0.1 is now available on [Huggingface](https://huggingface.co/ChanceFocus/finma-7b-nlp) for public use. We look forward to the valuable contributions that this initial version will make to the financial NLP field and encourage users to apply it to various financial tasks and scenarios. We also invite feedback and shared experiences to help improve future versions.

## Instruction Dataset

Our instruction dataset is uniquely tailored for the domain-specific LLM, FinMA. This dataset has been meticulously assembled to fine-tune our model on a diverse range of financial tasks. It features publicly available multi-task and multi-modal data derived from the multiple open released financial datasets.

The dataset is multi-faceted, featuring tasks including sentiment analysis, news headline classification, named entity recognition, question answering, and stock movement prediction. It covers both textual and time-series data modalities, offering a rich variety of financial data. The task specific instruction prompts for each task have been carefully degined by domain experts.

The table below summarizes the different tasks, their corresponding modalities, text types, and examples of the instructions used for each task:

| **Task** | **Modalities** | **Text Types** | **Instructions Examples** |
| --- | --- | --- | --- |
| Sentiment Analysis | Text | news headlines,tweets | "Analyze the sentiment of this statement extracted from a financial news article.Provide your answer as either negative, positive or neutral. For instance, 'The company's stocks plummeted following the scandal.' would be classified as negative." |
| News Headline Classification | Text | News Headlines | "Consider whether the headline mentions the price of gold. Is there a Price or Not in the gold commodity market indicated in the news headline? Please answer Yes or No." |
| Named Entity Recognition | Text | financial agreements | "In the sentences extracted from financial agreements in U.S. SEC filings, identify the named entities that represent a person ('PER'), an organization ('ORG'), or a location ('LOC'). The required answer format is: 'entity name, entity type'. For instance, in 'Elon Musk, CEO of SpaceX, announced the launch from Cape Canaveral.', the entities would be: 'Elon Musk, PER; SpaceX, ORG; Cape Canaveral, LOC'" |
| Question Answering | Text |earnings reports | "In the context of this series of interconnected finance-related queries and the additional information provided by the pretext, table data, and post text from a company's financial filings, please provide a response to the final question. This may require extracting information from the context and performing mathematical calculations. Please take into account the information provided in the preceding questions and their answers when formulating your response:" |
| Stock Movement Prediction | Text, Time-Series | tweets, Stock Prices | "Analyze the information and social media posts to determine if the closing price of *\{tid\}* will ascend or descend at *\{point\}*. Please respond with either Rise or Fall." |

The dataset contains a vast amount of instruction data samples (136K), allowing FinMA to capture the nuances of the diverse financial tasks. The table below provides the statistical details of the instruction dataset:

| Data | Task | Raw | Instruction | Data Types | Modalities | License |
|---|---|---|---|---|---|---|
| FPB | sentiment analysis | 4,845 | 48,450 | news | text | CC BY-SA 3.0 |
| FiQA-SA | sentiment analysis | 1,173 | 11,730 | news headlines, tweets | text | Public |
| Headline | news headline classification | 11,412 | 11,412 | news headlines | text | CC BY-SA 3.0 |
| NER | named entity recognition | 1,366 | 13,660 | financial agreements | text | CC BY-SA 3.0 |
| FinQA | question answering | 8,281 | 8,281 | earnings reports | text, table | MIT License |
| ConvFinQA | question answering | 3,892 | 3,892 | earnings reports | text, table | MIT License |
| BigData22 | stock movement prediction | 7,164 | 7,164 | tweets, historical prices | text, time series | Public |
| ACL18 | stock movement prediction | 27,053 | 27,053 | tweets, historical prices | text, time series | MIT License |
| CIKM18 | stock movement prediction | 4,967 | 4,967 | tweets, historical prices | text, time series | Public |


| Data | Task | Valid | Test | Evaluation | Original Paper |
|---|---|---|---|---|---|
| FPB | sentiment analysis | 7,740 | 9,700 | F1, Accuracy | [1] |
| FiQA-SA | sentiment analysis | 1,880 | 2,350 | F1, Accuracy | [2] |
| Headline | news headline classification | 10,259 | 20,547 | Avg F1 | [3] |
| NER | named entity recognition | 1,029 | 980 | Entity F1 | [4] |
| FinQA | question answering | 882 | 1,147 | EM Accuracy | [5] |
| ConvFinQA | question answering | 1,489 | 2,161 | EM Accuracy | [6] |
| BigData22 | stock movement prediction | 797 | 1,471 | Accuracy, MCC | [7] |
| ACL18 | stock movement prediction | 2,554 | 3,719 | Accuracy, MCC | [8] |
| CIKM18 | stock movement prediction | 430 | 1,142 | Accuracy, MCC | [9] |

1. Pekka Malo, Ankur Sinha, Pekka Korhonen, Jyrki Wallenius, and Pyry Takala. 2014. Good debt or bad debt: Detecting semantic orientations in economic texts. Journal of the Association for Information Science and Technology 65, 4 (2014), 782–796.
2. Macedo Maia, Siegfried Handschuh, André Freitas, Brian Davis, Ross McDermott, Manel Zarrouk, and Alexandra Balahur. 2018. Www’18 open challenge: financial opinion mining and question answering. In Companion proceedings of the the web conference 2018. 1941–1942
3. Ankur Sinha and Tanmay Khandait. 2021. Impact of news on the commodity market: Dataset and results. In Advances in Information and Communication: Proceedings of the 2021 Future of Information and Communication Conference (FICC), Volume 2. Springer, 589–601
4. Julio Cesar Salinas Alvarado, Karin Verspoor, and Timothy Baldwin. 2015. Domain adaption of named entity recognition to support credit risk assessment. In Proceedings of the Australasian Language Technology Association Workshop 2015. 84–90.
5. Zhiyu Chen, Wenhu Chen, Charese Smiley, Sameena Shah, Iana Borova, Dylan Langdon, Reema Moussa, Matt Beane, Ting-Hao Huang, Bryan R Routledge, et al . 2021. FinQA: A Dataset of Numerical Reasoning over Financial Data. In Proceedings of the 2021 Conference on Empirical Methods in Natural Language Processing. 3697–3711.
6. Zhiyu Chen, Shiyang Li, Charese Smiley, Zhiqiang Ma, Sameena Shah, and William Yang Wang. 2022. Convfinqa: Exploring the chain of numerical reasoning in conversational finance question answering. arXiv preprint arXiv:2210.03849 (2022).
7. Yejun Soun, Jaemin Yoo, Minyong Cho, Jihyeong Jeon, and U Kang. 2022. Accurate Stock Movement Prediction with Self-supervised Learning from Sparse Noisy Tweets. In 2022 IEEE International Conference on Big Data (Big Data). IEEE, 1691–1700.
8. Yumo Xu and Shay B Cohen. 2018. Stock movement prediction from tweets and historical prices. In Proceedings of the 56th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers). 1970–1979.
9. Huizhe Wu, Wei Zhang, Weiwei Shen, and Jun Wang. 2018. Hybrid deep sequential modeling for social text-driven stock prediction. In Proceedings of the 27th ACM international conference on information and knowledge management. 1627–1630.


## Benchmark

In this section, we provide a detailed performance analysis of FinMA compared to other leading models, including ChatGPT, GPT-4, and BloombergGPT et al. For this analysis, we've chosen a range of tasks and metrics that span various aspects of financial Natural Language Processing and financial prediction. 

| Dataset | Metrics | GPT NeoX | OPT 66B | BLOOM | Chat GPT | GPT 4 | Bloomberg GPT | FinMA 7B | FinMA 30B | FinMA 7B-full |
|---|---|---|---|---|---|---|---|---|---|---|
| FPB | Acc | - | - | - | 0.78 | 0.76 | - | 0.86 | **0.87** | 0.87 |
| FPB | F1 | 0.45 | 0.49 | 0.50 | 0.78 | 0.78 | 0.51 | 0.86 | **0.88** | 0.87 |
| FiQA-SA | F1 | 0.51 | 0.52 | 0.53 | - | - | 0.75 | 0.84 | **0.87** | 0.79 |
| Headline | AvgF1 | 0.73 | 0.79 | 0.77 | 0.77 | 0.86 | 0.82 | **0.98** | 0.97 | 0.97 |
| NER | EntityF1 | 0.61 | 0.57 | 0.56 | 0.77 | **0.83** | 0.61 | 0.75 | 0.62 | 0.69 |
| FinQA | EmAcc | - | - | - | 0.58 | **0.63** | - | 0.06 | 0.11 | 0.04 |
| ConvFinQA | EmAcc | 0.28 | 0.30 | 0.36 | 0.60 | **0.76** | 0.43 | 0.25 | 0.40 | 0.20 |
| BigData22 | Acc | - | - | - | 0.53 | **0.54** | - | 0.48 | 0.47 | 0.49 |
| BigData22 | MCC | - | - | - | -0.025 | 0.03 | - | 0.04 | **0.04** | 0.01 |
| ACL18 | Acc | - | - | - | 0.50 | 0.52 | - | 0.50 | 0.49 | **0.56** |
| ACL18 | MCC | - | - | - | 0.005 | 0.02 | - | 0.00 | 0.00 | **0.10** |
| CIKM18 | Acc | - | - | - | 0.55 | **0.57** | - | 0.56 | 0.43 | 0.53 |
| CIKM18 | MCC | - | - | - | 0.01 | **0.02** | - | -0.02 | -0.05 | -0.03 |


The metrics used for evaluation are:

- **Entity F1 (NER):** This metric evaluates the quality of Named Entity Recognition by calculating the harmonic mean of precision and recall.
  
- **Avg F1 (Headlines):** This metric averages the F1 scores across different categories in the headlines task. 

- **ACC (FPB & FIQASA):** Accuracy (ACC) measures the fraction of predictions our model got right.

- **F1 (FPB & FIQASA):** F1 score is the harmonic mean of precision and recall. It is a good way to show that a classifier has a good value for both recall and precision.

- **EM ACC (FinQA & ConvFinQA):** Exact Match Accuracy (EM ACC) is the percentage of predictions that exactly match the true answer. 
- **Matthews correlation coefficient (MCC) (BigData22, ACL18& CIKM18):** A more robust evaluation metric for binary classification tasks than ACC, especially when classes are imbalanced.

Note that while FinMA displays competitive performance in many of the tasks, it underperforms in tasks such as FinQA and ConvFinQA. This underperformance is attributable to the fact that the LLaMA model, which FinMA is based upon, has not been pre-trained on tasks involving mathematical reasoning. The ability to parse and respond to numerical inputs is critical for financial tasks and is a key area for potential improvement in future iterations of FinMA.

In subsequent versions, we plan to address these limitations by incorporating larger backbone models such as LLaMA 65B or pre-training on tasks involving mathematical reasoning and domain-specific datasets. We believe that this addition will significantly enhance FinMA's performance on finance-specific tasks that require numerical understanding.

## Creating new tasks for FLARE

Creating a new task for FLARE involves creating a Huggingface dataset and implementing the task in a Python file. This guide walks you through each step of setting up a new classification task using the FLARE framework

### Creating your dataset in Huggingface
Your dataset should be created in the following format:

```python
{
    "query": "...",
    "answer": "...",
    "choices": ["xx", "xxx"],
    "gold": 1,
    "text": "..."
}
```
In this format:

- `query`: Combination of your prompt and text
- `answer`: Your label
- `choices`: Set of labels
- `gold`: Index of the correct label in choices

### Implementing the task
Once your dataset is ready, you can start implementing your task. Your task should be defined within a new class in flare.py or any other Python file located within the tasks directory.

For a classification task, we provide a convenient base class called `Classification`. You can directly use this class to build your task. Let's illustrate this with an example of implementing a task named FLARE-FPB:

```python
class FlareFPB(Classification):
    DATASET_PATH = "flare-fpb"
    DATASET_NAME = "none"
```

And that's it! Once you've created your task class, the next step is to register it in the `src/tasks/__init__.py` file. To do this, add a new line following the format `"task_name": module.ClassName`. Here is how it's done:

```python
TASK_REGISTRY = {
    "flare_fpb": flare.FPB,
    "flare_fiqasa": flare.FIQASA,
    "flare_ner": flare.NER,
    "flare_finqa": flare.FinQA,
    "flare_headlines": flare.Headlines,
    "your_new_task": your_module.YourTask,  # This is where you add your task
    **flare.SM_TASKS,
}
```

Please note, the Classification base class provides three default metrics:

- **Accuracy**: This metric represents the ratio of correctly predicted observations to total observations. It is calculated as (True Positives + True Negatives) / Total Observations.
- **F1 Score**: The F1 Score is the harmonic mean of precision and recall, providing a balance between these two metrics. It's useful in cases where one measure is more important than the other. The F1 score is at its best at 1 (perfect precision and recall) and worst at 0.
- **Missing Ratio**: This metric calculates the proportion of responses where no options from the given choices in the task are returned.
Moreover, you can specify `CALCULATE_MCC` in your class definition to include the Matthews Correlation Coefficient (MCC). The MCC is a measure of the quality of binary classifications. It returns a value between -1 and +1. A coefficient of +1 represents a perfect prediction, 0 an average random prediction and -1 an inverse prediction.

For more custom metrics or requests, you may refer to `flare.NER` or `flare.FinQA` for examples.

## Generating Datasets for FIT (Financial Instruction Dataset)

When you are working with the Financial Instruction Dataset (FIT), it's crucial to follow the prescribed format for training and testing models.

### Dataset Format
The format should look like this:

```json
{
    "id": "unique id",
    "conversations": [
        {
            "from": "human",
            "value": "Your prompt and text"
        },
        {
            "from": "agent",
            "value": "Your answer"
        }
    ],
    "text": "Text to be classified",
    "label": "Your label"
}
```
Here's what each field means:

- "id": a unique identifier for each example in your dataset.
- "conversations": a list of conversation turns. Each turn is represented as a dictionary, with "from" representing the speaker, and "value" representing the text spoken in the turn.
- "text": the text to be classified.
- "label": the ground truth label for the text.


The first turn in the "conversations" list should always be from "human", and contain your prompt and the text. The second turn should be from "agent", and contain your answer.


## Assessment Instructions

### Automated Task Assessment

Using the task evaluation framework from [EleutherAI's lm-evaluation-harness](https://github.com/EleutherAI/lm-evaluation-harness), we've compiled Huggingface datasets for the following tasks:

- [NER (flare_ner)](https://huggingface.co/datasets/ChanceFocus/flare-ner)
- [FPB (flare_fpb)](https://huggingface.co/datasets/ChanceFocus/flare-fpb)
- [FIQASA (flare_fiqasa)](https://huggingface.co/datasets/ChanceFocus/flare-fiqasa)
- [FinQA (flare_finqa)](https://huggingface.co/datasets/ChanceFocus/flare-finqa)
- [FOMC (flare_fomc)](https://huggingface.co/datasets/ChanceFocus/flare-fomc)
- [Finer Ord (flare_finer_ord)](https://huggingface.co/datasets/ChanceFocus/flare-finer-ord)
- [German (flare_german)](https://huggingface.co/datasets/ChanceFocus/flare-german)
- [Australian (flare_german)](https://huggingface.co/datasets/ChanceFocus/flare-australian)
- [BigData22 for Stock Movement (flare_sm_bigdata)](https://huggingface.co/datasets/ChanceFocus/flare-sm-bigdata)
- [ACL18 for Stock Movement (flare_sm_acl)](https://huggingface.co/datasets/ChanceFocus/flare-sm-acl)
- [CIKM18 for Stock Movement (flare_sm_cikm)](https://huggingface.co/datasets/ChanceFocus/flare-sm-cikm)

For automated evaluation, please follow these instructions:
1. Huggingface Transformer (We are still working on llama-based models)
To evaluate a model hosted on the HuggingFace Hub (for instance, finma-7B-nlp), use this command:
```bash
export PYTHONPATH='{abs_path}/PIXIU/src:{abs_path}/PIXIU/src/lm-evaluation-harness'
python eval.py \
    --model hf-causal \
    --model_args pretrained=chancefocus/finma-7B-nlp \
    --tasks flare_ner,flare_sm_acl,flare_fpb
```

More details can be found in the [lm_eval](https://github.com/EleutherAI/lm-evaluation-harness) documentation.

2. Commercial APIs


Please note, for tasks such as NER, the automated evaluation is based on a specific pattern. This might fail to extract relevant information in zero-shot settings, resulting in relatively lower performance compared to previous human-annotated results.

```bash
export PYTHONPATH='{abs_path}/PIXIU/src:{abs_path}/PIXIU/src/lm-evaluation-harness'
export OPENAI_API_SECRET_KEY=YOUR_KEY_HERE
python eval.py \
    --model gpt-4 \
    --tasks flare_ner,flare_sm_acl,flare_fpb
```

### Self-Hosted Evaluation

To run inference backend:
```bash
bash scripts/run_interface.sh
```

Please adjust run_interface.sh according to your environment requirements.

To evaluate:

```bash
python data/*/evaluate.py
```


## Citation

If you use PIXIU in your work, please cite our paper.

```
@misc{xie2023pixiu,
      title={PIXIU: A Large Language Model, Instruction Data and Evaluation Benchmark for Finance}, 
      author={Qianqian Xie and Weiguang Han and Xiao Zhang and Yanzhao Lai and Min Peng and Alejandro Lopez-Lira and Jimin Huang},
      year={2023},
      eprint={2306.05443},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
```

## License

PIXIU is licensed under [MIT]. For more details, please see the [MIT](LICENSE) file.

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=chancefocus/pixiu&type=Date)](https://star-history.com/#chancefocus/pixiu&Date)

