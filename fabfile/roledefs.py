def get_bokaa():
    hosts = ['bcpp0{}'.format(i + 25) for i in range(0, 15)]
    hosts.pop(hosts.index('bcpp026'))
    hosts.pop(hosts.index('bcpp035'))
    return hosts


def get_oodi():
    hosts = ['bcpp0{}'.format(i + 55) for i in range(0, 15)]
    hosts.pop(hosts.index('bcpp057'))
    hosts.pop(hosts.index('bcpp065'))
    hosts.pop(hosts.index('bcpp066'))
    hosts.pop(hosts.index('bcpp067'))
    hosts.append('bcpp070')
    return hosts


def get_lentsweletau():
    hosts = ['bcpp0{}'.format(i + 25) for i in range(0, 15)]
    hosts.pop(hosts.index('bcpp026'))
    hosts.pop(hosts.index('bcpp035'))
    return hosts


def get_masunga():
    hosts = ['bcpp0{}'.format(i + 44) for i in range(0, 5)]
    hosts.append('bcpp026')
    hosts.append('bcpp040')
    hosts.append('bcpp052')
    hosts.append('bcpp053')
    hosts.append('bcpp059')
    hosts.append('bcpp061')
    hosts.append('bcpp062')
    hosts.append('bcpp063')
    hosts.append('bcpp070')
    return hosts


def get_mmathethe():
    hosts = ['bcpp0{}'.format(i + 40) for i in range(0, 15)]
    hosts.append('bcpp026')
    hosts.append('bcpp035')
    return hosts


def get_letlhakeng():
    hosts = ['bcpp0{}'.format(i + 55) for i in range(0, 15)]
    hosts.pop(hosts.index('bcpp057'))
    hosts.pop(hosts.index('bcpp065'))
    return hosts


def get_mmankgodi():
    hosts = ['bcpp0{}'.format(i + 10) for i in range(0, 15)]
    hosts.append('bcpp057')
    hosts.append('bcpp065')
    return hosts


def get_ramokgonami():
    hosts = ['bcpp0{}'.format(i + 25) for i in range(0, 15)]
    hosts.pop(hosts.index('bcpp026'))
    hosts.pop(hosts.index('bcpp035'))
    hosts.append('bcpp016')
    hosts.append('bcpp017')
    hosts.append('bcpp019')
    return hosts


def get_maunatlala():
    hosts = ['bcpp0{}'.format(i + 55) for i in range(0, 16)]
    hosts.pop(hosts.index('bcpp057'))
    hosts.pop(hosts.index('bcpp065'))
    hosts.pop(hosts.index('bcpp066'))
    hosts.pop(hosts.index('bcpp067'))
    hosts.append('bcpp035')
    hosts.append('bcpp052')
    hosts.append('bcpp042')
    hosts.append('bcpp050')
    return hosts


def get_lerala():
    hosts = ['bcpp0{}'.format(i + 10) for i in range(0, 15)]
    hosts.append('bcpp057')
    hosts.pop(hosts.index('bcpp016'))
    hosts.pop(hosts.index('bcpp017'))
    hosts.pop(hosts.index('bcpp019'))
    return hosts


def get_sefophe():
    hosts = ['bcpp0{}'.format(i + 40) for i in range(0, 15)]
    hosts.append('bcpp026')
    hosts.pop(hosts.index('bcpp042'))
    hosts.pop(hosts.index('bcpp050'))
    hosts.pop(hosts.index('bcpp052'))
    return hosts


def get_shoshong():
    hosts = ['bcpp0{}'.format(i + 10) for i in range(0, 15)]
    hosts.append('bcpp057')
    hosts.pop(hosts.index('bcpp016'))
    hosts.pop(hosts.index('bcpp017'))
    hosts.pop(hosts.index('bcpp019'))
    return hosts


def get_mmadinare():
    hosts = ['bcpp0{}'.format(i + 40) for i in range(0, 15)]
    hosts.append('bcpp026')
    hosts.pop(hosts.index('bcpp042'))
    hosts.pop(hosts.index('bcpp050'))
    hosts.pop(hosts.index('bcpp052'))
    return hosts


def get_metsimotlhabe():
    hosts = ['bcpp0{}'.format(i + 55) for i in range(0, 16)]
    hosts.pop(hosts.index('bcpp057'))
    hosts.pop(hosts.index('bcpp065'))
    hosts.pop(hosts.index('bcpp066'))
    hosts.pop(hosts.index('bcpp067'))
    hosts.append('bcpp035')
    hosts.append('bcpp052')
    hosts.append('bcpp042')
    hosts.append('bcpp050')
    return hosts


def get_tati_siding():
    hosts = ['bcpp0{}'.format(i + 25) for i in range(0, 15)]
    hosts.pop(hosts.index('bcpp026'))
    hosts.pop(hosts.index('bcpp035'))
    hosts.append('bcpp016')
    hosts.append('bcpp017')
    hosts.append('bcpp019')
    return hosts


def get_gumare():
    hosts = ['bcpp0{}'.format(i + 10) for i in range(0, 18)]
    hosts.pop(hosts.index('bcpp016'))
    hosts.pop(hosts.index('bcpp017'))
    hosts.pop(hosts.index('bcpp026'))
    hosts.pop(hosts.index('bcpp027'))
    hosts.append('bcpp030')
    hosts.append('bcpp031')
    hosts.append('bcpp057')
    return hosts


def get_shakawe():
    hosts = ['bcpp0{}'.format(i + 40) for i in range(0, 18)]
    hosts.pop(hosts.index('bcpp057'))
    hosts.pop(hosts.index('bcpp050'))
    hosts.pop(hosts.index('bcpp051'))
    hosts.pop(hosts.index('bcpp055'))
    hosts.pop(hosts.index('bcpp041'))
    hosts.pop(hosts.index('bcpp042'))
    hosts.append('bcpp026')
    return hosts


def get_gweta():
    hosts = ['bcpp035', 'bcpp041', 'bcpp042', 'bcpp068', 'bcpp050',
             'bcpp051', 'bcpp055', 'bcpp058', 'bcpp059', 'bcpp064', 'bcpp069']
    return hosts


def get_rakops():
    hosts = ['bcpp016', 'bcpp017', 'bcpp027', 'bcpp028', 'bcpp029',
             'bcpp033', 'bcpp036', 'bcpp037', 'bcpp038', 'bcpp039']
    return hosts


def get_tsetsebjwe():
    hosts = ['bcpp017', 'bcpp019', 'bcpp025', 'bcpp027', 'bcpp028',
             'bcpp029', 'bcpp033', 'bcpp036', 'bcpp037', 'bcpp038', 'bcpp039']
    return hosts


def get_sefhare():
    hosts = ['bcpp035', 'bcpp041', 'bcpp042', 'bcpp068', 'bcpp050', 'bcpp043',
             'bcpp049', 'bcpp051', 'bcpp055', 'bcpp058', 'bcpp059', 'bcpp064',
             'bcpp069']
    return hosts


def get_nata():
    hosts = ['bcpp010', 'bcpp011', 'bcpp012', 'bcpp013', 'bcpp014', 'bcpp015',
             'bcpp018', 'bcpp020', 'bcpp022', 'bcpp023', 'bcpp024', 'bcpp030',
             'bcpp057']
    return hosts


roledefs = {
    'deployment_hosts': ['localhost'],
    'mmankgodi': get_mmankgodi(),
    'lentsweletau': get_lentsweletau(),
    'mmathethe': get_mmathethe(),
    'letlhakeng': get_letlhakeng(),
    'oodi': get_oodi(),
    'bokaa': get_bokaa(),
    'maunatlala': get_maunatlala(),
    'ramokgonami': get_ramokgonami(),
    'lerala': get_lerala(),
    'sefophe': get_sefophe(),
    'shoshong': get_shoshong(),
    'masunga': get_masunga(),
    'mmadinare': get_mmadinare(),
    'metsimotlhabe': get_metsimotlhabe(),
    'tati_siding': get_tati_siding(),
    'rakops': get_rakops(),
    'gweta': get_gweta(),
    'gumare': get_gumare(),
    'shakawe': get_shakawe(),
    'tsetsebjwe': get_tsetsebjwe(),
    'sefhare': get_sefhare(),
    'testhosts': ['bcpp075', 'bcpp076', 'bcpp077', 'bcpp078', 'bcpp080',
                  'bcpp081'],
}
