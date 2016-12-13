from django.contrib.admin import AdminSite


class BcppLabAdminSite(AdminSite):
    site_title = 'BCPP Lab'
    site_header = 'BCPP Lab'
    index_title = 'BCPP Lab'
    site_url = '/'
bcpp_lab_admin = BcppLabAdminSite(name='bcpp_lab_admin')
