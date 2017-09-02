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
    'mmadinare': get_mmadinare(),
    'testhosts': ['bcpp075', 'bcpp076', 'bcpp077', 'bcpp078', 'bcpp080', 'bcpp081'],
}
