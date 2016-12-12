from django.contrib.admin import AdminSite


class BcppListAdminSite(AdminSite):
    site_title = 'BCPP List'
    site_header = 'BCPP List'
    index_title = 'BCPP List'
    site_url = '/'
bcpp_list_admin = BcppListAdminSite(name='bcpp_list_admin')
