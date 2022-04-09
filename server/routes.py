from crypt import methods
import json
from typing import List
from flask import Blueprint, redirect, url_for
from flask import request, render_template, jsonify
from time import time

from postmanager.manager import PostManager
from postmanager.proxy import BucketProxy
from postmanager.exception import PostManagerException
from postmanager.meta import PostMeta
from postmanager.post import Post

main = Blueprint("main", __name__)

post_manager = PostManager.setup("postmanager-flask-example", "advert")


# Show home page template
@main.route("/")
def home():

    return render_template("index.html")


# Posts route
@main.route("/posts", methods=["GET", "POST"])
def list_posts():
    if request.method == "GET":

        posts: List(Post) = []
        posts_meta: List = post_manager.index

        for meta in posts_meta:
            post = post_manager.get_by_id(meta["id"])

            posts.append(post)

        return render_template("posts.html", posts=posts)

    elif request.method == "POST":

        try:
            form_data = json.loads(request.get_data().decode("utf-8"))

            # Get raw data from request
            form_meta_data = form_data.get("metaData", {"title": "Unknown title"})
            post_title = form_meta_data.get("title")
            post_content = form_data.get("content", {"Header": "Unkown Content"})

            new_meta_dict = {"title": post_title, "timestamp": int(time())}

            post_meta_data = post_manager.create_meta(new_meta_dict)
            new_post = post_manager.create_post(post_meta_data, post_content)

            post_manager.save_post(new_post)

            data = {"title": "Create Post Success", "data": post.to_json()}

            return jsonify(data)

        except Exception as e:
            data = {"error": True, "title": "Create Post Error", "data": str(e)}

            return jsonify(data)


# Post with ID route
@main.route("/posts/<string:post_id>", methods=["GET", "PUT", "DELETE"])
def single_post(post_id):

    if request.method == "GET":
        try:
            post = post_manager.get_by_id(post_id)

            return render_template("post.html", post=post)

        except PostManagerException as e:
            data = {"error": True, "title": "Post not Found", "data": str(e)}

            return redirect(url_for("main.validate", data=data))

    elif request.method == "PUT":
        try:
            form_data = request.get_json()

            post = post_manager.get_by_id(post_id)

            # Update post meta
            post.meta_data.update(form_data.get("metaData"))

            # Update post content
            post.content = form_data.get("content")
            post_manager.save_post(post)

            data = {"title": "Update Post Success", "data": post.to_json()}

            return jsonify(data)

        except PostManagerException as e:
            data = {"error": True, "title": "Post not Found", "data": str(e)}

            return jsonify(data)

    elif request.method == "DELETE":

        try:
            post_manager.delete_post(post_id)

            data = {"title": "Post Deleted", "data": {"post_id": post_id}}

            return jsonify(data)

        except PostManagerException as e:
            data = {"error": True, "title": "Post not deleted", "data": str(e)}

            return jsonify(data)


@main.route("/posts/create")
def create():
    return render_template("create.html")


@main.route("/posts/update/<string:post_id>")
def update(post_id):
    try:
        post = post_manager.get_by_id(post_id)
        return render_template("update.html", post=post)

    except PostManagerException as e:
        data = {"title": "Post not Found", "data": str(e)}

        return redirect(url_for("main.validate", data=data))


@main.route("/validate", methods=["GET", "PUT", "POST", "DELETE"])
def validate():
    req_data = json.loads(request.args.get("data"))

    data = {"title": req_data.get("title"), "data": req_data.get("data")}

    return render_template("validate.html", data=data)
