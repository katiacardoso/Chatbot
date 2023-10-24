#python -m pip install --upgrade pip
#python --version: 3.9 (64-bits)
import json
#pip install requests
import requests
from io import StringIO
#pip install numpy
#import numpy as np
#pip install pandas
import pandas as pd
#pip install torch
import torch
#pip install transformers
from transformers import BertTokenizer, BertModel
#pip install -U scikit-learn
from sklearn.metrics.pairwise import cosine_similarity
from flask import Flask, render_template, request

#import json 

#pip install Flask

#importação dos dados
url = 'https://raw.githubusercontent.com/katiacardoso/EMAP_Chatbot/main/perguntas_respostass.csv'

# Baixar o conteúdo do arquivo usando requests
response = requests.get(url)

# Verificar se a requisição foi bem-sucedida
if response.status_code == 200:
# Criar um objeto pandas DataFrame a partir do conteúdo baixado
  df = pd.read_csv(StringIO(response.text), usecols=['Pergunta', 'Resposta'])
# Agora você pode usar o DataFrame 'data' normalmente
else:
  print("Falha ao baixar o arquivo. Código de status:", response.status_code)


#df.to_csv('perguntas_respostass.csv', index=False)

# Carregue o modelo BERT pré-treinado e o tokenizador
model_name = "bert-base-multilingual-uncased"
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertModel.from_pretrained(model_name)

# Carregue o arquivo CSV com perguntas e respostas
#df = pd.read_csv("perguntas_respostass.csv")

# Converter os dados para um formato adequado para JSON
data = []
for index, row in df.iterrows():
    pergunta = row['Pergunta']
    resposta = row['Resposta']
    data.append({'pergunta': pergunta, 'resposta': resposta})


# Salvar os dados como JSON em um arquivo
with open('perguntas_respostas.json', 'w', encoding='utf-8') as json_file:
    json.dump(data, json_file, ensure_ascii=False, indent=4)

# Carregar dados do arquivo JSON
with open('perguntas_respostas.json', 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)

# Extrair perguntas e respostas
perguntas = [qa['pergunta'] for qa in data]
respostas = [qa['resposta'] for qa in data]


app = Flask(__name__,template_folder='templates')


# Função para vetorizar texto usando BERT
def vetorizar_texto(texto):
    inputs = tokenizer(texto, return_tensors='pt', padding=True, truncation=True)
    with torch.no_grad():
        outputs = model(**inputs)
    embeddings = torch.mean(outputs.last_hidden_state, dim=1)  
  # Média das embeddings das palavras
    return embeddings

# Vetorizar perguntas usando BERT
perguntas_embeddings = torch.cat([vetorizar_texto(pergunta) for pergunta in perguntas])

# Função para encontrar a melhor resposta com base na pergunta do usuário
def chatbot(user_input):
    user_input_embedding = vetorizar_texto(user_input)
    similarity_scores = cosine_similarity(user_input_embedding, perguntas_embeddings)
    best_match_index = similarity_scores.argmax()
    resposta = respostas[best_match_index]
    return resposta

#Isso garantirá que o Flask aceite solicitações com conteúdo JSON
app.config['JSON_AS_ASCII'] = False

# Rota para a página inicial
@app.route('/')
def index():
    return render_template('index.html')

# Rota para processar a entrada do usuário e retornar a resposta do chatbot
@app.route('/get_response', methods=['POST'])
def get_response():
    '''user_input = request.form['user_input']
    response = chatbot(user_input)
    #return render_template('index.html', user_input=user_input, response=response)
    return response'''
    data = request.get_json()  # Obter dados JSON da requisição
    user_input = data.get('user_input', '')  # Obter 'user_input' do JSON
    response = chatbot(user_input)  # Obter resposta do chatbot
    return  response  # Retornar resposta como uma string simples

if __name__ == '__main__':
    app.run(debug=True)



'''# Lista para armazenar as perguntas e respostas
conversa = []

# Inicie uma conversa com o chatbot
while True:
    user_input = input("Você: ")
    if user_input.lower() == "sair":
        print("Chatbot: Adeus! Até logo.")
        break
    response = chatbot(user_input)
    print("Chatbot:", response)

    # Armazene a pergunta do usuário e a resposta do chatbot na lista
    conversa.append({'pergunta': user_input, 'resposta': response})

    # Salve a lista como JSON em um arquivo
    with open('conversa.json', 'a', encoding='utf-8') as json_file:
        json.dump(conversa, json_file, ensure_ascii=False, indent=4)'''

