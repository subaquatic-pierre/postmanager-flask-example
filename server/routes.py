from crypt import methods
import json
from typing import List
from flask import Blueprint, redirect, url_for
from flask import request, render_template, jsonify
from time import time

from postmanager.manager import PostManager
from postmanager.exception import PostManagerException
from postmanager.post import Post

main = Blueprint("main", __name__)

post_manager = PostManager.setup_local()


# Show home page template
@main.route("/")
def home():

    return render_template("index.html")


# Posts route
@main.route("/post", methods=["GET", "POST"])
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
            post_content = form_data.get("content", {"Header": "Unkown Content"})

            # Create meta dict
            post_title = form_meta_data.get("title")
            new_meta_dict = {"title": post_title, "timestamp": int(time())}

            # Create post
            new_post = post_manager.new_post(new_meta_dict, post_content)

            # Get media
            images = form_data.get("images")
            cover_image = images.get("coverImage", "")

            # Add media
            if cover_image:
                new_post.add_media(cover_image, "cover_image")

            # Save post
            post_manager.save_post(new_post)
            post_json = new_post.to_json()

            data = {"title": "Create Post Success", "data": post_json}

            return jsonify(data)

        except Exception as e:
            data = {"error": True, "title": "Create Post Error", "data": str(e)}

            return jsonify(data)


# Post with ID route
@main.route("/post/<string:post_id>", methods=["GET", "PUT", "DELETE"])
def single_post(post_id):

    if request.method == "GET":
        try:
            post = post_manager.get_by_id(post_id)

            data = {"title": "Post Data", "post": post.to_json()}

            return render_template("post.html", data=data, json_dump=json.dumps(data))

        except PostManagerException as e:
            data = {"error": True, "title": "Post not Found", "data": str(e)}

            return redirect(url_for("main.validate", data=data))

    elif request.method == "PUT":
        try:
            form_data = request.get_json()

            post = post_manager.get_by_id(post_id)

            # Update post data
            post.update_meta_data(form_data["metaData"])
            post.update_content(form_data["content"])

            # Update media
            images = form_data.get("images")
            cover_image = images.get("coverImage", "")

            if cover_image:
                post.add_media(cover_image, "cover_image")

            if form_data.get("deleteImage"):
                post.delete_media("cover_image")

            # Update post content

            post_manager.save_post(post)

            post_json = post.to_json()

            data = {"title": "Update Post Success", "data": post_json}

            return jsonify(data)

        except PostManagerException as e:
            data = {"error": True, "title": "Post not Found", "data": str(e)}

            return jsonify(data)

    elif request.method == "DELETE":

        try:
            post_manager.delete_post(post_id)

            data = {
                "title": "Post Deleted",
                "data": {"deleted": True, "post_id": post_id},
            }

            return jsonify(data)

        except PostManagerException as e:
            data = {"error": True, "title": "Post not deleted", "data": str(e)}

            return jsonify(data)


@main.route("/post/create")
def create():
    return render_template("create.html")


@main.route("/post/<string:post_id>/edit")
def update(post_id):
    try:
        post = post_manager.get_by_id(post_id)
        return render_template("edit.html", post=post.to_json())

    except PostManagerException as e:
        data = {"title": "Post not Found", "data": str(e)}

        return redirect(url_for("main.validate", data=data))


@main.route("/validate", methods=["GET", "PUT", "POST", "DELETE"])
def validate():
    req_data = json.loads(request.args.get("data"))

    data = {"title": req_data.get("title"), "data": req_data.get("data")}

    return render_template("validate.html", data=data, json_dump=json.dumps(data))


@main.route("/get-media", methods=["GET"])
def get_image():
    try:
        post_id = request.args.get("postId")
        media_name = request.args.get("mediaName")
        post = post_manager.get_by_id(post_id)

        media_src = post.get_media(media_name)

        data = {"mediaSrc": media_src}

        return jsonify(data)
    except Exception as e:

        return jsonify({"mediaSrc": f"{str(e)}"})
