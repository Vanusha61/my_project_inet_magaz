from app.models import Order, OrderItem, Customer, Product
from database import SessionLocal
from typing import List, Optional, Tuple
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func

def add_customer(name: str, email: str) -> Customer:
    try:
        with SessionLocal() as session:
            customer = Customer(
                name=name,
                email=email,
            )
            session.add(customer)
            session.commit()
            session.refresh(customer)
            return customer
    except Exception as err:
        print(err)
        raise
    except IntegrityError as err:
        print("Такой email уже есть")
        raise

def get_customer_by_email(email: str) -> Optional[Customer]:
    try:
        with SessionLocal() as session:
            customer = session.query(Customer).filter(Customer.email == email).first()
            return customer
    except Exception as err:
        print(err)
        raise

def add_product(name: str, category: str, price: float, stock: int) -> Product:

    try:
        with SessionLocal() as session:
            product = Product(
                name=name,
                category=category,
                price=price,
                stock=stock,
            )
            session.add(product)
            session.commit()
            session.refresh(product)
            return product
    except Exception as err:
        print(err)
        raise

def get_products_by_category(category: str) -> List[Product]:
    try:
        with SessionLocal() as session:
            product = session.query(Product).filter(Product.category == category).all()
            return product
    except Exception as err:
        print(err)
        raise

def add_order(customer_id: int, items: List[Tuple[int, int]]) -> Order:

    try:
        with SessionLocal() as session:
            total = 0
            products = []
            for product_id, quantity in items:
                product = session.query(Product).filter(Product.id == product_id).first()
                if not product or product.stock < quantity:
                    raise ValueError(f"Такого товара нет на складе или его кол-во на  складе меньше чем в заказе!")
                total += product.price * quantity
                product.stock -= quantity
                products.append((product, quantity))

            order = Order(customer_id=customer_id, total_price=total)
            session.add(order)
            session.flush()

            for product, quantity in products:
                order_item = OrderItem(
                    order_id=order.id,
                    product_id=product.id,
                    quantity=quantity,
                    price=product.price,
                )
                session.add(order_item)
            session.commit()
            session.refresh(order)
            return order
    except Exception as err:
        print(err)
        raise

def get_orders_by_customer(customer_id: int) -> List[Order]:
    try:
        with SessionLocal() as session:
            orders = session.query(Order).filter(Order.customer_id == customer_id).all()
            return orders
    except Exception as err:
        print(err)

def get_products_below_stock(threshold: int) -> List[Product]:
    try:
        with SessionLocal() as session:
            products = session.query(Product).filter(Product.stock < threshold).all()
            return products
    except Exception as err:
        print(err)

def get_total_sales() -> Optional[float]:
    try:
        with SessionLocal() as session:
            total = session.query(func.sum(Order.total_price)).scalar()
            return total or 0.0
    except Exception as err:
        print(err)

def list_get_total_customers(customer_id: int) -> str:
    try:
        with SessionLocal() as session:
            total = 0
            order_items = session.query(OrderItem).join(Order).filter(Order.customer_id == customer_id).all()
            for item in order_items:
                total += item.price * item.quantity
            return f"Имя покупателя:"
    except Exception as err:
        print(err)

if __name__ == "__main__":

    print(list_get_total_customers(1))
    print(list_get_total_customers(2))
    # # ------------------------
    # # 1️⃣ Создаём клиентов
    # # ------------------------
    # alice = add_customer("Alice", "alice@example.com")
    # bob = add_customer("Bob", "bob@example.com")
    #
    # print("Клиенты созданы:")
    # print(alice)
    # print(bob)
    #
    # # ------------------------
    # # 2️⃣ Создаём товары
    # # ------------------------
    # product1 = add_product("Laptop", "Electronics", 1000.0, 5)
    # product2 = add_product("Mouse", "Electronics", 50.0, 10)
    # product3 = add_product("Book", "Books", 20.0, 100)
    #
    # print("Товары созданы:")
    # print(product1)
    # print(product2)
    # print(product3)
    #
    # # ------------------------
    # # 3️⃣ Делаем заказ для Alice
    # # ------------------------
    # order1 = add_order(
    #     customer_id=alice.id,
    #     items=[
    #         (product1.id, 1),  # 1 Laptop
    #         (product2.id, 2),  # 2 Mouse
    #     ]
    # )
    # print("Заказ создан для Alice:")
    # print(order1)
    #
    # # ------------------------
    # # 4️⃣ Делаем заказ для Bob
    # # ------------------------
    # order2 = add_order(
    #     customer_id=bob.id,
    #     items=[
    #         (product3.id, 5),  # 5 Books
    #         (product2.id, 1),  # 1 Mouse
    #     ]
    # )
    # print("Заказ создан для Bob:")
    # print(order2)
    #
    # # ------------------------
    # # 5️⃣ Получаем все заказы Alice
    # # ------------------------
    # alice_orders = get_orders_by_customer(alice.id)
    # print(f"Все заказы Alice: {alice_orders}")
    #
    # # ------------------------
    # # 6️⃣ Проверяем товары с низким остатком (stock < 5)
    # # ------------------------
    # low_stock = get_products_below_stock(5)
    # print("Товары с остатком < 5:")
    # for product in low_stock:
    #     print(product)
    #
    # # ------------------------
    # # 7️⃣ Общие продажи
    # # ------------------------
    # total_sales = get_total_sales()
    # print(f"Общая сумма всех заказов: {total_sales}")
