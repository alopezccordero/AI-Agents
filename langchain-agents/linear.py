# Linear regression implementation from scratch
# Author: ChatGPT
# This module implements a simple linear regression model using the normal equation.
# It does not rely on scikit-learn or other ML libraries, only numpy.

import numpy as np

class LinearRegression:
    """Simple linear regression using the normal equation.

    Parameters
    ----------
    fit_intercept : bool, default=True
        Whether to calculate the intercept for this model.
        If set to False, no intercept will be used in calculations.
    normalize : bool, default=False
        This parameter is ignored in this implementation but kept for API
        compatibility with scikit-learn's LinearRegression.
    """

    def __init__(self, fit_intercept: bool = True, normalize: bool = False):
        self.fit_intercept = fit_intercept
        self.normalize = normalize
        self.coef_ = None
        self.intercept_ = None

    def _add_intercept(self, X: np.ndarray) -> np.ndarray:
        """Add a column of ones to X for the intercept term."""
        intercept = np.ones((X.shape[0], 1))
        return np.hstack((intercept, X))

    def fit(self, X: np.ndarray, y: np.ndarray) -> "LinearRegression":
        """Fit linear model.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Training data.
        y : array-like of shape (n_samples,)
            Target values.

        Returns
        -------
        self : LinearRegression
            Fitted estimator.
        """
        X = np.asarray(X)
        y = np.asarray(y)

        if X.ndim == 1:
            X = X.reshape(-1, 1)
        if y.ndim > 1:
            y = y.ravel()

        if self.fit_intercept:
            X_b = self._add_intercept(X)
        else:
            X_b = X

        # Normal equation: theta = (X^T X)^{-1} X^T y
        try:
            theta = np.linalg.inv(X_b.T @ X_b) @ X_b.T @ y
        except np.linalg.LinAlgError:
            # In case X_b.T @ X_b is singular, use pseudo-inverse
            theta = np.linalg.pinv(X_b.T @ X_b) @ X_b.T @ y

        if self.fit_intercept:
            self.intercept_ = theta[0]
            self.coef_ = theta[1:]
        else:
            self.intercept_ = 0.0
            self.coef_ = theta
        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        """Predict using the linear model.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Samples.

        Returns
        -------
        y_pred : ndarray of shape (n_samples,)
            Returns predicted values.
        """
        X = np.asarray(X)
        if X.ndim == 1:
            X = X.reshape(-1, 1)
        if self.fit_intercept:
            X_b = self._add_intercept(X)
            return X_b @ np.concatenate(([self.intercept_], self.coef_))
        else:
            return X @ self.coef_

    def score(self, X: np.ndarray, y: np.ndarray) -> float:
        """Return the coefficient of determination R^2 of the prediction.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Test samples.
        y : array-like of shape (n_samples,)
            True values for X.

        Returns
        -------
        score : float
            R^2 of self.predict(X) wrt. y.
        """
        y_pred = self.predict(X)
        ss_res = np.sum((y - y_pred) ** 2)
        ss_tot = np.sum((y - np.mean(y)) ** 2)
        return 1 - ss_res / ss_tot

# Example usage:
# if __name__ == "__main__":
#     import matplotlib.pyplot as plt
#     X = np.random.rand(100, 1) * 10
#     y = 3.5 * X.squeeze() + 2 + np.random.randn(100) * 2
#     model = LinearRegression()
#     model.fit(X, y)
#     print("Intercept:", model.intercept_)
#     print("Coefficients:", model.coef_)
#     y_pred = model.predict(X)
#     plt.scatter(X, y, label='Data')
#     plt.plot(X, y_pred, color='red', label='Fit')
#     plt.legend()
#     plt.show()
