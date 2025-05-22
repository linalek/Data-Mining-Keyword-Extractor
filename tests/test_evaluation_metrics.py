from src.evaluation_metrics import precision, recall, f1_score

# --------------------------- Helper to display test results ---------------------------

def display_metrics(tp, fp, fn):
    print(f"\nTrue Positives: {tp}, False Positives: {fp}, False Negatives: {fn}")

    p = precision(tp, fp)
    r = recall(tp, fn)
    f1 = f1_score(p, r)

    print(f"Precision: {p:.4f}")
    print(f"Recall: {r:.4f}")
    print(f"F1-Score: {f1:.4f}")

# --------------------------- Run test cases ---------------------------

def run_tests():
    test_cases = [
        {"tp": 10, "fp": 2, "fn": 3},
        {"tp": 0, "fp": 5, "fn": 5},
        {"tp": 5, "fp": 0, "fn": 0},
        {"tp": 0, "fp": 0, "fn": 0},  # edge case
        {"tp": 20, "fp": 10, "fn": 5},
    ]

    for case in test_cases:
        display_metrics(case["tp"], case["fp"], case["fn"])

# --------------------------- Execute ---------------------------

if __name__ == "__main__":
    run_tests()
