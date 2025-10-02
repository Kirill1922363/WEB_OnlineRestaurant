from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from flask_login import current_user, login_required
from sqlalchemy import select
from models import Menu, Orders, User
from settings import Session

bp = Blueprint("orders", __name__)

@bp.route("/create_order", methods=["GET", "POST"])
@login_required
def create_order():
    basket = session.get("basket", {})
    if not basket:
        flash("Your basket is empty!", "warning")
        return render_template("account/basket.html")
    
    menu_ids = list(basket.keys())
    quantities = basket.values()
    with Session() as db_session:
        menu_items = db_session.scalars(
            select(Menu).filter(Menu.id.in_(menu_ids))
        ).all()
    
    if request.method == "POST":
        with Session() as db_session:
            order = Orders(user_id=current_user.id)
            db_session.add(order)
            db_session.flush()
            
            for menu in menu_items:
                order.orders_items.append(menu)
            
            db_session.commit()
            session["basket"] = {}
            flash("Order created successfully!", "success")
            return redirect(url_for("orders.order_history"))
    
    return render_template(
        "account/basket.html", basket=dict(zip(menu_items, quantities))
    )

@bp.route("/clear_basket", methods=["POST"])
def clear_basket():
    session["basket"] = {}
    flash("Basket cleared!")
    return redirect(url_for("menu.list_menu_items"))

@bp.route("/my_orders")
@login_required
def order_history():
    with Session() as session:
        user = session.merge(current_user)
        orders = user.orders
    return render_template("account/history_orders.html", orders=orders)

@bp.route("/cancel_order/<int:order_id>", methods=["POST"])
@login_required
def delete_order(order_id):
    with Session() as session:
        order = session.scalar(select(Orders).filter(Orders.id == order_id))
        if order and order.user_id == current_user.id:
            session.delete(order)
            session.commit()
            flash("Замовлення видалено", "success")
    return redirect(url_for("orders.order_history"))


@bp.route("/basket")
@login_required
def view_basket():
    basket = session.get("basket", {})
    if not basket:
        return render_template("orders/basket.html", basket=None)
    
    menu_ids = [int(id) for id in basket.keys()]
    with Session() as db_session:
        menu_items = db_session.scalars(select(Menu).filter(Menu.id.in_(menu_ids))).all()
    
    basket_items = {}
    for item in menu_items:
        quantity = basket[str(item.id)]
        basket_items[item] = quantity
    
    return render_template("orders/basket.html", basket=basket_items)

@bp.route("/remove_from_basket/<int:item_id>", methods=["POST"])
@login_required
def remove_from_basket(item_id):
    basket = session.get("basket", {})
    if str(item_id) in basket:
        del basket[str(item_id)]
        session["basket"] = basket
        flash("Позицію видалено з кошика", "info")
    return redirect(url_for("orders.view_basket"))
