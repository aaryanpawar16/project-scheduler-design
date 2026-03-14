# src/similarity.py

import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.neighbors import NearestNeighbors
from sklearn.impute import SimpleImputer

def find_similar_projects(new_project: dict, metadata_df: pd.DataFrame, top_k: int = 3) -> list:
    """
    Finds the most similar historical projects based on input attributes.
    
    Args:
        new_project (dict): Attributes of the new project from the Streamlit UI.
        metadata_df (pd.DataFrame): The historical Project_JOB_meta_data.csv data.
        top_k (int): Number of similar projects to return.
        
    Returns:
        list: A list of dictionaries containing similar project IDs (CONTROL_JOB_NO) and their match scores.
    """
    
    new_df = pd.DataFrame([new_project])
    
    combined_df = pd.concat([metadata_df.drop(columns=['CONTROL_JOB_NO'], errors='ignore'), new_df], axis=0)
    
    
    numeric_features = combined_df.select_dtypes(include=['int64', 'float64']).columns.tolist()
    categorical_features = combined_df.select_dtypes(include=['object', 'category']).columns.tolist()

    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])

    
    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
        ('onehot', OneHotEncoder(handle_unknown='ignore'))
    ])

    
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features)
        ])

    
    processed_data = preprocessor.fit_transform(combined_df)
    
    
    historical_vectors = processed_data[:-1]
    target_vector = processed_data[-1].reshape(1, -1)
    
    nn_model = NearestNeighbors(n_neighbors=top_k, metric='cosine')
    nn_model.fit(historical_vectors)
    
    
    distances, indices = nn_model.kneighbors(target_vector)
    
    similar_projects = []
    
    for i in range(len(indices[0])):
        idx = indices[0][i]
        dist = distances[0][i]
        
        project_id = metadata_df.iloc[idx]['CONTROL_JOB_NO']
        
        match_score = max(0, round((1 - dist) * 100, 1))
        
        similar_projects.append({
            "id": project_id,
            "score": match_score
        })
        
    return similar_projects