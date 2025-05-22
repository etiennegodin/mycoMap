from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import RobustScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.decomposition import PCA
from sklearn.metrics import accuracy_score, classification_report
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import cross_val_score

import geopandas as gpd
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# --- Step 1: Load Data ---

df = pd.read_csv('data/interim/geodata/vector/preprocessedData/preprocessedData.csv', index_col= 0  )
print(df.head())
print(df.shape)
# Drop train data where no species were found
model_df = df[df['fungi_richness'] != 0]
print(model_df.shape)
print(model_df.info())

# --- 3. Separate Features (X) and Target (y) ---

X = model_df.drop(['FID', 'block_id','geometry', 'fungi_richness', 'fungi_shannon'], axis=1)
y = model_df['fungi_richness']

print(X['dep_sur'].nunique() + \
                                    X['etagement'].nunique() + \
                                    X['ty_couv_et'].nunique())


# --- 4. Split Data into Training and Testing Sets ---

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# --- 5. Dynamically Identify Numerical and Categorical Features ---

numerical_features = X_train.select_dtypes(include=['int64', 'float64']).columns.tolist()
categorical_features =  X_train.select_dtypes(include=['object']).columns.tolist()


# --- 6. Define Preprocessing Steps and Create a ColumnTransformer ---

numerical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')), # Example imputation
    ('scaler', RobustScaler())
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

# --- 7. Build the Pipeline with PCA and RandomForestClassifier ---
model_pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('pca', PCA(random_state=42)), # PCA for dimensionality reduction
    ('classifier', RandomForestRegressor(random_state=42)) # Random Forest Classifier
])

print("\nFull Pipeline Structure:")
print(model_pipeline)

# --- 8. Define the Parameter Grid for GridSearchCV ---
# Get an estimate of the number of features after preprocessing for PCA n_components
# Max features = numerical features + sum of unique categories (at most)
# Here: 4 numerical + (4 unique for cat_X) + (3 unique for cat_Y) = 11 max features
# A safe upper bound for n_components integers is 11, but often much less is needed.


# Estimate total features after preprocessing
# This is crucial for selecting appropriate n_components for PCA
estimated_numerical_output_features = len(numerical_features)
estimated_categorical_output_features = sum(X_train[col].nunique() for col in categorical_features)
n_features_after_preproc_estimate = estimated_numerical_output_features + estimated_categorical_output_features

param_grid = {
    # PCA parameters
    'pca__n_components': [
        0.99, 0.95, 0.90, # Keep 99%, 95%, or 90% of variance
        min(10, n_features_after_preproc_estimate), # Try a moderate fixed number
        min(15, n_features_after_preproc_estimate), # Try a larger fixed number
        min(20, n_features_after_preproc_estimate)  # Try an even larger fixed number
    ],
    # RandomForestClassifier parameters
    'classifier__n_estimators': [50, 100],
    'classifier__max_features': ['sqrt'], # 'sqrt' is default for classification in newer scikit-learn
    'classifier__max_depth': [10, 20, None], # Max depth of trees
    'classifier__min_samples_split': [2, 5], # Minimum samples required to split a node
    'classifier__min_samples_leaf': [1, 2] # Minimum samples required at a leaf node
}

print("\nParameter Grid for GridSearchCV (including PCA and RF):")
for param, values in param_grid.items():
    print(f"  {param}: {values}")

    # --- 9. Initialize and Run GridSearchCV ---
grid_search = GridSearchCV(
    estimator=model_pipeline,
    param_grid=param_grid,
    cv=3,                 # Reduced CV folds for faster execution during example
    scoring='neg_mean_squared_error',   # Metric to optimize for
    n_jobs=-1,            # Use all available CPU cores
    verbose=2             # Show progress
)

print("\nStarting GridSearchCV (this may take a while depending on grid size and data)...")
grid_search.fit(X_train, y_train)
print("GridSearchCV complete.")

# --- 10. Print Best Parameters and Best Score ---
print("\n--- Best Parameters Found by GridSearchCV ---")
print(f"Best Parameters: {grid_search.best_params_}")
print(f"Best Cross-Validation Accuracy: {grid_search.best_score_:.4f}")

best_pipeline = grid_search.best_estimator_
print("\nBest Estimator (Optimized Pipeline):")
print(best_pipeline)

# --- 11. Make Predictions and Evaluate on the Test Dataset ---
print("\nMaking predictions on the Test Dataset (simulating 'other dataset')...")
y_pred_test = best_pipeline.predict(X_test)

print("\nFirst 10 predictions on the test dataset:")
print(y_pred_test[:10])

print("\n--- Evaluation of Best Model on Test Dataset ---")
mse = mean_squared_error(y_test, y_pred_test)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred_test)


# Optional: Inspect PCA details from the best model
if 'pca' in best_pipeline.named_steps:
    best_pca_step = best_pipeline.named_steps['pca']
    print(f"\nActual PCA n_components_ used in best pipeline: {best_pca_step.n_components_}")
    print(f"Total variance explained by these components: {np.sum(best_pca_step.explained_variance_ratio_):.4f}")
else:
    print("\nPCA step not found in the best pipeline (this should not happen with current setup).")



# 2. Load the new dataset for prediction

new_data_df = df[df['fungi_richness'] == 0]
X_new_data = new_data_df.drop(['FID', 'block_id','geometry', 'fungi_richness', 'fungi_shannon'], axis=1)

# Make sure the columns are in the same order as X_train for consistency (good practice)
# Although ColumnTransformer can handle reordering, explicit reordering is safer.
X_new_data = X_new_data[X_train.columns]

print(f"\nLoaded new data for prediction. Shape: {X_new_data.shape}")
print(f"Column names match training data: {list(X_new_data.columns) == list(X_train.columns)}")


# 3. Use the best_pipeline to predict on the new data
print("\n--- Making predictions on the new, unseen dataset using best_pipeline ---")
predictions_new_data = best_pipeline.predict(X_new_data)

print(f"Predictions generated for {len(predictions_new_data)} samples.")
print("First 10 predictions on new data:")
print(predictions_new_data[:10])

# You can optionally add these predictions back to your new data DataFrame
new_data_df['predicted_target'] = predictions_new_data
print("\nProduction DataFrame with predictions:")
print(new_data_df.head())


new_data_df.to_csv('data/output/modelPrediction.csv')

gdf = gpd.GeoDataFrame(new_data_df, geometry= 'geometry')
gdf.to_file('data/output/modelPrediction.shp', driver='ESRI Shapefile')
