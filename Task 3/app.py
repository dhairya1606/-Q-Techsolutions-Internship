import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px

# Load data
data_path = 'C:\\Users\\dhairya\\OneDrive\\Documents\\8th Sem Internships\\QTechSolutions\\Task 3\\imdb_top_1000.csv'  # Replace with your CSV file path
data = pd.read_csv(data_path)
data.head()

# Null value removal
data.dropna(inplace=True)

# Preprocess data
data['Released_Year'] = pd.to_numeric(data['Released_Year'], errors='coerce')
data['Gross'] = data['Gross'].str.replace(',', '').str.extract('(\d+)').astype(float)
data['Runtime'] = data['Runtime'].str.replace(' min', '').astype(float)

# Bar chart: Top 10 Movies by Gross Earnings
top_10_gross = data.nlargest(10, 'Gross')
top_10_bar = px.bar(top_10_gross, x='Series_Title', y='Gross', title='Top 10 Movies by Gross Earnings',
                    labels={'Series_Title': 'Movie Title', 'Gross': 'Gross Earnings'}, color='Gross', text='Gross')
top_10_bar.update_layout(xaxis={'categoryorder': 'total descending'})

# Scatter plot: IMDb Rating vs Gross Earnings with Movie Title
scatter_plot = px.scatter(data, x='Gross', y='IMDB_Rating', size='No_of_Votes', color='Series_Title',
                           hover_data=['Series_Title'], title="IMDb Rating vs Gross Earnings (Movies)")

# Pie Chart: Gross Earnings Based on Certificates
certificate_gross = data.groupby('Certificate')['Gross'].sum().reset_index()
certificate_pie = px.pie(certificate_gross, names='Certificate', values='Gross', title="Gross Earnings Based on Certificates")

# Bar Chart: Average IMDb Rating by Certificate
avg_rating_by_certificate = data.groupby('Certificate')['IMDB_Rating'].mean().reset_index()
certificate_bar = px.bar(avg_rating_by_certificate, x='Certificate', y='IMDB_Rating', title='Average IMDb Rating by Certificate',
                         labels={'IMDB_Rating': 'Average IMDb Rating'}, color='Certificate', text='IMDB_Rating')

# Bubble Chart: Gross Earnings by Released Year and Runtime
bubble_chart = px.scatter(data, x='Released_Year', y='Runtime', size='Gross', color='Released_Year',
                          title='Gross Earnings by Released Year and Runtime',
                          labels={'Released_Year': 'Released Year', 'Runtime': 'Runtime (min)', 'Gross': 'Gross Earnings'},
                          hover_data=['Series_Title', 'IMDB_Rating'])
bubble_chart.update_layout(showlegend=False)

# Initialize Dash app
app = dash.Dash(__name__)
app.title = "IMDb Movies Hub"

# App layout
app.layout = html.Div(id='main-container', children=[
    html.Div([
        html.Img(src="https://upload.wikimedia.org/wikipedia/commons/6/69/IMDB_Logo_2016.svg", style={'width': '200px', 'vertical-align': 'middle'}),
        html.H1("IMDb Movies Hub", style={'display': 'inline', 'margin-left': '20px', 'vertical-align': 'middle', 'color': 'black'})
    ], style={'text-align': 'center'}),
    
    html.Div([
        html.Div([
            html.H3("Which Movie to be watched? ", style={'color': 'black', 'font-weight': 'bold'}),
            html.P("Discover the top 10 highest-grossing movies based on the IMDb dataset, showcasing cinematic masterpieces that have captivated global audiences and shattered box office records. These films demonstrate how a combination of star power, epic storytelling, and outstanding production values can lead to massive financial success. From iconic classics to modern blockbusters, these top earners have proven that critical acclaim and widespread appeal drive unparalleled earnings. Explore how these cinematic giants achieved their impressive revenue and find out which movie reigns supreme at the top of the box office!",
                   style={'color': 'black', 'text-align': 'justify', 'font-family': 'Times New Roman', 'margin-top': '20px'})
        ], style={'width': '40%', 'padding': '20px'}),
        html.Div([
            dcc.Graph(id='top-10-bar-chart', figure=top_10_bar, style={'height': '400px', 'border': '2px solid black', 'border-radius': '10px'})
        ], style={'width': '55%', 'padding': '20px'}),
    ], style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center'}),
    
    html.Div([
        html.Div([
            dcc.Graph(id='scatter-plot', figure=scatter_plot, style={'height': '450px', 'border': '2px solid black', 'border-radius': '10px'})
        ], style={'width': '55%', 'padding': '20px'}),
        html.Div([
            html.H3("How IMDb Ratings Propel Box Office Success!", style={'color': 'black', 'font-weight': 'bold'}),
            html.P("This graph delves into the fascinating relationship between IMDB ratings and the earnings of the highest-grossing films. It clearly illustrates how stellar ratings can drive a movie's box office success, showing the undeniable impact of audience approval. Not only does this reveal how good ratings correlate with high earnings, but it also serves as a guide to help moviegoers choose which films are truly worth watching. By examining this data, you’ll discover which top-rated blockbusters are not just popular, but deserving of your time and attention—ensuring you don’t miss out on cinematic gems that stand the test of both critics and fans alike.",
                   style={'color': 'black', 'text-align': 'justify', 'font-family': 'Times New Roman', 'margin-top': '20px'})
        ], style={'width': '40%', 'padding': '20px'}),
    ], style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center'}),
    
    html.Div([
        html.Div([
            html.H3("How Movie Ratings Shape Gross Earnings?", style={'color': 'black', 'font-weight': 'bold'}),
            html.P("Unlock the secret behind the success of movies with our Gross Earnings Based on Certificates chart! Ever wondered how movie ratings like PG, PG-13, or R influence a film's earnings? This captivating visualization reveals the financial impact of movie certifications, showing you which ratings dominate the box office. From family-friendly hits to thrilling R-rated blockbusters, explore how certification categories shape audience appeal and drive record-breaking earnings. Let the numbers speak as we uncover the connection between film ratings and its financial triumphs on IMDb!",
                   style={'color': 'black', 'text-align': 'justify', 'font-family': 'Times New Roman', 'margin-top': '20px'})
        ], style={'width': '40%', 'padding': '20px'}),
        html.Div([
            dcc.Graph(id='certificate-pie-chart', figure=certificate_pie, style={'height': '400px', 'border': '2px solid black', 'border-radius': '10px'})
        ], style={'width': '55%', 'padding': '20px'}),
    ], style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center'}),
    
    html.Div([
        html.Div([
            dcc.Graph(id='certificate-bar-chart', figure=certificate_bar, style={'height': '400px', 'border': '2px solid black', 'border-radius': '10px'})
        ], style={'width': '55%', 'padding': '20px'}),
        html.Div([
            html.H3("Exploring IMDb Ratings Across Film Certifications", style={'color': 'black', 'font-weight': 'bold'}),
            html.P("Discover how movie ratings influence audience reception with our Average IMDb Rating by Certificate chart! This insightful visualization reveals the relationship between a film's certification and its average IMDb rating. Are family-friendly films rated higher than intense thrillers? Does an R-rated movie have the same appeal as a PG-rated one? Dive into the data and see how movie certifications impact critical acclaim and audience ratings, providing a fascinating look into how certifications shape film reception and success on IMDb!",
                   style={'color': 'black', 'text-align': 'justify', 'font-family': 'Times New Roman', 'margin-top': '20px'})
        ], style={'width': '40%', 'padding': '20px'}),
    ], style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center'}),
    
    html.Div([
        html.Div([
            html.H3("The Impact of Runtime and Year on Gross Earnings", style={'color': 'black', 'font-weight': 'bold'}),
            html.P("Unveil the evolution of cinema's financial success with our Gross Earnings by Released Year and Runtime bubble chart! This dynamic visualization showcases how movies of various runtimes have performed at the box office over the years. The chart plots the gross earnings of top films, highlighting trends and shifts in the industry. Are longer films earning more over time? Does a shorter runtime correlate with massive success? Explore how the movie industry's runtime and release year have influenced box office performance, offering a deeper look into the financial impact of movie length and era!",
                   style={'color': 'black', 'text-align': 'justify', 'font-family': 'Times New Roman', 'margin-top': '20px'})
        ], style={'width': '40%', 'padding': '20px'}),
        html.Div([
            dcc.Graph(id='bubble-chart', figure=bubble_chart, style={'height': '400px', 'border': '2px solid black', 'border-radius': '10px'})
        ], style={'width': '55%', 'padding': '20px'}),
    ], style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center'}),
], style={'background-color': 'white', 'color': 'black', 'font-family': 'Arial, sans-serif'})

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)