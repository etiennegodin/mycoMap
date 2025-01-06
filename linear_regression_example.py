import numpy as np
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt

# Generate synthetic data
np.random.seed(42)
data = np.random.randint(0, 101, size=500)  # Replace with your dataset

# Create a DataFrame with value counts
value_counts = pd.DataFrame(data, columns=["value"])
value_counts = value_counts["value"].value_counts().reset_index()
value_counts.columns = ["value", "frequency"]

# Sort by value
value_counts = value_counts.sort_values("value")

# Features (X) and target (y)
X = value_counts["value"].values
y = value_counts["frequency"].values


# Add a constant term for the intercept
X_with_const = sm.add_constant(X)

# Fit the linear regression model
model = sm.OLS(y, X_with_const).fit()

# Print the model summary
print(model.summary())


# Predictions
value_counts["predicted_frequency"] = model.predict(X_with_const)
print(value_counts)


# Plot the data and regression line
plt.scatter(value_counts["value"], value_counts["frequency"], color='blue', label='Actual data')
plt.plot(value_counts["value"], value_counts["predicted_frequency"], color='red', label='Regression line')
plt.xlabel('Value')
plt.ylabel('Frequency')
plt.title('Linear Regression: Value vs Frequency')
plt.legend()
plt.show()

'''
# Predict likelihood for a new value
new_value = 42
new_value_with_const = sm.add_constant([new_value])
predicted_frequency = model.predict(new_value_with_const)
print(f"Predicted frequency for value {new_value}: {predicted_frequency[0]:.2f}")

'''