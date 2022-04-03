import json

from pprint import pprint

from dotenv import load_dotenv

from moltin_api import (
    create_good,
    upload_image,
    create_image_relationship,
)


def main():
    load_dotenv()

    # with open("addresses.json", "r", encoding="utf-8") as addresses_file:
    #     addresses = json.load(addresses_file)

    with open("menu.json", "r", encoding="utf-8") as menu_file:
        menu_dishes = json.load(menu_file)

    for menu_dish in menu_dishes:
        created_good = create_good(menu_dish)
        # pprint(created_good)

        uploaded_image = upload_image(menu_dish["product_image"]["url"])
        # pprint(uploaded_image)

        create_image_relationship(
            created_good["data"]["id"],
            uploaded_image["data"]["id"],
        )
        # pprint(created_image_relationship)


if __name__ == "__main__":
    main()
