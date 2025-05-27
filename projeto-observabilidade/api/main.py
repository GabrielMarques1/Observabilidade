# -*- coding: utf-8 -*-
"""API simples em Flask com instrumentação Prometheus."""

import time
import random
from flask import Flask, request, jsonify
from prometheus_client import Counter, Histogram, Gauge, Summary, make_wsgi_app
from werkzeug.middleware.dispatcher import DispatcherMiddleware

# --- Métricas Prometheus ---
# Contador total de requisições por rota e método
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total de requisições HTTP recebidas',
    ['method', 'endpoint', 'http_status']
)

# Histograma de latência das requisições por rota e método
REQUEST_LATENCY = Histogram(
    'http_request_duration_seconds',
    'Latência das requisições HTTP em segundos',
    ['method', 'endpoint']
)

# Contador de erros por rota e método
ERROR_COUNT = Counter(
    'http_request_errors_total',
    'Total de erros HTTP encontrados',
    ['method', 'endpoint']
)

# --- Aplicação Flask ---
app = Flask(__name__)

# Mock de dados para livros
mock_books = [
    {"id": 1, "title": "Engenharia de Software Moderna", "author": "Marco Tulio Valente"},
    {"id": 2, "title": "Código Limpo", "author": "Robert C. Martin"},
    {"id": 3, "title": "O Programador Pragmático", "author": "Andrew Hunt, David Thomas"}
]
next_book_id = 4

# Middleware para instrumentar métricas antes e depois de cada request
@app.before_request
def before_request():
    request.start_time = time.time()

@app.after_request
def after_request(response):
    endpoint = request.path
    method = request.method
    status = response.status_code

    # Calcula latência
    latency = time.time() - request.start_time
    REQUEST_LATENCY.labels(method=method, endpoint=endpoint).observe(latency)

    # Incrementa contador de requisições
    REQUEST_COUNT.labels(method=method, endpoint=endpoint, http_status=status).inc()

    # Incrementa contador de erros se status >= 400
    if status >= 400:
        ERROR_COUNT.labels(method=method, endpoint=endpoint).inc()

    return response

# --- Endpoints da API ---
@app.route('/health', methods=['GET'])
def health_check():
    """Verifica a saúde da aplicação."""
    # Simula uma pequena chance de falha para testar métricas de erro
    # if random.random() < 0.1:
    #     return jsonify({"status": "unhealthy"}), 500
    return jsonify({"status": "ok"}), 200

@app.route('/books', methods=['GET'])
def get_books():
    """Retorna a lista de livros."""
    return jsonify(mock_books), 200

@app.route('/books', methods=['POST'])
def add_book():
    """Adiciona um novo livro (sem persistência real)."""
    global next_book_id
    try:
        data = request.get_json()
        if not data or 'title' not in data or 'author' not in data:
            raise ValueError("Payload inválido")

        new_book = {
            "id": next_book_id,
            "title": data['title'],
            "author": data['author']
        }
        # Não persiste, apenas simula adição
        # mock_books.append(new_book)
        next_book_id += 1
        return jsonify(new_book), 201
    except Exception as e:
        # Registra o erro antes de retornar a resposta
        endpoint = request.path
        method = request.method
        ERROR_COUNT.labels(method=method, endpoint=endpoint).inc()
        # Retorna erro 400 para payload inválido ou outros problemas
        return jsonify({"error": str(e)}), 400

# --- Integração com Prometheus ---
# Adiciona o middleware do Prometheus para expor /metrics
app_dispatch = DispatcherMiddleware(app, {
    '/metrics': make_wsgi_app()
})

if __name__ == '__main__':
    # Executa a aplicação Flask com o middleware do Prometheus
    # Use '0.0.0.0' para ser acessível externamente (inclusive pelo Docker)
    from waitress import serve
    serve(app_dispatch, host='0.0.0.0', port=5000)

