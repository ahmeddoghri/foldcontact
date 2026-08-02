"""Compare the tautological compatibility metric to genuine identity recovery
across many seeds, showing the compatibility metric never moves (always
exactly 1.0) while identity recovery is a real, varying quantity."""
import json

import foldcontact
import foldcontact_v2
from adversarial import HOLDOUT_SEEDS, TUNING_SEEDS


def summarize(seeds):
    compat = [foldcontact.run(seed=seed)["guided_contact_satisfaction"] for seed in seeds]
    identity = [foldcontact_v2.run(seed=seed)["guided_identity_recovery"] for seed in seeds]
    naive_identity = [foldcontact_v2.run(seed=seed)["naive_identity_recovery"] for seed in seeds]
    return {
        "n": len(seeds),
        "compat_metric_min": min(compat),
        "compat_metric_max": max(compat),
        "guided_identity_mean": round(sum(identity) / len(seeds), 3),
        "guided_identity_min": round(min(identity), 3),
        "naive_identity_mean": round(sum(naive_identity) / len(seeds), 3),
    }


def main():
    print("foldcontact eval_v2: tautological compatibility metric vs. genuine identity recovery")
    for label, seeds in (("tuning", TUNING_SEEDS), ("holdout", HOLDOUT_SEEDS)):
        print(f"\n{label} ({len(seeds)} seeds):")
        print(json.dumps(summarize(seeds), indent=2))


if __name__ == "__main__":
    main()
