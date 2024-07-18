# Cidade Solidária

Este é um projeto de um aplicativo de cadastro de ações sociais e problemas na cidade, desenvolvido com Streamlit. O aplicativo permite que visitantes e usuários cadastrados vejam um mapa com os problemas e ações sociais, e que usuários cadastrados registrem novos problemas.

## Estrutura do Projeto

```
cidade_solidaria/
│
├── app.py
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

Crie um arquivo `.env` na raiz do projeto com o seguinte conteúdo:

```
# .env
ENVIRONMENT=development
DATABASE_URL_LOCAL=sqlite:///data.db
DATABASE_URL_DOCKER=postgresql://yourusername:yourpassword@localhost/yourdatabase
DATABASE_URL_PRODUCTION=postgresql://yourusername:yourpassword@production_host/yourdatabase
API_KEY=your_opencage_api_key
```

Substitua `yourusername`, `yourpassword`, `yourdatabase` e `your_opencage_api_key` pelos valores apropriados.

### 3. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 4. Executar a Aplicação Localmente com SQLite

```bash
streamlit run streamlit_app.py 
```

### 5. Executar a Aplicação com Docker

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

### 6. Executar a Aplicação em Produção

1. Defina a variável de ambiente `ENVIRONMENT` como `production` no arquivo `.env`.
2. Configure o banco de dados PostgreSQL de produção com as credenciais apropriadas.
3. Faça o deploy da aplicação para o ambiente de produção seguindo as práticas recomendadas para o seu provedor de hospedagem.

## Estrutura dos Arquivos

### `streamlit_app.py`

Contém a lógica principal do aplicativo Streamlit, incluindo autenticação, visualização do mapa, e formulários para registro de problemas e ações sociais.

### `database.py`

Configurações do SQLAlchemy para conexão com SQLite ou PostgreSQL, definição das tabelas e funções auxiliares para manipulação dos dados.

### `docker-compose.yml`

Configura um contêiner Docker para o PostgreSQL.

### `example.env`

Arquivo de variáveis de ambiente contendo configurações sensíveis e específicas para cada ambiente (desenvolvimento, Docker, produção).

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

### Conclusão

Esse README fornece uma visão completa do projeto, incluindo a estrutura dos arquivos, as funcionalidades, os requisitos, e as instruções de configuração e execução. Com isso, qualquer desenvolvedor deve ser capaz de configurar e rodar o projeto facilmente. Se precisar de mais alguma coisa ou tiver outras dúvidas, estou à disposição!