#!/usr/bin/env python3

from collections import defaultdict
import numpy as np

MAX_DYNAMIC = 50
ALLOWED = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789=+-*/.!?()")

# Read and clean
with open("dataset.txt", "r") as f:
    lines = f.read().strip().splitlines()

sentences = []
for line in lines:
    cleaned = ''.join(c for c in line if c in ALLOWED)
    if cleaned:
        sentences.append(cleaned + ".")

# Count variable-length n-grams
ngram_counts = defaultdict(int)
context_counts = defaultdict(int)

for sentence in sentences:
    for gram in range(1, min(len(sentence), MAX_DYNAMIC)):
        for i in range(len(sentence) - gram):
            context = sentence[i:i + gram]
            next_char = sentence[i + gram]
            ngram_counts[(context, next_char)] += 1
            context_counts[context] += 1

# Convert to arrays
contexts = []
next_chars = []
probs = []

for (context, next_char), count in ngram_counts.items():
    total = context_counts[context]
    contexts.append(context)
    next_chars.append(next_char)
    probs.append((count / total) * 100)

# Save as .npz
np.savez_compressed("Model.npz", contexts=np.array(contexts), next_chars=np.array(next_chars), probs=np.array(probs))
print(f"Training complete. Saved to Model.npz (MAX_DYNAMIC={MAX_DYNAMIC})")
