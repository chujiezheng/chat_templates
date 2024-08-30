# chat_templates

This is a repository that includes proper chat templates (or input formats) for instruction-tuned large language models (LLMs), to support `transformers`'s `chat_template` [feature](https://huggingface.co/docs/transformers/chat_templating). If you are interested to include more chat templates, feel free to open a pull request

If you find this repo useful, please kindly cite it:
```tex
@misc{zheng-2024-chat-templates,
  author = {Zheng, Chujie},
  title = {Chat Templates for HuggingFace Large Language Models},
  year = {2024},
  howpublished = {\url{https://github.com/chujiezheng/chat_templates}}
}
```

## Updates

* **[07/2024]** Added support for Meta's **Llama-3.1** models
* **[06/2024]** Added support for Google's **Gemma-2** models
* **[05/2024]** Added support for Nvidia's **ChatQA** models
* **[04/2024]** Added support for Microsoft's **Phi-3** models
* **[04/2024]** Added support for Meta's **Llama-3** models
* **[02/2024]** Added support for Google's **Gemma** models
* **[02/2024]** Added usage explanation for **generation_configs**
* **[01/2024]** Added support for Alibaba's **Qwen2** models

## What are Contained in This Repo?

- [`chat_templates`](/chat_templates/) contains the jinja files of collected chat templates, which can be directly replaced in the Huggingface tokenizers

- [`generation_configs`](/generation_configs/) contains the corresponding json configs used for controlling the ending of response generations. Specially, **the `stop_token_ids` should be directly passed into the `generate` method by the `eos_token_id` argument**


## Usage Examples

**Important NOTE:** As mentioned in [this issue](https://github.com/chujiezheng/chat_templates/issues/15), the `messages` should contain **at least one user message**. It is strongly not recommented to pass only the system message, as there may result in unexpected outputs (because the models are not trained in this way).


<details>
  <summary><b>Example 1: Meta-Llama-3-8B-Instruct</b></summary>

This example may check if the jinja file is correctly implemented.

```python
from transformers import AutoTokenizer

toker = AutoTokenizer.from_pretrained("meta-llama/Meta-Llama-3-8B-Instruct", token="YOUR_OWN_TOKEN")
messages = [
    {'role': 'system', 'content': 'This is a system prompt.'},
    {'role': 'user', 'content': 'This is the first user input.'},
    {'role': 'assistant', 'content': 'This is the first assistant response.'},
    {'role': 'user', 'content': 'This is the second user input.'},
]
print('###### Default (yet Correct) Chat Template ######')
print(toker.apply_chat_template(messages, tokenize=False, add_generation_prompt=True))
print('###### Corrected Chat Template ######')
chat_template = open('./chat_templates/llama-3-instruct.jinja').read()
chat_template = chat_template.replace('    ', '').replace('\n', '')
toker.chat_template = chat_template
print(toker.apply_chat_template(messages, tokenize=False, add_generation_prompt=True))
```

Expected output:

```
###### Default (yet Correct) Chat Template ######
<|begin_of_text|><|start_header_id|>system<|end_header_id|>

This is a system prompt.<|eot_id|><|start_header_id|>user<|end_header_id|>

This is the first user input.<|eot_id|><|start_header_id|>assistant<|end_header_id|>

This is the first assistant response.<|eot_id|><|start_header_id|>user<|end_header_id|>

This is the second user input.<|eot_id|><|start_header_id|>assistant<|end_header_id|>


###### Corrected Chat Template ######
<|begin_of_text|><|start_header_id|>system<|end_header_id|>

This is a system prompt.<|eot_id|><|start_header_id|>user<|end_header_id|>

This is the first user input.<|eot_id|><|start_header_id|>assistant<|end_header_id|>

This is the first assistant response.<|eot_id|><|start_header_id|>user<|end_header_id|>

This is the second user input.<|eot_id|><|start_header_id|>assistant<|end_header_id|>
```

</details>


<details>
  <summary><b>Example 2: Mistral-7B-Instruct-v0.2</b></summary>

For `mistral-instruct` (also `gemma-it`), it does not natively support the `system` message, so passing the `system` message would raise error.

```python
from transformers import AutoTokenizer

toker = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-Instruct-v0.2")
messages = [
    {'role': 'system', 'content': 'This is a system prompt.'},
    {'role': 'user', 'content': 'This is the first user input.'},
    {'role': 'assistant', 'content': 'This is the first assistant response.'},
    {'role': 'user', 'content': 'This is the second user input.'},
]
print('###### Default (but Improper) Chat Template ######')
# raising error
#print(toker.apply_chat_template(messages, tokenize=False, add_generation_prompt=True))
print('###### Corrected Chat Template ######')
chat_template = open('./chat_templates/mistral-instruct.jinja').read()
chat_template = chat_template.replace('    ', '').replace('\n', '')
toker.chat_template = chat_template
print(toker.apply_chat_template(messages, tokenize=False, add_generation_prompt=True))
```

Expected output:

```
###### Default (but Error-Raising) Chat Template ######
jinja2.exceptions.TemplateError: Conversation roles must alternate user/assistant/user/assistant/...
###### Corrected Chat Template ######
<s>[INST] This is a system prompt.

This is the first user input. [/INST] This is the first assistant response. </s>[INST] This is the second user input. [/INST]
```

</details>


<details>
  <summary><b>Example 3: vicuna-7b-v1.5</b></summary>

**NOTE:** In [fast-chat](https://github.com/lm-sys/FastChat/blob/d578599c69d060e6d40943f1b5b72af98956092a/fastchat/conversation.py#L287C3-L287C3), `vicuna` does not add linebreaks between roles' messages. But I found that adding linebreaks leads to a bit better performance (especially for the v1.5 version).

Also, I found `vicuna-7/13/33b-v1.3` may not work well when given a system message different from its default one. So I would recommend to use `vicuna-7/13b-v1.5` instead.

```python
from transformers import AutoTokenizer

toker = AutoTokenizer.from_pretrained("lmsys/vicuna-7b-v1.5")
messages = [
    {'role': 'system', 'content': 'This is a system prompt.'},
    {'role': 'user', 'content': 'This is the first user input.'},
    {'role': 'assistant', 'content': 'This is the first assistant response.'},
    {'role': 'user', 'content': 'This is the second user input.'},
]
print('###### Default (but Improper) Chat Template ######')
print(toker.apply_chat_template(messages, tokenize=False, add_generation_prompt=True))
print('###### Corrected Chat Template ######')
chat_template = open('./chat_templates/vicuna.jinja').read()
chat_template = chat_template.replace('    ', '').replace('\n', '')
toker.chat_template = chat_template
print(toker.apply_chat_template(messages, tokenize=False, add_generation_prompt=True))
```

Expected output:

```
###### Default (but Improper) Chat Template ######
<s>[INST] <<SYS>>
This is a system prompt.
<</SYS>>

This is the first user input. [/INST] This is the first assistant response. </s><s>[INST] This is the second user input. [/INST]
###### Corrected Chat Template ######
<s>This is a system prompt.

USER: This is the first user input.
ASSISTANT: This is the first assistant response.</s>
USER: This is the second user input.
ASSISTANT:
```

</details>


## Supported Models

**NOTE:** The listed models are not inclusive and also include other-sized ones in the same model family

<details>
  <summary><b>Llama-3.1-Instruct</b></summary>

- Models: `meta-llama/Meta-Llama-3.1-8B-Instruct`, `meta-llama/Meta-Llama-3.1-405B-Instruct-FP8`
- Chat template: `chat_templates/llama-3-instruct.jinja`
- Generation config: `generation_configs/llama-3.1-instruct.json`
- Reference: https://huggingface.co/meta-llama/Meta-Llama-3.1-8B-Instruct/blob/main/tokenizer_config.json#L2053

</details>


<details>
  <summary><b>Llama-3-Instruct</b></summary>

- Models: `meta-llama/Meta-Llama-3-8B-Instruct`
- Chat template: `chat_templates/llama-3-instruct.jinja`
- Generation config: `generation_configs/llama-3-instruct.json`
- Reference: https://huggingface.co/meta-llama/Meta-Llama-3-8B-Instruct/blob/main/tokenizer_config.json#L2053

</details>


<details>
  <summary><b>Llama-2-Chat, CodeLlama-Instruct</b></summary>

- Models: `meta-llama/Llama-2-7b-chat-hf`, `meta-llama/CodeLlama-7b-Instruct-hf`
- Chat template: `chat_templates/llama-2-chat.jinja`
- Generation config: `generation_configs/llama-2-chat.json`
- Reference: https://huggingface.co/meta-llama/Llama-2-7b-chat-hf/blob/main/tokenizer_config.json#L12

</details>


<details>
  <summary><b>Qwen2-Instruct, Qwen1.5-Chat</b></summary>

- Models: `Qwen/Qwen2-7B-Instruct`, `Qwen/Qwen1.5-7B-Chat`
- Chat template: `chat_templates/chatml.jinja`
- Generation config: `generation_configs/qwen2-instruct.json`
- Reference: https://huggingface.co/Qwen/Qwen2-72B-Instruct/blob/main/tokenizer_config.json#L31

</details>


<details>
  <summary><b>Mistral-Instruct</b></summary>

- Models: `mistralai/Mistral-7B-Instruct-v0.3`, `mistralai/Mixtral-8x7B-Instruct-v0.1`
- Chat template: `chat_templates/mistral-instruct.jinja`
- Generation config: `generation_configs/mistral-instruct.json`
- Reference: https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.3/blob/main/tokenizer_config.json#L42
- Comment: **System message is acceptable** by prepending it before the first user input

</details>


<details>
  <summary><b>Phi-3-Instruct</b></summary>

- Models: `microsoft/Phi-3-mini-4k-instruct`
- Chat template: `chat_templates/phi-3.jinja`
- Generation config: `generation_configs/phi-3.json`
- Reference: https://huggingface.co/microsoft/Phi-3-mini-128k-instruct/blob/main/tokenizer_config.json#L338

</details>


<details>
  <summary><b>Yi-1.5-Chat, Yi-Chat</b></summary>

- Models: `01-ai/Yi-1.5-6B-Chat`, `01-ai/Yi-6B-Chat`
- Chat template: `chat_templates/chatml.jinja`
- Generation config: `generation_configs/yi-chat.json`
- Reference: https://huggingface.co/01-ai/Yi-6B-Chat/blob/main/tokenizer_config.json#L60

</details>


<details>
  <summary><b>gemma-it, gemma-2-it</b></summary>

- Models: `google/gemma-7b-it`, `google/gemma-2-9b-it`
- Chat template: `chat_templates/gemma-it.jinja`
- Generation config: `generation_configs/gemma-it.json`
- Reference: https://huggingface.co/google/gemma-7b-it/blob/main/tokenizer_config.json#L1507
- Comment: **System message is acceptable**

</details>


<details>
  <summary><b>Llama3-ChatQA-1.5</b></summary>

- Models: `nvidia/Llama3-ChatQA-1.5-8B`
- Chat template: `chat_templates/chatqa.jinja`
- Generation config: `generation_configs/chatqa.json`
- Reference: https://huggingface.co/nvidia/Llama3-ChatQA-1.5-8B#when-context-is-available
- Comment: Context message is acceptable

</details>


<details>
  <summary><b>openchat-3.5, Starling-LM</b></summary>

- Models: `openchat/openchat_3.5`, `berkeley-nest/Starling-LM-7B-alpha`
- Chat template: `chat_templates/openchat-3.5.jinja`
- Generation config: `generation_configs/openchat-3.5.json`
- Reference: https://huggingface.co/openchat/openchat_3.5/blob/main/tokenizer_config.json#L51

</details>


<details>
  <summary><b>zephyr</b></summary>

- Models: `zephyr-7b-alpha`
- Chat template: `chat_templates/zephyr.jinja`
- Generation config: `generation_configs/zephyr.json`
- Reference: https://huggingface.co/HuggingFaceH4/zephyr-7b-beta/blob/main/tokenizer_config.json#L34

</details>


<details>
  <summary><b>vicuna</b></summary>

- Models: `vicuna-7b-v1.5`, `vicuna-7b-v1.3`
- Chat template: `chat_templates/vicuna.jinja`
- Generation config: `generation_configs/vicuna.json`
- Reference: https://github.com/lm-sys/FastChat/blob/main/docs/vicuna_weights_version.md#prompt-template

</details>


<details>
  <summary><b>Orca-2</b></summary>

- Models: `microsoft/Orca-2-7b`
- Chat template: `chat_templates/chatml.jinja`
- Generation config: `generation_configs/orca-2.json`
- Reference: https://huggingface.co/microsoft/Orca-2-7b

</details>


<details>
  <summary><b>falcon-instruct</b></summary>

- Models: `tiiuae/falcon-7b-instruct`
- Chat template: `chat_templates/falcon-instruct.jinja`
- Reference: https://github.com/lm-sys/FastChat/blob/main/docs/vicuna_weights_version.md#prompt-template

</details>


<details>
  <summary><b>SOLAR-Instruct</b></summary>

- Models: `upstage/SOLAR-10.7B-Instruct-v1.0`
- Chat template: `chat_templates/solar-instruct.jinja`
- Generation config: `generation_configs/solar-instruct.json`
- Reference: https://huggingface.co/upstage/SOLAR-10.7B-Instruct-v1.0/blob/main/tokenizer_config.json#L31

</details>


<details>
  <summary><b>Alpaca</b></summary>

- Models: `tatsu-lab/alpaca-7b-wdiff`
- Chat template: `chat_templates/alpaca.jinja`
- Generation config: `generation_configs/alpaca.json`
- Reference: https://github.com/tatsu-lab/stanford_alpaca

</details>


<details>
  <summary><b>AmberChat</b></summary>

- Models: `LLM360/AmberChat`, `LLM360/AmberSafe`
- Chat template: `chat_templates/amberchat.jinja`
- Generation config: `generation_configs/amberchat.json`
- Reference: https://huggingface.co/LLM360/AmberChat

</details>


<details>
  <summary><b>saiga</b></summary>

- Models: `IlyaGusev/saiga_mistral_7b_lora`
- Chat template: `chat_templates/saiga.jinja`
- Generation config: `generation_configs/saiga.json`
- Reference: https://huggingface.co/IlyaGusev/saiga_mistral_7b_lora#saigamistral-7b-russian-mistral-based-chatbot
- Comment: A series of Russian models

</details>

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=chujiezheng/chat_templates&type=Date)](https://star-history.com/#chujiezheng/chat_templates&Date)
