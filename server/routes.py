from typing import List
from flask import Blueprint, redirect, url_for
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
def list_posts():
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
@main.route("/posts/<string:post_id>", methods=['GET', 'PUT', 'DELETE'])
def single_post(post_id):

    post_id = int(post_id)
    # Return single post 
    if request.method == 'GET':

        posts = post_manager.get_by_id(post_id)

        post = {
            'metaData':{
                'id':post_id,
                'title':'Coolest'
            },
            'content':{
                'Header':'Coolest'
            }
        }

        posts.append(post)

        return render_template("post.html", post=post)

    elif request.method == 'PUT':

        # Get post by ID

        # Update post

        # Save post

        # Return post

        data = {'updated': True,'post_id':post_id}

        return redirect(url_for("success.html", data=data))

    elif request.method == 'DELETE':

        # delete post 

        # return boolean and post id

        data = {'deleted': True,'post_id':1}

        return redirect(url_for("success.html", data=data))


@main.route("/success")
def success():
    data = request.args.get('data')
    return render_template("success.html", data=data)

@main.route("/posts/create")
def create():
    return render_template("create.html")



# # Show about privacy policy template
# @main.route("/policy")
# def policy():
#     return render_template("main/policy.html", title="Privacy Policy")
