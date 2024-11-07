import sqlite3
import csv
import pandas as pd 


conexao = sqlite3.connect(r'D:\desenvolvimento\python\panel_acess\database\database.db')
cursor = conexao.cursor()   

# with open(r'D:\desenvolvimento\python\panel_acess\utils\SAC_ENTIDADES_ATIVAS.csv', mode='r',encoding="utf8") as file:
#     ri = csv.reader(file)
#     for linha in ri:
#         print(linha[0].strip().find('PREFEITURA'))

df = pd.read_csv(r'D:\desenvolvimento\python\panel_acess\utils\SAC_ENTIDADES_ATIVAS.csv', delimiter=';',encoding="utf8")

# Função para modificar o nome conforme as regras
def alterar_nome(nome):
    if "PREFEITURA MUNICIPAL" in nome or "PREFEITURA" in nome:
        nome = nome.replace("PREFEITURA MUNICIPAL DE ", "PM ").replace("PREFEITURA ", "PM ")
    elif "CAMARA MUNICIPAL" in nome:
        nome = nome.replace("CAMARA MUNICIPAL DE ", "CM ")
    elif "MUNICIPIO " in nome:
        nome = nome.replace("MUNICIPIO DE ", "PM")
    return nome

# Aplica a função à coluna 'NOME'
df['NOME'] = df['NOME'].apply(alterar_nome)

# Remove a coluna 'CODIGO' pois não é necessária no novo arquivo
df = df.drop(columns=['CODIGO'])

for nome,tipo in zip(df['NOME'],df["TIPO"]): 
    # Inserir no banco de dados
            cursor.execute('''
            INSERT INTO entidades (nome, tipo) VALUES (?, ?)
            ''', (nome, tipo))

# Salvar e fechar a conexão
conexao.commit()
conexao.close()
    