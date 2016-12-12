from edc_consent.managers import ConsentManager

from bcpp.manager_mixins import CurrentCommunityManagerMixin


class SubjectConsentManager(CurrentCommunityManagerMixin, ConsentManager):

    pass
