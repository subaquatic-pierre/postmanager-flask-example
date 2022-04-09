from crypt import methods
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

bucket_proxy = BucketProxy("postmanager-flask-example", "post/")
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

    if request.method == 'GET':
        try:
            post = post_manager.get_by_id(post_id)

            return render_template("post.html", post=post)

        except PostManagerException as e:
            data = {
                'title': 'Post not Found',
                'data': str(e)
            }

            return redirect(url_for('main.validate',data=data))


    elif request.method == 'PUT':
        try:
            data = request.get_json()

            post = post_manager.get_by_id(post_id)

            new_meta = PostMeta.from_json({'id':post.id,**data.get('metaData')})

            post.content = data.get('content')
            post.meta_data = new_meta

            post_manager.save_post(post)

            data = {
                'title': 'Update Post Success',
                'data': post
            }

            return redirect(url_for('main.validate',data=data))

        except PostManagerException as e:
            data = {
                'title': 'Post not Found',
                'data': str(e)
            }

            return redirect(url_for('main.validate',data=data))


    elif request.method == 'DELETE':

        try:
            post_manager.delete_post(post_id)

            data = {'title': 'Post Deleted','data': {'post_id':post_id}}

            return redirect(url_for('main.validate',data=data))

        except PostManagerException as e:
            data = {
                'title': 'Post not deleted',
                'data': str(e)
            }

            return redirect(url_for('main.validate',data=data))
       

@main.route("/posts/create")
def create():
    return render_template("create.html")

@main.route("/posts/update/<string:post_id>")
def update(post_id):
    try:
        post = post_manager.get_by_id(post_id)
        return render_template("update.html", post=post)


    except PostManagerException as e:
        data = {
            'title': 'Post not Found',
            'data': str(e)
        }

        return redirect(url_for('main.validate',data=data))


@main.route("/validate")
def validate():
    req_data = json.loads(request.args.get('data'))

    data = {
        'title': req_data.get('title'),
        'data':req_data.get('data')
    }
    
    return render_template("validate.html", data=data)



