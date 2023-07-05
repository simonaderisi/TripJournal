from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
#from flask_login import current_user, login_required
#from flaskblog.posts.forms import PostForm
from tripJournal.model import Post
from datetime import datetime
from tripJournal import db, app
from tripJournal.config import S3_BUCKET


@app.route('/create_post', methods=['GET', 'POST'])
#@login_required
def create_post():
    if request.method == 'POST':
        post = Post(
            title=request.form.get('title'),
            author=request.form.get('author'),
            description=request.form.get('description'),
            images=[],
            date=datetime.now()
        )
        p_id = post.id
        for i, image in enumerate(request.files.getlist('images')):
            filename = str(p_id) + str(i) + image.filename.split('.')[1]
            upload_file_to_s3(image, S3_BUCKET, filename)
            file_url = f"https://{S3_BUCKET}.s3.amazonaws.com/{filename}"
            post.images.append(file_url)
        db.session.add(post)
        db.session.commit()
        flash("Posted!")
        return redirect(url_for('homepage'))
    # Se il metodo HTTP non è POST, restituisci la pagina di creazione del post
    return render_template('create_post.html')


@app.route('/delete/<id>', methods=['GET', 'POST'])
def delete_post(id):
    to_delete = Post.query.get(id)
    db.session.delete(to_delete)
    db.session.commit()
    flash("Book is deleted")
    return redirect(url_for('homepage'))
