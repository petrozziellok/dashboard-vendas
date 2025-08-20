import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("vendas.csv")
print(df.head())

df['Order Date'] = pd.to_datetime(df['Order Date'], dayfirst=True, errors="coerce")
df['Month'] = df['Order Date'].dt.to_period('M')


receita_mensal = df.groupby('Month')['Sales'].sum()
print(receita_mensal)
df['Month'] = df['Order Date'].dt.to_period('M')
receita_mensal = df.groupby('Month')['Sales'].sum().reset_index()
print(receita_mensal.head())

plt.figure(figsize=(10,5))
plt.plot(receita_mensal['Month'].astype(str), receita_mensal['Sales'], marker='o')
plt.xticks(rotation=45)
plt.title("Receita Mensal")
plt.xlabel("Mês")
plt.ylabel("Receita (Sales)")
plt.show()

produtos = df.groupby('Product Name')['Sales'].sum().sort_values(ascending=False).head(10)

plt.figure(figsize=(10,5))
produtos.plot(kind='bar')
plt.title("Top 10 Produtos por Receita")
plt.xlabel("Produto")
plt.ylabel("Receita")
plt.xticks(rotation=75)
plt.show()

regioes = df.groupby('Region')['Sales'].sum().sort_values(ascending=False)

plt.figure(figsize=(8,5))
regioes.plot(kind='bar', color='orange')
plt.title("Receita por Região")
plt.ylabel("Receita")
plt.show()

ticket_medio = df.groupby('Customer Name')['Sales'].mean().sort_values(ascending=False).head(10)

plt.figure(figsize=(10,5))
ticket_medio.plot(kind='bar', color='green')
plt.title("Top 10 Clientes por Ticket Médio")
plt.ylabel("Ticket Médio (R$)")
plt.xticks(rotation=75)
plt.show()

df.to_csv("vendas_tratadas.csv", index=False)
