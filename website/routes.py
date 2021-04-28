import os
from flask import render_template, url_for, flash, redirect, request, abort, request
from website import app, db, mail
from flask_login import login_user, current_user, logout_user, login_required
from website.models import load_user, User, Post
from website.forms import LoginForm, SearchForm
from flask_mail import Message
import hashlib
import os
from dotenv import load_dotenv





@app.route('/')
@app.route('/home')
def home(): 
    post1 = Post.query.filter_by(category="Topic1").order_by(Post.date_posted.desc())
    post2 = Post.query.filter_by(category="Topic2").order_by(Post.date_posted.desc())
    post3 = Post.query.filter_by(category="Topic3").order_by(Post.date_posted.desc())
    posts = []
    if(post1.count()>0):
        posts = posts + [post1[0]]
    if(post2.count()>0):
        posts = posts + [post2[0]]
    if(post3.count()>0):
        posts = posts + [post3[0]]
    return render_template('home.html',posts=posts)

@app.route('/about_me')
def about_me():
    post = Post.query.filter_by(category="About")[0]
    return render_template('about_me.html',post=post)

@app.route('/portfolio')
def portfolio():
    return render_template('about_me.html')







@app.route('/topic1')
def topic1():
    page = request.args.get('page',1,type=int)
    posts = Post.query.filter_by(category="Topic1").order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('topic1.html',posts=posts)

@app.route('/topic2')
def topic2():
    page = request.args.get('page',1,type=int)
    posts = Post.query.filter_by(category="Topic2").order_by(Post.date_posted.desc()).paginate(page=page,per_page=5)
    return render_template('topic2.html',posts=posts)

@app.route('/topic3')
def topic3():
    page = request.args.get('page',1,type=int)
    posts = Post.query.filter_by(category="Topic3").order_by(Post.date_posted.desc()).paginate(page=page,per_page=5)
    return render_template('topic3.html', posts=posts)

@app.route("/post/<category>/<int:post_id>")
def post(post_id,category):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


 


@app.route('/search')
def search():
    if(app.elasticsearch.ping()==True):
        Post.reindex()
        query = request.args.get('query')
        posts,total  = Post.search(query,1,5)
        return render_template('search.html',posts=posts)
    else:
        print("Not Connected")
        return redirect(url_for('home'))
    

load_dotenv()
password = os.getenv("ADMIN_PASS")
sender = os.getenv('SENDER_MAIL')
receiver = os.getenv('RECEIVER_MAIL')
#GET ENVIRONMENT VARS HERE
@app.route('/email', methods=["GET","POST"])
def email():
    address = request.args.get('from')
    body = request.args.get('message')
    topic = request.args.get('subject')
    subject = "Blog Message from "+ address + "  " + topic
    msg = Message(subject, 
                    sender='mrhammdotnet@yahoo.com', 
                    recipients=['hammbenjamini@gmail.com'],
                    body = body) 
    
    mail.send(msg)
    return redirect(url_for('home'))



password = os.getenv("ADMIN_PASS")

@app.route('/LoginToEdit',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.get(1)
        submittedPw = hashlib.sha256(form.password.data.encode('ascii')).hexdigest()
        print(submittedPw)
        if user and submittedPw==password:
            login_user(user)
            return redirect(url_for('home'))
    return render_template('login.html',form=form)

@app.route('/logout', methods = ['GET'])
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/testpost')
def testpost():
    return render_template('testpost.html')

@app.errorhandler(404)
def error_404(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(403)
def error_403(error):
    return render_template('errors/403.html'), 403

@app.errorhandler(500)
def error_500(error):
    return render_template('errors/500.html'), 500