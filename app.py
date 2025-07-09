from flask import Flask, request, jsonify
from flask_cors import CORS
import json

# Inicializa o aplicativo Flask
app = Flask(__name__)
# Permite que outros sites (como o seu Google Sites) acessem esta API
CORS(app) 

# Carrega o arquivo de "memória" do Léo assim que o programa inicia
with open('intents.json', 'r', encoding='utf-8') as f:
    intents = json.load(f)

def get_bot_response(user_message):
    """
    Esta função procura a mensagem do usuário no arquivo de intenções
    e retorna a resposta correspondente.
    """
    message = user_message.lower() # Converte a mensagem para minúsculas para facilitar a busca

    # Procura em todas as intenções cadastradas
    for intent in intents['intents']:
        # Procura em todos os padrões (perguntas) daquela intenção
        for pattern in intent['patterns']:
            if pattern in message:
                # Se encontrar um padrão correspondente, retorna a resposta daquela intenção
                return intent['responses'][0]
    
    # Se não encontrar nenhuma resposta, retorna uma mensagem padrão
    return "Desculpe, não entendi bem. Você poderia reformular sua pergunta? Você também pode pedir para falar com um atendente ou solicitar um orçamento."

# Define a rota principal do chat, que "escuta" por novas mensagens
@app.route('/chat', methods=['POST'])
def chat():
    # Pega a mensagem que o usuário enviou
    data = request.get_json()
    user_message = data.get('message')

    # Verifica se a mensagem não está vazia
    if not user_message:
        return jsonify({'error': 'Nenhuma mensagem recebida'}), 400
    
    # Pega a resposta do Léo usando a função que criamos
    bot_response = get_bot_response(user_message)
    
    # Envia a resposta de volta para a interface do chat
    return jsonify({'response': bot_response})

# A linha abaixo é usada apenas para testes locais. 
# O Gunicorn (no Render) irá iniciar o app de outra forma.
if __name__ == '__main__':
    app.run(debug=True)