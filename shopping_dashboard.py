import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

# Load data
df = pd.read_csv("customer_shopping_data.csv")

# Create the app
app = Dash(__name__)
app.title = "Online Shopping Store Dashboard"

# Layout of the dashboard
app.layout = html.Div([
    html.H1("🛍️ Customer Shopping Dashboard", style={'textAlign': 'center'}),

    html.Div([
        html.Label("Select Gender:"),
        dcc.Dropdown(
            id='gender-filter',
            options=[{'label': g, 'value': g} for g in df['gender'].unique()],
            value='Female',
            clearable=False
        ),
        html.Br(),
        html.Label("Select Category:"),
        dcc.Dropdown(
            id='category-filter',
            options=[{'label': c, 'value': c} for c in df['category'].unique()],
            value='Clothing',
            clearable=False
        ),
    ], style={'width': '45%', 'display': 'inline-block', 'padding': '10px'}),

    html.Div([
        dcc.Graph(id='price-by-age'),
        dcc.Graph(id='quantity-by-category'),
        dcc.Graph(id='payment-method-plot')
    ])
])

# Define callback to update charts
@app.callback(
    Output('price-by-age', 'figure'),
    Output('quantity-by-category', 'figure'),
    Output('payment-method-plot', 'figure'),
    Input('gender-filter', 'value'),
    Input('category-filter', 'value')
)
def update_graphs(selected_gender, selected_category):
    filtered_df = df[(df['gender'] == selected_gender) & (df['category'] == selected_category)]

    # Scatter plot: Age vs Price
    fig1 = px.scatter(filtered_df, x='age', y='price', color='shopping_mall',
                      title="Age vs Price (Filtered by Gender & Category)")

    # Box plot: Quantity by Category
    fig2 = px.box(df[df['gender'] == selected_gender], x='category', y='quantity',
                  title=f"Quantity by Category - {selected_gender}")

    # Box plot: Price by Payment Method
    fig3 = px.box(df[df['gender'] == selected_gender], x='payment_method', y='price',
                  title=f"Price by Payment Method - {selected_gender}")

    return fig1, fig2, fig3

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
