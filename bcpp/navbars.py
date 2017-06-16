from edc_base.navbar_item import NavbarItem
from edc_lab_dashboard.navbars import navbar_items as edc_lab_navbar_items

navbars = {}
navbar_items = []
config = [
    ('plot', 'plots', 'fa-building', 'listboard_url_name'),
    ('household', 'households', 'fa-home', 'listboard_url_name'),
    ('enumeration', 'enumeration', 'fa-sitemap', 'listboard_url_name'),
    ('member', 'members', 'fa-users', 'listboard_url_name'),
    ('bcpp_subject', 'subjects', 'fa-user-circle-o', 'listboard_url_name'),
    ('bcpp_follow', 'follow', 'fa-comments-o', 'listboard_url_name'),
    ('edc_lab', None, 'fa-flask', 'home_url_name')
]
for app_config_name, label, fa_icon, app_config_attr in config:
    navbar_item = NavbarItem(
        app_config_name=app_config_name,
        label=label,
        fa_icon=fa_icon,
        app_config_attr=app_config_attr)
    navbar_items.append(navbar_item)
navbars.update(default=navbar_items)

navbar_items = []
config = [
    ('bcpp_subject', 'Anonymous Subjects', 'fa-user-secret'),
]
for app_config_name, label, fa_icon in config:
    navbar_item = NavbarItem(
        app_config_name=app_config_name,
        label=label,
        fa_icon=fa_icon,
        app_config_attr='anonymous_listboard_url_name')
    navbar_items.append(navbar_item)

navbars.update(anonymous=navbar_items)
navbars.update(specimens=edc_lab_navbar_items)
