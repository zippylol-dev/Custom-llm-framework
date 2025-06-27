#!/usr/bin/env python3
from collections import defaultdict
import random

MAX_DYNAMIC = 13  # Must match train.py

def load_model(path='Model.txt'):
    model = defaultdict(list)
    with open(path, 'r') as f:
        for line in f:
            if 'after' in line and '=' in line:
                parts = line.strip().split()
                if len(parts) >= 5:
                    next_char = parts[0]
                    context = parts[2]
                    try:
                        prob = float(parts[4].replace('%', ''))
                        model[context].append((next_char, prob))
                    except ValueError:
                        continue
    return model

def sample_next(model, context, temperature=1.0):
    # Try longest suffix context down to smallest
    for i in range(len(context)):
        sub = context[i:]
        if sub in model:
            chars, probs = zip(*model[sub])
            if temperature < 0.001:
                return chars[probs.index(max(probs))]
            # Apply temperature scaling
            adjusted = [p ** (1.0 / temperature) for p in probs]
            total = sum(adjusted)
            norm_probs = [p / total for p in adjusted]
            return random.choices(chars, weights=norm_probs)[0]
    return ''  # Fallback

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
    global username, temp, max_len
    model = load_model()
    try:
        seed = input("Start with: ").strip()
        temperature = float(temp) if temp else 1.0
        max_len = int(max_len) if max_len else 100

        output = generate_chain(model, seed, temperature, max_len)
        output = output.replace("<END>", "")
        output = output.replace("\\s", " ")
        output = output.replace("\\u", username)
        if "Bot" in output:
            output = output[output.find("Bot"):]
        print("Generated:", output)
    except Exception as e:
        print("[!] Error:", e)

if __name__ == '__main__':
    try:
        username = input("tell your name!: ")
        temp = input("Temperature (e.g. 1 = normal, >1 = creative): ").strip()
        max_len = input("Max length (default 100): ").strip()
        while True:
            main()
    except (KeyboardInterrupt, EOFError):
        print("Bot: Bye!")
        exit()
