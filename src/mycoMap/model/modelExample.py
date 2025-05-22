import pandas as pd 

"""

Negative Binomial Regression: More flexible, allows variance > mean (overdispersion), common in ecology.
Zero-Inflated Models (ZIP/ZINB): Useful if you have far more zero-richness cells than expected. They model the zero-generating process separately from the count-generating process.
"""

"""
Robustness of Tree Models: Often, tree-based ensemble models like Random Forest handle count-like data quite well without explicitly assuming a distribution, making them a good default choice.
"""

# bias covariate 

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder, OrdinalEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer

bias_layers = pd.read_csv('data/interim/geodata/vector/bias/csv/combinedBiases.csv')

df = pd.read_csv('data/interim/geodata/vector/allIntegratedData/allIntegratedData.csv')



# --- Step 2: Preprocessing ---

# Define features (X) and target (y)
X = df.drop(['FID', 'fungi_richness', 'fungi_shannon', 'item_count'], axis=1)
y = df['fungi_richness']

numerical_features = ['cl_age_et','hauteur','tree_diver','tree_shann', 'cl_dens','cl_haut','cl_pent','cl_drai']

#add all bioclims
for i in range(1,20):
    i = "{:02}".format(i)
    numerical_features.append(f'bioclim_{i}')

ordered_features = ['cl_dens','cl_haut','cl_pent','cl_drai']

categorical_features = ['ty_couv_et','etagement','dep_sur']

# Split data BEFORE preprocessing to avoid data leakage from test set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create preprocessing pipelines for each column type
# Add imputation if you have missing values, e.g., SimpleImputer(strategy='mean')
numerical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')), # Example imputation
    ('scaler', StandardScaler())
])

categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')), # Example imputation
    # handle_unknown='ignore' will create all-zero columns for unknown categories in test data
    ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
])

# Combine preprocessing steps using ColumnTransformer
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numerical_transformer, numerical_features),
        ('cat', categorical_transformer, categorical_features)
    ],
    remainder='passthrough' # Keep other columns (if any) - usually 'drop' is safer
)

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score, root_mean_squared_error
from sklearn.model_selection import cross_val_score

model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1) # Example model

# Create the full pipeline
full_pipeline = Pipeline(steps=[('preprocessor', preprocessor),
                              ('regressor', model)])


# Train the model
print("Training the model...")
full_pipeline.fit(X_train, y_train)

# Make predictions on the test set
y_pred = full_pipeline.predict(X_test)

# Evaluate the model
mae = mean_absolute_error(y_test, y_pred)
rmse = root_mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("\n--- Model Evaluation ---")
print(f"Test Set MAE: {mae:.2f}")
print(f"Test Set RMSE: {rmse:.2f}")
print(f"Test Set R-squared: {r2:.3f}")


#cv_scores = cross_val_score(full_pipeline, X, y, cv=5, scoring='neg_mean_absolute_error')
#print(f"\nCross-Validation MAE: {-cv_scores.mean():.2f} (+/- {cv_scores.std() * 2:.2f})")

import shap
import matplotlib.pyplot as plt
# Install shap if you don't have it: pip install shap
# import shap

# --- Step 5: Interpretation (Example for Random Forest) ---

# Get feature names after preprocessing (can be tricky with OneHotEncoder)
# Easier way: access feature names from the fitted ColumnTransformer
feature_names_out = full_pipeline.named_steps['preprocessor'].get_feature_names_out()

importances = full_pipeline.named_steps['regressor'].feature_importances_
feature_importance_df = pd.DataFrame({'feature': feature_names_out, 'importance': importances})
feature_importance_df = feature_importance_df.sort_values('importance', ascending=False)

print("\n--- Feature Importances ---")
print(feature_importance_df.head(10))

# Plotting (simple example)
plt.figure(figsize=(10, 6))
plt.barh(feature_importance_df['feature'].head(10), feature_importance_df['importance'].head(10))
plt.xlabel("Feature Importance")
plt.ylabel("Feature")
plt.gca().invert_yaxis()
plt.title("Top 10 Feature Importances")
plt.show()

"""
#SHAP analysis (more involved, requires fitting explainer on processed data)
explainer = shap.TreeExplainer(full_pipeline.named_steps['regressor'])
X_train_processed = full_pipeline.named_steps['preprocessor'].transform(X_train)
shap_values = explainer.shap_values(X_train_processed)
shap.summary_plot(shap_values, X_train_processed, feature_names=feature_names_out)

"""
