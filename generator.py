import secrets
import string

AMBIGUOUS = "Il1O0"
SYMBOLS = "!@#$%^&*()-_=+[]{};:,.?"

def generate_password(length=16, upper=True, digits=True,
                      symbols=True, avoid_ambiguous=False):
    if length < 8:
        raise ValueError("Password length must be at least 8")

    pools = [string.ascii_lowercase]
    if upper:
        pools.append(string.ascii_uppercase)
    if digits:
        pools.append(string.digits)
    if symbols:
        pools.append(SYMBOLS)

    if avoid_ambiguous:
        pools = ["".join(c for c in p if c not in AMBIGUOUS) for p in pools]

    # One guaranteed character from each pool
    chars = [secrets.choice(pool) for pool in pools]

    # Fill the remainder from the combined pool
    combined = "".join(pools)
    chars += [secrets.choice(combined) for _ in range(length - len(chars))]

    # Shuffle so the guaranteed characters aren't always at the start
    secrets.SystemRandom().shuffle(chars)
    return "".join(chars)

if __name__ == "__main__":
    print(generate_password())