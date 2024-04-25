from config import app, api, email
from flask import request
from flask_restful import Resource
import resend

@app.route("/")
def home():
    return "Hello World!"


class SendEmail(Resource):
    def post(self):
        try:
            data = request.get_json()
            params = {
                "from": "Your own Portfolio <onboarding@resend.dev>",
                "to": email,
                "subject": data["subject"],
                "html": "<p>Email: {0}</p><p>Subject: {2}</p><p>Message:</p><p style='white-space: pre-wrap;'>{1}</p>".format(
                    data["email"]["value"], data["message"]["value"], data["subject"]["value"]
                ),
            }
            resend.Emails.send(params)
            return "Sent Successfully!", 201
        except Exception as e:
            print(e)
            return "Error occured while validation Data", 400


api.add_resource(SendEmail, "/email")

