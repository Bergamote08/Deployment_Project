import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import  OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from joblib import dump, load


# Load your dataset and perform feature engineering
pricing_data = pd.read_csv("https://full-stack-assets.s3.eu-west-3.amazonaws.com/Deployment/get_around_pricing_project.csv")

# Split your data into features (X) and target (y)
target_name = 'rental_price_per_day'
Y = pricing_data.loc[:,target_name]
X = pricing_data.drop(target_name, axis = 1)

# Automatically detect names of numeric/categorical columns
numeric_features = []
categorical_features = []
for i,t in X.dtypes.items():
    if ('float' in str(t)) or ('int' in str(t)) :
        numeric_features.append(i)
    else :
        categorical_features.append(i)

# Create pipeline for categorical features
categorical_transformer = Pipeline(
    steps=[
    ('encoder', OneHotEncoder(handle_unknown='ignore'))
    ])

# Create pipeline for numeric features
numeric_transformer = Pipeline(steps=[
    ('scaler', StandardScaler())
])

# Use ColumnTransformer to make a preprocessor object that describes all the treatments to be done
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features)
    ])

# Split your data into training and testing sets
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

# Preprocessings on train set
X_train = preprocessor.fit_transform(X_train)

# Preprocessings on test set
X_test = preprocessor.transform(X_test)

model = RandomForestRegressor(max_depth = 10, min_samples_leaf = 2, min_samples_split = 8, n_estimators = 40)

# Train the model
model.fit(X_train, Y_train)

# Make predictions on the test data
y_pred = model.predict(X_test)

# Export model in joblib
dump(model, "model.joblib")

#Export prepocessor in joblib
dump(preprocessor, "preprocessor.joblib")