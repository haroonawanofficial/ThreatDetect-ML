import sqlite3
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
import pandas as pd

class MachineLearningModel:
    def __init__(self, db_file="exploitation_results.db"):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def load_data(self):
        query = "SELECT target, service_name, service_version, port, cve_list, exploitation_result FROM exploitation_results"
        data = self.cursor.execute(query).fetchall()
        df = pd.DataFrame(data, columns=['target', 'service_name', 'service_version', 'port', 'cve_list', 'exploitation_result'])
        return df

    def preprocess_data(self, data):
        label_encoder = LabelEncoder()
        data['service_name'] = label_encoder.fit_transform(data['service_name'])
        data['service_version'] = label_encoder.fit_transform(data['service_version'])
        data['exploitation_result'] = label_encoder.fit_transform(data['exploitation_result'])

        X = data[['service_name', 'service_version', 'port', 'cve_list']]
        y = data['exploitation_result']
        return X, y

    def train_model(self, X, y):
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        model = RandomForestClassifier()
        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        return model, accuracy

    def close(self):
        self.connection.close()

if __name__ == '__main__':
    ml = MachineLearningModel()
    data = ml.load_data()
    X, y = ml.preprocess_data(data)
    model, accuracy = ml.train_model(X, y)
    print(f"Model accuracy: {accuracy}")
