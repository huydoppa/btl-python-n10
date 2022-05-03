from flask import render_template,session, request,redirect,url_for,flash
from shop import app,db,bcrypt
from .forms import RegistrationForm,LoginForm
from .models import User
from shop.products.models import Addproduct,Category,Brand


@app.route('/admin')
def admin():
    if session.get('role') == 'admin':
        products = Addproduct.query.all()
        return render_template('admin/index.html', title='Admin page',products=products)
    else:
        return redirect(url_for('login'))

@app.route('/brands')
def brands():
    if session.get('role') == 'admin':
        brands = Brand.query.order_by(Brand.id.desc()).all()
        return render_template('admin/brand.html', title='brands',brands=brands)
    else:
        return redirect(url_for('login'))
        


@app.route('/categories')
def categories():
    if session.get('role') == 'admin':
        categories = Category.query.order_by(Category.id.desc()).all()
        return render_template('admin/brand.html', title='categories',categories=categories)
    else:
        return redirect(url_for('login'))
        

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        user = User(name=form.name.data,username=form.username.data, email=form.email.data,
                    password=hash_password,role="admin")
        db.session.add(user)
        flash(f'welcome {form.name.data} Thanks for registering','success')
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('admin/register.html',title='Register user', form=form)


@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if request.method == "POST":
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                session['email'] = form.email.data
                session['role']='admin'
                flash(f'welcome {form.email.data} you are logedin now','success')
                return redirect(url_for('admin'))
            else:
                flash(f'Wrong email and password', 'success')
                return redirect(url_for('login'))
    return render_template('admin/login.html',title='Login page',form=form)