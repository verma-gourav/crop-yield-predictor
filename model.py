import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.ensemble import RandomForestRegressor

import os
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("data/cleaned_data.csv")

# features and target
features = ["state", "district", "year", "season", "crop", "area"]
target = "yield"
df_model = df[features + [target]].copy()

#  X and y
X = df_model.drop("yield", axis=1)
y = df_model["yield"]

# categorical columns
cat_col = ["state", "district", "season", "crop"]
num_col = ["year", "area"]

# transformer: OneHot for categorical, passthrough for numeric
preprocessor = ColumnTransformer(
    transformers=[
        ("cat", OneHotEncoder(handle_unknown="ignore"), cat_col),
        ("num", "passthrough", num_col),
    ]
)

# pipeline with linear regression
pipeline = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("regressor", RandomForestRegressor(n_estimators=100, random_state=42))
])

# split and train
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
pipeline.fit(X_train, y_train)

y_pred = pipeline.predict(X_test)

# evaluation
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Mean Squared Error: {mse:.3f}")
print(f"R² Score: {r2:.3f}")


# plotting actual vs predicted yield
def plot_actual_vs_pred(y_test, y_pred, model_name):
    # Ensure plots folder exists
    os.makedirs("plots", exist_ok=True)

    plt.figure(figsize=(7, 6))
    sns.scatterplot(x=y_test, y=y_pred, alpha=0.5)
    plt.xlabel("Actual Yield")
    plt.ylabel("Predicted Yield")
    plt.title(f"Actual vs Predicted Yield ({model_name})")
    plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--')
    plt.tight_layout()
    plt.savefig(f"plots/actual_vs_pred_{model_name.lower().replace(' ', '_')}.png")
    plt.show()

plot_actual_vs_pred(y_test, y_pred, "Random Forest")    