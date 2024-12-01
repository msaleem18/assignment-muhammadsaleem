from pydantic import BaseModel
from typing import Dict, Tuple
import matplotlib.pyplot as plt

class DataModelPR(BaseModel):
    "Datamodel for DataModelPR"
    data: Dict[float, Tuple]

class BestThresholdResponse(BaseModel):
    "Datamodel for BestThresholdResponse"
    threshold: float | None
    recall_value: float | None


class PrecissionRecallCalcs():
    """ A class to perform precision and recall calculations. 
    Attributes: 
    data (dict): A dictionary containing precision and recall data. 
    
    Methods:
    best_threshold(self, recall_threshold: float = 0.97) -> float | None:
    plot_precision_recall_curve(self) -> None:
    """
    def __init__(self, precission_recall_data: DataModelPR) -> None:
        """
        Constructor to initialize the PrecisionRecallCalcs with data.

        Parameters:
        precision_recall_data (DataModelPR): An instance of DataModelPR containing the precision and recall data.
        """

        if not isinstance(precission_recall_data, DataModelPR):
            raise Exception("Incorrect data type for precission_recall_data parameter")
        
        self.data = precission_recall_data.data


    def best_threshold(self, recall_threshold: float = 0.97) -> float | None:
        """
        Determine the best confidence score threshold that yields a recall >= recall_threshold.

        Parameters:
        recall_threshold (float): The minimum recall value to achieve. Default is 0.97.

        Returns:
        BestThresholdResponse: An instance containing the best threshold and the corresponding recall value.
        """
        if not isinstance(recall_threshold, float):
            raise Exception("Incorrect data type for recall_threshold parameter")
        
        if recall_threshold <0 or recall_threshold > 1:
            raise Exception("recall_threshold should be between 0 and 1")

        best_threshold = None
        max_recall = -1  # Initialize max recall to track the best recall value
        
        for threshold, (tp, tn, fp, fn) in sorted(self.data.items(), reverse=True):
            total_pos = tp + fn  # Precompute the denominator for recall

            # Calculate recall
            recall = tp / total_pos if total_pos > 0 else 0
            
            if recall >= recall_threshold:
                if recall > max_recall:  # Track the highest recall
                    best_threshold = threshold
                    max_recall = recall
        
        return BestThresholdResponse(threshold=best_threshold, recall_value=max_recall)

    def plot_precision_recall_curve(self) -> None:
        """
        Plot the precision-recall curve based on the provided data.

        Parameters:
        None

        Returns:
        None
        """
        thresholds = []
        precisions = []
        recalls = []
        
        for threshold, (tp, tn, fp, fn) in sorted(self.data.items()):
            precision = tp / (tp + fp) if (tp + fp) > 0 else 0
            recall = tp / (tp + fn) if (tp + fn) > 0 else 0
            
            thresholds.append(threshold)
            precisions.append(precision)
            recalls.append(recall)
        
        # Print the precision-recall values
        #print(f"{'Threshold':<10}{'Precision':<10}{'Recall':<10}")
        #for t, p, r in zip(thresholds, precisions, recalls):
        #    print(f"{t:<10}{p:<10.2f}{r:<10.2f}")

        # Plot the precision-recall curve
        plt.figure(figsize=(10, 6))
        plt.plot(thresholds, precisions, marker='o', label='Precision')
        plt.plot(thresholds, recalls, marker='x', label='Recall')
        plt.xlabel('Threshold')
        plt.ylabel('Score')
        plt.title('Precision-Recall Curve')
        plt.legend()
        plt.grid(True)
        plt.show()
