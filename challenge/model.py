import pickle
import pandas as pd
import numpy as np
from typing import Tuple, Union, List
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from datetime import datetime

class DelayModel:

    TARGET_COL = "delay"
    THRESHOLD_IN_MINUTES = 15
    FEATURES_COLS = [
            "OPERA_Latin American Wings", 
            "MES_7",
            "MES_10",
            "OPERA_Grupo LATAM",
            "MES_12",
            "TIPOVUELO_I",
            "MES_4",
            "MES_11",
            "OPERA_Sky Airline",
            "OPERA_Copa Air"
        ]

    def __init__(self):
        self._model = None
        
    def get_min_diff(self, data: pd.Series) -> float:
        """
        Obtiene los minutos de diferencia
        Args:
            data (pd.Series): data.

        Returns: 
            float: minutos de diferencia        
        """
        fecha_o = datetime.strptime(data['Fecha-O'], '%Y-%m-%d %H:%M:%S')
        fecha_i = datetime.strptime(data['Fecha-I'], '%Y-%m-%d %H:%M:%S')
        min_diff = ((fecha_o - fecha_i).total_seconds())/60
        return min_diff        

    def preprocess(self, data: pd.DataFrame, target_column: str = None ) -> Union[Tuple[pd.DataFrame, pd.DataFrame], pd.DataFrame]:
        """
        Prepare raw data for training or predict.

        Args:
            data (pd.DataFrame): raw data.
            target_column (str, optional): if set, the target is returned.

        Returns:
            Tuple[pd.DataFrame, pd.DataFrame]: features and target.
            or
            pd.DataFrame: features.
        """
        features = pd.concat([
            pd.get_dummies(data['OPERA'], prefix = 'OPERA'),
            pd.get_dummies(data['TIPOVUELO'], prefix = 'TIPOVUELO'), 
            pd.get_dummies(data['MES'], prefix = 'MES')], 
            axis = 1
        )

        if target_column:
            data['min_diff'] = data.apply(self.get_min_diff, axis = 1)
            data[target_column] = np.where(data['min_diff'] > self.THRESHOLD_IN_MINUTES, 1, 0)            

            return (features[self.FEATURES_COLS], data[[target_column]])
        else: 
            return features[self.FEATURES_COLS]
    
    def fit(self, features: pd.DataFrame, target: pd.DataFrame ) -> None:
        """
        Fit model with preprocessed data.

        Args:
            features (pd.DataFrame): preprocessed data.
            target (pd.DataFrame): target.
        """
        x_train, _, y_train, _ = train_test_split(features, target[self.TARGET_COL], test_size = 0.33, random_state = 42)

        n_y0 = len(y_train[y_train == 0])
        n_y1 = len(y_train[y_train == 1])    
        scale = n_y0/n_y1

        self._model = XGBClassifier(random_state=1, learning_rate=0.01, scale_pos_weight = scale)
        self._model.fit(x_train, y_train)

        self.save_model()

        return self

    def predict(self, features: pd.DataFrame) -> List[int]:
        """
        Predict delays for new flights.

        Args:
            features (pd.DataFrame): preprocessed data.
        
        Returns:
            (List[int]): predicted targets.
        """
        if self._model is None:
            self.load_model()   

        return [int(pred) for pred in self._model.predict(features)]
    
    def save_model(self, filename: str = "delay_model.pkl") -> None:
        """
        Guarda el modelo entrenado en un archivo .pkl.

        Args:
            filename (str): Nombre del archivo donde se guardará el modelo.
        """
        with open(filename, "wb") as file:
            pickle.dump(self, file)

    def load_model(self, filename: str = "delay_model.pkl") -> None:
        """
        Carga un modelo desde un archivo .pkl.

        Args:
            filename (str): nombre del archivo desde donde se cargará el modelo.
        """
        with open(filename, "rb") as file:
            self._model = pickle.load(file)

def main():
    # Inicializa el modelo
    model = DelayModel()

    # obtiene los datos
    data = pd.read_csv(filepath_or_buffer="data/data.csv")

    # procesar datos
    features, target = model.preprocess(data=data, target_column=model.TARGET_COL)

    # ajustar el modelo
    model.fit(features=features, target=target)

if __name__ == "__main__":
    main()