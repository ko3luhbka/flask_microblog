from flask import jsonify, request

from flaskr.api import bp
from flaskr.models import Post


@bp.route('/posts/<int:id_>', methods=['GET'])
def get_post(id_):
    """
    Get blog post with id = `id_`.

    :param int id_: post ID in database (primary key).
    :return: Flask `Response` object with added JSON representation of `Post` and
    `Content-Type: application/json` HTTP header.
    """
    return jsonify(Post.query.get_or_404(id_).to_dict())


@bp.route('/posts', methods=['GET'])
def get_posts():
    """
    Get all posts available in database.

    :return: Flask `Response` object with added JSON representation of all `Post`
    objects available and `Content-Type: application/json` HTTP header.
    """
    return jsonify(Post.to_collection_dict())
