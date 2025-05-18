def precision(true_positives:float, false_positives:float) -> float:
    return true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0.0

def recall(true_positives:float, false_negatives:float) -> float:
    return true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0.0

def f1_score(precision:float, recall:float) -> float:
    return 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0