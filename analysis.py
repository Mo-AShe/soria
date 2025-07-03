import dash
from dash import Dash, html, dcc, dash_table, Input, Output
import pandas as pd

# Load data from Excel file
df = pd.read_excel('Job1.xlsx')

# Check that 'Category' column exists
if 'Category' not in df.columns:
    raise ValueError("The Excel file must contain a 'Category' column.")

# Remove rows where Category is missing
df = df.dropna(subset=['Category'])

# Initialize Dash app
app = Dash(__name__)

app.layout = html.Div([
    html.H1("Syrian Companies Directory", style={'textAlign': 'center'}),

    # Dropdown filter
    dcc.Dropdown(
        id='category-dropdown',
        options=[
            {"label": cat, "value": cat}
            for cat in sorted(df['Category'].unique())
        ],
        placeholder="Select a Category",
        style={'width': '300px', 'margin': 'auto'}
    ),

    html.Br(),

    # DataTable (initially empty)
    html.Div([
        dash_table.DataTable(
        id='company-table',
        columns=[
            {"name": col, "id": col}
            for col in df.columns if col != 'Category'
        ],
        data=[],  # Start with no rows
        style_table={'overflowX': 'auto'},
        style_cell={'textAlign': 'left', 'padding': '6px'},
        style_header={'backgroundColor': '#f0f0f0', 'fontWeight': 'bold'},
        page_size=10
    )] , id='table')
])
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>Shopping Trends Dashboard</title>
        {%css%}
    </head>
    <body>
        {%app_entry%}  <!-- REQUIRED -->
        <footer>
            {%config%}   <!-- REQUIRED -->
            {%scripts%}  <!-- REQUIRED -->
            {%renderer%} <!-- REQUIRED -->
        </footer>
    </body>
</html>
'''
# Callback to update the table based on selected category
@app.callback(
    Output('company-table', 'data'),
    Input('category-dropdown', 'value')
)
def update_table(selected_category):
    if selected_category:
        filtered_df = df[df['Category'] == selected_category]
        return filtered_df.drop(columns=['Category']).to_dict("records")
    else:
        return []  # Return empty table if nothing selected
 
if __name__=="__main__":
    print("Starting server...")
    app.run(host='127.0.0.1', port=8051, debug=True, use_reloader=True)



