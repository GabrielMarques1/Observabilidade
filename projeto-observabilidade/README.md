
## Integrantes


- Edimar Gabriel Marques Mina - 37021899

## Estrutura do Projeto

```
projeto-observabilidade/
├── api/
│   ├── Dockerfile
│   ├── main.py
│   └── requirements.txt
├── prometheus/
│   └── prometheus.yml
├── docker-compose.yml
└── README.md
```

## Funcionalidades

- **API Flask (`api/main.py`)**:
    - `GET /health`: Retorna o status de saúde da aplicação.
    - `GET /books`: Retorna uma lista mock de livros.
    - `POST /books`: Simula a adição de um livro (sem persistência).
    - `GET /metrics`: Expõe métricas no formato Prometheus, incluindo:
        - `http_requests_total`: Total de requisições por rota, método e status.
        - `http_request_duration_seconds`: Histograma da latência das requisições por rota e método.
        - `http_request_errors_total`: Contador de erros (status >= 400) por rota e método.
- **Prometheus (`prometheus/prometheus.yml`)**:
    - Configurado para coletar (scrape) as métricas expostas pela API Flask no endpoint `/metrics` a cada 15 segundos.
- **Grafana**:
    - Serviço configurado para visualização das métricas coletadas pelo Prometheus.
- **Docker Compose (`docker-compose.yml`)**:
    - Orquestra a execução dos containers da API, Prometheus e Grafana.
    - Define as redes e volumes necessários.

## Como Executar

1.  **Pré-requisitos**:
    - Docker e Docker Compose instalados.
2.  **Clone o repositório** (ou descompacte o arquivo .zip fornecido).
3.  **Navegue até o diretório raiz do projeto** (`projeto-observabilidade`).
4.  **Execute o Docker Compose**:
    ```bash
    sudo docker compose up -d --build
    ```
    *Observação: Pode ser necessário usar `sudo` dependendo das permissões do Docker na sua máquina.*

5.  **Acesse os serviços**:
    - **API**: `http://localhost:5000` (ex: `http://localhost:5000/books`, `http://localhost:5000/metrics`)
    - **Prometheus**: `http://localhost:9090`
    - **Grafana**: `http://localhost:3000` (Login padrão: `admin` / `admin`. Será solicitado alterar a senha no primeiro login).

6.  **Configurar o Grafana (se necessário)**:
    - Acesse o Grafana (`http://localhost:3000`).
    - Faça login (admin/admin).
    - Navegue até "Connections" -> "Data sources".
    - O datasource "Prometheus" já deve estar configurado. Se não estiver, adicione um novo datasource do tipo Prometheus:
        - **Nome**: Prometheus (ou qualquer nome desejado)
        - **URL**: `http://prometheus:9090` (O Grafana acessa o Prometheus pelo nome do serviço dentro da rede Docker)
        - Clique em "Save & test".
    - Crie um novo dashboard e adicione painéis utilizando o datasource Prometheus para visualizar as métricas (ex: `http_requests_total`, `http_request_duration_seconds_sum`, `http_request_errors_total`).

## Parar a Execução

Para parar os containers, execute no diretório raiz do projeto:

```bash
sudo docker compose down
```

# o b s e r v a b i l i d a d e 
 
 
