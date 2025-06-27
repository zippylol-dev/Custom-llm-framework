# 🧠 Custom-LLM-Framework

A local LLM framework built completely **from scratch** — without PyTorch, TensorFlow, or even NumPy.  
Uses only `collections.defaultdict`, `threading`, `time`, and pure Python data structures.

> 🔍 Models are trained into a **readable `.txt` file** with context-based probabilities.  
> No black-box weight matrices. You can literally open the file and understand what it learned.

---

## ✨ Features

- ✅ **Custom architecture** (not Transformer, not RNN — original design)
- 🧠 **Infinitely dynamic context support** (`MAX_DYNAMIC`)
- ⚙️ Token-level or character-level training
- 📦 **No dependencies**
- 📚 Readable, hackable `Model.txt`
- 🧪 Fast training — even on mobile (Termux)
- 🔥 In some tasks, *outperforms PyTorch models*

---

## 🚀 Getting Started

```bash
git clone https://github.com/zippylol-dev/Custom-llm-framework
cd Custom-llm-framework
python train.py
python infer.py


---

🧱 How It Works

train.py: Builds n-gram statistics up to MAX_DYNAMIC, writes probabilities to Model.txt.

infer.py: Generates text based on context and optional temperature sampling.

tokenized_train.py: For word/subword level training.

Model.txt: Trained model in plain text — shows predictions like:

l after he = 100%
l after hel = 100%
o after hell = 100%



---

🗂️ Example Datasets

🗣️ General chatbot

🧠 Code assistant

🤪 Meme/joke language

🔣 Case-sensitive prompt detection


All datasets are stored in dataset.txt or in the trash/ folder as alternates.


---

🧪 Example

Start with: print
Generated: print("Hello, world!")

Start with: who are you
Generated: Bot: I'm just code, but I'm doing great, \u!


---

📦 Model Format

Each line of Model.txt is a learned rule:

token after context = probability%

Example:

o after hell = 100%

Can be edited, merged, or understood without code.


---

🧠 Parameters

Variable	Description

MAX_DYNAMIC	Controls how much context is used
temperature	Sampling randomness during inference
END_TOKEN	Sentence stop marker



---

📜 License

MIT — Free to use, modify, or meme.


---

🤖 Credits

Made with 💀 by zippylol-dev

A framework that teaches Python how to Python — using Python.
