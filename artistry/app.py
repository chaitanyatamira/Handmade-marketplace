from flask import Flask, render_template, request, redirect, url_for
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import User, Product, Artist, Cart
from db import db

app = Flask(__name__)
app.config.from_object(Config)
import secrets
import string

def generate_secret_key(length=24):
    alphabet = string.ascii_letters + string.digits + '!@#$%^&*(-_=+)'
    return ''.join(secrets.choice(alphabet) for i in range(length))

app.secret_key = generate_secret_key() 
db.init_app(app)
migrate = Migrate(app, db)

# Routes

@app.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)
    





@app.route('/shop')
def shop():
    products = Product.query.all()
    return render_template('shop.html', products=products)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product_detail.html', product=product)

@app.route('/artist/<int:artist_id>')
def artist_profile(artist_id):
    artist = Artist.query.get_or_404(artist_id)
    return render_template('artist_profile.html', artist=artist)

from flask import flash

from models import User  # Assuming you have a User model imported

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # Query the database for the user with the provided email
        user = User.query.filter_by(email=email).first()
        
        if user:
            # Check if the password matches
            if user.password == password:
                # Successful login, flash message and redirect to home page
                flash(f'Logged in as {user.username}', 'success')
                return redirect(url_for('index'))
            else:
                # Password does not match, show error message
                flash('Invalid email or password', 'error')
                return render_template('login.html')
        else:
            # User does not exist, show error message
            flash('Email is not registered', 'error')
            return render_template('login.html')
    
    # For GET request or if login fails, render the login form
    return render_template('login.html')

from flask import flash, redirect, render_template, request, url_for
from models import db, User  # Assuming User model and db instance are imported

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        # Check if the username already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Please choose a different username.', 'error')
            return render_template('register.html')
        
        # If username is unique, create a new user
        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        
        # Flash message for successful registration
        flash('Registration successful! You can now login.', 'success')
        return redirect(url_for('login'))
    
    # For GET request or if registration fails, render the registration form
    return render_template('register.html')




@app.route('/cart')
def cart():
    cart_items = Cart.query.all()  # Replace with your actual query logic
    total_items = len(cart_items)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render_template('cart.html', cart_items=cart_items, total_items=total_items, total_price=total_price)


@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    # Dummy implementation to add product to cart
    user_id = 1  # Replace with actual user ID or retrieve dynamically
    
    # Check if the product is already in the cart
    existing_item = Cart.query.filter_by(user_id=user_id, product_id=product_id).first()
    
    if existing_item:
        # If item exists, increase quantity
        existing_item.quantity += 1
    else:
        # Otherwise, create a new cart item
        new_cart_item = Cart(user_id=user_id, product_id=product_id, quantity=1)
        db.session.add(new_cart_item)
    
    db.session.commit()
    
    # Redirect to cart page after adding the product
    return redirect(url_for('cart'))

@app.route('/remove_from_cart/<int:cart_item_id>', methods=['POST'])
def remove_from_cart(cart_item_id):
    # Implement logic to remove item from cart
    cart_item = Cart.query.get_or_404(cart_item_id)
    db.session.delete(cart_item)
    db.session.commit()
    
    # Redirect back to cart page after removal
    return redirect(url_for('cart'))


@app.route('/payment')
def payment():
    # Implement payment logic here
    return render_template('payment.html')

if __name__ == '__main__':
    app.run(debug=True, port=5007)

