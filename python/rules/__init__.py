"""Validation rules: ONE FILE PER RULE, so teammates never edit the same file.

Each rule file in this folder defines:

    CODE  = "R2"            the reason code written to data/reject.dat
    ORDER = 20              rules run from the lowest ORDER to the highest
    def ok(line) -> bool    True if the 26-character record passes this rule

To add a rule, add a new file here. Nothing else needs to change.
A rule that crashes counts as a failure, so one bug never stops the whole job.
"""
import importlib
import pkgutil

_RULES = None


def load_rules():
    global _RULES
    if _RULES is None:
        found = []
        for info in pkgutil.iter_modules(__path__):
            module = importlib.import_module(f"{__name__}.{info.name}")
            if hasattr(module, "CODE") and hasattr(module, "ok"):
                found.append(module)
        _RULES = sorted(found, key=lambda m: (getattr(m, "ORDER", 50), m.CODE))
    return _RULES


def check(line):
    """Return the reason code of the first rule the record fails, or None if it is valid."""
    for rule in load_rules():
        try:
            passed = rule.ok(line)
        except Exception:
            passed = False
        if not passed:
            return rule.CODE
    return None
