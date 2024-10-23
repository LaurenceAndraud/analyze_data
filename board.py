import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px

app = dash.Dash(__name__)

df_transactions = pd.read_csv("data/transactions.csv")
df_products = pd.read_csv("data/products.csv")

df = pd.merge(df_transactions, df_products, on='product_id', how='inner')

montant_par_client = df.groupby('customer_id')['amount'].sum().reset_index()
transaction_par_categorie = df.groupby('category')['transaction_id'].count().reset_index()
transaction_par_annee = df.groupby(df['date'].str[:4])['transaction_id'].count().reset_index()

top_clients = df.groupby('customer_id')['transaction_id'].count().reset_index().nlargest(5, 'transaction_id')

app.layout = html.Div([
    html.H1('Tableau de bord des transactions'),

    # Montant total des transactions par client
    dcc.Graph(
        id='montants-graph',
        figure=px.bar(
            montant_par_client, x='customer_id', y='amount',
            title='Montant Total des Transactions par Client',
            labels={'customer_id': 'ID Client', 'amount': 'Montant Total'}
        )
    ),

    # Transactions par catégorie
    dcc.Graph(
        id="transactions-categorie-graph",
        figure=px.pie(
            transaction_par_categorie, values="transaction_id", names="category",
            title='Répartition des transactions par catégorie de produits',
            hole=0.3
        )
    ),

    # Transactions par année
    dcc.Graph(
        id='transactions-annee-graph',
        figure=px.line(
            transaction_par_annee, x='date', y='transaction_id',
            title='Nombre de Transactions par Année',
            labels={'date': 'Année', 'transaction_id': 'Nombre de Transactions'}
        )
    ),

    # Top 5 clients ayant fait le plus de transactions
    dcc.Graph(
        id='top-clients-graph',
        figure=px.bar(
            top_clients, x='customer_id', y='transaction_id',
            title='Top 5 Clients avec le Plus de Transactions',
            labels={'customer_id': 'ID Client', 'transaction_id': 'Nombre de Transactions'}
        )
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)