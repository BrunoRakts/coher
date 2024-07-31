from flask import Flask, request, jsonify
import cohere
from dotenv import load_dotenv
import os

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Récupérer la clé API depuis les variables d'environnement
api_key = os.getenv('COHERE_API_KEY')

if api_key is None:
    raise ValueError("La clé API COHERE_API_KEY n'est pas définie dans le fichier .env")

# Initialiser le client Cohere avec la clé API
co = cohere.Client(api_key=api_key)

# Initialiser l'application Flask
app = Flask(__name__)

@app.route('/ask', methods=['GET'])
def ask():
    # Obtenir le message depuis les paramètres de la requête
    message = request.args.get('message', default='Bonjour! Qui es-tu ?', type=str)

    # Générer la réponse avec Cohere
    try:
        stream = co.chat_stream( 
            model='command-r-plus',
            message=message,
            temperature=0.3,
            chat_history=[],
            prompt_truncation='AUTO',
            connectors=[{"id":"web-search"}]
        )

        response_text = ''
        for event in stream:
            if event.event_type == "text-generation":
                response_text += event.text

        return jsonify({'response': response_text})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Exécuter l'application Flask
    app.run(host='0.0.0.0', port=5000)
