from fastapi import FastAPI, HTTPException
import snowflake.connector
import pandas as pd
import requests
import uvicorn

app = FastAPI()

# Snowflake configuration
snowflake_config = {
    'user': 'EDUARDSLEONOVICS',
    'password': 'ZBmainitp@1',
    'account': 'jqgjuzc-qx24021',
    'warehouse': 'COMPUTE_WH',
    'database': 'COVID19_EPIDEMIOLOGICAL_DATA',
    'schema': 'PUBLIC',
    'role': 'ACCOUNTADMIN'
}

@app.get("/query/")
async def run_snowflake_query(query: str):
    try:
        connection = snowflake.connector.connect(**snowflake_config)
        cursor = connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        df = pd.DataFrame(result, columns=columns)
        return df.to_dict(orient='records')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        connection.close()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)


# pip install fastapi uvicorn snowflake-connector-python


response = requests.get("http://localhost:8000/query/?query=SELECT * FROM JHU_COVID_19_TIMESERIES")
data = response.json()
print(data)









# example how I would implement a chart 



app1 = dash.Dash(__name__)
app1.layout = html.Div([
    html.H1("COVID-19 Restrictions Status by Date"),
    dcc.Graph(id='line-chart'),
])

@app1.callback(
    Output('line-chart', 'figure'),
    Input('line-chart', 'relayoutData'))
def update_graph(relayoutData):
    # If 'df' is not globally defined, you would need to load it within this function or pass it in another way.
    
    # Check if 'relayoutData' is not None and the required keys are present
    if relayoutData and 'xaxis.range[0]' in relayoutData and 'xaxis.range[1]' in relayoutData:
        start_date = pd.to_datetime(relayoutData['xaxis.range[0]'])
        end_date = pd.to_datetime(relayoutData['xaxis.range[1]'])
    else:
        start_date = df['DATE'].min()
        end_date = df['DATE'].max()

    filtered_df = df[(df['DATE'] >= start_date) & (df['DATE'] <= end_date)]

    # Group by DATE and STATUS and count the occurrences
    status_counts = filtered_df.groupby(['DATE', 'STATUS']).size().reset_index(name='COUNT')

    # Create the Plotly line chart
    fig = px.line(status_counts, x='DATE', y='COUNT', color='STATUS', markers=True, title='COVID-19 Restrictions Status by Date')
    
    return fig

if __name__ == '__main__':
    app1.run_server(debug=True, port=8058) 


