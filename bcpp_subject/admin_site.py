from django.contrib.admin import AdminSite


class BcppSubjectAdminSite(AdminSite):
    site_title = 'BCPP Subject'
    site_header = 'BCPP Subject'
    index_title = 'BCPP Subject'
    site_url = '/'
bcpp_subject_admin = BcppSubjectAdminSite(name='bcpp_subject_admin')
