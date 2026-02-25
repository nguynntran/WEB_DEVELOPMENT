from flask import Flask, request, render_template

app = Flask(__name__, template_folder ='templates')

@app.route("/")
def home():
    return render_template('home.html')
@app.route('/tournaments')
def tournaments():
    return render_template('tournaments.html')

@app.route('/teams')
def teams():
    return render_template('teams.html')

@app.route('/matches')
def matches():
    return render_template('matches.html')

@app.route('/standings')
def standings():
    return render_template('standings.html')
   

if __name__ == '__main__':
    app.run(host='0.0.0.0', port = 5555, debug=True)