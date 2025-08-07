from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import pandas as pd


def load_data(test_size=0.2, random_state=42, add_features=False):

    iris = load_iris()
    X = pd.DataFrame(iris.data, columns=iris.feature_names)
    y = iris.target

    if add_features:
        # New feature: Petal Area
        X["petal_area"] = X["petal length (cm)"] * X["petal width (cm)"]

        # New feature: Sepal-to-Petal Length Ratio
        X["sepal_to_petal_length_ratio"] = (
            X["sepal length (cm)"] / X["petal length (cm)"]
        )

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, stratify=y, random_state=random_state
    )

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    return X_train_scaled, X_test_scaled, y_train, y_test
