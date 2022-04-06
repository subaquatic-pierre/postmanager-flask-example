from typing import List
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

    return render_template("index.html")

# Posts route
@main.route("/posts", methods=['GET', 'POST'])
def posts():
    posts: List = post_manager.index

    post = {
        'metaData':{
            'id':0,
            'title':'Coolest'
        },
        'content':{
            'Header':'Coolest'
        }
    }

    posts.append(post)


    return render_template("posts.html", posts=posts)

# Post with ID route
@main.route("/posts/<string:id>", methods=['GET', 'PUT', 'DELETE'])
def single_post():
    posts: List = post_manager.index

    post = {
        'metaData':{
            'id':0,
            'title':'Coolest'
        },
        'content':{
            'Header':'Coolest'
        }
    }

    posts.append(post)


    return render_template("posts.html", posts=posts)



# # Show about privacy policy template
# @main.route("/policy")
# def policy():
#     return render_template("main/policy.html", title="Privacy Policy")
