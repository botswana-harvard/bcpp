from edc_base.navbar_item import NavbarItem

navbars = {}
navbar_items = []
config = [
    ('plot', 'plots', 'fa-building'),
    ('household', 'households', 'fa-home'),
    ('enumeration', 'enumeration', 'fa-sitemap'),
    ('member', 'members', 'fa-users'),
    ('bcpp_subject', 'subjects', 'fa-user-circle-o')
]
for app_config_name, label, fa_icon in config:
    navbar_item = NavbarItem(
        app_config_name=app_config_name,
        label=label,
        fa_icon=fa_icon,
        app_config_attr='listboard_url_name')
    navbar_items.append(navbar_item)
navbars.update(default=navbar_items)

navbar_items = []
config = [
    ('member', 'Anonymous Members', 'fa-user-secret'),
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
