from flask import Flask, jsonify, request, render_template
import numpy as np
import csv
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

app = Flask(__name__) 

@app.route('/')
def home():
    generated_data = {
        f"department_{i}": generate_random_data(30, 10, 5).tolist()
        for i in range(5)
    }
    save_to_csv("generated_data.csv", generated_data)  
    return render_template('index.html', message="Welcome to the Threat Score API!", data=generated_data)

@app.route('/generate', methods=['GET'])
def generate_data():
    generated_data = {
        f"department_{i}": generate_random_data(30, 10, 5).tolist()
        for i in range(5)
    }
    save_to_csv("generated_data.csv", generated_data)
    return render_template('results.html', data=generated_data)

@app.route('/threat_scores', methods=['GET'])
def get_threat_scores():
    data, department_names = load_from_csv("generated_data.csv")
    es_result = index_data_to_elasticsearch(data, department_names)
    return jsonify(es_result)

def save_to_csv(filename, data):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Department', 'Scores'])
        for department, scores in data.items():
            writer.writerow([department, ','.join(map(str, scores))])

def load_from_csv(filename):
    with open(filename, mode='r') as file:
        reader = csv.DictReader(file)
        data = {}
        for row in reader:
            department = row['Department']
            scores = list(map(int, row['Scores'].split(',')))
            if department not in data:
                data[department] = []
            data[department].extend(scores)
        return list(data.values()), list(data.keys())

def generate_random_data(mean, variance, num_samples):
    lower_bound = max(mean - variance, 0)
    upper_bound = min(mean + variance + 1, 90)
    if lower_bound >= upper_bound:
        raise ValueError(f"Invalid range: lower_bound >= upper_bound. Lower bound: {lower_bound}, Upper bound: {upper_bound}")
    return np.random.randint(lower_bound, upper_bound, num_samples)

def calculate_aggregated_threat_score(department_scores):
    means = [np.mean(scores) for scores in department_scores]
    variances = [np.var(scores) for scores in department_scores]
    max_variance = max(variances)
    weights = [(var / max_variance) if max_variance > 0 else 1 for var in variances]
    weighted_sum = sum(mean * weight for mean, weight in zip(means, weights))
    total_weight = sum(weights)
    aggregated_score = weighted_sum / total_weight if total_weight > 0 else np.mean(means)
    return min(max(aggregated_score, 0), 90)

def index_data_to_elasticsearch(data, departments, index_name="department_scores"):
    es = Elasticsearch("http://localhost:9200")

    actions = []
    for department, department_scores in zip(departments, data):
        aggregated_score = calculate_aggregated_threat_score([department_scores])  
        action = {
            "_op_type": "index",  
            "_index": index_name,
            "_source": {
                "department": department,
                "threat_scores": department_scores,
                "aggregated_threat_score": aggregated_score  
            }
        }
        actions.append(action)

    bulk(es, actions)
    return {"message": "Data indexed to Elasticsearch successfully."}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
