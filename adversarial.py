"""Adversarial seeds for the identity-recovery metric.

TUNING_SEEDS: used to characterize foldcontact_v2's exact-identity recovery.
HOLDOUT_SEEDS: disjoint, evaluated exactly once after the fix was finalized.

Unlike foldcontact.py's guided_contact_satisfaction (mathematically
guaranteed to equal 1.0 for every seed -- see the module docstring in
foldcontact_v2.py), identity recovery has genuine variance: it is a real
empirical quantity, not a tautology, so it is worth checking across many
seeds rather than trusting a single one.
"""

TUNING_SEEDS = list(range(1, 41))
HOLDOUT_SEEDS = list(range(1000, 1025))
