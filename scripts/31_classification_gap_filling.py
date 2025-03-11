import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report

# 1. Read Excel file
df = pd.read_excel("Community_Profile_Report_GT_Class.xlsx")

# 2. Define feature columns and target column
feature_cols = [
    "cases",
    "FIPS code",
    "County",
    "State Abbreviation",
    "Daily cases last week",
    "Cases per 100k daily.1",
    "Number of days of downward case trajectory"
]
target_col = "Area of Concern Category"

# 3. Subset DataFrame to relevant columns
df = df[feature_cols + [target_col]].copy()
df.dropna(subset=feature_cols, inplace=True)

# 4. Separate labeled and unlabeled data
labeled_df = df[df[target_col].notnull()].copy()
unlabeled_df = df[df[target_col].isnull()].copy()

print("Labeled data shape:", labeled_df.shape)
print("Unlabeled data shape:", unlabeled_df.shape)

# 5. Further split the labeled data into training and testing sets for evaluation
X_labeled = labeled_df[feature_cols]
y_labeled = labeled_df[target_col]
X_train, X_test, y_train, y_test = train_test_split(
    X_labeled,
    y_labeled,
    test_size=0.2,
    random_state=42,
    stratify=y_labeled
)

# 6. Define numeric and categorical features
numeric_features = [
    "cases",
    "FIPS code",
    "Daily cases last week",
    "Cases per 100k daily.1",
    "Number of days of downward case trajectory"
]
categorical_features = [
    "County",
    "State Abbreviation"
]

# 7. Build preprocessing and modeling pipeline
preprocessor = ColumnTransformer(
    transformers=[
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features),
        ("num", "passthrough", numeric_features)
    ]
)

model_pipeline = Pipeline([
    ("preprocessing", preprocessor),
    ("classifier", RandomForestClassifier(random_state=42))
])

# 8. Define parameter grid for GridSearchCV
param_grid = {
    "classifier__n_estimators": [50, 100, 200],
    "classifier__max_depth": [None, 5, 10],
}

grid_search = GridSearchCV(
    model_pipeline,
    param_grid,
    cv=3,
    n_jobs=-1,
    verbose=1
)

# 9. Train the model on the training set
grid_search.fit(X_train, y_train)

print("Best parameters:", grid_search.best_params_)
print("Best cross-validation score:", grid_search.best_score_)

best_model = grid_search.best_estimator_

# 10. Evaluate the best model on the labeled test set
y_pred_test = best_model.predict(X_test)
print("\nClassification Report on Labeled Test Data:")
print(classification_report(y_test, y_pred_test))

# 11. Predict the missing labels for the unseen (unlabeled) data
if not unlabeled_df.empty:
    X_unlabeled = unlabeled_df[feature_cols]
    predicted_labels = best_model.predict(X_unlabeled)
    # Update the unlabeled DataFrame with predictions
    unlabeled_df[target_col] = predicted_labels
    # Merge predictions back into the original DataFrame
    df.loc[df[target_col].isnull(), target_col] = predicted_labels
else:
    print("No unlabeled data to predict.")

# 12. Write the updated DataFrame with predictions to a new Excel file
output_file = "Community_Profile_Report_GT_Class_predictions.xlsx"
df.to_excel(output_file, index=False)
print(f"\nUpdated Excel file saved as: {output_file}")
