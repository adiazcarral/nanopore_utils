import os
import numpy as np
import scipy.io
import pandas as pd

def load_data(file_path):
    """
    Load nanopore data from a .mat or .csv file.
    """
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".mat":
        try:
            mat = scipy.io.loadmat(file_path)
            return mat, "mat"
        except Exception as e:
            raise ValueError(f"Error loading .mat file: {e}")
    elif ext == ".csv":
        try:
            df = pd.read_csv(file_path)
            return df, "csv"
        except Exception as e:
            raise ValueError(f"Error loading .csv file: {e}")
    else:
        raise ValueError("Unsupported file format. Please provide a .mat or .csv file.")

def extract_features_from_mat(mat):
    """
    Extract features from a .mat file.
    """
    crd = mat['EventDatabase']['ConcatenatedStartCoordinates'][0, 0]
    coord = extract_coordinates(crd)
    ev = mat['ConcatenatedEvents'].flatten()
    fits = mat['ConcatenatedFits'].flatten()
    evfit = mat['EventDatabase']['AllLevelFits'][0, 0].flatten()
    lvl = mat['EventDatabase']['NumberOfLevels'][0, 0].flatten()
    
    return calculate_features(coord, ev, fits, evfit, lvl)

def extract_features_from_csv(df):
    """
    Extract features from a CSV file.
    """
    coord = df['Coordinates'].to_numpy()
    ev = df['Events'].to_numpy()
    fits = df['Fits'].to_numpy()
    evfit = df['EventFits'].to_numpy()
    lvl = df['Levels'].to_numpy()
    
    return calculate_features(coord, ev, fits, evfit, lvl)

def extract_coordinates(crd):
    """
    Extract coordinates from the input data.
    """
    n_events = crd.shape[1]
    coord = np.zeros(n_events)
    for i in range(n_events):
        coord[i] = np.asscalar(crd[0, i])
    return coord

def calculate_features(coord, ev, fits, evfit, lvl):
    """
    Calculate features: dwell time, mean, height, and number of levels using coord.
    """
    n_events = len(coord)
    
    # Initialize arrays for features
    dwell_time = np.zeros(n_events)
    mean_vals = np.zeros(n_events)
    height = np.zeros(n_events)
    num_levels = np.zeros(n_events)
    
    for i in range(n_events):
        start = int(coord[i])
        end = start + len(evfit[i])
        
        # Calculate dwell time
        dwell_time[i] = len(evfit[i])
        
        # Calculate mean
        mean_vals[i] = np.mean(fits[start:end])
        
        # Calculate height
        height[i] = max(ev[start:end]) - min(ev[start:end])
        
        # Number of levels
        num_levels[i] = lvl[i]
    
    return dwell_time, mean_vals, height, num_levels

def normalize_features(features, smin=0, smax=255):
    """
    Normalize features to the range [smin, smax].
    """
    normalized_features = []
    for feature in features:
        feature_min, feature_max = feature.min(), feature.max()
        normalized = (feature - feature_min) * (smax - smin) / (feature_max - feature_min) + smin
        normalized_features.append(normalized)
    return normalized_features

def save_features(output_path, features, column_names):
    """
    Save features as columns in a .csv or .mat file.
    """
    ext = os.path.splitext(output_path)[1].lower()
    data = {name: feature for name, feature in zip(column_names, features)}
    
    if ext == ".mat":
        scipy.io.savemat(output_path, data)
    elif ext == ".csv":
        df = pd.DataFrame(data)
        df.to_csv(output_path, index=False)
    else:
        raise ValueError("Unsupported output file format. Please use .mat or .csv.")

def main(input_file, output_file):
    """
    Main function to process the nanopore data.
    """
    # Load data
    data, file_type = load_data(input_file)
    
    # Extract features based on file type
    if file_type == "mat":
        dwell_time, mean_vals, height, num_levels = extract_features_from_mat(data)
    elif file_type == "csv":
        dwell_time, mean_vals, height, num_levels = extract_features_from_csv(data)
    else:
        raise ValueError("Unsupported file type.")
    
    # Normalize features
    dwell_time, mean_vals, height, num_levels = normalize_features(
        [dwell_time, mean_vals, height, num_levels]
    )
    
    # Save features
    save_features(output_file, [dwell_time, mean_vals, height, num_levels], 
                  column_names=["dwell_time", "mean", "height", "num_levels"])
    print(f"Features saved to {output_file}")

if __name__ == "__main__":
    # Change working directory if needed
    os.chdir("/tikhome/angel/Code2/Preprocessing/Homopolymers")
    
    # File paths
    input_file = "input.mat"  # Input file (can be .mat or .csv)
    output_file = "output.csv"  # Output file (can be .mat or .csv)
    
    # Run the script
    main(input_file, output_file)
