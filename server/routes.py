from flask import Blueprint
from flask import request, render_template

main = Blueprint("main", __name__)


# Show home page template
@main.route("/")
def home():
    return render_template("index.html")


# # Show about privacy policy template
# @main.route("/policy")
# def policy():
#     return render_template("main/policy.html", title="Privacy Policy")
