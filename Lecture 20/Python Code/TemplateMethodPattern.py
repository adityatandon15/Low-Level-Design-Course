from abc import ABC, abstractmethod


# ───────────────────────────────────────────────────────────
# 1. Base class defining the template method
# ───────────────────────────────────────────────────────────
class ModelTrainer(ABC):
    # The template method — final so subclasses can’t change the sequence
    def trainPipeline(self, dataPath):
        self.loadData(dataPath)
        self.preprocessData()
        self.trainModel()      # subclass-specific
        self.evaluateModel()   # subclass-specific
        self.saveModel()       # subclass-specific or default

    def loadData(self, path):
        print("[Common] Loading dataset from " + path)
        # e.g., read CSV, images, etc.

    def preprocessData(self):
        print("[Common] Splitting into train/test and normalizing")

    @abstractmethod
    def trainModel(self):
        pass

    @abstractmethod
    def evaluateModel(self):
        pass

    # Provide a default save, but subclasses can override if needed
    def saveModel(self):
        print("[Common] Saving model to disk as default format")


# ───────────────────────────────────────────────────────────
# 2. Concrete subclass: Neural Network
# ───────────────────────────────────────────────────────────
class NeuralNetworkTrainer(ModelTrainer):
    def trainModel(self):
        print("[NeuralNet] Training Neural Network for 100 epochs")
        # pseudo-code: forward/backward passes, gradient descent...

    def evaluateModel(self):
        print("[NeuralNet] Evaluating accuracy and loss on validation set")

    def saveModel(self):
        print("[NeuralNet] Serializing network weights to .h5 file")


# ───────────────────────────────────────────────────────────
# 3. Concrete subclass: Decision Tree
# ───────────────────────────────────────────────────────────
class DecisionTreeTrainer(ModelTrainer):
    # Use the default preprocessData() (train/test split + normalize)

    def trainModel(self):
        print("[DecisionTree] Building decision tree with max_depth=5")
        # pseudo-code: recursive splitting on features...

    def evaluateModel(self):
        print("[DecisionTree] Computing classification report (precision/recall)")
    # use the default saveModel()


# ───────────────────────────────────────────────────────────
# 4. Usage
# ───────────────────────────────────────────────────────────
class TemplateMethodPattern:
    @staticmethod
    def main(args):
        print("=== Neural Network Training ===")
        nnTrainer = NeuralNetworkTrainer()
        nnTrainer.trainPipeline("data/images/")

        print("\n=== Decision Tree Training ===")
        dtTrainer = DecisionTreeTrainer()
        dtTrainer.trainPipeline("data/iris.csv")


if __name__ == "__main__":
    TemplateMethodPattern.main([])
