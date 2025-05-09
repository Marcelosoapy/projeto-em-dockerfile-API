📦 Projeto - API REST + Frontend para Cadastro de Veículos

Este projeto consiste em:

Uma API REST (FastAPI + SQLite) para gerenciamento de veículos.

Um Frontend (HTML + JavaScript) servido por Nginx.

Containers Docker para facilitar a execução.


🚀 Tecnologias Utilizadas

FastAPI

SQLite

Nginx

Docker

Docker Compose


⚙ Como Rodar o Projeto
Requisitos: Docker e Docker Compose instalados na máquina.

Clone o repositório:

bash
Copiar
Editar
git clone https://github.com/seu-usuario/seu-projeto.git
cd seu-projeto
Suba os containers:

bash
Copiar
Editar
docker-compose up --build
Acesse no navegador:

Frontend: http://localhost:8080

Backend (API): http://localhost:8000/docs → (documentação automática Swagger UI)


🎯 Funcionalidades da API

Cadastrar veículo: POST /veiculos/

Listar todos os veículos: GET /veiculos/

Buscar veículo específico: GET /veiculos/{id}

Atualizar veículo: PUT /veiculos/{id}

Deletar veículo: DELETE /veiculos/{id}

A API segue boas práticas REST e inclui HATEOAS nos retornos, indicando links para navegação entre recursos.




📑 Observações

Banco de dados SQLite é criado automaticamente no container da API (veiculos.db).

O Frontend faz chamadas AJAX para a API (não precisa recarregar a página).

O projeto foi estruturado para ser facilmente escalável.#   p r o j e t o - e m - d o c k e r f i l e - A P I 
 
 
