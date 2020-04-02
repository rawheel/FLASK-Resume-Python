from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import datetime
import json
from flask_mail import Mail


with open('config.json','r') as c:
    params = json.load(c)["params"]
local_server = True
app = Flask(__name__)

#to connect with gmail

app.config.update(
    MAIL_SERVER  = 'smtp.gmail.com',
    MAIL_PORT = '465',
    MAIL_USE_SSL =True,
    MAIL_USERNAME = params['user_mail'],
    MAIL_PASSWORD = params['user_pass']
)
mail = Mail(app)

#a9apppp.config['SQLALCHEMY_DATABASE_URI'] = 'mysql//username:password@localhost/db_name'



if(local_server):

    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']

db = SQLAlchemy(app)

class Contact(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(20),nullable=False)
    email=db.Column(db.String(20),nullable=False)
    phone_no=db.Column(db.String(12),nullable=False)
    message=db.Column(db.String(200),nullable=False)
    date=db.Column(db.String(20),nullable=True)

class Posts(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(20),nullable=False)
    content=db.Column(db.String(200),nullable=False)
    date=db.Column(db.String(20),nullable=True)
    slug = db.Column(db.String(21), nullable=False)
    img_file = db.Column(db.String(20))
@app.route('/')
def home():
    return render_template("index.html",params=params)

@app.route('/about')
def about():
    return render_template("about.html",params=params)

@app.route('/contact', methods = ['GET', 'POST'])
def contact():
    if(request.method=='POST'):

        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')
        date = str(datetime.datetime.now().strftime("%d %B %Y"))
        #red wala name,email etc Contact ke attributes hen
        ob1 = Contact(name=name,email=email,phone_no=phone,message=message,date=date)
        db.session.add(ob1)
        db.session.commit()
        mail.send_message('New message from '+name,
                          sender=email,
                          recipients= [params['user_mail']],
                          body=message + "\n" + phone )

    return render_template('contact.html',params=params)


@app.route('/post/<string:post_slug>',methods=['GET'])
def post(post_slug):
    post = Posts.query.filter_by(slug=post_slug).first()
    return render_template("post.html",params=params,post=post)

app.run()