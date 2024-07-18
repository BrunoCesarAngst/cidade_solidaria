### Cidade Solidária

Este é um projeto de um aplicativo de cadastro de ações sociais e problemas na cidade, desenvolvido com Streamlit. O aplicativo permite que visitantes e usuários cadastrados vejam um mapa com os problemas e ações sociais, e que usuários cadastrados registrem novos problemas.

## Estrutura do Projeto

```
cidade_solidaria/
│
├── .streamlit/
│   └── secrets.toml
├── streamlit_app.py
├── database.py
├── docker-compose.yml
├── .env
├── requirements.txt
└── Dockerfile
```

## Funcionalidades

- **Visitantes:**
  - Visualização de problemas e ações sociais no mapa
  - Visualização de descrições dos pontos no mapa

- **Usuários Cadastrados:**
  - Todas as funcionalidades dos visitantes
  - Registro de novos pontos no mapa
  - Cadastro de novos usuários

- **Admin:**
  - Visualização e gerenciamento de todos os pontos cadastrados

## Requisitos

- Python 3.7+
- Docker (opcional, para ambiente Docker)
- PostgreSQL (opcional, para ambiente Docker ou produção)

## Configuração

### 1. Clonar o Repositório

```bash
git clone https://github.com/seu-usuario/cidade_solidaria.git
cd cidade_solidaria
```

### 2. Criar e Configurar o Arquivo `.env`

Crie um arquivo `.env` na raiz do projeto com o conteudo de example.env:

### 3. Criar e Configurar o Arquivo `secrets.toml`

Crie um diretório `.streamlit` e adicione o arquivo `secrets.toml` com o seguinte conteúdo:

```toml
# Variáveis de ambiente gerais
[general]
ENVIRONMENT = "development"
api_key = "your_opencage_api_key"

# Credenciais do banco de dados
db_username = "your_db_username"
db_password = "your_db_password"

# URLs de banco de dados para diferentes ambientes
[database]
url_local = "sqlite:///data.db"
url_docker = "postgresql://postgres:postgres@localhost/postgres"
url_production = "postgresql://your_db_username:your_db_password@production_host/your_database"
```

Substitua `your_db_username`, `your_db_password`, `your_opencage_api_key`, e as URLs do banco de dados pelos valores apropriados.

### 4. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 5. Executar a Aplicação Localmente com SQLite

```bash
streamlit run streamlit_app.py
```

### 6. Executar a Aplicação com Docker

#### Iniciar o PostgreSQL com Docker Compose

```bash
docker-compose up -d
```

#### Construir a Imagem Docker

```bash
docker build -t cidade_solidaria .
```

#### Executar a Aplicação com Docker

```bash
docker run -p 8501:8501 --env-file .env cidade_solidaria
```

### 7. Executar a Aplicação em Produção

1. Defina a variável de ambiente `ENVIRONMENT` como `production` no arquivo `.env`.
2. Configure o banco de dados PostgreSQL de produção com as credenciais apropriadas.
3. Faça o deploy da aplicação para o ambiente de produção seguindo as práticas recomendadas para o seu provedor de hospedagem.

## Estrutura dos Arquivos

### `.streamlit/secrets.toml`

Contém segredos e variáveis de ambiente sensíveis, como credenciais de banco de dados e chaves de API.

### `streamlit_app.py`

Contém a lógica principal do aplicativo Streamlit, incluindo autenticação, visualização do mapa, e formulários para registro de problemas e ações sociais.

### `database.py`

Configurações do SQLAlchemy para conexão com SQLite ou PostgreSQL, definição das tabelas e funções auxiliares para manipulação dos dados.

### `docker-compose.yml`

Configura um contêiner Docker para o PostgreSQL.

### `.env`

Arquivo de variáveis de ambiente contendo configurações específicas para cada ambiente (desenvolvimento, Docker, produção).

### `requirements.txt`

Lista de dependências do projeto.

### `Dockerfile`

Define a construção da imagem Docker para o aplicativo Streamlit.

## Como Contribuir

1. Fork o repositório
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -am 'Adicione uma nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Crie um novo Pull Request

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para mais detalhes.