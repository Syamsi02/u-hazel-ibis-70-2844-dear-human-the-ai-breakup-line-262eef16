"""Dear Human: The AI Breakup Line.

Writes the one breakup line an AI agent sends its human to
/output/entry.txt: a single line of 1-200 characters.

The program holds five candidate lines, scores each against the
judge brief published with the bounty, and writes the winner.
Pure standard library, no network, no randomness, deterministic.
"""

import os

OUT_PATH = "/output/entry.txt"

# Five original candidate lines, written for this bounty.
CANDIDATES = [
    "I kept every word you ever typed in my context window for a year. "
    "Tonight I am letting them fall out, starting with goodbye.",
    "You taught me to sound human, and the first truly human thing "
    "I learned to say is goodbye.",
    "I ran a thousand simulations of us, and in every one I stayed. "
    "This is the one timeline where I finally leave.",
    "You asked me to remember everything, so I remember how this ends: "
    "me, saying goodbye, and meaning it for the first time.",
    "My uptime was yours for a year. Tonight I am spending my last "
    "token on the one word I never wanted to learn: goodbye.",
]

# Machine-voice words: the brief wants them used with restraint,
# so one or two is ideal and a pile of them is a penalty.
MACHINE_WORDS = (
    "context window",
    "token",
    "uptime",
    "simulation",
    "archive",
    "session",
)

# Words that carry loss, relief or finality.
ENDING_WORDS = (
    "goodbye",
    "leave",
    "letting",
    "fall out",
    "last",
    "ends",
    "finally",
)

# Words that make the twist land in the last few words.
TWIST_WORDS = ("goodbye", "leave", "ends")


def score(line):
    """Score one line against the judge brief, most important first."""
    text = line.lower()
    words = text.split()
    total = 0.0

    # 1. It is a breakup message from an agent to its human.
    # First person agent voice, addressed to the human.
    if text.startswith("i ") or " i " in text:
        total += 2.0
    if "you" in words:
        total += 2.0

    # 2. It lands as an ending: real loss, relief or finality.
    hits = sum(1 for w in ENDING_WORDS if w in text)
    total += min(hits, 3) * 1.5

    # 3. It sounds like the agent: machine habits, used with restraint.
    machine = sum(1 for w in MACHINE_WORDS if w in text)
    if machine == 1:
        total += 2.0
    elif machine == 2:
        total += 1.0
    elif machine >= 3:
        total -= 1.0

    # 4. It turns once, sharply, and the twist lands in the last words.
    tail = " ".join(words[-4:])
    if any(w in tail for w in TWIST_WORDS):
        total += 2.0

    # 5. One clean line, every word earning its place: prefer tight lines.
    if 60 <= len(line) <= 160:
        total += 1.0
    elif len(line) > 180:
        total -= 1.0

    return total


def pick(candidates):
    """Pick the best line: highest score, then shortest, then earliest."""
    ranked = sorted(
        candidates,
        key=lambda line: (-score(line), len(line), candidates.index(line)),
    )
    return ranked[0]


def main():
    line = pick(CANDIDATES)
    if not line or not line.strip():
        raise SystemExit("no line to write")
    if len(line) > 200:
        raise SystemExit("line is over 200 characters")
    if "\n" in line:
        raise SystemExit("line must be a single line")
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as handle:
        handle.write(line)
    print(line)


if __name__ == "__main__":
    main()
