import os
import time

import requests


_moltin_token = None


def get_elasticpath_access_token():
    elasticpath_client_id = os.environ["ELASTICPATH_CLIENTD_ID"]
    elasticpath_client_secret = os.environ["ELASTICPATH_CLIENTD_SECRET"]

    elasticpath_api_key_url = "https://api.moltin.com/oauth/access_token"
    data = {
        "client_id": elasticpath_client_id,
        "client_secret": elasticpath_client_secret,
        "grant_type": "client_credentials",
    }

    response = requests.post(elasticpath_api_key_url, data=data)
    response.raise_for_status()

    return response.json()


def get_elasticpath_headers():
    global _moltin_token
    global _token_expires

    if not _moltin_token or time.time() > _token_expires:
        access_token = get_elasticpath_access_token()

        _moltin_token = access_token["access_token"]
        _token_expires = access_token["expires"]

    return {
        "Authorization": f"Bearer {_moltin_token}",
        "X-MOLTIN_CURRENCY": "USD",
    }


def fetch_fish_shop_goods():
    headers = get_elasticpath_headers()

    fish_shop_url = "https://api.moltin.com/v2/products"

    response = requests.get(fish_shop_url, headers=headers)
    response.raise_for_status()

    return response.json()


def fetch_fish_shop_good(good_id):
    headers = get_elasticpath_headers()

    fish_shop_url = f"https://api.moltin.com/v2/products/{good_id}"

    response = requests.get(fish_shop_url, headers=headers)
    response.raise_for_status()

    return response.json()


def add_good_to_cart(good_id, cart_id, quantity):
    headers = get_elasticpath_headers()

    add_good_to_cart_url = f"https://api.moltin.com/v2/carts/{cart_id}/items"

    payload = {
        "data": {
            "id": good_id,
            "type": "cart_item",
            "quantity": quantity,
        },
    }

    response = requests.post(
        add_good_to_cart_url,
        headers=headers,
        json=payload,
    )
    response.raise_for_status()

    return response.json()


def get_cart_items(cart_id):
    headers = get_elasticpath_headers()

    cart_items_url = f"https://api.moltin.com/v2/carts/{cart_id}/items"

    response = requests.get(cart_items_url, headers=headers)
    response.raise_for_status()

    return response.json()


def get_cart_total(cart_id):
    headers = get_elasticpath_headers()

    total_cart_url = f"https://api.moltin.com/v2/carts/{cart_id}"

    response = requests.get(total_cart_url, headers=headers)
    response.raise_for_status()

    return response.json()


def get_or_create_cart(cart_id):
    headers = get_elasticpath_headers()

    cart_url = f"https://api.moltin.com/v2/carts/{cart_id}"

    response = requests.get(cart_url, headers=headers)
    response.raise_for_status()

    return response.json()


def get_product_image_url(file_id):
    headers = get_elasticpath_headers()

    image_url = f"https://api.moltin.com/v2/files/{file_id}"

    response = requests.get(image_url, headers=headers)
    response.raise_for_status()

    return response.json()


def remove_cart_item(cart_id, product_id):
    headers = get_elasticpath_headers()

    remove_cart_item_url = (
        f"https://api.moltin.com/v2/carts/{cart_id}/items/{product_id}"
    )

    response = requests.delete(remove_cart_item_url, headers=headers)
    response.raise_for_status()

    return response.json()


def create_customer(user_name, user_email):
    headers = get_elasticpath_headers()

    create_customer_url = "https://api.moltin.com/v2/customers"

    payload = {
        "data": {
            "type": "customer",
            "name": user_name,
            "email": user_email,
        },
    }

    response = requests.post(
        create_customer_url,
        headers=headers,
        json=payload,
    )
    response.raise_for_status()

    return response.json()


def create_good(good_information):
    headers = get_elasticpath_headers()

    create_good_url = "https://api.moltin.com/v2/products"

    payload = {
        "data": {
            "type": "product",
            "name": good_information["name"],
            "slug": f"pizza-slug-{good_information['id']}",
            "sku": f"pizza-{good_information['id']}",
            "description": good_information["description"],
            "manage_stock": False,
            "price": [
                {
                    "amount": good_information["price"],
                    "currency": "RUB",
                    "includes_tax": True,
                },
            ],
            "status": "live",
            "commodity_type": "physical",
        },
    }

    response = requests.post(
        create_good_url,
        headers=headers,
        json=payload,
    )
    response.raise_for_status()

    return response.json()


def upload_image(image_url):
    headers = get_elasticpath_headers()

    upload_image_url = "https://api.moltin.com/v2/files"

    files = {
        "file_location": (None, image_url),
    }

    response = requests.post(
        upload_image_url,
        headers=headers,
        files=files,
    )
    response.raise_for_status()

    return response.json()


def create_image_relationship(good_id, image_id):
    headers = get_elasticpath_headers()

    create_image_relationship_image_url = f"https://api.moltin.com/v2/products/{good_id}/relationships/main-image"

    payload = {
        "data": {
            "type": "main_image",
            "id": image_id,
        },
    }

    response = requests.post(
        create_image_relationship_image_url,
        headers=headers,
        json=payload,
    )
    response.raise_for_status()

    return response.json()
