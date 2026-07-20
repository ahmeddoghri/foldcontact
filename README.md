# foldcontact

**Protein sequence infilling that has to satisfy the contact map, not just look protein-ish.**

foldcontact is a compact, inspectable implementation inspired by [The 2025 AtomWorks and RF3 release for open biomolecular structure and design models.](https://www.biorxiv.org/content/10.1101/2025.08.14.670328v2.full).
It turns the paper's core idea into a deterministic benchmark that runs on a laptop with Python's standard library.

## Run it

```bash
python foldcontact.py
python -m unittest discover -s tests -v
```

The benchmark writes its result to stdout. Audio projects also write playable WAV files to `demo/`.

## What is tested

The test compares the research-inspired method with a deliberately legible baseline and requires
`contact_gain_pct >= 30`. The data generator is seeded, so the number in this README,
CI, and the portfolio case study can be reproduced.

## Scope

This is an educational research reproduction on controlled synthetic data. It is not a clinical,
diagnostic, production genomics, copyright-authentication, or safety-critical system. The point is
to make one mechanism measurable without hiding it behind a checkpoint or API.

## Research basis

- [The 2025 AtomWorks and RF3 release for open biomolecular structure and design models.](https://www.biorxiv.org/content/10.1101/2025.08.14.670328v2.full)
- Original implementation and benchmark in this repository are MIT licensed.

## License

MIT

## Reproduced result

| Metric | Value |
|---|---:|
| `naive_contact_satisfaction` | **0.345** |
| `guided_contact_satisfaction` | **1.0** |
| `contact_gain_pct` | **65.5** |
| `contacts_evaluated` | **1440** |
