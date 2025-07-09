def product_data(**kwargs):
    data = {
        "name": "Iphone 14 Pro Max",
        "quantity": 10,
        "price": "8500",
        "status": True,
    }
    data.update(kwargs)
    return data


def products_data():
    return [
        product_data(name="iPhone 15 Pro", price="7500"),
        product_data(name="iPhone 13 Mini", price="4500"),
        product_data(name="MacBook Pro", price="10500"),
    ]