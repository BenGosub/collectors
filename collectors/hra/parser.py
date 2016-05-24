# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from .record import Record
from datetime import date
import logging
import six
logger = logging.getLogger(__name__)


def parse_response(response, endpoint, from_date, to_date, errors, success, conn):
    for application in response.json():
        try:
            data = {}
            data['last_updated'] = date.today().strftime('%Y-%m-%d')
            data['api_date_from'] = from_date.strftime('%Y-%m-%d')
            data['api_date_to'] = to_date.strftime('%Y-%m-%d')
            app_id = six.u(str(application['ApplicationID']))
            data['application_id'] = app_id
            data['publication_date'] = application['PublicationDate']
            data['updated_date'] = application['UpdatedDate']
            data['comittee_name'] = application['CommitteeName']
            data['comittee_ref_number'] = application['CommitteeReferenceNumber']
            data['iras_proj_id'] = application['IrasProjectID']
            data['contact_name'] = application['ContactName']
            data['contact_email'] = application['ContactEmail']
            data['application_title'] = application['ApplicationTitle']
            data['study_type_id'] = application['StudyTypeID']
            data['study_type'] = application['StudyType']
            data['sponsor_org'] = application['SponsorOrganisation']
            data['research_programme'] = application['ResearchProgramme']
            data['data_coll_arrangements'] = application['DataCollectionArrangements']
            data['establishment_org'] = application['EstablishmentOrganisation']
            data['establishment_org_address_1'] = ['EstablishmentOrganisationAddress1']
            data['establishment_org_address_2'] = application['EstablishmentOrganisationAddress2']
            data['establishment_org_address_3'] = application['EstablishmentOrganisationAddress3']
            data['establishment_org_post_code'] = application['EstablishmentOrganisationPostcode']
            data['decision'] = application['Decision']
            data['decision_date'] = application['DecisionDate']
            data['human_tissue_license'] = application['HumanTissueAuthorityStorageLicence']
            data['rtb_title'] = application['RTBTitle']
            data['research_database_title'] = application['ResearchDatabaseTitle']
            data['application_full_title'] = application['ApplicationFullTitle']
            data['isrctn'] = application['ISRCTN']
            data['nct'] = application['NCT']
            data['additional_ref_numbers'] = application['AdditionalReferenceNumbers']
            data['duration_of_study_in_uk'] = application['DurationOfStudyInUK']
            data['research_summary'] = application['ResearchSummary']
            data['eudra_ct'] = application['EudraCT']
            data['social_value'] = application['SocialValue']
            data['recuitment_arrangements'] = application['RecruitmentArrangements']
            data['risk_and_benefit'] = application['RiskAndBenefit']
            data['participants_protection_and_care'] = application['ParticipantsProtectionAndCare']
            data['informed_consent'] = application['InformedConsent']
            data['applicant_and_staff_suitability'] = application['ApplicantAndStaffSuitability']
            data['independent_review'] = application['IndependentReview']
            data['supporting_info_suitability'] = application['SupportingInfoSuitability']
            data['other_comments'] = application['OtherComments']
            data['research_summary_suitability'] = application['ResearchSummarySuitability']

            record = Record.create(endpoint, data)
            return (record, app_id)

            success += 1
            if not success % 100:
                    logger.info('Collected %s "%s" interventions',
                        success, record.table)
        except Exception as exception:

            # Log warning
            errors += 1
            logger.warning('Collecting error: %s', repr(exception))
