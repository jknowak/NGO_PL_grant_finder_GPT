from flask import Flask, render_template, request
import modules.query_engine as qe  # Import your query engine module

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        query = request.form['query']
        results = qe.query_grants(query)  # Use your query engine
        return render_template('results.html', results=results)
    return render_template('index.html')

@app.route('/results')
def results():
    # ... (Handle results display)

if __name__ == '__main__':
    app.run(debug=True)  # Run the Flask app