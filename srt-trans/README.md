# srt-trans

## 한글->영어

1. 구글

```python
pip install google-cloud-translate

from googletrans import Translator

translator = Translator()
text = "Hello, how are you?"
translated = translator.translate(text, src='en', dest='ko')
print(translated.text)  # 안녕하세요, 어떻게 지내세요?

```

2. Papago NMT API

key가 필요

3. DeepL API

key가 필요

```python
import deepl

auth_key = "YOUR_AUTH_KEY"
translator = deepl.Translator(auth_key)
result = translator.translate_text("Hello, how are you?", target_lang="KO")
print(result.text)  # 안녕하세요, 어떻게 지내세요?

```

4. Hugging Face Transformers

```python
from transformers import MarianMTModel, MarianTokenizer

model_name = 'Helsinki-NLP/opus-mt-en-ko'
tokenizer = MarianTokenizer.from_pretrained(model_name)
model = MarianMTModel.from_pretrained(model_name)

text = "Hello, how are you?"
inputs = tokenizer.encode(text, return_tensors="pt", padding=True)
outputs = model.generate(inputs, max_length=40, num_beams=4, early_stopping=True)
translated = tokenizer.decode(outputs[0], skip_special_tokens=True)
print(translated)  # 안녕하세요, 어떻게 지내세요?

```
