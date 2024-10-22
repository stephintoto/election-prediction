from flask import Flask, render_template, request
import pandas as pd
import plotly.graph_objects as go
import os

app = Flask(__name__)

# Load the predicted results
predicted_results = pd.read_csv('predicted_election_day_results.csv')

@app.route('/')
def index():
    # Get unique states for the dropdown menu
    states = predicted_results['state'].unique()
    return render_template('index.html', states=states)

@app.route('/predict', methods=['POST'])
def predict():
    # Get the selected state from the form
    state = request.form.get('state')  # Fetching the selected state from the form

    # Get the predicted poll estimates for the selected state
    state_result = predicted_results[predicted_results['state'] == state].iloc[0]

    rep_poll = state_result['Trump']   # Republican (Trump) estimate
    dem_poll = state_result['Harris']  # Democrat (Harris) estimate

    # Determine the winner
    if rep_poll > dem_poll:
        winner_party = 'Republican'
        winner_image = 'trump pointing_0.jpg'  # Replace with the correct image path
    else:
        winner_party = 'Democrat'
        winner_image = 'harris.jpg'  # Replace with the correct image path

    # Render the results.html page and pass the necessary data
    return render_template('result.html', state=state, rep_poll=rep_poll, dem_poll=dem_poll, winner_party=winner_party, winner_image=winner_image)



# Route for the Predictions page
@app.route('/predictions')
def predictions():
    # The HTML file is served directly, stored in the static directory
    return render_template('predictions.html')

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
