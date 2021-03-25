from logging import debug
from flask import Flask, app
from settings import PORT, DEBUG
from views import Views

app = Flask(__name__)

# Routes
app.route('/verify/<token>', methods=['POST'])(Views.verify)
app.route('/generate')(Views.generate)
app.route('/captcha/<token>')(Views.captcha)

if DEBUG:
    app.run(port=PORT, debug=DEBUG)
