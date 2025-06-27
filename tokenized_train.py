#!/usr/bin/env python3
from collections import defaultdict
import threading, time

MAX_DYNAMIC = float('inf')  # Must match with infer.py
END_TOKEN = "<END>"

# Subword tokens: common keywords + symbols
TOKENS = [
    "print", "def", "return", "if", "else", "while", "for", "in", "input",
    "(", ")", ":", "[", "]", "{", "}", ",", ".", "+", "-", "*", "/", "=",
    "\"", "'", "\\n", "\\t"
]

print("📥 Loading dataset...")
with open("dataset.txt", "r") as f:
    lines = [line.strip() for line in f if line.strip()]

def tokenize(line):
    i = 0
    tokens = []
    while i < len(line):
        matched = False
        for tok in sorted(TOKENS, key=len, reverse=True):
            if line[i:i+len(tok)] == tok:
                tokens.append(tok)
                i += len(tok)
                matched = True
                break
        if not matched:
            c = line[i]
            tokens.append(c if c != ' ' else "\\s")
            i += 1
    return tokens + [END_TOKEN]

sentences = [tokenize(line) for line in lines]
print(f"✅ {len(sentences)} tokenized sentences loaded.")

ngram_counts = defaultdict(int)
context_counts = defaultdict(int)

print("🧠 Counting token-grams...")
for idx, tokens in enumerate(sentences):
    limit = min(len(tokens), MAX_DYNAMIC)
    for gram in range(1, limit + 1):
        for i in range(len(tokens) - gram):
            context = "|".join(tokens[i:i + gram])
            next_tok = tokens[i + gram]
            ngram_counts[(context, next_tok)] += 1
            context_counts[context] += 1
    if idx % 5 == 0 or idx == len(sentences) - 1:
        print(f"step: {idx + 1}/{len(sentences)}, ppl=🙃, loss=👍, ema=🔥 ")

def write_model():
    print("💾 Writing model to Model.txt...")
    with open("Model.txt", "w") as f:
        for (context, next_tok), count in sorted(ngram_counts.items()):
            total = context_counts[context]
            prob = (count / total) * 100
            spacing = " " * max(1, 30 - len(context))
            f.write(f"{next_tok} after {context}{spacing}= {prob:.3f}%\n")
    print("✅ Model write complete.")

threading.Thread(target=write_model).start()

print(f"\n🎉 [✓] Training done! MAX_DYNAMIC={MAX_DYNAMIC}. Output in Model.txt")
