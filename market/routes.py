from flask_login import login_user, login_required, logout_user, current_user
from market import app
from flask import render_template, redirect, url_for, flash, request
from market.forms import PurchaseItemForm, RegisterForm, LoginForm
from market.models import *



@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html',title='HomePage')

@app.route('/items',methods=['GET', 'POST'])
@login_required
def view_items():
    form = PurchaseItemForm()
    if request.method == 'POST':
        purchased_item = request.form.get('purchased_item')
        p_item = item.query.filter_by(name=purchased_item).first()
        if p_item:
            if current_user.can_purchase(p_item):
                p_item.buy(current_user)
                flash(f'Congrats!You have succesfully bought {p_item.name} for {p_item.price}','success')
            else:
                flash(f'Unfortunately, you don\'t have enough money to purchase {p_item.name}!','danger')    

        return redirect(url_for('view_items'))
    if request.method  == 'GET':
        items = item.query.filter_by(owner=None)

    
    return render_template('items.html',items=items,title='Items Page',purchase_form=form)

@app.route('/register',methods=['GET','POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email=form.email.data,
                              password = form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        flash('Account Created Succesfully! Please log in.','success')
        return redirect(url_for('login_page'))
    if form.errors != {}:
        for err in form.errors.values():
            flash(f'An error occured while registering. {err}','danger')
    return render_template('register.html',form=form)

@app.route('/login',methods=['GET','POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password(attempted_password=form.password.data):
            login_user(attempted_user)
            flash(f'You have succesfully logged in as {attempted_user.username}','success')
            return redirect(url_for('home'))
        else:
            flash(f'Login failed! Please provide valid credentials and try again!','danger')
                
    return render_template('login.html',form=form,title='Login Page')

@app.route("/logout",methods=['GET','POST'])
@login_required
def logout_page():
    logout_user()
    flash(f'Logged out succesfully!','success')
    return redirect(url_for('login_page'))

@app.route("/profile/<id>",methods=['GET','POST'])
@login_required
def user_profile(id):
    user = User.query.filter_by(id=id).first_or_404()
    return render_template('profile.html',user=user)