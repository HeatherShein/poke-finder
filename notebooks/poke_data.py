# %%
# Imports
import re
import pandas as pd

# %%
# Load dataset
df = pd.read_csv("../data/sinnoh/routes/route-210.csv")


# %%
# Refine names
def clean_names(row):
    # Remove extra character
    if row["name"][-1] == "-":
        n = len(row["name"])
        row["name"] = row["name"][: n - 1]
    # Find versions
    version = re.search("(DE|PS)$", row["name"])
    if version:
        # Update version
        row["version"] = version.group()
        n = len(row["name"])
        # Clean name
        row["name"] = row["name"][: n - 2]
    return row


df = df.apply(clean_names, axis=1)

# %%
# Explore
names = df.head().name.values
names

# %%
# Test
df

# %%
# Refine probability
df.head().probability.values

# %%
# Test
txt = df[df.index == 1].probability.values[0]
probability = re.findall("[0-9]+%", txt)
probability_type = re.split("[0-9]+%", txt)[1:]
for i in range(len(probability)):
    probability[i] = int(probability[i][:-1])
probability, probability_type


# %%
# Clean probabilities
def clean_prob(row):
    p_version = False
    txt = row["probability"]
    probabilities, probability_types = (
        re.findall("[0-9]+%", txt),
        re.split("[0-9]+%", txt)[1:],
    )
    for i in range(len(probabilities)):
        probabilities[i] = int(probabilities[i][:-1])
    if len(probabilities) > 1:
        for i in range(len(probabilities)):
            if "DE" in probability_types[i] or "PS" in probability_types[i]:
                p_version = True
        if p_version:
            for i in range(len(probabilities)):
                for v in ["DE", "PS"]:
                    if v in probability_types[i]:
                        row["probability_" + v] = int(probabilities[i])
            row["probability_M"] = -1
            row["probability_J"] = -1
            row["probability_N"] = -1
        else:
            for i in range(len(probabilities)):
                for x in ["M", "J", "N"]:
                    if x in probability_types[i]:
                        row["probability_" + x] = int(probabilities[i])
            row["probability_DE"] = -1
            row["probability_PS"] = -1
    else:
        for x in ["M", "J", "N", "DE", "PS"]:
            row["probability_" + x] = probabilities[0]
    return row


df = df.apply(clean_prob, axis=1)
del df["probability"]

# %%
# Test
df
