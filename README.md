# Django&Angular admin generator.

# Installing

    ./bin/install

# Load test data

    ./bin/load_data

# Running django server

    ./bin/run_backend

# Running frontend
You need nodejs version 12

    ./bin/run_frontend
# Config of model section

    {
        "copyright": "For authogeneration Angular admin interface by Django! Author: Zharikov Dimitry zdimon77@gmail.com",
        "title": "User",
        "root": "admin",
        "dirname": "user",
        "fileprefix": "user",
        "camelName": "user",
        "upname": "User",
        "url_list": "account/user/list",
        "url_create": "account/user/list",
        "url_update": "account/user/list",
        "url_delete": "account/user/list",
        "rout": "user",
        "new_button": false,
        "edit_button": true,
        "bulk_operation": true,
        "bulk_list": [
            {"name": "delete", "title": "Delete", "help": "Delete selected users", "icon": "delete"}
        ],
        "list_fields": [
            {"name": "id", "type": "number", "title": "Username"},
            {"name": "email", "type": "string", "title": "Email"},
            {"name": "username", "type": "string", "title": "Username"},
            {"name": "is_superuser", "type": "string", "title": "Is superuser"},
            {"name": "is_staff", "type": "string", "title": "Is staff"},
            {"name": "is_active", "type": "string", "title": "Is active"}
        ],
        "filter_fields": [
            {"name": "username", "type": "string", "title": "Username"},
            {"name": "email", "type": "string", "title": "Email"},
            {"name": "is_superuser", "type": "options", "items": [
                    {"name": "yes", "value": "true"},
                    {"name": "no", "value": "false"}
                ]
            },
            {"name": "is_staff", "type": "options", "items": [
                    {"name": "yes", "value": "true"},
                    {"name": "no", "value": "false"}
                ]
            },
            {"name": "is_active", "type": "options", "items": [
                    {"name": "yes", "value": "true"},
                    {"name": "no", "value": "false"}
                ]
            }
        ],
        "edit_fields": [
            {"name": "email", "type": "string", "title": "Email"},
            {"name": "username", "type": "string", "title": "Username"},
            {"name": "is_superuser", "type": "string", "title": "Is superuser"},
            {"name": "is_staff", "type": "string", "title": "Is staff"},
            {"name": "is_active", "type": "string", "title": "Is active"}
        ],
        "tabs": [
            {
                "title": "Groups", 
                "class": "UserGroup", 
                "folder": "user_group", 
                "selector": "user-group-list",
                "url_list": "account/group/list",
                "url_create": "account/group/create",
                "url_update": "account/group/update",
                "url_delete": "account/group/delete",
                "fields": [
                    {"name": "get_small_url_square", "type": "string", "widget": "image", "title": "Image"},
                    {"name": "role_media", "type": "string", "title": "Role media"}
                ]
            }
        ]
    }

# Config of tabs

    "tabs": [
        {
            "title": "Groups", 
            "class": "UserGroup", 
            "folder": "user_group", 
            "selector": "user-group-list",
            "url_list": "account/group/list",
            "url_create": "account/group/create",
            "url_update": "account/group/update",
            "url_delete": "account/group/delete",
            "fields": [
                {"name": "get_small_url_square", "type": "string", "widget": "image", "title": "Image"},
                {"name": "role_media", "type": "string", "title": "Role media"}
            ]
        }