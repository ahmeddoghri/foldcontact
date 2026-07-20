import json, random

GROUP = {"A":0,"V":0,"L":0,"I":0,"D":1,"E":1,"K":1,"R":1,"S":2,"T":2,"N":2,"Q":2}
AA = tuple(GROUP)

def compatible(a, b):
    return GROUP[a] == GROUP[b] or {GROUP[a], GROUP[b]} == {1}

def run(seed=11):
    rng = random.Random(seed)
    length, trials = 48, 120
    contacts = [(i, length-1-i) for i in range(10, 22)]
    naive_ok = guided_ok = total = 0
    for _ in range(trials):
        seq = [rng.choice(AA) for _ in range(length)]
        for i, j in contacts:
            seq[j] = rng.choice([a for a in AA if compatible(seq[i], a)])
        masked = {j for _, j in contacts}
        naive = seq[:]
        guided = seq[:]
        for i, j in contacts:
            naive[j] = rng.choice(AA)
            guided[j] = max(AA, key=lambda a: (compatible(guided[i], a), -AA.index(a)))
            naive_ok += compatible(naive[i], naive[j])
            guided_ok += compatible(guided[i], guided[j])
            total += 1
    n, g = naive_ok/total, guided_ok/total
    return {"naive_contact_satisfaction":round(n,3), "guided_contact_satisfaction":round(g,3),
            "contact_gain_pct":round(100*(g-n),1), "contacts_evaluated":total}

if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
