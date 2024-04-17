from flask import Flask
from flask_restful import Api
import resend
import os

app = Flask(__name__)
api = Api(app)
resend.api_key = os.environ["RESEND_API_KEY"]
email = os.environ["EMAIL"]