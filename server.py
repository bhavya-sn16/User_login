from flask import Flask, render_template,request, url_for,flash,redirect
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,PasswordField,BooleanField,ValidationError
from wtforms.validators import DataRequired,EqualTo,Length
from sqlalchemy import Column, Integer, String, ForeignKey, func
from sqlalchemy.orm import relationship, Mapped, MappedColumn, mapped_column,backref
from datetime import datetime,timezone
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user




app  = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SECRET_KEY'] = "keysecret"
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class LoginForm(FlaskForm):
    username= StringField("Enter Username", validators=[DataRequired()])
    password = PasswordField("Enter password", validators=[DataRequired()])
    submit = SubmitField("Submit", validators=[DataRequired()])

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
      
        # user = User.query.filter_by(email=form.username.data).first()
     if form.username.data == 'admin@123' and  form.password.data == 'admin':
            
                # login_user(user)
                flash("Login successful")
                return render_template('dashboard.html')
     else:
                flash("Wrong Password")
    else:
            flash("The user does'nt exist")
    return render_template('login.html',form=form)    

@app.route('/users')
# @login_required
def users():
    user_list = User.query.all()
    return render_template('table.html', users=user_list)


@app.route('/dashboard')
# @login_required
def dashboard():
    return render_template('dashboard.html')

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


