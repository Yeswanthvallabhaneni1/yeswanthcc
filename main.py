from flask import Flask, render_template
import requests
import plotly.graph_objs as go

app = Flask(__name__)

# Function to fetch COVID-19 data from the API
def fetch_covid_data():
    api_key = "9eba7ea7fe3c4f3fbe6f9a8e5e4115b8"  # Replace this with your API key
    url = f"https://api.covidactnow.org/v2/states.json?apiKey={api_key}"
    response = requests.get(url)
    data = response.json()
    return data

# Function to extract necessary data for plotting
def extract_data_for_plotting(data):
    states = []
    cases = []
    deaths = []
    for state_data in data:
        states.append(state_data['state'])
        cases.append(state_data['actuals']['cases'])
        deaths.append(state_data['actuals']['deaths'])
    return states, cases, deaths

# Function to create plots
def create_plots(states, cases, deaths):
    # Sort the states based on case counts in descending order
    sorted_cases = sorted(zip(cases, states), reverse=True)
    sorted_states_cases = [state for count, state in sorted_cases]
    sorted_case_counts = [count for count, state in sorted_cases]

    # Sort the states based on death counts in descending order
    sorted_deaths = sorted(zip(deaths, states), reverse=True)
    sorted_states_deaths = [state for count, state in sorted_deaths]
    sorted_death_counts = [count for count, state in sorted_deaths]

    case_plot = go.Bar(x=sorted_states_cases, y=sorted_case_counts, name='Cases')
    death_plot = go.Bar(x=sorted_states_deaths, y=sorted_death_counts, name='Deaths')

    layout = go.Layout(
        title='COVID-19 Cases and Deaths by State',
        xaxis=dict(title='States'),
        yaxis=dict(title='Count')
    )

    case_fig = go.Figure(data=[case_plot], layout=layout)
    death_fig = go.Figure(data=[death_plot], layout=layout)

    case_graph = case_fig.to_html(full_html=False)
    death_graph = death_fig.to_html(full_html=False)

    return case_graph, death_graph

# Route for the dashboard
@app.route('/')
def dashboard():
    data = fetch_covid_data()
    states, cases, deaths = extract_data_for_plotting(data)
    case_graph, death_graph = create_plots(states, cases, deaths)
    return render_template('dashboard.html', case_graph=case_graph, death_graph=death_graph)

if __name__ == '__main__':
    app.run(debug=True)