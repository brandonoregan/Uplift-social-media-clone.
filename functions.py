# Function from the app.py


# function for post_like() route
def updateLikes(current_user, request, Post, Like, db):
    user_id = current_user.id
    post_id = request.form.get("post_id")

    post = Post.query.filter_by(id=post_id).first()
    if post:
        if post.likes is None:
            post.likes = 1
        else:
            post.likes = post.likes + 1
        db.session.flush()
        db.session.refresh(post)
        db.session.commit()

    like = Like(user_id=user_id, post_id=post_id)
    db.session.add(like)
    db.session.commit()


# function for signup()
def signUpUser(form, bcrypt, User, db, flash, login_user):
    """retrieve form data and add user to database"""

    # Retrieve and store form data in variables
    username = form.username.data
    email = form.email.data
    password = form.password.data

    # Generate hashed password and store in variable
    hashed_pw = bcrypt.generate_password_hash(password).decode("utf-8")

    # Create a user instace of the User class
    user = User(username=username, email=email, password=hashed_pw)

    # Add user to database
    db.session.add(user)
    db.session.commit()

    # notify user of successful for submission
    flash("Sign up successful, Welcome to UPLIFT!")

    # Log in the user and redirect to the specified page
    login_user(user)


# function for adding post to db in upload_post() route function
def addPost(db, Image, Post, current_user, post_form, desc):
    # Query database to find most recent image
    img_tup = db.session.query(Image.id).order_by(Image.id.desc()).first()
    pic_id = img_tup[0]

    # create instance of model
    post = Post(user_id=current_user.id, content=post_form.title.data, pic_id=pic_id)

    # add post to db
    db.session.add(post)
    db.session.commit()


# reset post form to default state
def resetFormPost(Image, db, desc, post_form):
    # Update state of most recent image in database
    most_recent_image = db.session.query(Image).order_by(desc(Image.id)).first()
    most_recent_image.draft = False
    db.session.commit()

    # clear form inputs
    post_form.title.data = ""


# Check user credentials and login user
def loginUser(User, form, bcrypt, login_user, flash):
    user = User.query.filter_by(username=form.username.data).first()
    if user:
        if bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)

        else:
            flash("Incorrect username or password.")
    else:
        flash("Username does not exist.")


# function for deleting comment from UI & db
def deleteComment(request, db, Comment, current_user):
    db_comment_id = request.form.get("comment_id")
    comment = db.session.get(Comment, db_comment_id)

    if comment and comment.user_id == current_user.id:
        db.session.delete(comment)
        db.session.commit()


# Add post comment to database
def addComment(datetime, Comment, current_user, request, newComForm, db):
    # Get user current time
    timestamp = datetime.utcnow()

    # create instance of class
    comment = Comment(
        user_id=current_user.id,
        post_id=request.form.get("post_id"),
        content=newComForm.comment.data,
        timestamp=timestamp,
    )

    # add instance to db
    db.session.add(comment)
    db.session.commit()

    # clear form input data
    newComForm.comment.data = ""


# upload an image to the UI and db
def uploadImage(request, secure_filename, app, os, flash, Image, current_user, db):
    # Get uploaded image data
    file = request.files["upload"]
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    draft = True

    # Save the uploaded image to the server
    file.save(filepath)

    # Check if file exists
    if not file:
        flash("No file uploaded")

    # Create Image instance and add to db
    img = Image(
        filepath=filepath,
        mimetype=file.mimetype,
        name=filename,
        user_id=current_user.id,
        draft=draft,
    )

    # Add instance to database
    db.session.add(img)
    db.session.commit()


# Update profile image in UI and DB
def updateProfileImage(
    request, secure_filename, app, os, flash, Image, current_user, db, User
):
    # Get uploaded image data
    file = request.files["upload"]
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)

    # Save the uploaded image to the server
    file.save(filepath)

    # Check if file exists
    if not file:
        flash("No file uploaded")

    # Create Image instance and add to db
    img = Image(
        filepath=filepath,
        mimetype=file.mimetype,
        name=filename,
        user_id=current_user.id,
    )

    # Update database
    db.session.add(img)
    db.session.commit()

    # Update associated database tables
    user = db.session.get(User, current_user.id)
    user.pic_id = img.id
    db.session.commit()
