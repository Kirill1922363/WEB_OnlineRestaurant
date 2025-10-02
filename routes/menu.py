from flask import (
    Blueprint,
    abort,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from flask_login import login_required
from sqlalchemy import select
from models import Menu, User
from settings import Session

bp = Blueprint("menu", __name__)


@bp.route("/menu")
def list_menu_items():
    with Session() as session:
        menu_items = session.scalars(select(Menu).filter_by(active=True))
        menu_items_list = [
            {"id": i.id, "name": i.name, "price": i.price, "image_path": i.image_path}
            for i in menu_items
        ]
    return render_template(
        "menu/list.html", menu_items=menu_items_list, title="Menu Aurora"
    )


@bp.route("/<int:item_id>")
def details_menu_item(item_id):
    with Session() as session:
        menu_item = session.scalar(select(Menu).where(Menu.id == item_id))
        if not menu_item:
            return abort(404)

        similar_items = session.scalars(
            select(Menu)
            .where(
                Menu.category == menu_item.category,
                Menu.id != item_id,
                Menu.active == True,
            )
            .limit(4)
        ).all()

    return render_template(
        "menu/details.html", menu_item=menu_item, similar_items=similar_items
    )


@bp.route("/order/add/<int:item_id>", methods=["POST"])
@login_required
def add_to_order(item_id):
    quantity = request.form.get("quantity", 1, type=int)
    if "basket" not in session:
        basket: dict = {}
        basket[str(item_id)] = quantity
        session["basket"] = basket
    else:
        basket = session.get("basket", {})
        if str(item_id) in basket:
            basket[str(item_id)] += quantity
        else:
            basket[str(item_id)] = quantity
        session["basket"] = basket
    flash(f"позицію {item_id} додано до кошика")
    return redirect(url_for("menu.details_menu_item", item_id=item_id))
