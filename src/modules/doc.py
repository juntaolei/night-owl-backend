from flask import Blueprint, render_template

doc = Blueprint("doc", __name__, url_prefix="/api")


@doc.route("/doc", methods=["GET"])
def register():
    return render_template("api-doc.html")
