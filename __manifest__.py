# -*- coding: utf-8 -*-
{
    "name": "Website Product Creator",
    "summary": "Creates a new product",
    "description": """
        Creates new product to the database by providing the name, image, price, and description of the product.
    """,
    "author": "Metamorphosis Ltd",
    "website": "https://metamorphosis.com.bd",
    "category": "Website",
    "version": "1.0.1",
    "license": "AGPL-3",
    "depends": [
        "website",
        "portal",
        "product_barcodelookup",
        "base",
    ],
    "data": [
        "views/create_product.xml",
        "views/product_create_form.xml",
        "views/product_creation_success_views.xml",
        "views/menu.xml",
        "views/user_product_list_template.xml",
    ],
    "assets": {
        "web.assets_frontend": [
            "meta_product_creation/static/src/js/product_selection.js",
        ],
    },
}
