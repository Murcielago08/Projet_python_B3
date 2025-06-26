from flask import Flask, render_template, request
from support_bot import process_support_message

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        email = request.form["email"]
        message = request.form["message"]
        commande = request.form.get("commande")
        process_support_message(email, message, commande)
        return "Message envoyé !"
    return render_template("form.html")
