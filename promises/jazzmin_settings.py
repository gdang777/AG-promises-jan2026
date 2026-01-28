
# Jazzmin Settings
JAZZMIN_SETTINGS = {
    "site_title": "Promises Admin",
    "site_header": "Promises Administration",
    "site_brand": "Promises Admin",
    "welcome_sign": "Welcome to the Promises Admin",
    "copyright": "Promises Movie",
    "topmenu_links": [
        {"name": "Home",  "url": "admin:index", "permissions": ["auth.view_user"]},
        {"name": "View Site", "url": "/"},
    ],
    "user_avatar": None,
    # "order_with_respect_to": ["web_app"],
    "show_sidebar": True,
    "navigation_expanded": True,
    "hide_apps": [],
    "hide_models": [],
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "web_app.TabOne": "fas fa-mountain",
        "web_app.TabTwo": "fas fa-tree",
        "web_app.TabThree": "fas fa-leaf",
        "web_app.VideoLink": "fas fa-video",
        "web_app.SponsoredBlockTwo": "fas fa-hand-holding-usd",
        "web_app.SponsoredBlockThree": "fas fa-hand-holding-usd",
        "web_app.SponsoredBlockFour": "fas fa-hand-holding-usd",
    },
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": False,
    "accent": "accent-primary",
    "navbar": "navbar-dark",
    "no_navbar_border": False,
    "navbar_fixed": False,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": False,
    "sidebar": "sidebar-dark-primary",
    "sidebar_nav_small_text": False,
    "theme": "darkly",  # Dark theme
    "dark_mode_theme": "darkly",
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success"
    }
}
