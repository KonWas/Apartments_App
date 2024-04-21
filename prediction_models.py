import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import joblib  # For saving and loading models
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.svm import SVR
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import mean_squared_error
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.losses import MeanSquaredError

def load_and_preprocess_data(filepath):
    data = pd.read_csv(filepath)
    # data = data[(data['price'] <= 2000000)]
    # data = data[(data['area'] <= 100)]
    data = data[(data['price'] <= 1250000)]
    data = data[(data['area'] <= 80)]
    label_encoders = {}
    for column in ['location', 'state', 'market']:
        le = LabelEncoder()
        data[column] = le.fit_transform(data[column])
        label_encoders[column] = le
        joblib.dump(le, f"{column}_encoder.pkl")
    return data, label_encoders

def prepare_data(data):
    columns_to_drop = ['price', 'floor', 'total_floors', 'year', 'parking', 'state', 'furnished', 'market']
    y = data['price']
    X = data.drop(columns_to_drop, axis=1)
    scaler_X = StandardScaler()
    scaler_y = StandardScaler()
    X_scaled = scaler_X.fit_transform(X)
    y_scaled = scaler_y.fit_transform(y.values.reshape(-1, 1))
    joblib.dump(scaler_X, 'scaler_X.pkl')
    joblib.dump(scaler_y, 'scaler_y.pkl')
    return X_scaled, y_scaled, scaler_X, scaler_y

def load_models():
    models = {
        "Linear Regression": joblib.load("Linear_Regression.txt"),
        "Random Forest Regressor": joblib.load("Random_Forest_Regressor.txt"),
        "Gradient Boosting Regressor": joblib.load("Gradient_Boosting_Regressor.txt"),
        "Optimized SVR": joblib.load("Optimized_SVR.txt"),
        "Neural Network": load_model('neural_network_model.keras')
    }
    return models

def train_models(X_train, y_train):
    models = {
        "Linear Regression": LinearRegression(),
        "Random Forest Regressor": RandomForestRegressor(n_estimators=100),
        "Gradient Boosting Regressor": GradientBoostingRegressor(n_estimators=100),
        "Optimized SVR": optimize_svr(X_train, y_train),  # Optimize SVR during training
        "Neural Network": build_and_train_nn(X_train, y_train)  # Train and build NN during training
    }
    for name, model in models.items():
        if "Neural Network" not in name:
            model.fit(X_train, y_train.ravel())
            joblib.dump(model, f"{name.replace(' ', '_')}.txt")
    return models

def optimize_svr(X_train, y_train):
    param_grid = {
        'C': [0.1, 1, 10, 100],
        'gamma': ['scale', 'auto', 0.01, 0.1, 1],
        'epsilon': [0.01, 0.1, 1]
    }
    grid_search = GridSearchCV(SVR(kernel='rbf'), param_grid, cv=5, verbose=2, scoring='neg_mean_squared_error')
    grid_search.fit(X_train, y_train.ravel())
    best_svr = grid_search.best_estimator_
    joblib.dump(best_svr, 'Optimized_SVR.txt')
    return best_svr

def build_and_train_nn(X_train, y_train):
    input_dim = X_train.shape[1]
    nn_model = Sequential([
        Dense(128, input_dim=input_dim, activation='relu'),
        Dense(64, activation='relu'),
        Dense(32, activation='relu'),
        Dense(1, activation='linear')
    ])
    nn_model.compile(optimizer=Adam(learning_rate=0.001), loss='mse')
    nn_model.fit(X_train, y_train, epochs=200, validation_split=0.2, verbose=1)
    nn_model.save('neural_network_model.keras')
    return nn_model

def evaluate_models(models, X_test, y_test, scaler_y):
    results = {}
    for name, model in models.items():
        predictions = model.predict(X_test)
        mse = mean_squared_error(scaler_y.inverse_transform(y_test), scaler_y.inverse_transform(predictions.reshape(-1, 1)))
        rmse = np.sqrt(mse)
        results[name] = rmse
    return results

def plot_data(df: pd.DataFrame, column: str) -> None:
    # Plot prive vs area for each location on one figure
    plt.figure(figsize=(10, 6))
    for location in df['location'].unique():
        sns.scatterplot(data=df[df['location'] == location], x='area', y='price', label=location)
    plt.title('Price vs Area for each location')
    plt.legend()
    plt.show()

def plot_results(results):
    plt.figure(figsize=(10, 5))
    models = list(results.keys())
    rmse_values = list(results.values())
    plt.bar(models, rmse_values, color='blue')
    plt.xlabel('Models')
    plt.ylabel('RMSE')
    plt.title('Model Comparison based on RMSE')
    plt.show()

def display_sample_predictions(models, X_test, y_test, scaler_y, num_samples=5):
    indices = np.random.choice(np.arange(len(X_test)), size=num_samples, replace=False)
    sample_X = X_test[indices]
    sample_y_actual = scaler_y.inverse_transform(y_test[indices])

    predictions = {}
    for name, model in models.items():
        sample_y_pred = scaler_y.inverse_transform(model.predict(sample_X).reshape(-1, 1))
        predictions[name] = sample_y_pred[:, 0]

    # Tworzenie DataFrame dla łatwiejszego zarządzania danymi
    df_results = pd.DataFrame(sample_y_actual, columns=['Actual Price'])
    for name in predictions:
        df_results[name + ' Predictions'] = predictions[name]

    # Wykresy porównujące rzeczywiste ceny z przewidywaniami modeli
    plt.figure(figsize=(12, 8))
    for name in predictions:
        plt.plot(df_results[name + ' Predictions'], label=f'{name} Predictions', marker='o')
    plt.plot(df_results['Actual Price'], label='Actual Price', marker='x', linestyle='--', color='black')

    plt.xlabel('Sample Index')
    plt.ylabel('Price')
    plt.title('Comparison of Model Predictions with Actual Prices')
    plt.legend()
    plt.grid(True)
    plt.show()

    # Wyświetlanie DataFrame w konsoli
    print(df_results)

# Main execution block
train = False  # Change to False if you want to load models instead of training
data, label_encoders = load_and_preprocess_data('data_cleaned_formated.csv')
X_scaled, y_scaled, scaler_X, scaler_y = prepare_data(data)
X_train_scaled, X_test_scaled, y_train_scaled, y_test_scaled = train_test_split(X_scaled, y_scaled, test_size=0.2, random_state=42)

if train:
    models = train_models(X_train_scaled, y_train_scaled)
else:
    models = load_models()

results = evaluate_models(models, X_test_scaled, y_test_scaled, scaler_y)
print("Models have been trained and saved. RMSE scores are calculated and displayed.")
for model_name, rmse in results.items():
    print(f"{model_name}: RMSE = {rmse:.2f}")
plot_results(results)

# Display sample predictions
display_sample_predictions(models, X_test_scaled, y_test_scaled, scaler_y, num_samples=100)

# Display price vs area data
# plot_data(data, 'location')
