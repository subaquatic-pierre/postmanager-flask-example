from flask import Blueprint
from flask import request, render_template
from postmanager.manager import PostManager
from postmanager.proxy import BucketProxy

main = Blueprint("main", __name__)

bucket_proxy = BucketProxy("postmanager-flask-example", "/post")
post_manager = PostManager(bucket_proxy, "post")


# Show home page template
@main.route("/")
def home():
    posts = post_manager.index
    return render_template("index.html", posts=posts)


# # Show about privacy policy template
# @main.route("/policy")
# def policy():
#     return render_template("main/policy.html", title="Privacy Policy")
