from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from flask_login import login_required
from datetime import datetime

from . import db
from .models import Content, Tag, ContentAndTag
from .blog import Blog

import json

views = Blueprint("views", __name__)

def show_blogs(search="", tag_id=None):
    list_blogs = []
    if tag_id == None:
        all_contents = Content.query.filter(Content.data.like('%'+search+'%')).order_by(Content.id.desc()).all()
        for content in all_contents:
            list_tags = []
            all_content_and_tag = ContentAndTag.query.filter_by(content_id=content.id).all()
            for content_and_tag in all_content_and_tag:
                tag = Tag.query.filter_by(id=content_and_tag.tag_id).first()
                list_tags.append(tag.name_tag)
            blog = Blog(content.id, content.title, content.data, content.date, list_tags)
            list_blogs.append(blog)

    else:
        filter_contentAndTags = ContentAndTag.query.filter_by(tag_id=tag_id).order_by(ContentAndTag.id.desc()).all()
        for contentAndTag in filter_contentAndTags:
            content = Content.query.filter_by(id=contentAndTag.content_id).first()
            list_tags = []
            all_content_and_tag = ContentAndTag.query.filter_by(content_id=content.id).all()
            for content_and_tag in all_content_and_tag:
                tag = Tag.query.filter_by(id=content_and_tag.tag_id).first()
                list_tags.append(tag.name_tag)
            blog = Blog(content.id, content.title, content.data, content.date, list_tags)
            list_blogs.append(blog)
    
    return list_blogs

def show_tags():
    list_tags = []
    all_tags = Tag.query.all()
    for tag in all_tags:
        list_tags.append(tag)

    return list_tags

@views.route("/index")
@views.route("/")
def guest():
    return render_template("index.html", list_blogs=show_blogs(), list_tags=show_tags())

@views.route("/admin")
@login_required
def admin():
    return render_template("admin.html", list_blogs=show_blogs(), list_tags=show_tags())

@views.route("/add", methods=["GET", "POST"])
@login_required
def add():
    if request.method == "POST":
        title = request.form.get("title")
        data = request.form.get("data")
        tags = request.form.get("tags")
        tag_list = tags.replace(" ", "").split(",")

        new_content = Content(title=title, data=data, date=datetime.now())
        db.session.add(new_content)
        db.session.commit()

        content_new_id = Content.query.order_by(Content.id.desc()).first().id
        for name_tag in tag_list:
            tag = Tag.query.filter_by(name_tag=name_tag).first()
            if not tag:
                new_tag = Tag(name_tag=name_tag)
                db.session.add(new_tag)
                db.session.commit()
                new_tag_id = Tag.query.order_by(Tag.id.desc()).first().id
                new_contentAndTag = ContentAndTag(content_id=content_new_id, tag_id=new_tag_id)
            else:
                new_contentAndTag = ContentAndTag(content_id=content_new_id, tag_id=tag.id)
            db.session.add(new_contentAndTag)
            db.session.commit()

    return redirect(url_for("views.admin"))

@views.route("/update", methods=["GET", "POST"])
@login_required
def update():
    if request.method == "POST":
        content_id = request.form.get("content_id")
        title = request.form.get("title")
        data = request.form.get("data")
        tags = request.form.get("tags")
        tag_list = tags.replace(" ", "").split(",")

        content_update = Content.query.filter_by(id=content_id).first()
        if content_update:
            content_update.title = title
            content_update.data = data
            content_update.date = datetime.now()
            db.session.commit()

        contentAndTags_delete = ContentAndTag.query.filter_by(content_id=content_id).all()
        for contentAndTag in contentAndTags_delete:
            count_tag = ContentAndTag.query.filter_by(tag_id=contentAndTag.tag_id).count()
            if count_tag == 1:
                delete_tag = Tag.query.filter_by(id=contentAndTag.tag_id).first()
                db.session.delete(delete_tag)
            db.session.delete(contentAndTag)
        db.session.commit()

        for name_tag in tag_list:
            tag = Tag.query.filter_by(name_tag=name_tag).first()
            if not tag:
                new_tag = Tag(name_tag=name_tag)
                db.session.add(new_tag)
                db.session.commit()
                new_tag_id = Tag.query.order_by(Tag.id.desc()).first().id
                new_contentAndTag = ContentAndTag(content_id=content_id, tag_id=new_tag_id)
            else:
                new_contentAndTag = ContentAndTag(content_id=content_id, tag_id=tag.id)
            db.session.add(new_contentAndTag)
            db.session.commit()
    
    return redirect(url_for("views.admin"))

@views.route("/delete", methods=["GET", "POST"])
@login_required
def delete():
    blog = json.loads(request.data)
    blog_id = blog["blog_id"]

    contentAndTags_delete = ContentAndTag.query.filter_by(content_id=blog_id).all()
    for contentAndTag in contentAndTags_delete:
        count_tag = ContentAndTag.query.filter_by(tag_id=contentAndTag.tag_id).count()
        if count_tag == 1:
            delete_tag = Tag.query.filter_by(id=contentAndTag.tag_id).first()
            db.session.delete(delete_tag)
        db.session.delete(contentAndTag)

    content = Content.query.filter_by(id=blog_id).first()
    db.session.delete(content)
    db.session.commit()

    return jsonify({"code": 200})

@views.route("/search_in_admin", methods=["GET", "POST"])
@login_required
def search_in_admin():
    if request.method == "POST":
        text = request.form.get("search")
        print(text)
    return render_template("admin.html", list_blogs=show_blogs(text), list_tags=show_tags())

@views.route("/search_in_guest", methods=["GET", "POST"])
def search_in_guest():
    if request.method == "POST":
        text = request.form.get("search")
        print(text)
    return render_template("index.html", list_blogs=show_blogs(text), list_tags=show_tags())

@views.route("/filter_in_admin", methods=["GET", "POST"])
@login_required
def filter_in_admin():
    tag_id = request.args.get('tag_id')
    return render_template("admin.html", list_blogs=show_blogs(tag_id=tag_id), list_tags=show_tags())

@views.route("/filter_in_guest", methods=["GET", "POST"])
def filter_in_guest():
    tag_id = request.args.get('tag_id')
    return render_template("index.html", list_blogs=show_blogs(tag_id=tag_id), list_tags=show_tags())