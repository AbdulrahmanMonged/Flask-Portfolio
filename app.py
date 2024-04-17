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
                "html": "<p><b>From: {0}</b></p><h6>Message: </h6><p>{1}</p>".format(
                    data["email"], data["message"]
                ),
            }
            resend.Emails.send(params)
            return "Sent Successfully!", 201
        except Exception as e:
            return "Error occured while validation Data", 400


api.add_resource(SendEmail, "/email")

