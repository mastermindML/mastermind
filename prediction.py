# Prediction Start
import os
import joblib
import pandas as pd

def load_model(model_dir):
    """
    Load a trained machine learning model from the specified directory.

    Args:
        model_dir: The directory containing the trained model.

    Returns:
        The loaded machine learning model.
    """
    model_filename = os.path.join(model_dir, 'trained_model.pkl')
    clf = joblib.load(model_filename)
    return clf

def predict(model, features):
    """
    Make predictions using a trained machine learning model.

    Args:
        model: The trained machine learning model.
        features: A Pandas DataFrame containing the features of new data.

    Returns:
        A Pandas Series containing the predicted labels.
    """
    predictions = model.predict(features)
    return pd.Series(predictions, name='predicted_label')

def main(input_dir, model_dir, output_dir):
    """
    Main function to make predictions using a trained model and save the results.

    Args:
        input_dir: The directory containing the new data features.
        model_dir: The directory containing the trained machine learning model.
        output_dir: The directory where the prediction results will be saved.

    Returns:
        None
    """
    # Load the trained model
    model = load_model(model_dir)

    # Load new data features
    features = pd.read_csv(os.path.join(input_dir, 'new_data_features.csv'))

    # Make predictions
    predictions = predict(model, features)

    # Save the prediction results
    output_filename = os.path.join(output_dir, 'predictions.csv')
    predictions.to_csv(output_filename, index=False)

if __name__ == "__main__":
    # Example usage when running this script directly
    input_dir = "data/new_data"
    model_dir = "models"
    output_dir = "results"
    main(input_dir, model_dir, output_dir)


# Prediction End
