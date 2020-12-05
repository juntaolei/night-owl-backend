from flask import Blueprint

doc = Blueprint("doc", __name__, url_prefix="/api")


@doc.route("/doc", methods=["GET"])
def register():
    return doc.send_static_file("api-doc.html")
