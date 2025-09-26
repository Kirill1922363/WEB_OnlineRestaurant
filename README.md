Online Coffee Shop on Flask ☕

This web application simulates an online coffee shop where users can browse the menu, add items to the cart, and place orders.

The application is built using Flask and popular Python libraries.

📌 Features

Browse the menu with different categories of drinks and desserts.

Add items to the cart and update quantities.

Place orders with customer information.

Admin panel for managing menu items and orders.

Responsive design for mobile-friendly use.

🛠 Technologies

Backend: Python, Flask

Database: SQLite / PostgreSQL

Frontend: HTML, CSS, Jinja2 (Flask templates)

Extras: Flask-Login, Flask-WTF, Flask-Migrate

⚡ Installation & Setup

Clone the repository:

git clone https://github.com/yourusername/online-coffee-shop.git
cd online-coffee-shop


Create and activate a virtual environment:

python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate


Install dependencies:

pip install -r requirements.txt


Configure environment variables in a .env file:

FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your_secret_key
DATABASE_URL=sqlite:///coffee_shop.db


Initialize the database:

flask db init
flask db migrate -m "Initial migration"
flask db upgrade


Run the application:

flask run


Open your browser at http://127.0.0.1:5000


📝 Notes

Make sure to set a secure SECRET_KEY for production.

You can switch to PostgreSQL or MySQL by updating DATABASE_URL in .env.

Admin credentials can be configured directly in the database or through an admin registration route.
