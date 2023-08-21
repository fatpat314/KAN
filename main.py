import config
from dotenv import load_dotenv
import openai
from flask import Flask, jsonify, request, session, g
from flask_jwt_extended import JWTManager, jwt_required, \
                               create_access_token, get_jwt_identity
import requests, names, random, threading, uuid, json
import argparse

from gpt import GPT_symptoms_disease_correlation, GPT_disease_info, GPT_request
from stats import do_stats_stuff

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = config.JWT_SECRET_KEY # change this to a random string in production
CNM_url = "http://localhost:6000"
jwt = JWTManager(app)
load_dotenv()

@app.route('/', methods = ['GET'])
def home():
    if(request.method == 'GET'):
        data = "hello Class!"
        return jsonify({'data': data})

@app.route('/disease_data', methods = ['GET', 'POST'])
def disease_data():
    data = request.json.get('symptoms')
    # print(data)
    disease_names = GPT_symptoms_disease_correlation(data)
    disease_names = disease_names[1:-1]
    print(disease_names)
    return jsonify(disease_names)

@app.route('/disease_info', methods = ['GET', 'POST'])
def disease_info():
    disease = request.json.get('disease')
    # Get LLM memo
    response = GPT_disease_info(disease)
    print(response)
    return jsonify(response)

@app.route('/disease_stats', methods=['GET', 'POST'])
def disease_stats():
    data = request.get_json()
    disease = data['disease']
    # symptoms_list = json.loads(data['symptoms'])
    symptoms = data['symptoms']
    # Reach out to CNM to get symptom names
    CNM_url_symptoms = f'{CNM_url}/get_symptom_names'
    data = {'symptoms': symptoms}
    symptom_names = requests.post(CNM_url_symptoms, json=data)
    symptom_names = symptom_names.json()
    # symptoms = get_symptom_info(data['symptoms'])
    # symptom_names_list = json.dumps(symptom_names)
    
    # print("STATS:", disease, symptom_names, type(symptom_names))
    # print(response.json())

    stats = do_stats_stuff(disease, symptom_names)

    print(stats)
    return jsonify(stats)

@app.route('/GPT_request', methods=['GET', 'POST'])
def GPT_response():
    data = request.get_json()
    age = data['age']
    symptoms_list = data['symptoms_list']
    response = GPT_request(age, symptoms_list)
    return jsonify(response)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8050, help="Port to run the server on")
    args = parser.parse_args()
    port = args.port
    app.run(host="0.0.0.0", port=port)