#!/usr/bin/env python3

import numpy as np
import random

MAX_DYNAMIC = 50

def load_model_npz(path='Model.npz'):
    data = np.load(path, allow_pickle=True)
    contexts = data['contexts']
    next_chars = data['next_chars']
    probs = data['probs']

    model = {}
    for ctx, ch, pr in zip(contexts, next_chars, probs):
        ctx = str(ctx)
        ch = str(ch)
        if ctx not in model:
            model[ctx] = []
        model[ctx].append((ch, float(pr)))
    return model

def sample_next(model, context, temperature=1.0):
    for i in range(len(context)):
        sub = context[i:]
        if sub in model:
            chars, probs = zip(*model[sub])
            if temperature < 0.001:
                return chars[probs.index(max(probs))]
            adjusted = [p ** (1.0 / temperature) for p in probs]
            total = sum(adjusted)
            norm_probs = [p / total for p in adjusted]
            return random.choices(chars, weights=norm_probs)[0]
    return ''

def generate_chain(model, seed, temperature=1.0, max_len=100):
    result = seed
    while len(result) < max_len:
        context = result[-MAX_DYNAMIC:]
        next_char = sample_next(model, context, temperature)
        if not next_char:
            break
        result += next_char
        if next_char == '.':
            break
    return result

def main():
    model = load_model_npz()
    try:
        seed = input("Start with: ").strip()
        temp = input("Temperature (e.g. 1 = normal, >1 = creative): ").strip()
        max_len = input("Max length (default 100): ").strip()

        temperature = float(temp) if temp else 1.0
        max_len = int(max_len) if max_len else 100

        print("Generated:", generate_chain(model, seed, temperature, max_len))
    except Exception as e:
        print("Error:", e)

if __name__ == '__main__':
    main()
