import sys

from collections import namedtuple

from django.core.management.color import color_style

style = color_style()

Community = namedtuple('Community', 'code name pair intervention')

if 'test' in sys.argv:
    communities = {'test_community': Community(
        '01', 'test_community', 1, True),
        'botswana': Community('00', 'botswana', 0, False),
    }
else:
    communities = {
        'test_community': Community('99', 'test_community', 99, True),
        'botswana': Community('00', 'botswana', 0, False),
        'bokaa': Community('17', 'bokaa', 4, False),
        'digawana': Community('12', 'digawana', 1, True),
        'gumare': Community('35', 'gumare', 13, True),
        'gweta': Community('34', 'gweta', 12, True),
        'lentsweletau': Community('16', 'lentsweletau', 3, True),
        'lerala': Community('21', 'lerala', 6, True),
        'letlhakeng': Community('15', 'letlhakeng', 3, False),
        'masunga': Community('37', 'masunga', 15, True),
        'mathangwane': Community('31', 'mathangwane', 11, True),
        'maunatlala': Community('23', 'maunatlala', 7, True),
        'metsimotlhabe': Community('29', 'metsimotlhabe', 9, False),
        'mmadinare': Community('26', 'mmadinare', 8, False),
        'mmandunyane': Community('32', 'mmandunyane', 11, False),
        'mmankgodi': Community('19', 'mmankgodi', 5, True),
        'mmathethe': Community('20', 'mmathethe', 5, False),
        'molapowabojang': Community('13', 'molapowabojang', 2, False),
        'nata': Community('38', 'nata', 15, False),
        'nkange': Community('27', 'nkange', 10, True),
        'oodi': Community('18', 'oodi', 4, True),
        'otse': Community('14', 'otse', 2, True),
        'rakops': Community('33', 'rakops', 12, False),
        'ramokgonami': Community('24', 'ramokgonami', 7, False),
        'ranaka': Community('11', 'ranaka', 1, False),
        'sebina': Community('28', 'sebina', 10, False),
        'sefhare': Community('39', 'sefhare', 14, True),
        'sefophe': Community('22', 'sefophe', 6, False),
        'shakawe': Community('36', 'shakawe', 13, False),
        'shoshong': Community('25', 'shoshong', 8, True),
        'tati_siding': Community('30', 'tati_siding', 9, True),
        'tsetsebjwe': Community('40', 'tsetsebjwe', 14, False)
    }


communities_by_code = {}
for name, community in communities.items():
    communities_by_code.update({community.code: community})


def to_community(code):
    return communities_by_code.get(code).name


def is_intervention(community):
    try:
        return communities.get(community).intervention
    except AttributeError as e:
        sys.stdout.write(style.ERROR(
            '\n * ERROR: Assuming \'{}\' is an intervention community. \n'
            '   Got {}\n\n'.format(community, str(e))))
        return True
