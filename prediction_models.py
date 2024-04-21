# Importing necessary libraries
import pandas as pd
import numpy as np
import joblib  # For saving and loading models
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.svm import SVR
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import mean_squared_error
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import Adam

# Load data
data = pd.read_csv('data_cleaned_formated.csv')

# Filter out expensive apartments (more than 2,000,000 zł)
data = data[data['price'] <= 2000000]
data = data[data['area'] <= 100]

# Preprocessing
# Convert categorical variables using Label Encoding
label_encoders = {}
for column in ['location', 'state', 'market']:
    le = LabelEncoder()
    data[column] = le.fit_transform(data[column])
    label_encoders[column] = le
    joblib.dump(le, f"{column}_encoder.pkl")

# Feature selection: preparing input and output for models
X = data.drop('price', axis=1)
X = data.drop(['floor', 'total_floors', 'furnished', 'parking', 'year'], axis=1)
y = data['price']

# Initialize and apply scalers for input and output
scaler_X = StandardScaler()
scaler_y = StandardScaler()
X_scaled = scaler_X.fit_transform(X)
y_scaled = scaler_y.fit_transform(y.values.reshape(-1, 1))
joblib.dump(scaler_X, 'scaler_X.pkl')
joblib.dump(scaler_y, 'scaler_y.pkl')

# Split the scaled data into training and testing sets
X_train_scaled, X_test_scaled, y_train_scaled, y_test_scaled = train_test_split(X_scaled, y_scaled, test_size=0.2, random_state=42)

# Define and train different regression models
models = {
    "Linear Regression": LinearRegression(),
    "Random Forest Regressor": RandomForestRegressor(n_estimators=100),
    "Gradient Boosting Regressor": GradientBoostingRegressor(n_estimators=100),
    # SVR will be configured with GridSearchCV
}

# Train each model and save it
for name, model in models.items():
    model.fit(X_train_scaled, y_train_scaled.ravel())
    joblib.dump(model, f"{name.replace(' ', '_')}.txt")
    

# Optimizing SVR with GridSearchCV
param_grid = {
    'C': [0.1, 1, 10, 100],
    'gamma': ['scale', 'auto', 0.01, 0.1, 1],
    'epsilon': [0.01, 0.1, 1]
}
grid_search = GridSearchCV(SVR(kernel='rbf'), param_grid, cv=5, verbose=2, scoring='neg_mean_squared_error')
grid_search.fit(X_train_scaled, y_train_scaled.ravel())
best_svr = grid_search.best_estimator_
joblib.dump(best_svr, 'Optimized_SVR.txt')

# Neural network setup
input_dim = X_train_scaled.shape[1]
nn_model = Sequential([
    Dense(128, input_dim=input_dim, activation='relu'),
    Dense(64, activation='relu'),
    Dense(32, activation='relu'),
    Dense(1, activation='linear')
])
nn_model.compile(optimizer=Adam(learning_rate=0.001), loss='mse')
nn_model.fit(X_train_scaled, y_train_scaled, epochs=200, validation_split=0.2, verbose=1)
nn_model.save('neural_network_model.h5')

# Predicting and evaluating RMSE for each model
results = {}
for name, model in models.items():
    predictions = model.predict(X_test_scaled)
    mse = mean_squared_error(scaler_y.inverse_transform(y_test_scaled), scaler_y.inverse_transform(predictions.reshape(-1, 1)))
    rmse = np.sqrt(mse)
    results[name] = rmse

# SVR and Neural Network predictions
svr_predictions = best_svr.predict(X_test_scaled)
svr_rmse = np.sqrt(mean_squared_error(scaler_y.inverse_transform(y_test_scaled), scaler_y.inverse_transform(svr_predictions.reshape(-1, 1))))
results['Optimized SVR'] = svr_rmse

nn_predictions = nn_model.predict(X_test_scaled)
nn_mse = mean_squared_error(scaler_y.inverse_transform(y_test_scaled), scaler_y.inverse_transform(nn_predictions))
nn_rmse = np.sqrt(nn_mse)
results['Neural Network'] = nn_rmse

# Display the RMSE results for each model
for model_name, rmse in results.items():
    print(f"{model_name}: RMSE = {rmse:.2f}")
print("Models have been trained and saved. RMSE scores are calculated and displayed.")


# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# import joblib  # For saving and loading models
# from sklearn.model_selection import train_test_split, GridSearchCV
# from sklearn.linear_model import LinearRegression
# from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
# from sklearn.svm import SVR
# from sklearn.preprocessing import StandardScaler, LabelEncoder
# from sklearn.metrics import mean_squared_error
# from tensorflow.keras.models import Sequential
# from tensorflow.keras.layers import Dense, Dropout
# from tensorflow.keras.optimizers import Adam

# def load_and_preprocess_data(filepath):
#     data = pd.read_csv(filepath)
#     data = data[(data['price'] <= 2000000)]
#     data = data[(data['area'] <= 100)]
#     label_encoders = {}
#     for column in ['location', 'state', 'market']:
#         le = LabelEncoder()
#         data[column] = le.fit_transform(data[column])
#         label_encoders[column] = le
#         joblib.dump(le, f"{column}_encoder.pkl")
#     return data, label_encoders

# def prepare_data(data):
#     X = data.drop(['price', 'floor', 'total_floors', 'furnished', 'parking', 'year'], axis=1)
#     y = data['price']
#     scaler_X = StandardScaler()
#     scaler_y = StandardScaler()
#     X_scaled = scaler_X.fit_transform(X)
#     y_scaled = scaler_y.fit_transform(y.values.reshape(-1, 1))
#     joblib.dump(scaler_X, 'scaler_X.pkl')
#     joblib.dump(scaler_y, 'scaler_y.pkl')
#     return X_scaled, y_scaled, scaler_X, scaler_y

# def train_models(X_train, y_train):
#     models = {
#         "Linear Regression": LinearRegression(),
#         "Random Forest Regressor": RandomForestRegressor(n_estimators=100),
#         "Gradient Boosting Regressor": GradientBoostingRegressor(n_estimators=100)
#     }
#     for name, model in models.items():
#         model.fit(X_train, y_train.ravel())
#         joblib.dump(model, f"{name.replace(' ', '_')}.txt")
#     return models

# def optimize_svr(X_train, y_train):
#     param_grid = {
#         'C': [0.1, 1, 10, 100],
#         'gamma': ['scale', 'auto', 0.01, 0.1, 1],
#         'epsilon': [0.01, 0.1, 1]
#     }
#     grid_search = GridSearchCV(SVR(kernel='rbf'), param_grid, cv=5, verbose=2, scoring='neg_mean_squared_error')
#     grid_search.fit(X_train, y_train.ravel())
#     best_svr = grid_search.best_estimator_
#     joblib.dump(best_svr, 'Optimized_SVR.txt')
#     return best_svr

# def build_and_train_nn(X_train, y_train):
#     input_dim = X_train.shape[1]
#     nn_model = Sequential([
#         Dense(128, input_dim=input_dim, activation='relu'),
#         Dense(64, activation='relu'),
#         Dense(32, activation='relu'),
#         Dense(1, activation='linear')
#     ])
#     nn_model.compile(optimizer=Adam(learning_rate=0.001), loss='mse')
#     nn_model.fit(X_train, y_train, epochs=200, validation_split=0.2, verbose=1)
#     nn_model.save('neural_network_model.h5')
#     return nn_model

# def evaluate_models(models, X_test, y_test, scaler_y):
#     results = {}
#     for name, model in models.items():
#         predictions = model.predict(X_test)
#         mse = mean_squared_error(scaler_y.inverse_transform(y_test), scaler_y.inverse_transform(predictions.reshape(-1, 1)))
#         rmse = np.sqrt(mse)
#         results[name] = rmse
#     return results

# def plot_results(results):
#     plt.figure(figsize=(10, 5))
#     models = list(results.keys())
#     rmse_values = list(results.values())
#     plt.bar(models, rmse_values, color='blue')
#     plt.xlabel('Models')
#     plt.ylabel('RMSE')
#     plt.title('Model Comparison based on RMSE')
#     plt.show()

# # Main execution block
# data, label_encoders = load_and_preprocess_data('data_cleaned_formated.csv')
# X_scaled, y_scaled, scaler_X, scaler_y = prepare_data(data)
# X_train_scaled, X_test_scaled, y_train_scaled, y_test_scaled = train_test_split(X_scaled, y_scaled, test_size=0.2, random_state=42)
# models = train_models(X_train_scaled, y_train_scaled)
# best_svr = optimize_svr(X_train_scaled, y_train_scaled)
# models['Optimized SVR'] = best_svr
# nn_model = build_and_train_nn(X_train_scaled, y_train_scaled)
# models['Neural Network'] = nn_model
# results = evaluate_models(models, X_test_scaled, y_test_scaled, scaler_y)
# print("Models have been trained and saved. RMSE scores are calculated and displayed.")
# for model_name, rmse in results.items():
#     print(f"{model_name}: RMSE = {rmse:.2f}")
# plot_results(results)
