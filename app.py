from flask import Flask, redirect, url_for, request, render_template, session
import requests, os, uuid, json
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def index_post():
    #Ler o texto que o usuário inseriu e o idioma selecionado no formulário
    original_text = request.form['text']
    target_language = request.form['language']

    #Ler as variáveis ambientais criadas no arquivo .env
    key = os.environ['KEY']
    endpoint = os.environ['ENDPOINT']
    location = os.environ['LOCATION']

    #Indica o que se deseja traduzir, a versão da API (3.0) e o idioma selecionado
    path = '/translate?api-version=3.0'
    #Adiciona o parâmetro de seleção do idioma
    target_language_parameter = '&to=' + target_language
    #Cria a URL completa
    constructed_url = endpoint + path + target_language_parameter
    
    #Configura as informações de cabeçalho, que incluem nossa chave de assinatura, o local do serviço e uma ID arbitrária para a tradução
    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    #Cria o corpo da requisição com o texto a ser traduzido
    body = [{'text': original_text}]

    #Faz a chamada usando o método POST
    translator_request = requests.post(constructed_url, headers=headers, json=body)
    #Recupera a resposta JSON do servidor
    translator_response = translator_request.json()
    #Recupera a tradução
    translated_text = translator_response[0]['translations'][0]['text']

    #Retorna render_template, passando o texto traduzido, o texto original e o idioma selecionado para o template
    return render_template(
        'results.html',
        translated_text=translated_text,
        original_text=original_text,
        target_language=target_language
    )



