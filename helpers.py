"""
Helper functions for assessing ML models performance.
"""

import numpy as np
from sklearn.metrics import (
    make_scorer,
    f1_score,
    recall_score,
    precision_score,
    accuracy_score,
)
from sklearn.model_selection import KFold, cross_validate


def report_model_cv_metrics(model, X, y):
    """
    Return the accuracy, recall, precision, F1 from CV for a model.

    Performs a 10-fold cross-validation then averages model metrics.

    Args:
        model: The classification ML model.
        X: The features of the model.
        y: The target of the model.
    """
    kf = KFold(n_splits=10, shuffle=True, random_state=13)

    scoring = {
        "f1_score": make_scorer(f1_score, zero_division=1),
        "recall_score": make_scorer(recall_score, zero_division=1),
        "precision_score": make_scorer(precision_score, zero_division=1),
        "accuracy_score": make_scorer(accuracy_score),
    }
    cv_metrics = cross_validate(model, X, y, cv=kf, scoring=scoring)

    accuracy = np.mean(cv_metrics["test_accuracy_score"])
    recall = np.mean(cv_metrics["test_recall_score"])
    precision = np.mean(cv_metrics["test_precision_score"])
    f1 = np.mean(cv_metrics["test_f1_score"])

    metrics = f"Accuracy: {accuracy:.1%}\nRecall: {recall:.1%}\nPrecision: {precision:.1%}\nF1: {f1:.1%}"
    return metrics


def report_oversampling_model_cv_metrics(model, X, y, sampling_model):
    """
    Return the accuracy, recall, precision, F1 from CV for a model that utilizes oversampling.

    Performs a 10-fold cross-validation then averages model metrics.

    Args:
        model: The classification ML model.
        X: The features of the model.
        y: The target of the model.
        sampling_strategy: degree to adjust the sample (1=even split).
    """
    kf = KFold(n_splits=10, shuffle=True, random_state=13)

    percent_breakdown, accuracy, recall, precision, f1 = [], [], [], [], []

    for fold, (train_index, validate_index) in enumerate(kf.split(X), 1):
        # Different data types entered sometimes.
        if type(X) == np.ndarray:
            X_train = X[train_index]
            X_validate = X[validate_index]
        else:
            X_train = X.iloc[train_index]
            X_validate = X.iloc[validate_index]
        y_train = y.iloc[train_index]
        y_validate = y.iloc[validate_index]

        X_train_oversampled, y_train_oversampled = sampling_model.fit_resample(
            X_train, y_train
        )
        model.fit(X_train_oversampled, y_train_oversampled)
        y_predicted = model.predict(X_validate)

        percent_of_ones = len(y_train_oversampled[y_train_oversampled == 1]) / len(
            y_train_oversampled
        )
        percent_breakdown.append(percent_of_ones)
        accuracy.append(accuracy_score(y_validate, y_predicted))
        recall.append(recall_score(y_validate, y_predicted, zero_division=1))
        precision.append(precision_score(y_validate, y_predicted, zero_division=1))
        f1.append(f1_score(y_validate, y_predicted, zero_division=1))

    metrics = f"NEW percentage of 1's: {np.mean(percent_breakdown):.1%}"
    metrics += f"\nAccuracy: {np.mean(accuracy):.1%}\nRecall: {np.mean(recall):.1%}"
    metrics += f"\nPrecision: {np.mean(precision):.1%}\nF1: {np.mean(f1):.1%}"
    return metrics
