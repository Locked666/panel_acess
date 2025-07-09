# Panel Access

Bem-vindo ao **Panel Access**, um sistema desenvolvido em Python para gerenciar e controlar acessos de forma eficiente e segura. Este projeto foi criado com o objetivo de facilitar a administração de permissões e acessos em diferentes ambientes.

## 🚀 Funcionalidades

- **Gerenciamento de Usuários**: Criação, edição e exclusão de usuários.
- **Controle de Acessos**: Definição de permissões específicas para cada usuário.
- **Logs de Atividade**: Registro detalhado de todas as ações realizadas no sistema.
- **Interface Intuitiva**: Design simples e fácil de usar.

## 🛠️ Tecnologias Utilizadas

- **Python**: Linguagem principal do projeto.
- **Bibliotecas**: 
    - `Flask` para o backend.
    - `SQLAlchemy` para gerenciamento do banco de dados.
    - `Jinja2` para renderização de templates.
- **Banco de Dados**: SQLite (ou outro banco de sua escolha).

## 📦 Instalação

1. Clone este repositório:
     ```bash
     git clone https://github.com/Locked666/panel-access.git
     ```
2. Acesse o diretório do projeto:
     ```bash
     cd panel-access
     ```
3. Crie um ambiente virtual e ative:
     ```bash
     python -m venv venv # No Windows: venv\Scripts\activate
     source venv/bin/activate 
     ```
4. Instale as dependências:
     ```bash
     pip install -r requirements.txt
     ```
5. Execute o sistema:
     ```bash
     python app.py
     ```

## 📖 Como Usar

1. Acesse o sistema pelo navegador em `http://localhost:5000`.
2. Faça login com suas credenciais.
3. Navegue pelas opções para gerenciar usuários e acessos.

## 🤝 Contribuição

Contribuições são bem-vindas! Siga os passos abaixo para contribuir:

1. Faça um fork do repositório.
2. Crie uma branch para sua feature:
     ```bash
     git checkout -b minha-feature
     ```
3. Faça commit das suas alterações:
     ```bash
     git commit -m "Minha nova feature"
     ```
4. Envie para o repositório remoto:
     ```bash
     git push origin minha-feature
     ```
5. Abra um Pull Request.


# ⏏ Telas:

## Tela de Login. 
* Adicionado tela de Login com validação de credencias.

![Imagem Tela de Login com Validação](.\img_md\img_validacao.png)

## Tela de Home. 
* Tela Home, com Dashboards e Cards com informações pricipais. 
* Adicionado SidBar Lateral. 

![Imagem Tela de Home](.\.\img_md\img_home.png)

## Telas de Cadastros. 

* Tela de Cadastros de Usuários e Viagens com Filtros e Crud Completo.
* Adicionado Validação de Busca de dados.  

![Imagem Tela de Usuários](.\.\img_md\img_users.png)  ![Imagem Tela de Viagens](.\.\img_md\img_viagens.png)


## Telas de Usuaios Comuns. 

* Adicionado tela de Cadastro de Viagens, com possibilidade de adicionar Gastos com imagens e calculo dinamico de valor realizado pelo backend. 

![Imagem de tela de cadastro de viagens](.\.\img_md\img_cadastro.png)

![Imagem de tela de cadastro de gasto](.\.\img_md\img_add_gastos.png)

## 💥 Extras: 

* O sistema e desenvolvido com base em permissão de usuario, permitindo que os usuários adicionados possam ser adicionados como Administradores ou usuários comuns, sem acesso a parte de administrador. 

* Os usuários também, pode ser setados como "Diarista" que  utiliza para cadastro de viagens, caso não forem marcados não podem lançar viagem. 


## 📄 Licença

Este projeto está licenciado sob a [MIT License](LICENSE).

---

Desenvolvido com ❤️ por [Julio Sales](https://github.com/Locked666).