def precision(true_positives, false_positives):
    return true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0

def recall(true_positives, false_negatives):
    return true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0

def f1_score(precision, recall):
    return 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0