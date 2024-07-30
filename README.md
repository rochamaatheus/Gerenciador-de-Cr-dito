# Gerenciador de Créditos e Débitos

Este projeto é uma aplicação simples em Python para gerenciar créditos e débitos, utilizando Tkinter para a interface gráfica e SQLite para o banco de dados. A aplicação permite adicionar créditos, registrar débitos, limpar débitos antigos e atualizar o saldo com base na passagem do tempo.

## Funcionalidades

- **Adicionar Crédito**: Permite adicionar um valor de crédito ao banco de dados.
- **Registrar Débito**: Permite registrar um débito com item, valor e número de parcelas.
- **Limpar Débitos Antigos**: Remove débitos que já foram completamente pagos.
- **Atualizar Saldo**: Calcula e exibe o saldo atual, considerando a passagem do tempo e os débitos pagos.

## Estrutura do Projeto

- **Database**: Utiliza SQLite para armazenar informações de créditos e débitos.
- **Interface Gráfica**: Utiliza Tkinter para a criação da interface gráfica do usuário (GUI).

## Como Executar

### Pré-requisitos

- Python 3.x
- Bibliotecas `tkinter` e `sqlite3` (já incluídas na instalação padrão do Python)

### Passo a Passo

1. **Clone o repositório**:

   ```sh
   git clone https://github.com/rochamaatheus/Gerenciador-de-Cr-dito.git
   cd seu-repositorio
   ```

2. **Execute o Script**:

   ```sh
    python gerenciador_creditos.py
   ```

ou inicie o seu .exe

## Interface do Usuário

- **Adicionar Crédito**: Insira um valor e clique em "Adicionar".
- **Registrar Débito**: Insira o item, valor, número de parcelas e clique em "Registrar".
- **Limpar Débitos** Antigos: Clique em "Limpar Débitos Antigos".
- **Atualizar Saldo**: Insira o número de meses passados (opcional) e clique em "Atualizar Saldo".
- **Saldo Atual**: O saldo atual será exibido na interface.

## Código Fonte

### Funções Principais

`execute_db_query(query, params=())`
Função para executar consultas ao banco de dados SQLite.

`add_credit()`
Função para adicionar um crédito ao banco de dados.

`add_debt()`
Função para registrar um débito no banco de dados.

`clean_old_debts()`
Função para limpar débitos antigos que já foram pagos.

`update_balance(discount_first_installment=False)`
Função para atualizar o saldo atual considerando créditos e débitos.

`clear_entries()`
Função para limpar os campos de entrada da interface.

## Estrutura da Interface Tkinter

- **Adicionar Crédito**
- **Registrar Débito**
- **Limpar Débitos Antigos**
- **Atualizar Saldo**
- **Saldo Atual**

## Contato

Se você tiver alguma dúvida ou precisar de assistência adicional, fique à vontade para entrar em contato através do LinkedIn, Instagram ou por e-mail. As informações de contato estão disponíveis na minha página principal do GitHub.

---

👨‍💻 Criado por [rochamaatheus](https://github.com/rochamaatheus).
