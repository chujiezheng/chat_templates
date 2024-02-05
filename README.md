# chat_templates

This is a repository that includes proper chat templates (or input formats) for large language models (LLMs), to support `transformers`'s `chat_template` [feature](https://huggingface.co/docs/transformers/chat_templating).

We know that different models are trained with different input formats, especially for those instruction-tuned or chat models. This is especially noted in `transformers`'s new `chat_template` feature. However, I found that popular models (e.g., `vicuna`, `falcon`) on HuggingFace do not include this parameter in their `tokenizer_config.json` files, which may make it troublesome to properly run these models. Also, the `chat_template` feature requires to implement a Jinja template, which may be not intuitive to be directly done in the json files.

So I collect proper chat templates of several popular models from official reference or implementations, which are put under  `chat_templates`. If you are interested to include more chat templates, feel free to open a pull request.

If you find this repo useful, please kindly cite it:
```tex
@misc{zheng-2023-chat-templates,
  author = {Zheng, Chujie},
  title = {Chat Templates for HuggingFace Large Language Models},
  year = {2023},
  howpublished = {\url{https://github.com/chujiezheng/chat_templates}}
}
```

## Supported Models

| Model (Family)     | Template File            | Reference                                                    | Comment                        |
| ------------------ | ------------------------ | ------------------------------------------------------------ | ------------------------------ |
| `llama-2-chat`     | `llama-2-chat.jinja`     | [link](https://huggingface.co/meta-llama/Llama-2-7b-chat-hf/blob/e1ce257bd76895e0864f3b4d6c7ed3c4cdec93e2/tokenizer_config.json#L12) | Official template              |
| `mistral-instruct` | `mistral-instruct.jinja` | [link](https://docs.mistral.ai/usage/guardrailing)           | `Mistral-7B-Instruct-v0.1/0.2` |
| `qwen2-chat`           | `chatml.jinja`           | [link](https://huggingface.co/Qwen/Qwen1.5-72B-Chat/blob/c31f50d339b6fdd93a6364d731a0ddbaca9931f5/tokenizer_config.json#L31)           | ChatML format; `Qwen1.5-0.4/1.8/4/7/14/72B-Chat`  | |
| `openchat`         | `openchat.jinja`         | [link](https://huggingface.co/openchat/openchat_3.5/blob/99d59d4447dc8d46f4847b3cb147cbd3330ba31b/tokenizer_config.json#L51) | `openchat-3.5`                 |
| `yi-chat`          | `chatml.jinja`           | [link](https://huggingface.co/01-ai/Yi-6B-Chat/blob/36326f9bc1c8020e0cf29ea830ee5e6679a66a23/tokenizer_config.json#L60) | ChatML format; `Yi-6/34B-Chat`|
| `orca-2`           | `chatml.jinja`           | [link](https://huggingface.co/microsoft/Orca-2-7b)           | ChatML format; `Orca-2-7/13b`  |
| `vicuna`           | `vicuna.jinja`           | [link](https://github.com/lm-sys/FastChat/blob/main/docs/vicuna_weights_version.md#prompt-template) | `vicuna-7/13b-v1.5`
| `zephyr`           | `zephyr.jinja`           | [link](https://huggingface.co/HuggingFaceH4/zephyr-7b-alpha/blob/2ce2d025864af849b3e5029e2ec9d568eeda892d/tokenizer_config.json#L34) | `zephyr-7b-alpha/beta`         |            |
| `starling-lm`      | `openchat.jinja`         | [link](https://huggingface.co/berkeley-nest/Starling-LM-7B-alpha/blob/f721e85293598f2ef774e483ae95343e39811577/tokenizer_config.json#L49) | `Starling-LM-7B-alpha`         |
| `solar-instruct`   | `solar-instruct.jinja`   | [link](https://huggingface.co/upstage/SOLAR-10.7B-Instruct-v1.0/blob/aac9da581d58d0ec8ae7146cc8f5d973569c49bc/tokenizer_config.json#L31) | `SOLAR-10.7B-Instruct-v1.0`    |
| `falcon-instruct`  | `falcon-instruct.jinja`  | [link](https://github.com/lm-sys/FastChat/blob/d578599c69d060e6d40943f1b5b72af98956092a/fastchat/conversation.py#L675) | `falcon-7/40b-instruct`        |
| `amberchat`        | `amberchat.jinja`        | [link](https://huggingface.co/LLM360/AmberChat)              | `AmberChat`, `AmberSafe`       |

## Examples of Setting `chat_template`

### Example 1: `llama-2-chat`

This example may check if the jinja file is correctly implemented.

```python
from transformers import AutoTokenizer

toker = AutoTokenizer.from_pretrained("meta-llama/Llama-2-7b-chat-hf", token="YOUR_OWN_TOKEN")
messages = [
    {'role': 'system', 'content': 'This is a system prompt.'},
    {'role': 'user', 'content': 'This is the first user input.'},
    {'role': 'assistant', 'content': 'This is the first assistant response.'},
    {'role': 'user', 'content': 'This is the second user input.'},
]
print('###### Default (yet Correct) Chat Template ######')
print(toker.apply_chat_template(messages, tokenize=False, add_generation_prompt=True))
print('###### Corrected Chat Template ######')
chat_template = open('./chat_templates/llama-2-chat.jinja').read()
chat_template = chat_template.replace('    ', '').replace('\n', '')
toker.chat_template = chat_template
print(toker.apply_chat_template(messages, tokenize=False, add_generation_prompt=True))
```

Expected output:

```
###### Default (yet Correct) Chat Template ######
<s>[INST] <<SYS>>
This is a system prompt.
<</SYS>>

This is the first user input. [/INST] This is the first assistant response. </s><s>[INST] This is the second user input. [/INST]
###### Corrected Chat Template ######
<s>[INST] <<SYS>>
This is a system prompt.
<</SYS>>

This is the first user input. [/INST] This is the first assistant response. </s><s>[INST] This is the second user input. [/INST]
```

### Example 2: `mistral-instruct`

For `mistral-instruct`, it does not natively support the `system` message, so passing the `system` message would raise error.

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

### Example 3: `vicuna`

NOTE: In [fast-chat](https://github.com/lm-sys/FastChat/blob/d578599c69d060e6d40943f1b5b72af98956092a/fastchat/conversation.py#L287C3-L287C3), `vicuna` does not add linebreaks between roles' messages. But I found that adding linebreaks leads to a bit better performance (especially for the v1.5 version).

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
