from flask import abort, g, jsonify

from flaskr.api import api_bp
from flaskr.api.auth import token_auth
from flaskr.models import Post


@api_bp.route('/posts/<int:id_>', methods=['GET'])
@token_auth.login_required
def get_post(id_):
    """
    Get blog post with id = `id_`.

    :param int id_: post ID in database (primary key).
    :return: Flask `Response` object with added JSON representation of `Post` and
    `Content-Type: application/json` HTTP header.
    """
    post = Post.query.get(id_) or abort(404)
    if g.current_user.id_ != post.author.id_:
        abort(403)
    return jsonify(post.to_dict())


@api_bp.route('/posts', methods=['GET'])
@token_auth.login_required
def get_all_posts():
    """
    Get all posts available in database.

    :return: Flask `Response` object with added JSON representation of all `Post`
    objects available and `Content-Type: application/json` HTTP header.
    """
    return jsonify(Post.to_collection_dict())


# TODO: add delete & edit endpoints
