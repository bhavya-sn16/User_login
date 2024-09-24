from flask import Flask, render_template,request, url_for,flash,redirect,jsonify,send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,PasswordField,BooleanField,ValidationError
from wtforms.validators import DataRequired,EqualTo,Length
from sqlalchemy import Column, Integer, String, ForeignKey, func
from sqlalchemy.orm import relationship, Mapped, MappedColumn, mapped_column,backref
from datetime import datetime,timezone
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from jinja_partials import render_partial
from flask_migrate import Migrate




app  = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SECRET_KEY'] = "keysecret"
db = SQLAlchemy(app)

migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class LoginForm(FlaskForm):
    username= StringField("Enter Username", validators=[DataRequired()])
    password = PasswordField("Enter password", validators=[DataRequired()])
    submit = SubmitField("Submit", validators=[DataRequired()])
    

class AddUser(FlaskForm):
    name= StringField("Enter your name", validators=[DataRequired()])
    email = StringField("Enter e-mail id", validators=[DataRequired()])
    contactno =StringField("Your Contact number", validators=[DataRequired()])
    submit = SubmitField("Add", validators=[DataRequired()])
    # submit = SubmitField("Close", validators=[DataRequired()])


@app.route('/add_user',methods = ['GET','POST'])
def add_user():
     print("***")
     form = AddUser()
     data = request.json
     name = data.get('name')
     email = data.get('email')
     contactno = data.get('contactno')
     print(f"Name: {name}, Email: {email}, Contact: {contactno}")
    
     print("5555555")
     if request.method == 'POST':
          user = User.query.filter_by(email = email).first()
          print("bla")
          if user is None:
               user = User(first_name=name, email=email, contact_no= contactno,
                             password_hash="2222220",middle_name= "Bilius",last_name="Weasly",created_by="Arthur and Molly", 
                             updated_by="Hogwarts")
               print("you have not failed")
               db.session.add(user)
               db.session.commit()
               users = User.query.all()
               users = [{"first_name": User.first_name, "email": User.email, "contact_no": User.contact_no}]
               flash("User added successfully")
               
               return render_template('partials/table.html',users = users)
          else:
             flash("User already exists")

          form.name.data=''
          form.email.data=''
          form.contactno.data=''

     return render_template('partials/_add.html', name= name, form = form )


@app.route('/update',methods = ['GET','POST'])
def update():
    print("blablabla")
    form = AddUser()
    data = request.json
    name = data.get('name')
    email = data.get('email')
    contactno = data.get('contactno')
    user_id = data.get('userId')
    print(f"Name: {name}, Email: {email}, Contact: {contactno}, UserId:{user_id}")
    name_to_update = User.query.get_or_404(user_id)
    users = User.query.all()
    print(f"Fetched user: {name_to_update}")
    if request.method == "POST":
        print("trick")
        name_to_update.first_name = name
        name_to_update.email = email
        name_to_update.contact_no = contactno
        try:
            db.session.commit()
            
            flash("User Updated")
            return render_template('partials/table.html',users = users, name_to_update = name_to_update)
        except:
            flash("There is some kind of error")
            return render_template('partials/table.html',users = users, name_to_update= name_to_update)
        
    else:
        return render_template('partials/table.html',users = users, name_to_update= name_to_update)  



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/', methods=['GET', 'POST'])
@app.route('/login',methods = ['GET','POST'])
def login():
    print("hiii")
    form = LoginForm()
    if request.method== 'POST':
     print(".......")
     print(form.username.data)
     print(form.password.data)

    #  if form.validate_on_submit():
      
    #  user = User.query.filter_by(email=form.username.data).first()
     if form.username.data == 'admin@123' and  form.password.data == 'admin':
            
                # login_user(user)
                flash("Login successful")
                return render_template('dashboard.html')
     else:
                flash("Wrong Password")
    else:
            flash("The user does'nt exist")
    return render_template('partials/login.html',form=form)    

@app.route('/users',methods=['GET', 'POST'] )
# @login_required
def users():
    user_list = User.query.all()
    return render_template('partials/table.html', users=user_list)


@app.route("/search")
def search():
    q = request.args.get("q")
    print(q)

    if q:
        results = User.query.filter(User.first_name.icontains(q) | User.email.icontains(q)) \
        .order_by(User.first_name.asc()).limit(100).all()
    else:
        results = []

    return render_template("search_results.html", results=results)

@app.route('/delete/<int:id>')
def delete(id):
    user_to_delete = User.query.get_or_404(id)
    name = None
    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash("User Deleted")
        users = User.query.all()
        return render_template('partials/table.html', name= name, users = users)
    except:
        flash("There was a problem")
        users = User.query.all()
        return render_template('partials/table.html',  name= name, users = users)


@app.route("/reload")
def reload():
#    q = db.query(User).order_by(User.user_id)
#    results = q.all()
   
   results = User.query.all()
   return render_template("search_results.html", results=results)
#   return '<p>hii</p>'

@app.route('/get_user_data/<user_id>', methods=['GET'])
def get_user_data(user_id):
    # Fetch user from the database based on user_id
    user = User.query.get_or_404(user_id)
    
    if user:
        print("Pudding....")
        return jsonify({
            'name': user.first_name,
            'email': user.email,
            'contactno': user.contact_no
        })
    else:
        return jsonify({'error': 'User not found'}), 404


@app.route('/dashboard',methods=['GET', 'POST'] )
# @login_required
def dashboard():
    return render_template('dashboard.html')

@app.route("/show/table")
def show_post():
    print("jjjjjjj")
    post = User.query.all()
    return render_template('partials/show.html', post=post)

class User(db.Model, UserMixin):  
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100),unique=True)
    password_hash = db.Column(db.String(500))
    first_name = db.Column(db.String(100),nullable=False)
    middle_name = db.Column(db.String(100),nullable=False)
    last_name = db.Column(db.String(100))
    contact_no =  db.Column(db.String(100),nullable=False)
    alt_contact_no = db.Column(db.String(100), nullable=True, default=None)
    company_id = mapped_column(Integer, ForeignKey("company.comp_id"))
    company = relationship("Company",backref=backref('users', lazy=True))
    is_deleted = db.Column(db.Boolean, default=False) 
    created_by = db.Column(db.String(100), nullable=False)
    created_dt = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_by = db.Column(db.String(100), nullable=False)
    updated_dt = db.Column(db.DateTime(timezone=True), server_default=func.now())

    # @property
    # def password(self):
    #     raise AttributeError("Not Readable")
    # @password.setter
    # def password(self,password):
    #     self.password_hash = generate_password_hash(password)

    # def varify_password(self,password)  :
    #     return check_password_hash(self.password_hash)  
    

class Company(db.Model):
    comp_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    code = db.Column(db.String(5),  unique=True, nullable=False)
    name = db.Column(db.String(100),unique=True,nullable=False)
    contact_no =  db.Column(db.String(100))
    email_address = db.Column(db.String(100),unique=True)
    address = db.Column(db.String(100),unique=False)
    license_num = db.Column(db.String(100))
    logo_url = db.Column(db.String(500),unique=False)
    is_deleted = db.Column(db.Boolean, default=False)
    created_by = db.Column(db.String(100), nullable=False)
    created_dt = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_by = db.Column(db.String(100), nullable=False)
    updated_dt = db.Column(db.DateTime(timezone=True), server_default=func.now())
    def _repr_(self):
        return f'<Company {self.name}>'
    
c1 = Company(
    code='h1',
    name='Gryffindor',
    contact_no='51879565984',
    email_address='gryffindor@hogwarts.com',
    address='Hogsmede village',
    license_num='BMOM558785',
    logo_url='http://example.com/logo1.png',
    created_by='admin',
    updated_by='admin'
)    

c2 = Company(
    code='H2',
    name='Slytherin',
    contact_no='441125',
    email_address='raven@h.com',
    address='godrics hollow',
    license_num='BMOM4474',
    logo_url='http://example.com/logo1.png',
    created_by='admin',
    updated_by='admin'
)








with app.app_context():
     db.create_all()
  
    #  db.session.add_all([c1, c2])
    #  db.session.commit()
#      g1 = Company.query.filter_by(code='h1').first()
#      r1 = Company.query.filter_by(code='H2').first()
#      print(g1)
#      print(r1)


#      user1 = User(
#     email='harry@hogwarts.com',
#     password_hash='hashed_password1',
#     first_name='Harry',
#     middle_name='James',
#     last_name='Potter',
#     contact_no='1125587444',
#     alt_contact_no='2225455441',
#     company=g1,
#     created_by='admin',
#     updated_by='admin'
# )

#      user2 = User(
#     email='albus@hogwarts.com',
#     password_hash='hashed_password2',
#     first_name='Albus',
#     middle_name='Severus',
#     last_name='Potter',
#     contact_no='548799631',
#     alt_contact_no='4122581295',
#     company=r1,
#     created_by='admin',
#     updated_by='admin'
# )

#      user3 = User(
#     email='hermione@hogwarts.com',
#     password_hash='hashed_password3',
#     first_name='Hermione',
#     middle_name='Jean',
#     last_name='Granger',
#     contact_no='54879798731',
#     alt_contact_no='4121121295',
#     company=g1,
#     created_by='admin',
#     updated_by='admin'
# )
#      db.session.add_all([user1, user2, user3])
#      db.session.commit()


if __name__ == '__main__':
    app.run(debug=True)     


