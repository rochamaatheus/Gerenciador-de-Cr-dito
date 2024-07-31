import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta
import sqlite3
import openpyxl
from openpyxl.styles import Font, Alignment

# Função para gerenciar a conexão com o banco de dados
def execute_db_query(query, params=()):
    with sqlite3.connect('finance.db') as conn:
        c = conn.cursor()
        c.execute(query, params)
        conn.commit()
        return c

# Criação das tabelas de créditos e débitos
execute_db_query('''
    CREATE TABLE IF NOT EXISTS credits (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        amount REAL,
        date TEXT
    )
''')
execute_db_query('''
    CREATE TABLE IF NOT EXISTS debts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item TEXT,
        amount REAL,
        installments INTEGER,
        date TEXT
    )
''')
execute_db_query('''
    CREATE TABLE IF NOT EXISTS fixed_expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item TEXT,
        amount REAL,
        date TEXT
    )
''')
execute_db_query('''
    CREATE TABLE IF NOT EXISTS monthly_salaries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        month TEXT,
        amount REAL,
        is_default INTEGER DEFAULT 0
    )
''')

# Função para adicionar crédito
def add_credit():
    try:
        amount = float(credit_entry.get())
        date = datetime.now().strftime('%Y-%m-%d')
        execute_db_query('INSERT INTO credits (amount, date) VALUES (?, ?)', (amount, date))
        messagebox.showinfo('Sucesso', 'Crédito adicionado com sucesso!')
        update_balance()
        clear_entries()
    except ValueError:
        messagebox.showerror('Erro', 'Por favor, insira um valor válido para o crédito.')

# Função para registrar débito
def add_debt():
    try:
        item = debt_item_entry.get()
        amount = float(debt_amount_entry.get())
        installments = int(debt_installments_entry.get())
        date = datetime.now().strftime('%Y-%m-%d')
        execute_db_query('INSERT INTO debts (item, amount, installments, date) VALUES (?, ?, ?, ?)', (item, amount, installments, date))
        messagebox.showinfo('Sucesso', 'Débito registrado com sucesso!')
        update_balance(discount_first_installment=True)
        clear_entries()
    except ValueError:
        messagebox.showerror('Erro', 'Por favor, insira valores válidos para o débito.')

# Função para adicionar despesa fixa
def add_fixed_expense():
    try:
        item = fixed_expense_item_entry.get()
        amount = float(fixed_expense_amount_entry.get())
        date = datetime.now().strftime('%Y-%m-%d')
        execute_db_query('INSERT INTO fixed_expenses (item, amount, date) VALUES (?, ?, ?)', (item, amount, date))
        messagebox.showinfo('Sucesso', 'Despesa Fixa adicionada com sucesso!')
        update_balance(discount_first_installment=True)
        clear_entries()
    except ValueError:
        messagebox.showerror('Erro', 'Por favor, insira valores válidos para a despesa fixa.')

# Função para adicionar salário
def add_salary():
    try:
        amount = float(salary_entry.get())
        month = salary_month_entry.get()
        is_default = int(default_salary_var.get())
        execute_db_query('INSERT INTO monthly_salaries (month, amount, is_default) VALUES (?, ?, ?)', (month, amount, is_default))
        messagebox.showinfo('Sucesso', 'Salário adicionado com sucesso!')
        update_balance()
        clear_entries()
    except ValueError:
        messagebox.showerror('Erro', 'Por favor, insira valores válidos para o salário.')

# Função para atualizar salário
def update_salary():
    try:
        amount = float(salary_entry.get())
        month = salary_month_entry.get()
        execute_db_query('UPDATE monthly_salaries SET amount = ? WHERE month = ?', (amount, month))
        messagebox.showinfo('Sucesso', 'Salário atualizado com sucesso!')
        update_balance()
        clear_entries()
    except ValueError:
        messagebox.showerror('Erro', 'Por favor, insira valores válidos para o salário.')

# Função para limpar débitos antigos que já foram completamente pagos
def clean_old_debts():
    debts = execute_db_query('SELECT id, installments, date FROM debts').fetchall()
    current_date = datetime.now()

    for debt_id, installments, date in debts:
        debt_date = datetime.strptime(date, '%Y-%m-%d')
        months_passed = (current_date.year - debt_date.year) * 12 + current_date.month - debt_date.month
        if months_passed >= installments:
            execute_db_query('DELETE FROM debts WHERE id = ?', (debt_id,))

# Função para calcular os débitos
def calculateDebts(total_debts, debts, current_date, discount_first_installment, months_to_add):
    for amount, installments, date in debts:
        print("Entrou no Loop de \"debts\"")
        debt_date = datetime.strptime(date, '%Y-%m-%d')
        months_passed = (current_date.year - debt_date.year) * 12 + current_date.month - debt_date.month + months_to_add
        print(f"Meses passados: {months_passed}")

        if discount_first_installment:
            paid_installments = 1
        else:
            paid_installments = min(months_passed, installments)

        total_debts += (amount / installments) * paid_installments
        print(f"Débitos totais: {total_debts}")

    return total_debts

# Função para atualizar o saldo
def update_balance(discount_first_installment=False):
    print("-"*20)
    total_credits = execute_db_query('SELECT SUM(amount) FROM credits').fetchone()[0] or 0
    print(f"Créditos: {total_credits}")
    debts = execute_db_query('SELECT amount, installments, date FROM debts').fetchall()
    print(f"Débitos: {debts}")

    total_debts = 0
    current_date = datetime.now()
    months_to_add = int(months_entry.get()) if months_entry.get().isdigit() else 0

    # Salário padrão
    default_salary = execute_db_query('SELECT amount FROM monthly_salaries WHERE is_default = 1').fetchone()
    default_salary = default_salary[0] if default_salary else 0
    print(f"Salário padrão: {default_salary}")

    total_salaries = 0
    for month_offset in range(months_to_add + 1):
        simulated_date = current_date + timedelta(days=30 * month_offset)
        month_str = simulated_date.strftime('%Y-%m')
        salary_for_month = execute_db_query('SELECT amount FROM monthly_salaries WHERE month = ?', (month_str,)).fetchone()
        print(f"DB Salário por Mês: {salary_for_month}")
        if salary_for_month:
            total_salaries += salary_for_month[0]
            print(f"Salário Total POR MÊS: {total_salaries}")
        else:
            total_salaries += default_salary
            print(f"Salário Total: {total_salaries}")

    total_debts = calculateDebts(total_debts, debts, current_date, discount_first_installment, months_to_add)

    balance = total_credits + total_salaries - total_debts
    balance_label.config(text=f'Saldo Atual: {balance:.2f} reais')
    print(f"Saldo total: {balance}")

# Função para limpar os campos de entrada
def clear_entries():
    credit_entry.delete(0, tk.END)
    debt_item_entry.delete(0, tk.END)
    debt_amount_entry.delete(0, tk.END)
    debt_installments_entry.delete(0, tk.END)
    fixed_expense_item_entry.delete(0, tk.END)
    fixed_expense_amount_entry.delete(0, tk.END)
    salary_entry.delete(0, tk.END)
    salary_month_entry.delete(0, tk.END)
    months_entry.delete(0, tk.END)

# Função para exportar os dados para um arquivo Excel
def export_to_excel():
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = 'Relatório Financeiro'

    headers = ['ID', 'Tipo', 'Item', 'Valor', 'Parcelas', 'Data']
    sheet.append(headers)
    for cell in sheet[1]:
        cell.font = Font(bold=True)
        cell.alignment = Alignment(horizontal='center')

    credits = execute_db_query('SELECT id, amount, date FROM credits').fetchall()
    for credit in credits:
        sheet.append([credit[0], 'Crédito', '', credit[1], '', credit[2]])

    debts = execute_db_query('SELECT id, item, amount, installments, date FROM debts').fetchall()
    for debt in debts:
        sheet.append([debt[0], 'Débito', debt[1], debt[2], debt[3], debt[4]])

    salaries = execute_db_query('SELECT id, month, amount FROM monthly_salaries').fetchall()
    for salary in salaries:
        sheet.append([salary[0], 'Salário', '', salary[2], '', salary[1]])

    fixed_expenses = execute_db_query('SELECT id, item, amount, date FROM fixed_expenses').fetchall()
    for expense in fixed_expenses:
        sheet.append([expense[0], 'Despesa Fixa', expense[1], expense[2], '', expense[3]])

    workbook.save('relatorio_financeiro.xlsx')
    messagebox.showinfo('Sucesso', 'Relatório exportado com sucesso!')

# Configuração da interface Tkinter
root = tk.Tk()
root.title('Gerenciador Financeiro')

# Configuração das labels e entries para crédito
tk.Label(root, text='Adicionar Crédito').grid(row=0, column=0, pady=10)
credit_entry = tk.Entry(root)
credit_entry.grid(row=0, column=1)
tk.Button(root, text='Adicionar', command=add_credit).grid(row=0, column=2)

# Configuração das labels e entries para débito
tk.Label(root, text='Registrar Débito').grid(row=1, column=0, pady=10)
debt_item_entry = tk.Entry(root)
debt_item_entry.grid(row=1, column=1)
tk.Label(root, text='Valor').grid(row=1, column=2, pady=10)
debt_amount_entry = tk.Entry(root)
debt_amount_entry.grid(row=1, column=3, pady=10)
tk.Label(root, text='Parcelas').grid(row=1, column=4, pady=10)
debt_installments_entry = tk.Entry(root)
debt_installments_entry.grid(row=1, column=5, pady=10)
tk.Button(root, text='Registrar', command=add_debt).grid(row=1, column=6, pady=10, padx=10)

# Configuração das labels e entries para despesas fixas
tk.Label(root, text='Adicionar Despesa Fixa').grid(row=2, column=0, pady=10)
fixed_expense_item_entry = tk.Entry(root)
fixed_expense_item_entry.grid(row=2, column=1, pady=10)
tk.Label(root, text='Valor').grid(row=2, column=2, pady=10)
fixed_expense_amount_entry = tk.Entry(root)
fixed_expense_amount_entry.grid(row=2, column=3, pady=10)
tk.Button(root, text='Adicionar', command=add_fixed_expense).grid(row=2, column=4, pady=10)

# Configuração das labels e entries para salários
tk.Label(root, text='Adicionar Salário').grid(row=3, column=0, pady=10)
salary_entry = tk.Entry(root)
salary_entry.grid(row=3, column=1, pady=10)
tk.Label(root, text='Mês (YYYY-MM)').grid(row=3, column=2, pady=10)
salary_month_entry = tk.Entry(root)
salary_month_entry.grid(row=3, column=3, pady=10)
default_salary_var = tk.IntVar()
tk.Checkbutton(root, text='Salário Padrão', variable=default_salary_var).grid(row=3, column=4, pady=10)
tk.Button(root, text='Adicionar', command=add_salary).grid(row=3, column=5, pady=10)
tk.Button(root, text='Atualizar', command=update_salary).grid(row=3, column=6, pady=10)

# Configuração das labels e entries para meses de simulação
tk.Label(root, text='Simular Meses').grid(row=4, column=0, pady=10)
months_entry = tk.Entry(root)
months_entry.grid(row=4, column=1, pady=10)
tk.Button(root, text='Simular', command=update_balance).grid(row=4, column=2, pady=10)

# Configuração do botão para exportar para Excel
tk.Button(root, text='Exportar para Excel', command=export_to_excel).grid(row=5, column=0, pady=10)

# Label para exibir o saldo atual
balance_label = tk.Label(root, text='Saldo Atual: 0.00 reais')
balance_label.grid(row=6, column=0, columnspan=2, pady=10)

# Botão para limpar débitos antigos
tk.Button(root, text='Limpar Débitos Antigos', command=clean_old_debts).grid(row=5, column=1, pady=10)

# Inicialização do saldo
update_balance()

# Inicia o loop principal do Tkinter
root.mainloop()
