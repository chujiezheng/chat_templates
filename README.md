# chat_templates

This is a repository that includes proper chat templates (or input formats) for large language models (LLMs), to support `transformers`'s `chat_template` [feature](https://huggingface.co/docs/transformers/chat_templating).

We know that different models are trained with different input formats, especially for those instruction-tuned or chat models. This is especially noted in `transformers`'s new `chat_template` feature. However, I found that popular models (e.g., `vicuna`, `falcon`) on HuggingFace do not include this parameter in their `tokenizer_config.json` files, which may make it troublesome to properly run these models. Also, the `chat_template` feature requires to implement a Jinja template, which may be not intuitive to be directly done in the json files.

So I collect proper chat templates of several popular models from official reference or implementations, which are put under  `chat_templates`. If you are interested to include more chat templates, feel free to open a pull request.

## Examples of Setting `chat_template`

### Example 1: `llama(-2)`

```python
from transformers import AutoTokenizer

toker = AutoTokenizer.from_pretrained("huggyllama/llama-7b")
messages = [
    {'role': 'user', 'content': 'This is the first user input.'},
    {'role': 'assistant', 'content': 'This is the first assistant response.'},
    {'role': 'user', 'content': 'This is the second user input.'},
]
print('###### Default (but Improper) Chat Template ######')
print(toker.apply_chat_template(messages, tokenize=False, add_generation_prompt=True))
print('###### Corrected Chat Template ######')
toker.use_default_system_prompt = False
chat_template = open('./chat_templates/llama.jinja').read()
chat_template = chat_template.replace('    ', '').replace('\n', '')
toker.chat_template = chat_template
print(toker.apply_chat_template(messages, tokenize=False, add_generation_prompt=True))
```

Expected output:

```
###### Default (but Improper) Chat Template ######
<s>[INST] <<SYS>>
You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe. Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature.

If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information.
<</SYS>>

This is the first user input. [/INST] This is the first assistant response. </s><s>[INST] This is the second user input. [/INST]
###### Corrected Chat Template ######
<s>

User: This is the first user input.

Assistant: This is the first assistant response.

User: This is the second user input.

Assistant:
```

### Example 2: `llama-2-chat`

This example may check if the jinja file is correctly implemented

```python
from transformers import AutoTokenizer

toker = AutoTokenizer.from_pretrained("meta-llama/Llama-2-7b-chat-hf", token="YOUR_OWN_TOKEN")
messages = [
    {'role': 'user', 'content': 'This is the first user input.'},
    {'role': 'assistant', 'content': 'This is the first assistant response.'},
    {'role': 'user', 'content': 'This is the second user input.'},
]
print('###### Default (yet Correct) Chat Template ######')
print(toker.apply_chat_template(messages, tokenize=False, add_generation_prompt=True))
print('###### Corrected Chat Template ######')
messages = [{'role': 'system', 'content': 'This is a system prompt.'}] + messages
chat_template = open('./chat_templates/llama-2-chat.jinja').read()
chat_template = chat_template.replace('    ', '').replace('\n', '')
toker.chat_template = chat_template
print(toker.apply_chat_template(messages, tokenize=False, add_generation_prompt=True))
```

Expected output:

```
###### Default (yet Correct) Chat Template ######
<s>[INST] This is the first user input. [/INST] This is the first assistant response. </s><s>[INST] This is the second user input. [/INST]
###### Corrected Chat Template ######
<s>[INST] <<SYS>>
This is a system prompt.
<</SYS>>

This is the first user input. [/INST] This is the first assistant response. </s><s>[INST] This is the second user input. [/INST]
```

### Example 3: `vicuna-v1.3/1.5`

```python
from transformers import AutoTokenizer

toker = AutoTokenizer.from_pretrained("lmsys/vicuna-7b-v1.3")
messages = [
    {'role': 'user', 'content': 'This is the first user input.'},
    {'role': 'assistant', 'content': 'This is the first assistant response.'},
    {'role': 'user', 'content': 'This is the second user input.'},
]
print('###### Default (but Improper) Chat Template ######')
print(toker.apply_chat_template(messages, tokenize=False, add_generation_prompt=True))
print('###### Corrected Chat Template ######')
messages = [{'role': 'system', 'content': 'This is a system prompt.'}] + messages
chat_template = open('./chat_templates/vicuna.jinja').read()
chat_template = chat_template.replace('    ', '').replace('\n', '')
toker.chat_template = chat_template
print(toker.apply_chat_template(messages, tokenize=False, add_generation_prompt=True))
```

Expected output:

```
###### Default (but Improper) Chat Template ######
<s>[INST] <<SYS>>
You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe. Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature.

If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information.
<</SYS>>

This is the first user input. [/INST] This is the first assistant response. </s><s>[INST] This is the second user input. [/INST]
###### Corrected Chat Template ######
This is a system prompt. USER: This is the first user input. ASSISTANT: This is the first assistant response.</s> USER: This is the second user input. ASSISTANT:
```

### Example 4: `falcon(-instruct)`

```python
from transformers import AutoTokenizer

toker = AutoTokenizer.from_pretrained("tiiuae/falcon-7b-instruct")
messages = [
    {'role': 'system', 'content': 'This is a system prompt.'},
    {'role': 'user', 'content': 'This is the first user input.'},
    {'role': 'assistant', 'content': 'This is the first assistant response.'},
    {'role': 'user', 'content': 'This is the second user input.'},
]
print('###### Default (but Improper) Chat Template ######')
print(toker.apply_chat_template(messages, tokenize=False, add_generation_prompt=True))
print('###### Corrected Chat Template ######')
chat_template = open('./chat_templates/falcon.jinja').read()
chat_template = chat_template.replace('    ', '').replace('\n', '')
toker.chat_template = chat_template
print(toker.apply_chat_template(messages, tokenize=False, add_generation_prompt=True))
```

Expected output:

```
###### Default (but Improper) Chat Template ######
<|im_start|>system
This is a system prompt.<|im_end|>
<|im_start|>user
This is the first user input.<|im_end|>
<|im_start|>assistant
This is the first assistant response.<|im_end|>
<|im_start|>user
This is the second user input.<|im_end|>
<|im_start|>assistant

###### Corrected Chat Template ######
This is a system prompt.

User: This is the first user input.

Assistant: This is the first assistant response.

User: This is the second user input.

Assistant:
```

## Template Reference

| Model Family        | Template File        | Reference                                                    | Comment                                                      |
| ------------------- | -------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| `llama(-2)`         | `llama.jinja`        | [link](https://github.com/lm-sys/FastChat/blob/d578599c69d060e6d40943f1b5b72af98956092a/fastchat/conversation.py#L514) | Since `llama(-2)` is not fine-tuned, we may use the same template as `claude` |
| `llama-2-chat`      | `llama-2-chat.jinja` | [link](https://huggingface.co/meta-llama/Llama-2-7b-chat-hf/blob/e1ce257bd76895e0864f3b4d6c7ed3c4cdec93e2/tokenizer_config.json#L12) | Official template                                            |
| `vicuna-v1.3/1.5`   | `vicuna.jinja`       | [link](https://github.com/lm-sys/FastChat/blob/d578599c69d060e6d40943f1b5b72af98956092a/fastchat/conversation.py#L287) |                                                              |
| `falcon(-instruct)` | `falcon.jinja`       | [link](https://github.com/lm-sys/FastChat/blob/d578599c69d060e6d40943f1b5b72af98956092a/fastchat/conversation.py#L675) |                                                              |
| `orca-2` | `orca.jinja`       | [link](https://huggingface.co/microsoft/Orca-2-7b) |  ChatML format   |
| `mistra`      | `mistra.jinja` | [link](https://docs.mistral.ai/usage/guardrailing) |  |
