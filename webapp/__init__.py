from flask import Flask

app = Flask(__name__)
app.run(debug=True, port=5000, host="0.0.0.0")

from webapp.main.views import main

app.register_blueprint(main)
