import json
import random

with open("webdjango/shop/fixtures/fashions.json") as f:
    fashions = json.load(f)

for fashion in fashions:
    fashion["fields"]["price"] = random.randint(10, 500) * 1000

with open("webdjango/shop/fixtures/fashions.json", "w") as f:
    json.dump(fashions, f, indent=4)
