from models import Base, User, Menu, Orders, Reservations
from settings import Session
from werkzeug.security import generate_password_hash


# Ініціалізація бази даних і додавання товарів
def init_db():
    base = Base()
    base.drop_db()
    base.create_db()  # Створюємо таблиці

    session = Session()

    user = User(
        username="admin", 
        email="admin@example.com", 
        hash_password=generate_password_hash("admin"),
        is_admin=True
    )
    
    user2 = User(
        username="user", 
        email="user@example.com", 
        hash_password=generate_password_hash("user"),
    )
    
    m1 = Menu(
        name="Гункани з тунцем",
        price=150.00,
        rating=4,
        description="4 шт., тунець, ікра тобіко, майонез",
        image_path=None,
        category="Гункани",
        active=True
    )

    m2 = Menu(
        name="Філадельфія класична",
        price=220.00,
        rating=5,
        description="8 шт., лосось, авокадо, вершковий сир, рис, норі",
        image_path=None,
        category="Роли",
        active=True
    )

    m3 = Menu(
        name="Піца Маргарита",
        price=180.00,
        rating=5,
        description="Класична піца з сиром моцарела та томатним соусом",
        image_path=None,
        category="Піца",
        active=True
    )

    m4 = Menu(
        name="Паста Карбонара",
        price=200.00,
        rating=4,
        description="Паста з беконом, вершковим соусом і сиром пармезан",
        image_path=None,
        category="Паста",
        active=True
    )

    m5 = Menu(
        name="Лимонад",
        price=60.00,
        rating=5,
        description="Домашній лимонад з лимоном і м’ятою",
        image_path=None,
        category="Напої",
        active=True
    )

    session.add_all([user, user2, m1, m2, m3, m4, m5])  
    session.commit()
    session.close()


if __name__ == "__main__":
    init_db()
