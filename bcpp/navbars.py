from edc_navbar import NavbarItem, site_navbars, Navbar


bcpp = Navbar(name='bcpp')

bcpp.append_item(
    NavbarItem(name='plots',
               title='Plots',
               label='plots',
               fa_icon='fa-building',
               url_name=f'plot_dashboard:listboard_url'))

bcpp.append_item(
    NavbarItem(name='households',
               title='Households',
               label='households',
               fa_icon='fa-home',
               url_name=f'household_dashboard:listboard_url'))

bcpp.append_item(
    NavbarItem(name='enumeration',
               title='Enumeration',
               label='enumeration',
               fa_icon='fa-sitemap',
               url_name=f'enumeration:listboard_url'))

bcpp.append_item(
    NavbarItem(name='members',
               title='Members',
               label='members',
               fa_icon='fa-users',
               url_name=f'member_dashboard:listboard_url'))

bcpp.append_item(
    NavbarItem(name='subjects',
               title='Subjects',
               label='subjects',
               fa_icon='fa-user-circle-o',
               url_name=f'bcpp_subject_dashboard:listboard_url'))

bcpp.append_item(
    NavbarItem(name='follow-up',
               title='Follow',
               label='follow-up',
               fa_icon='fa-comments-o',
               url_name=f'bcpp_follow:listboard_url'))

bcpp.append_item(
    NavbarItem(name='plots',
               title='Plots',
               label='plots',
               fa_icon='fa-building',
               url_name=f'edc_lab_dashboard:home_url'))


anonymous = Navbar(name='anonymous')
anonymous.append_item(
    NavbarItem(name='anonymous_subjects',
               title='Anonymous Subjects',
               label='anonymous_subjects',
               fa_icon='fa-user-secret',
               url_name=f'bcpp_subject_dashboard:anonymous_listboard_url'))

site_navbars.register(bcpp)
site_navbars.register(anonymous)
