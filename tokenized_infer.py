#!/usr/bin/env python3
from collections import defaultdict
import random

MAX_DYNAMIC = 2000  # Must match train.py
END_TOKEN = "<END>"

# Match same tokens as in train.py
TOKENS = [
    "print", "def", "return", "if", "else", "while", "for", "in", "input",
    "(", ")", ":", "[", "]", "{", "}", ",", ".", "+", "-", "*", "/", "=",
    "\"", "'", "\\n", "\\t"
]

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
    return tokens

def detokenize(tokens):
    s = ""
    for t in tokens:
        if t == "\\s":
            s += " "
        elif t == "\\n":
            s += "\n"
        elif t == "\\t":
            s += "\t"
        else:
            s += t
    return s

def load_model(path='Model.txt'):
    model = defaultdict(list)
    with open(path, 'r') as f:
        for line in f:
            if 'after' in line and '=' in line:
                parts = line.strip().split('after')
                if len(parts) != 2:
                    continue
                next_tok = parts[0].strip()
                rest = parts[1].split('=')
                context = rest[0].strip()
                try:
                    prob = float(rest[1].replace('%', '').strip())
                    model[context].append((next_tok, prob))
                except ValueError:
                    continue
    return model

def sample_next(model, context_tokens, temperature=1.0):
    for i in range(len(context_tokens)):
        sub = "|".join(context_tokens[i:])
        if sub in model:
            toks, probs = zip(*model[sub])
            if temperature < 0.001:
                return toks[probs.index(max(probs))]
            adjusted = [p ** (1.0 / temperature) for p in probs]
            total = sum(adjusted)
            norm_probs = [p / total for p in adjusted]
            return random.choices(toks, weights=norm_probs)[0]
    return ''  # fallback

def generate_chain(model, seed, temperature=1.0, max_len=100):
    tokens = tokenize(seed)
    result = tokens[:]
    while len(result) < max_len:
        context = result[-MAX_DYNAMIC:]
        next_tok = sample_next(model, context, temperature)
        if not next_tok or next_tok == END_TOKEN:
            break
        result.append(next_tok)
        if next_tok == ".":
            break
    return detokenize(result)

def main():
    global username, temp, max_len
    model = load_model()
    try:
        seed = input("Start with: ").strip()
        temperature = float(temp) if temp else 1.0
        max_len = int(max_len) if max_len else 100

        output = generate_chain(model, seed, temperature, max_len)
        output = output.replace("\\u", username)
        output = output.replace(END_TOKEN, "")
        output = output[output.find("Bot"):]
        output = output.replace("\\p", seed)
        print("Generated:", output)
    except Exception as e:
        print("Bye!")
        exit()

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
