"""Exact-identity recovery, as a parallel non-destructive fix.

foldcontact.py's "guided_contact_satisfaction: 1.0" is not an empirical
result. guided[j] is chosen with
max(AA, key=lambda a: (compatible(guided[i], a), -AA.index(a))), and by
construction there is always at least one amino acid in GROUP compatible
with guided[i] (its own group). The metric is defined purely as
compatible(...) == True, which the guided infiller directly optimizes --
it is guaranteed to be exactly 1.0 for every seed, every input, with zero
variance, because it isn't measuring inference, it's re-evaluating the same
predicate the guided method already satisfies by definition.

This module replaces "is the pick compatible" with "did the pick match the
true (pre-masking) residue identity" -- a metric the guided method cannot
trivially guarantee, since narrowing to a compatible group of up to 4 amino
acids still leaves real uncertainty about which one was actually there.
"""
import json
import random

from foldcontact import AA, GROUP, compatible


def run(seed=11):
    rng = random.Random(seed)
    length, trials = 48, 120
    contacts = [(i, length - 1 - i) for i in range(10, 22)]
    naive_id = guided_id = total = 0
    for _ in range(trials):
        seq = [rng.choice(AA) for _ in range(length)]
        for i, j in contacts:
            seq[j] = rng.choice([a for a in AA if compatible(seq[i], a)])
        true_seq = seq[:]
        naive = seq[:]
        guided = seq[:]
        for i, j in contacts:
            naive[j] = rng.choice(AA)
            guided[j] = max(AA, key=lambda a: (compatible(guided[i], a), -AA.index(a)))
            naive_id += naive[j] == true_seq[j]
            guided_id += guided[j] == true_seq[j]
            total += 1
    n, g = naive_id / total, guided_id / total
    return {
        "naive_identity_recovery": round(n, 3),
        "guided_identity_recovery": round(g, 3),
        "identity_recovery_gain_pct": round(100 * (g - n), 1),
        "contacts_evaluated": total,
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
