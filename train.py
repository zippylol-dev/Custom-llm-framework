#!/usr/bin/env python3
from collections import defaultdict
import threading, time

MAX_DYNAMIC = 3  # Good generalization
MAX_DYNAMIC = 13  # temporary overridden for python learning
ALLOWED = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789=+-*/.!?()[]{}<>'\"\\:, \t\n_")
END_TOKEN = "<END>"

print("📥 Loading dataset...")
with open("dataset.txt", "r") as f:
    lines = [line.strip() for line in f if line.strip()]

sentences = []
for line in lines:
    cleaned = ''.join(c for c in line if c in ALLOWED)
    cleaned = cleaned.replace(" ", "\\s")
    if cleaned:
        sentences.append(cleaned + END_TOKEN)

print(f"✅ {len(sentences)} cleaned sentences loaded.")

ngram_counts = defaultdict(int)
context_counts = defaultdict(int)

print("🧠 Counting n-grams...")
for idx, sentence in enumerate(sentences):
    limit = min(len(sentence), int(MAX_DYNAMIC) if MAX_DYNAMIC != float('inf') else len(sentence))
    for gram in range(1, limit + 1):
        for i in range(len(sentence) - gram):
            context = sentence[i:i + gram]
            next_char = sentence[i + gram]
            ngram_counts[(context, next_char)] += 1
            context_counts[context] += 1
    if idx % 5 == 0 or idx == len(sentences) - 1:
        print(f"⚙️ Prestep {idx + 1}/{len(sentences)}...")

def write_model():
    print("💾 Writing model to Model.txt...")
    with open("Model.txt", "w") as f:
        for (context, next_char), count in sorted(ngram_counts.items()):
            total = context_counts[context]
            prob = (count / total) * 100
            spacing = " " * max(1, 20 - len(context))
            f.write(f"{next_char} after {context}{spacing}= {prob:.3f}%\n")
    print("✅ Model write complete.")

threading.Thread(target=write_model).start()

for a in range(1, 5):
    time.sleep(0.2)
    print(f"📊 step {a} — Loss=🤷, EMA=🚫, Perplexity=¯\\_(ツ)_/¯")

print(f"\n🎉 [✓] Training done! MAX_DYNAMIC={MAX_DYNAMIC}. Output in Model.txt")
