import json

data = {
    "PROF_ALPHA": {
        "binary search": [
            "Initialize Low = 0, High = N-1",
            "Calculate Mid = (Low + High) // 2",
            "If Target == Mid, Return Index",
            "Else if Target < Mid, High = Mid - 1",
            "Else, Low = Mid + 1"
        ],
        "dom tree": [
            "Document Object Model represents HTML as a tree",
            "Root node is the Document object",
            "Elements are branches",
            "Attributes and Text are leaf nodes"
        ]
    }
}

with open("patterns.json", "w") as f:
    json.dump(data, f, indent=4)