from flask import Flask, jsonify, request

app = Flask(__name__)

# Ranking em memória (Stateless para o Docker)
ranking = []

@app.route('/ranking', methods=['GET'])
def obter_ranking():
    # Retorna o ranking ordenado por pontos (do maior para o menor)
    ranking_ordenado = sorted(ranking, key=lambda x: x['pontos'], reverse=True)
    return jsonify(ranking_ordenado)

@app.route('/registrar', methods=['POST'])
def registrar_pontos():
    dados = request.get_json()
    if not dados or 'nome' not in dados or 'pontos' not in dados:
        return jsonify({"erro": "Dados inválidos"}), 400
    
    ranking.append(dados)
    return jsonify({"status": "Sucesso", "ranking_atual": ranking}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)