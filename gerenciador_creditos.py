import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta
import sqlite3

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

# Função para limpar débitos antigos que já foram completamente pagos
def clean_old_debts():
    debts = execute_db_query('SELECT id, installments, date FROM debts').fetchall()
    current_date = datetime.now()

    for debt_id, installments, date in debts:
        debt_date = datetime.strptime(date, '%Y-%m-%d')
        months_passed = (current_date.year - debt_date.year) * 12 + current_date.month - debt_date.month
        if months_passed >= installments:
            execute_db_query('DELETE FROM debts WHERE id = ?', (debt_id,))

    messagebox.showinfo('Sucesso', 'Débitos antigos limpos com sucesso!')

# Função para atualizar o saldo considerando as parcelas e a passagem do tempo
def update_balance(discount_first_installment=False):
    total_credits = execute_db_query('SELECT SUM(amount) FROM credits').fetchone()[0] or 0
    debts = execute_db_query('SELECT amount, installments, date FROM debts').fetchall()
    
    total_debts = 0
    current_date = datetime.now()
    months_to_add = int(months_entry.get()) if months_entry.get().isdigit() else None
    
    if months_to_add is not None:
        current_date += timedelta(days=30 * months_to_add)  # Simular passagem de meses

    for amount, installments, date in debts:
        debt_date = datetime.strptime(date, '%Y-%m-%d')
        months_passed = (current_date.year - debt_date.year) * 12 + current_date.month - debt_date.month
        
        if discount_first_installment or months_to_add is None:
            paid_installments = 1
        else:
            paid_installments = min(months_passed, installments)
        
        total_debts += (amount / installments) * paid_installments
    
    balance = total_credits - total_debts
    balance_label.config(text=f'Saldo Atual: {balance:.2f} reais')

# Função para limpar os campos de entrada
def clear_entries():
    credit_entry.delete(0, tk.END)
    debt_item_entry.delete(0, tk.END)
    debt_amount_entry.delete(0, tk.END)
    debt_installments_entry.delete(0, tk.END)
    months_entry.delete(0, tk.END)

# Configuração da interface Tkinter
root = tk.Tk()
root.title('Gerenciador de Créditos')

# Adicionar crédito
tk.Label(root, text='Adicionar Crédito').grid(row=0, column=0, pady=10)
credit_entry = tk.Entry(root)
credit_entry.grid(row=0, column=1, pady=10)
tk.Button(root, text='Adicionar', command=lambda: (add_credit(), update_balance(discount_first_installment=True))).grid(row=0, column=2, pady=10, padx=10)

# Registrar débito
tk.Label(root, text='Registrar Débito').grid(row=1, column=0, pady=10)
debt_item_entry = tk.Entry(root)
debt_item_entry.grid(row=1, column=1, pady=10)
tk.Label(root, text='Valor').grid(row=2, column=0, pady=10)
debt_amount_entry = tk.Entry(root)
debt_amount_entry.grid(row=2, column=1, pady=10)
tk.Label(root, text='Parcelas').grid(row=3, column=0, pady=10)
debt_installments_entry = tk.Entry(root)
debt_installments_entry.grid(row=3, column=1, pady=10)
tk.Button(root, text='Registrar', command=lambda: (add_debt(), update_balance(discount_first_installment=True))).grid(row=4, column=1, pady=10)

# Entrada para alterar meses manualmente (para depuração)
tk.Label(root, text='Meses Passados').grid(row=5, column=0, pady=10)
months_entry = tk.Entry(root)
months_entry.grid(row=5, column=1, pady=10)
tk.Button(root, text='Atualizar Saldo', command=lambda: update_balance(discount_first_installment=False)).grid(row=5, column=2, pady=10, padx=10)

# Mostrar saldo
balance_label = tk.Label(root, text='Saldo Atual: 0.00 reais')
balance_label.grid(row=6, column=0, columnspan=3, pady=10)

# Adicionar botão na interface para limpar débitos antigos
tk.Button(root, text='Limpar Débitos Antigos', command=clean_old_debts).grid(row=7, column=2, pady=10)

# Atualizar saldo ao iniciar
update_balance(discount_first_installment=True)

root.mainloop()
