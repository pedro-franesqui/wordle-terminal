
secret = CRANE
guess  = EERIE

E E R I E
_ _ r i E

Counter:
    C 1
    R 1
    A 1
    N 1

First pass:
    - Mark greens
    - For every position not green, add counter[secret[i]] += 1
Second pass:
    - For each non-green position, if guess letter has count > 0
      mark it yellow and decrement count. Otherwise, red

counter = Counter()
result = [None] * WORD_LEN
for i in range(WORD_LEN):
    if guess[i] == secret[i]:
        result[i] = "green"
    else:
        counter[secret[i]] += 1
for i in range(WORD_LEN):
    if result[i] == "green":
        continue    # Skip greens
    if counter[guess[i]] > 0:
        result[i] = "yellow"
        counter[guess[i]] -= 1
    else:
        result[i] = "red"
