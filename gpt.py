import config
from dotenv import load_dotenv
from openai import OpenAI

client = OpenAI(api_key=config.openai_key)

def GPT_request(age, symptoms):
    response = client.chat.completions.create(model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a Doctor"},
        {"role": "user", "content": f"The patient is {age} years old and experiencing {str(symptoms)}. What is the possible diagnosis for the disease?"},
    ])
    result = []
    for choice in response.choices:
        result.append(choice.message.content)
    # print(GPT_symptoms_disease_correlation(symptoms))
    return(result)

def GPT_symptoms_disease_correlation(symptoms):
    response = client.chat.completions.create(model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a Doctor"},
        # {"role": "user", "content": f"The patient is {age} years old and experiencing {str(symptoms)}. What is the diagnosis?"},
        {"role": "system", "content": f"Return a list of various diseases that manifest these symptoms. Return the list in the format of a python list and say nothing else please. {str(symptoms)}"}
    ])
    result = []
    for choice in response.choices:
        result.append(choice.message.content)
    return(result[0])
    # print(result)

def GPT_disease_info(disease):
    response = client.chat.completions.create(model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a Doctor"},
        {"role": "user", "content": f"Give me information about {disease}"},
    ])
    result = []
    for choice in response.choices:
        result.append(choice.message.content)
    # print(GPT_symptoms_disease_correlation(symptoms))
    return(result)

def GPT_disease_word_search(GPT_result):
    result = "".join(GPT_result)
    disease_word_search = client.chat.completions.create(model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a chat bot"},
        {"role": "user", "content": f"Could you please isolate and return the disease names, and only disease names from this sentence, separate the disease names by a comma, without any acronyms and say nothing else. If there are no disease names, return 0. '{result}'"},
    ])
    disease_names = ''
    for choice in disease_word_search.choices:
        disease_names += choice.message.content
    if disease_names == 0:
        return jsonify(result)
    
    return(disease_names)

def GPT_risk_factors(disease):
    response = client.chat.completions.create(model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a Doctor"},
        {"role": "user", "content": f"Return a python list of risk factors related to {disease} and say nothing else."},
        # Remove numbers, ., and -
    ])
    result = []
    for choice in response.choices:
        result.append(choice.message.content)
    # print(result)
    return(result)

def GPT_key_symptoms(disease):
    response = client.chat.completions.create(model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a Doctor"},
        {"role": "user", "content": f"Return a python list of the most likely symptoms that will indicate {disease} rather then any other disease, and say nothing else. Follow this format: ['symp1, symp2,symp3]"},
        # Remove numbers, ., and -
    ])
    result = []
    for choice in response.choices:
        result.append(choice.message.content)
    return(result)