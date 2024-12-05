import tkinter as tk
from tkinter import messagebox
import sqlite3

# Conectar ao banco de dados SQLite ou criar se não existir
conn = sqlite3.connect("imc_data.db")
cursor = conn.cursor()

# Criar a tabela se não existir
cursor.execute("""
CREATE TABLE IF NOT EXISTS imc_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    endereco TEXT,
    altura REAL,
    peso REAL,
    imc REAL,
    situacao TEXT
)
""")
conn.commit()

# Função para salvar os dados no banco de dados


def salvar_no_banco(nome, endereco, altura, peso, imc, situacao):
    cursor.execute("""
    INSERT INTO imc_data (nome, endereco, altura, peso, imc, situacao)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (nome, endereco, altura, peso, imc, situacao))
    conn.commit()

# Função para calcular o IMC e exibir a classificação


def calcular_imc():
    try:
        nome = nome_entry.get()
        endereco = endereco_entry.get()
        # Converte altura de cm para metros
        altura = float(altura_entry.get()) / 100
        peso = float(peso_entry.get())
        imc = peso / (altura ** 2)
        situacao = avaliar_imc(imc)

        # Exibir o resultado na interface
        resultado_texto.set(f"IMC: {imc:.2f} - {situacao}")

        # Salvar no banco de dados
        salvar_no_banco(nome, endereco, altura * 100, peso, imc, situacao)
        messagebox.showinfo(
            "Sucesso", "Os dados foram salvos no banco de dados!")
    except ValueError:
        messagebox.showerror(
            "Erro", "Por favor, insira valores numéricos válidos para altura e peso.")

# Função para avaliar o IMC e retornar a situação correspondente


def avaliar_imc(imc):
    if imc < 17:
        return "Muito abaixo do peso"
    elif 17 <= imc < 18.5:
        return "Abaixo do peso"
    elif 18.5 <= imc < 25:
        return "Peso normal"
    elif 25 <= imc < 30:
        return "Acima do peso"
    elif 30 <= imc < 35:
        return "Obesidade I"
    elif 35 <= imc < 40:
        return "Obesidade II (severa)"
    else:
        return "Obesidade III (mórbida)"

# Função para limpar os campos


def reiniciar():
    nome_entry.delete(0, tk.END)
    endereco_entry.delete(0, tk.END)
    altura_entry.delete(0, tk.END)
    peso_entry.delete(0, tk.END)
    resultado_texto.set("Resultado")

# Função para sair do programa


def sair():
    conn.close()  # Fechar a conexão com o banco de dados
    root.destroy()


# Criação da janela principal
root = tk.Tk()
root.title("Cálculo do IMC - Índice de Massa Corporal")
root.geometry("500x350")

# Labels e campos de entrada
tk.Label(root, text="Nome do Paciente:").grid(
    row=0, column=0, sticky="w", padx=10, pady=5)
nome_entry = tk.Entry(root, width=40)
nome_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Endereço Completo:").grid(
    row=1, column=0, sticky="w", padx=10, pady=5)
endereco_entry = tk.Entry(root, width=40)
endereco_entry.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Altura (cm):").grid(
    row=2, column=0, sticky="w", padx=10, pady=5)
altura_entry = tk.Entry(root, width=15)
altura_entry.grid(row=2, column=1, sticky="w", padx=10, pady=5)

tk.Label(root, text="Peso (Kg):").grid(
    row=3, column=0, sticky="w", padx=10, pady=5)
peso_entry = tk.Entry(root, width=15)
peso_entry.grid(row=3, column=1, sticky="w", padx=10, pady=5)

# Área de resultado alinhada mais à esquerda
resultado_texto = tk.StringVar(value="Resultado")
resultado_label = tk.Label(root, textvariable=resultado_texto,
                           width=30, height=4, relief="sunken", bg="white")
resultado_label.grid(row=4, column=1, padx=10, pady=10, sticky="w")

# Botões
calcular_button = tk.Button(root, text="Calcular",
                            command=calcular_imc, width=10)
calcular_button.grid(row=5, column=0, padx=10, pady=10)

reiniciar_button = tk.Button(
    root, text="Reiniciar", command=reiniciar, width=10)
reiniciar_button.grid(row=5, column=1, padx=10, pady=10)

sair_button = tk.Button(root, text="Sair", command=sair, width=10)
sair_button.grid(row=5, column=2, padx=10, pady=10)

# Inicia o loop principal da interface
root.mainloop()
