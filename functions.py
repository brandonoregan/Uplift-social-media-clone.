def updateLikes(current_user, request, Post, Like, db):
    user_id = current_user.id
    post_id = request.form.get("post_id")

    post = Post.query.filter_by(id=post_id).first()
    if post:
        post.likes = post.likes + 1
        db.session.flush()
        db.session.refresh(post)
        db.session.commit()

    like = Like(user_id=user_id, post_id=post_id)
    db.session.add(like)
    db.session.commit()