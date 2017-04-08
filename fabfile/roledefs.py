
def get_lenstweletau():
    hosts = ['bcpp0{}'.format(i + 25) for i in range(0, 15)]
    hosts.pop(hosts.index('bcpp026'))
    hosts.pop(hosts.index('bcpp035'))
    return hosts


def get_mmathethe():
    hosts = ['bcpp0{}'.format(i + 40) for i in range(0, 15)]
    hosts.append('bcpp026')
    hosts.append('bcpp035')
    return hosts


roledefs = {
    'deployment_hosts': ['localhost'],
    'mmankgodi': ['bcpp0{}'.format(i + 10) for i in range(0, 15)],
    'lentsweletau': get_lenstweletau(),
    'mmathethe': get_mmathethe(),
    'letlhakeng': ['bcpp0{}'.format(i + 55) for i in range(0, 15)],
    'testhosts': ['bcpp075', 'bcpp076', 'bcpp077', 'bcpp078', 'bcpp080', 'bcpp081'],
}
