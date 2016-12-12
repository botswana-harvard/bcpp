import factory

from datetime import date, datetime

from bhp066.apps.bcpp_subject.models import Cancer


class CancerFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Cancer

    report_datetime = datetime.today()
    date_cancer = date.today()
    dx_cancer = (("Kaposi's sarcoma (KS)", u"Kaposi's sarcoma (KS)"), ('Cervical cancer', u'Cervical cancer'), ('Breast cancer', u'Breast cancer'), ("Non-Hodgkin's lymphoma (NHL)", u"Non-Hodgkin's lymphoma (NHL)"), ('Colorectal cancer', u'Colorectal cancer'), ('Prostate cancer', u'Prostate cancer'), ('Cancer of mouth, throat, voice box (larynx)', u'Cancer of mouth, throat, voice box (larynx)'), ('Cancer of oesophagus', u'Cancer of oesophagus'), ('Other', u'Other, specify:'), ('not_answering', u"Don't want to answer"))[0][0]
