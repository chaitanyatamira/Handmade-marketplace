from app import app
from db import db
from models import User, Product, Artist, Cart

with app.app_context():
    db.create_all()

    # Adding dummy artists
    artist1 = Artist(name="Rajesh Kumar", bio="Rajesh is a traditional weaver from Rajasthan, known for his intricate patterns.")
    artist2 = Artist(name="Srikant Sahu", bio="Srikant crafts beautiful pottery, inspired by ancient Indian designs.")
    artist3 = Artist(name="Ramesh Chandra", bio="Ramesh Chandra is a woodworker who creates stunning furniture pieces.")

    db.session.add_all([artist1, artist2, artist3])
    db.session.commit()

    # Adding dummy products with image URLs
    product1 = Product(name="Handwoven Scarf", description="A beautiful handwoven scarf made from organic cotton.", price=25.0, artist_id=artist1.id)
    product2 = Product(name="Clay Pot", description="A traditional clay pot perfect for your kitchen.", price=15.0, artist_id=artist2.id)
    product3 = Product(name="Wooden Chair", description="A handcrafted wooden chair with intricate carvings.", price=150.0, artist_id=artist3.id)
    product4 = Product(name="Embroidered Cushion Cover", description="A cushion cover with exquisite embroidery.", price=20.0, artist_id=artist1.id)
    product5 = Product(name="Ceramic Vase", description="A beautifully painted ceramic vase.", price=30.0, artist_id=artist2.id)
    product6 = Product(name="Wooden Table", description="A sturdy wooden table made from reclaimed wood.", price=200.0, artist_id=artist3.id)

    db.session.add_all([product1, product2, product3, product4, product5, product6])
    db.session.commit()
