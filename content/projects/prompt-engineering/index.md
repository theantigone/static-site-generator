# ✍️ Prompt Engineering LLMs

[< Back to Projects](/projects)

[< Back Home](/)

![Prompt Engineering Analysis Report](/images/prompt-engineering.png)

> Figure 1: An analysis of `ChatGPT-4.1` and `Codestral 25.01` using the **Code Summarization** prompting strategy.

This project is about **Prompt Engineering for In-Context Learning** that investigates the impact of different prompt designs on the performance of **Large Language Models** (`LLMs`) across a variety of software engineering tasks.

In this assignment, five prompting strategies—_zero-shot_, _few-shot_, _chain-of-thought_, _prompt-chaining_, and _self-consistency_—were applied to 22 tasks, including code summarization, bug fixing, API generation, and code translation.

Experiments compared four models—[gpt-4.1](https://github.com/marketplace/models/azure-openai/gpt-4-1/), [Codestral-2501](https://github.com/marketplace/models/azureml-mistral/Codestral-2501), [gpt-4.1-mini](https://github.com/marketplace/models/azure-openai/gpt-4-1-mini), and [gpt-4.1-nano](https://github.com/marketplace/models/azure-openai/gpt-4-1-nano)—to demonstrate how the strategic use of prompt examples and structured reasoning influences the quality and clarity of generated code.

_Self-consistency prompting_ employed `3` repetitions, with a temperature setting of `0.7` and a maximum token limit of `1024` tokens across all evaluations.

[Source Code](https://github.com/theantigone/Prompt-Engineering-for-In-Context-Learning)
