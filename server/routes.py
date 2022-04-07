import json
from typing import List
from flask import Blueprint, redirect, url_for
from flask import request, render_template,jsonify
from postmanager.manager import PostManager
from postmanager.proxy import BucketProxy
from postmanager.exception import PostManagerException
from postmanager.meta import PostMeta
from postmanager.post import Post

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
    if request.method == 'GET':
            
        posts: List(Post) = []
        posts_meta: List = post_manager.index

        for meta in posts_meta:
            post = post_manager.get_by_id(meta['id'])

            posts.append(post)
            
        return render_template("posts.html", posts=posts)

    elif request.method == 'POST':

        try:
            form_data = json.loads(request.get_data().decode('utf-8'))

            # Get new ID from post manager
            new_post_id = post_manager._get_latest_id()

            # Get raw data from request
            post_meta_data = form_data.get('metaData',{'title':'Unknown title'})
            post_title = post_meta_data.get('title')
            post_content = form_data.get('content',{'Header':'Unkown Content'})

            post_meta_data = post_manager.create_meta(post_title)
            new_post = post_manager.create_post(post_meta_data, post_content)

            post_manager.save_post(new_post)

            return jsonify(new_post.to_json())

        except Exception as e:
            data = {
                'error':True,
                'message': str(e)
            }
            return jsonify(data)


# Post with ID route
@main.route("/posts/<string:post_id>", methods=['GET', 'PUT', 'DELETE'])
def single_post(post_id):

    post_id = int(post_id)
    # Return single post 
    if request.method == 'GET':

        try:

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
        except PostManagerException:
            post = {
                'error': True,
                'message': 'Post not found'
            }

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
