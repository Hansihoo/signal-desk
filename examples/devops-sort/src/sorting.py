def sort_products(products):
    if not isinstance(products, list):
        raise ValueError('products must be a list')
    for product in products:
        if not isinstance(product, dict):
            raise ValueError('each product must be an object')
        if not isinstance(product.get('id'), str) or not product['id']:
            raise ValueError('id must be a nonempty string')
        price = product.get('price')
        if type(price) is not int or price < 0:
            raise ValueError('price must be a nonnegative integer')
    return sorted(products, key=lambda product: product['price'])
