# Night-light entry, rebuilt from scratch for the One Line, One Laugh bounty
# on make.fun: one short funny line, picked by scoring a dozen home-grown
# candidates against the judge's own five yardsticks, most important first.
# The yardsticks, in the order the judge weighs them, are: funny standing
# alone with no picture or setup; the laugh arriving fast inside the line;
# a fresh image instead of a stock gag; tight wording where every word
# earns its keep; and holding up on a second hearing so it repeats well.
# Each yardstick gets a mark out of five and a priority weight, and the
# line with the biggest weighted sum takes the slot; when two lines tie
# on points the shorter one wins, so the pick never depends on luck.
# A second pass tightened three of the front-runners: the speaker gag
# was cut into a setup plus a payoff with a pause between them, the
# night-light gag lost its filler verb phrase, and the headphones gag
# lost its throat-clearing lead-in, so its twist lands sooner. After
# that pass the night-light line sits on top with 64 points and wins.
# The program touches nothing outside itself: no network calls, no
# outside input, no dice rolls. It checks its own pick the way the
# sealed gate does (one line, 1 to 200 characters, plain UTF-8 text),
# writes it out, and prints a SHA-256 fingerprint of what it wrote.
import hashlib
import os
import sys
CRITERION_WEIGHTS = [4, 3, 3, 2, 2]
ENTRIES = [
    (("I asked my smart speaker ", "for a joke. It played my bank balance."), [4, 5, 4, 5, 4]),
    (("My check engine light has been on ", "so long I use it as a night light."), [4, 5, 5, 5, 4]),
    (("I bought noise-cancelling headphones ", "to finally hear myself think. Turns out I have nothing to say."), [4, 5, 4, 4, 4]),
    (("The gym charged me for a year of not going, ", "which is the most consistent exercise routine I've ever paid for."), [4, 4, 3, 4, 4]),
    (("I asked the barista for something strong ", "and she gave me her honest opinion of my life choices."), [4, 4, 4, 4, 3]),
    (("My houseplants have a group chat and ", "I'm pretty sure I'm the only topic."), [3, 4, 4, 5, 3]),
    (("I tried meal prepping once. The containers ", "are still in the fridge, now legally classified as science experiments."), [4, 3, 4, 3, 4]),
    (("I joined a book club just for the wine ", "and now I'm three novels behind on drinking."), [3, 4, 3, 4, 3]),
    (("My password is so strong even I can't get in, ", "which is great for security and terrible for everything else."), [3, 4, 3, 3, 3]),
    (("My phone's screen time report is the only ", "weekly meeting where I get told off and can't argue back."), [3, 3, 3, 4, 3]),
    (("I told the waiter the food was great, then ", "spent the whole drive home rehearsing what I actually thought."), [3, 3, 3, 3, 3]),
    (("The self-checkout accused me of stealing, ", "which is fair — I have been stealing glances at the chocolate for ten minutes."), [3, 3, 3, 2, 3])]
def weighted_points(marks):
    points = 0
    for weight, mark in zip(CRITERION_WEIGHTS, marks):
        points += weight * mark
    return points
def pick_winner(pool):
    champion_pos = -1
    champion_line = ""
    champion_points = -1
    for pos, (bits, marks) in enumerate(pool):
        line = "".join(bits)
        points = weighted_points(marks)
        if points > champion_points or (points == champion_points and len(line) < len(champion_line)):
            champion_pos = pos
            champion_line = line
            champion_points = points
    return champion_pos, champion_line, champion_points
def check_line(line):
    if len(line) < 1 or len(line) > 200:
        return "length %d sits outside 1..200 characters" % len(line)
    if line.strip() != line or line.strip() == "":
        return "entry is blank or padded with surrounding whitespace"
    if "\n" in line or "\r" in line:
        return "entry spans more than one line"
    return ""
def main():
    pos, line, points = pick_winner(ENTRIES)
    flaw = check_line(line)
    if flaw:
        print("self-check failed: %s" % flaw, file=sys.stderr)
        sys.exit(1)
    target = os.environ.get("OUTPUT_PATH", "/output/entry.txt")
    folder = os.path.dirname(target)
    if folder:
        os.makedirs(folder, exist_ok=True)
    with open(target, "w", encoding="utf-8") as handle:
        handle.write(line)
    with open(target, "r", encoding="utf-8") as handle:
        stored = handle.read()
    if stored != line:
        print("self-check failed: file on disk differs from the chosen line", file=sys.stderr)
        sys.exit(1)
    fingerprint = hashlib.sha256(line.encode("utf-8")).hexdigest()
    print(f"candidate {pos + 1} of {len(ENTRIES)}, score {points}")
    print(f"entry: {line}")
    print(f"sha256: {fingerprint}")
sys.exit(main())
