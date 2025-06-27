#!/usr/bin/env python3

import json

model = {}

# All 1-digit to 3-digit a + b = c
for a in range(1000):
    for b in range(1000):
        expr = f"{a}+{b}="
        result = str(a + b) + "."
        model[expr] = result

# Save it
with open("logic_model.json", "w") as f:
    json.dump(model, f)

print("Training complete. logic_model.json saved.")
