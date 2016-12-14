import factory

from datetime import date, datetime

from bhp066.apps.bcpp_subject.models import HeartAttack


class HeartAttackFactory(factory.DjangoModelFactory):
    FACTORY_FOR = HeartAttack

    report_datetime = datetime.today()
    date_heart_attack = date.today()
    dx_heart_attack_other = factory.Sequence(lambda n: 'dx_heart_attack_other{0}'.format(n))
