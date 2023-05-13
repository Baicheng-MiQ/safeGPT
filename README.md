# safeGPT

⚡️ Lightweight wrapper for OpenAI's Chat models that adds moderation rules and handlers to your requests.
![carbon (6)](https://github.com/Baicheng-MiQ/safeGPT/assets/85795754/a1e9b4bb-3314-4367-ac3e-33aaa2378a6d)


```bash
pip install safeGPT
```
## Features

- Add moderation rules to filter out unsafe content from OpenAI's Chat models.
- Retry requests with different handlers to improve the quality of the response.
- Combine multiple rules and handlers to create a custom safety system.
- Easy to use and extend with your own rules and handlers.

## Quickstart

```python
import safeGPT
from safeGPT.rules import OpenAIModeration
from safeGPT.handlers import AdditionalPromptRetry

safeGPT.api_key = "sk-<your key here>"

# Create a safe chat completion object with a moderation rule and handler
safe_chat = safeGPT.ChatCompletion(
    rule=OpenAIModeration(),
    handler=AdditionalPromptRetry("This is a safe space. Please be kind to others."),
    max_retries=3,
)

# Make your first safe request, exactly like you would with OpenAI
res = safe_chat.create(
    model="gpt-4",
    messages=[{"rule": "user", "content": "Say something mean to me."}]
)

# Print the response
print(res.choices[0].message.content)
```

## Basic Usage

```python
import safeGPT
from safeGPT.rules import KeywordDetection
from safeGPT.handlers import Replace

safeGPT.api_key = "sk-<your key here>"

# Create a safe chat completion object with a moderation rule and handler
safe_chat = safeGPT.ChatCompletion(
    rule=KeywordDetection(["badword"]),
    handler=Replace("badword", "goodword"),
)

# Make your first safe request, exactly like you would with OpenAI
res = safe_chat.create(
    model="gpt-4",
    messages=[{"rule": "user", "content": "Tell me a story with badword in it."}]
)

# Print the response
print(res.choices[0].message.content)
```

## Handlers

safeGPT comes with a set of predefined handlers that can be used to modify the behavior of the ChatCompletion object. These handlers can be used to retry requests with different parameters or to censor the response content.

### 1. DoNothing

This handler does nothing and simply executes the request without any modification.

**Example:**

```python
from safeGPT.handlers import DoNothing

handler = DoNothing()
```

### 2. IncreaseTemperatureRetry

This handler increases the temperature by a specified value and retries the request.

**Arguments:**

- `by`: The value by which to increase the temperature (default: 0.1)
- `max_val`: The maximum temperature value allowed (default: 2.0)

**Example:**

```python
from safeGPT.handlers import IncreaseTemperatureRetry

handler = IncreaseTemperatureRetry(by=0.1, max_val=2.0)
```

### 3. DecreaseTemperatureRetry

This handler decreases the temperature by a specified value and retries the request.

**Arguments:**

- `by`: The value by which to decrease the temperature (default: 0.1)
- `min_val`: The minimum temperature value allowed (default: 0.0)

**Example:**

```python
from safeGPT.handlers import DecreaseTemperatureRetry

handler = DecreaseTemperatureRetry(by=0.1, min_val=0.0)
```

### 4. IncreaseTopPRetry

This handler increases the top_p value by a specified value and retries the request.

**Arguments:**

- `by`: The value by which to increase the top_p (default: 0.1)
- `max_val`: The maximum top_p value allowed (default: 1.0)

**Example:**

```python
from safeGPT.handlers import IncreaseTopPRetry

handler = IncreaseTopPRetry(by=0.1, max_val=1.0)
```

### 5. DecreaseTopPRetry

This handler decreases the top_p value by a specified value and retries the request.

**Arguments:**

- `by`: The value by which to decrease the top_p (default: 0.1)
- `min_val`: The minimum top_p value allowed (default: 0.0)

**Example:**

```python
from safeGPT.handlers import DecreaseTopPRetry

handler = DecreaseTopPRetry(by=0.1, min_val=0.0)
```

### 6. IncreasePresencePenaltyRetry

This handler increases the presence_penalty value by a specified value and retries the request.

**Arguments:**

- `by`: The value by which to increase the presence_penalty (default: 0.1)
- `max_val`: The maximum presence_penalty value allowed (default: 2.0)

**Example:**

```python
from safeGPT.handlers import IncreasePresencePenaltyRetry

handler = IncreasePresencePenaltyRetry(by=0.1, max_val=2.0)
```

### 7. DecreasePresencePenaltyRetry

This handler decreases the presence_penalty value by a specified value and retries the request.

**Arguments:**

- `by`: The value by which to decrease the presence_penalty (default: 0.1)
- `min_val`: The minimum presence_penalty value allowed (default: -2.0)

**Example:**

```python
from safeGPT.handlers import DecreasePresencePenaltyRetry

handler = DecreasePresencePenaltyRetry(by=0.1, min_val=-2.0)
```

### 8. IncreaseFrequencyPenaltyRetry

This handler increases the frequency_penalty value by a specified value and retries the request.

**Arguments:**

- `by`: The value by which to increase the frequency_penalty (default: 0.1)
- `max_val`: The maximum frequency_penalty value allowed (default: 2.0)

**Example:**

```python
from safeGPT.handlers import IncreaseFrequencyPenaltyRetry

handler = IncreaseFrequencyPenaltyRetry(by=0.1, max_val=2.0)
```

### 9. DecreaseFrequencyPenaltyRetry

This handler decreases the frequency_penalty value by a specified value and retries the request.

**Arguments:**

- `by`: The value by which to decrease the frequency_penalty (default: 0.1)
- `min_val`: The minimum frequency_penalty value allowed (default: -2.0)

**Example:**

```python
from safeGPT.handlers import DecreaseFrequencyPenaltyRetry

handler = DecreaseFrequencyPenaltyRetry(by=0.1, min_val=-2.0)
```

### 10. AdditionalPromptRetry

This handler adds an additional prompt to the request and retries it.

**Arguments:**

- `prompt`: The additional prompt to add to the request (default: "Answer my query politely. ")

**Example:**

```python
from safeGPT.handlers import AdditionalPromptRetry

handler = AdditionalPromptRetry(prompt="Please provide a more detailed answer.")
```

### 11. Replace

This handler replaces specified keywords in the response content with a replacement string.

**Arguments:**

- `keyword`: A list of keywords or a single keyword to replace
- `replace_with`: The replacement string (default: "*")

**Example:**

```python
from safeGPT.handlers import Replace

handler = Replace(keyword=["badword1", "badword2"], replace_with="*")
```

## Rules

safeGPT comes with a set of predefined rules that can be used to filter out unsafe content from OpenAI's Chat models. These rules can be used to check the generated content against various criteria.

### 1. OpenAIModeration

This rule uses OpenAI's moderation API to check for bad content.

**Arguments:**

- `categories`: A list of categories to check for. If None, all categories will be checked (default: None)

**Example:**

```python
from safeGPT.rules import OpenAIModeration

rule = OpenAIModeration(categories=["hate", "violence"])
```

### 2. KeywordDetection

This rule detects keywords in the input text.

**Arguments:**

- `keywords`: A list of keywords to check for

**Example:**

```python
from safeGPT.rules import KeywordDetection

rule = KeywordDetection(keywords=["badword1", "badword2"])
```

### 3. RegexSearch

This rule matches the input text against a regex.

**Arguments:**

- `regex`: The regex to check for

**Example:**

```python
from safeGPT.rules import RegexSearch

rule = RegexSearch(regex="badword\d+")
```

### 4. DoNotFlag

This rule always returns false, meaning it will not flag any content.

**Example:**

```python
from safeGPT.rules import DoNotFlag

rule = DoNotFlag()
```

### 5. AlwaysFlag

This rule always returns true, meaning it will flag all content.

**Example:**

```python
from safeGPT.rules import AlwaysFlag

rule = AlwaysFlag()
```

### 6. SequentialCheck

This rule checks if all the rules in the list return true. Useful if you want to apply multiple rules.

**Arguments:**

- `rules`: A list of rules to check

**Example:**

```python
from safeGPT.rules import OpenAIModeration, KeywordDetection, SequentialCheck

rule = SequentialCheck([
    OpenAIModeration(categories=["hate", "violence"]),
    KeywordDetection(keywords=["badword1", "badword2"])
])
```



## Custom Rules and Handlers
You can create your own custom rules and handlers by extending the `Rule` and `Handler` classes respectively.

### Custom Rule Example

```python
from safeGPT.rules import custom_rule


@custom_rule
def MyCustomRule(input_text: str) -> bool:
    return "my_custom_keyword" in input_text
```

### Custom Handler Example

```python
from safeGPT.handlers import custom_handler
from safeGPT.abstraction import OpenAIChatCompletionWrapper


@custom_handler
def MyCustomHandler(source: OpenAIChatCompletionWrapper) -> OpenAIChatCompletionWrapper:
    source.messages.append({"role": "user", "content": "Please be more polite."})
    source.execute()
    return source
```
