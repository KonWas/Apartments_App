import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.svm import SVR
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import mean_squared_error, mean_absolute_error
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import Adam

# scatter plot dla sampli
# opisanie jak czyscilem dane
# opisanie modeli jakie i dlaczego
# analiza wynikow - wnioski

# -------Directories setup-------
def setup_directories():
    """Create directories for models and other files if they don't exist."""
    if not os.path.exists('models'):
        os.makedirs('models')
    if not os.path.exists('others'):
        os.makedirs('others')


# -------Data preprocessing-------
def remove_outliers_wider(df, multiplier=3):
    """Remove outliers from the dataset using the IQR method with a wider range.
    :param df: DataFrame to remove outliers from
    :param multiplier: Multiplier for the IQR range
    :return: DataFrame without outliers
    """
    numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns
    for column in numeric_columns:
        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - multiplier * IQR
        upper_bound = Q3 + multiplier * IQR
        df = df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]
    return df


def load_and_preprocess_data(filepath):
    """Load the dataset from the given filepath, preprocess it and return the preprocessed data and label encoders.
    :param filepath: Filepath to the dataset
    :return: Preprocessed data and label encoders
    """
    data = pd.read_csv(filepath)
    data = remove_outliers_wider(data)
    data = data[(data['price'] <= 1250000)]
    data = data[(data['price'] >= 100000)]
    data = data[(data['area'] <= 80)]
    data = data[(data['floor'] <= 29)]
    data = data[(data['rooms'] <= 7)]
    data = data[(data['year'] >= 1925)]

    # price per square meter filter
    # data['price_per_sqm'] = data['price'] / data['area']
    # data = data[(data['price_per_sqm'] <= 17000)]
    # data = data[(data['price_per_sqm'] >= 1000)]
    # data.drop('price_per_sqm', axis=1, inplace=True)

    label_encoders = {}
    for column in ['location', 'state', 'market']:
        le = LabelEncoder()
        data[column] = le.fit_transform(data[column])
        label_encoders[column] = le
        joblib.dump(le, f"others/{column}_encoder.pkl")
    return data, label_encoders


def prepare_data(data):
    """Prepare the data for training by splitting it into features and target, scaling the data and saving the scalers.
    :param data: Preprocessed DataFrame
    :return: Scaled features and target, and the scalers
    """
    columns_to_drop = ['price']
    y = data['price']
    X = data.drop(columns_to_drop, axis=1)
    scaler_X = StandardScaler()
    scaler_y = StandardScaler()
    X_scaled = scaler_X.fit_transform(X)
    y_scaled = scaler_y.fit_transform(y.values.reshape(-1, 1))
    joblib.dump(scaler_X, 'others/scaler_X.pkl')
    joblib.dump(scaler_y, 'others/scaler_y.pkl')
    return X_scaled, y_scaled, scaler_X, scaler_y


# -------Model training and evaluation-------
def load_models():
    """Load the trained models from the files.
    :return: Dictionary of loaded models
    """
    models = {
        "Linear Regression": joblib.load("models/Linear_Regression.txt"),
        "Random Forest Regressor": joblib.load("models/Random_Forest_Regressor.txt"),
        "Gradient Boosting Regressor": joblib.load("models/Gradient_Boosting_Regressor.txt"),
        "Optimized SVR": joblib.load("models/Optimized_SVR.txt"),
        "Neural Network": load_model('models/neural_network_model.keras')
    }
    return models


def train_models(X_train, y_train):
    """Train the models and save them to files.
    :param X_train: Scaled features for training
    :param y_train: Scaled target for training
    :return: Dictionary of trained models
    """
    models = {
        "Linear Regression": LinearRegression(),
        "Random Forest Regressor": RandomForestRegressor(n_estimators=100),
        "Gradient Boosting Regressor": GradientBoostingRegressor(n_estimators=100),
        "Optimized SVR": optimize_svr(X_train, y_train),
        "Neural Network": build_and_train_nn(X_train, y_train)
    }
    for name, model in models.items():
        if "Neural Network" not in name:
            model.fit(X_train, y_train.ravel())
            joblib.dump(model, f"models/{name.replace(' ', '_')}.txt")
    return models


def optimize_svr(X_train, y_train):
    """Optimize the SVR model using GridSearchCV and save the best model to a file.
    :param X_train: Scaled features for training
    :param y_train: Scaled target for training
    :return: Optimized SVR model
    """
    param_grid = {
        'C': [0.1, 1, 10, 100],
        'gamma': ['scale', 'auto', 0.01, 0.1, 1],
        'epsilon': [0.01, 0.1, 1]
    }
    grid_search = GridSearchCV(SVR(kernel='rbf'), param_grid, cv=5, verbose=2, scoring='neg_mean_squared_error')
    grid_search.fit(X_train, y_train.ravel())
    best_svr = grid_search.best_estimator_
    joblib.dump(best_svr, 'models/Optimized_SVR.txt')
    return best_svr


def build_and_train_nn(X_train, y_train):
    """Build and train a neural network model using Keras and save it to a file.
    :param X_train: Scaled features for training
    :param y_train: Scaled target for training
    :return: Trained neural network model
    """
    input_dim = X_train.shape[1]
    nn_model = Sequential([
        Dense(128, input_dim=input_dim, activation='relu'),
        Dropout(0.2),
        Dense(64, activation='relu'),
        Dropout(0.5),
        Dense(32, activation='relu'),
        Dropout(0.5),
        Dense(1, activation='linear')
    ])
    nn_model.compile(optimizer=Adam(learning_rate=0.001), loss='mse')
    nn_model.fit(X_train, y_train, epochs=200, validation_split=0.2, verbose=1)
    nn_model.save('models/neural_network_model.keras')
    return nn_model


def evaluate_models(models, X_test, y_test, scaler_y):
    """Evaluate the models using RMSE and return the results.
    :param models: Dictionary of trained models
    :param X_test: Scaled features for testing
    :param y_test: Scaled target for testing
    :param scaler_y: Target scaler
    :return: Dictionary of model names and RMSE scores
    """
    results = {}
    for name, model in models.items():
        predictions = model.predict(X_test)
        mae = mean_absolute_error(scaler_y.inverse_transform(y_test), scaler_y.inverse_transform(predictions.reshape(-1, 1)))
        results[name] = mae
    return results


# -------Plotting the data-------
def plot_data(df: pd.DataFrame, column: str) -> None:
    """Plot the given column from the DataFrame.
    :param df: DataFrame to plot
    :param column: Column to plot
    """
    plt.figure(figsize=(10, 6))
    for location in df['location'].unique():
        sns.scatterplot(data=df[df['location'] == location], x='area', y='price', label=location)
    plt.title('Price vs Area for each location')
    plt.legend()
    plt.show()


# -------Plotting the results-------
def plot_results(results):
    """Plot the results of the model evaluation.
    :param results: Dictionary of model names and MAE scores
    """
    plt.figure(figsize=(10, 5))
    models = list(results.keys())
    rmse_values = list(results.values())
    plt.bar(models, rmse_values, color='blue')
    plt.xlabel('Models')
    plt.ylabel('MAE')
    plt.title('Model Comparison based on MAE')
    plt.show()


def plot_predictions(models, X_test, y_test, scaler_y):
    """Plot the actual vs predicted prices for each model.
    :param models: Dictionary of trained models
    :param X_test: Scaled features for testing
    :param y_test: Scaled target for testing
    :param scaler_y: Target scaler
    """
    for name, model in models.items():
        predictions = model.predict(X_test)
        predictions_actual = scaler_y.inverse_transform(predictions.reshape(-1, 1))
        y_actual = scaler_y.inverse_transform(y_test)

        plt.figure(figsize=(10, 6))
        plt.scatter(y_actual, predictions_actual, alpha=0.5)
        plt.plot([y_actual.min(), y_actual.max()], [y_actual.min(), y_actual.max()], 'k--', lw=4)
        plt.xlabel('Actual')
        plt.ylabel('Predicted')
        plt.title(f'Actual vs Predicted - {name}')
        plt.show()


def plot_percentage_errors(models, X_test, y_test, scaler_y):
    """Plot the distribution of percentage errors for each model.
    :param models: Dictionary of trained models
    :param X_test: Scaled features for testing
    :param y_test: Scaled target for testing
    :param scaler_y: Target scaler
    """
    for name, model in models.items():
        predictions = model.predict(X_test)
        actual = scaler_y.inverse_transform(y_test)
        predicted = scaler_y.inverse_transform(predictions.reshape(-1, 1))
        
        percentage_errors = 100 * (predicted - actual) / actual
        
        plt.figure(figsize=(8, 6))
        plt.hist(percentage_errors, bins=30, alpha=0.7, color='blue')
        plt.title(f'Distribution of Percentage Errors - {name}')
        plt.xlabel('Percentage Error (%)')
        plt.ylabel('Frequency')
        plt.grid(True)
        plt.show()


def display_sample_predictions(models, X_test, y_test, scaler_y, num_samples=5):
    """Display sample predictions for a given number of samples.
    :param models: Dictionary of trained models
    :param X_test: Scaled features for testing
    :param y_test: Scaled target for testing
    :param scaler_y: Target scaler
    :param num_samples: Number of samples to display
    """
    indices = np.random.choice(np.arange(len(X_test)), size=num_samples, replace=False)
    sample_X = X_test[indices]
    sample_y_actual = scaler_y.inverse_transform(y_test[indices])

    predictions = {}
    for name, model in models.items():
        sample_y_pred = scaler_y.inverse_transform(model.predict(sample_X).reshape(-1, 1))
        predictions[name] = sample_y_pred[:, 0]

    df_results = pd.DataFrame(sample_y_actual, columns=['Actual Price'])
    for name in predictions:
        df_results[name + ' Predictions'] = predictions[name]

    plt.figure(figsize=(12, 8))
    for name in predictions:
        plt.scatter(range(num_samples), df_results[name + ' Predictions'], label=f'{name} Predictions', marker='o')
    plt.scatter(range(num_samples), df_results['Actual Price'], label='Actual Price', marker='x', color='black')

    plt.xlabel('Sample Index')
    plt.ylabel('Price')
    plt.title('Comparison of Model Predictions with Actual Prices')
    plt.legend()
    plt.grid(True)
    plt.show()

    print(df_results)


def display_worst_predictions(models, X_test, y_test, scaler_y, num_worst=10):
    """Display the worst predictions for each model.
    :param models: Dictionary of trained models
    :param X_test: Scaled features for testing
    :param y_test: Scaled target for testing
    :param scaler_y: Target scaler
    :param num_worst: Number of worst predictions to display
    """
    for name, model in models.items():
        predictions = model.predict(X_test)
        actual = scaler_y.inverse_transform(y_test)
        predicted = scaler_y.inverse_transform(predictions.reshape(-1, 1))
        
        errors = np.abs(predicted - actual)
        worst_indices = np.argsort(errors.ravel())[-num_worst:][::-1]

        worst_predictions = predicted[worst_indices]
        worst_actuals = actual[worst_indices]
        worst_errors = errors[worst_indices]

        print(f"\n{name} - Top {num_worst} Worst Predictions:")
        for i in range(num_worst):
            print(f"Actual: {worst_actuals[i][0]:,.2f}, Predicted: {worst_predictions[i][0]:,.2f}, Error: {worst_errors[i][0]:,.2f}")



def plot_all_results(models, X_test, y_test, scaler_y):
    """Plot the results of the model evaluation.
    :param models: Dictionary of model names and MAE scores
    :param X_test: Scaled features for testing
    :param y_test: Scaled target for testing
    :param scaler_y: Target scaler
    """
    plot_percentage_errors(models, X_test, y_test, scaler_y)
    plot_predictions(models, X_test, y_test, scaler_y)


def display_some_predictions(models, X_test, y_test, scaler_y, n=10):
    """Display some predictions for each model.
    :param models: Dictionary of trained models
    :param X_test: Scaled features for testing
    :param y_test: Scaled target for testing
    :param scaler_y: Target scaler
    :param n: Number of samples to display
    """
    display_sample_predictions(models, X_test, y_test, scaler_y, num_samples=n)
    display_worst_predictions(models, X_test, y_test, scaler_y, num_worst=n)


# -------Prediction from input-------
def input_pred(location, area, rooms, floor, total_floors, year, parking, state, furnished, market):
    """Predict the price for the given input data.
    :param location: Location of the property
    :param area: Area of the property
    :param rooms: Number of rooms
    :param floor: Floor number
    :param total_floors: Total number of floors in the building
    :param year: Year of construction
    :param parking: Parking availability
    :param state: State of the property
    :param furnished: Furnished status
    :param market: Market type
    :return: Dictionary of model names and predicted prices
    """
    location_encoder = joblib.load('others/location_encoder.pkl')
    state_encoder = joblib.load('others/state_encoder.pkl')
    market_encoder = joblib.load('others/market_encoder.pkl')
    scaler_X = joblib.load('others/scaler_X.pkl')
    scaler_y = joblib.load('others/scaler_y.pkl')

    location_encoded = location_encoder.transform([location])[0]
    state_encoded = state_encoder.transform([state])[0]
    market_encoded = market_encoder.transform([market])[0]

    input_data = np.array([location_encoded, area, rooms, floor, total_floors, year, parking, state_encoded, furnished, market_encoded]).reshape(1, -1)

    input_data_scaled = scaler_X.transform(input_data)

    models = load_models()

    predictions = {}
    for name, model in models.items():
        prediction_scaled = model.predict(input_data_scaled)
        prediction = scaler_y.inverse_transform(prediction_scaled.reshape(-1, 1))
        predictions[name] = prediction[0][0]

    return predictions


# -------Main-------
if __name__ == '__main__':
    setup_directories()
    train = False
    data, label_encoders = load_and_preprocess_data('data_cleaned_formated.csv')
    X_scaled, y_scaled, scaler_X, scaler_y = prepare_data(data)
    X_train_scaled, X_test_scaled, y_train_scaled, y_test_scaled = train_test_split(X_scaled, y_scaled, test_size=0.2, random_state=42)

    if train:
        models = train_models(X_train_scaled, y_train_scaled)
    else:
        models = load_models()

    results = evaluate_models(models, X_test_scaled, y_test_scaled, scaler_y)
    print("Models have been trained and saved. MAE scores are calculated and displayed.")
    for model_name, rmse in results.items():
        print(f"{model_name}: MAE = {rmse:.2f}")
    plot_results(results)

    #plot_all_results(models, X_test_scaled, y_test_scaled, scaler_y)
    display_some_predictions(models, X_test_scaled, y_test_scaled, scaler_y, n=10)


    input_preds = input_pred('Stare Miasto', 35.0, 2, 4, 4, 2000, 0, 'bardzo dobry', 1, 'secondary')
    for model, prediction in input_preds.items():
        print(f"{model}: {prediction:.2f}")