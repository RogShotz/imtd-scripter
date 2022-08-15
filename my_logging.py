import json

def log_add(name: str):
    stats = None
    with open(r"stats.json", 'r') as f:
        stats = json.load(f)

    stats["total"][name] += 1

    with open('stats.json', 'w') as f:
        json.dump(stats, f, indent=4)

def log_get(name: str):
    stats = None
    with open(r"stats.json", 'r') as f:
        stats = json.load(f)

    return stats["total"][name]