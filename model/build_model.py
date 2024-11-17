import pandas as pd
import joblib
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

#inspired by code from: https://www.datacamp.com/tutorial/guide-to-the-gradient-boosting-algorithm


def load_data(file_path):
    df = pd.read_csv(file_path)
    return df


def main():
    data_file = 'model/F1_Final_Table_with_RaceName.csv'
    features = ['air_temperature', 'circuit_short_name', 'humidity', 'pressure', 'track_temperature', 'wind_direction', 'wind_speed']
    target_var = 'compound'
    df = load_data(data_file)
    X = df[features]
    y = df[target_var]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25
    )

    # Define categorical and numerical features
    categorical_features = X.select_dtypes(
        include=["object"]
    ).columns.tolist()

    numerical_features = X.select_dtypes(
        include=["float64", "int64"]
    ).columns.tolist()

    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(), categorical_features),
            ("num", StandardScaler(), numerical_features),
        ]
    )

    model = Pipeline(
        [
            ("preprocessor", preprocessor),
            ("classifier", GradientBoostingClassifier()),
        ]
    )

    # Perform 5-fold cross-validation
    cv_scores = cross_val_score(model, X_train, y_train, cv=5)

    # Fit the model on the training data
    model.fit(X_train, y_train)

    # Predict on the test set
    y_pred = model.predict(X_test)

    # Generate classification report
    report = classification_report(y_test, y_pred)
    print(f"Mean Cross-Validation Accuracy: {cv_scores.mean():.4f}")
    print("\nClassification Report:")
    print(report)

    # predict single value
    

    #Save model
    joblib.dump(model, 'model/dva_project.model')

if __name__ == '__main__':
    main()
