import os
import pytest

# some_file.py
#import sys
# caution: path[0] is reserved for script path (or '' in REPL)
#sys.path.append(str(app_path))

from app.question1.q1_binary_classification import DataModelPR, PrecissionRecallCalcs

# Test data
test_data = {
    0.1: (50, 30, 10, 10),
    0.2: (48, 32, 8, 12),
    0.3: (46, 34, 6, 14),
    0.4: (44, 36, 4, 16),
    0.5: (42, 38, 2, 18),
    0.6: (40, 40, 0, 20),
    0.7: (38, 42, 2, 22),
    0.8: (36, 44, 4, 24),
    0.9: (34, 46, 6, 26)
}

# Mock DataModelPR instance
mock_data_model_pr = DataModelPR(data=test_data)

# Initialize PrecisionRecallCalcs with mock data
pr_calcs = PrecissionRecallCalcs(mock_data_model_pr)

def test_best_threshold():
    # Test with recall_threshold = 0.8
    response = pr_calcs.best_threshold(recall_threshold=0.8)
    print(f"Response is {response}")
    assert response.threshold == 0.1, "Expected threshold 0.1"
    assert response.recall_value == pytest.approx(0.8333, 0.01), "Expected recall value approx 0.83"
    
    # Test with recall_threshold = 0.9
    response = pr_calcs.best_threshold(recall_threshold=0.9)
    assert response.threshold is None, "Expected no threshold to meet the recall threshold of 0.9"

if __name__ == "__main__":
    pytest.main()
