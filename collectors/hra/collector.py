# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging
import requests
import sqlalchemy
import os
from datetime import date, timedelta
import time
from .. import base
from .record import Record
logger = logging.getLogger(__name__)

parse_datetime = base.helpers.parse_datetime

url = 'https://stage.harp.org.uk/HARPApiExternal/api/ResearchSummaries'
hra_user = os.environ.get('HRA_USERNAME')
hra_pass = os.environ.get('HRA_PASSWORD')

s = requests.Session()


def make_request(url, from_, to, filter=None):
    # Updates filter is optional-categorical value
    # 1 - returns all studies for the given period
    # 2 - returns only studies published in the period
    # 3 - returns only studies modified in the period
    result_str = url + '?datePublishedFrom=' + str(from_) + '&datePublishedTo=' + str(to)
    if filter is None:
        pass
    else:
        result_str = result_str + '&updatesFilter=' + str(filter)
    response = s.get(result_str, auth=(hra_user, hra_pass))
    return (response, result_str)

# Module API


def collect(conf, conn):
    errors = 0
    success = 0

    def parse_response(response, endpoint, from_api, to_date, errors, success, conn=conn):
        for application in response.json():
            try:
                data = {}
                data['last_updated'] = str(date.today())
                data['api_date_from'] = str(from_date)
                data['api_date_to'] = str(to_date)
                data['application_id'] = str(application['ApplicationID'])
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

                # Insert into database only if app_id not inserted already
                check_id = conn['warehouse'].query("select count(*) from hra where application_id='%s'" % str(application['ApplicationID']))
                for row in check_id:
                    if row[0]['count'] == 0:
                        record = Record.create(endpoint, data)
                        base.writers.write_record(conn, record)

                success += 1
                print("Successful parsing iteration")
            except Exception as exception:

                # Log warning
                errors += 1
                logger.warning('Collecting error: %s', repr(exception))
                print(exception)

    def get_to_date():
        to_date = conn['warehouse'].query('select min(api_date_from) from hra').result_proxy.first()[0] - timedelta(days=1)
        return to_date

    try:
        table = conn['warehouse'].load_table('hra')
        if table.count() == 0:
            to_date = date.today()
        else:
            to_date = get_to_date()

    except sqlalchemy.exc.NoSuchTableError:
        to_date = date.today()

    query_period = 6
    from_date = to_date - timedelta(days=query_period)
    response, endpoint = make_request(from_=from_date, to=to_date, url=url, filter=None)
    parse_response(response, endpoint, from_date, to_date, errors, success)

    if (len(response.json()) > 0):
        while True:
            to_date = get_to_date()
            from_date = to_date - timedelta(days=query_period)
            print('Sleeping for 30sec.')
            time.sleep(30)
            response, endpoint = make_request(from_=from_date, to=to_date, url=url, filter=None)
            parse_response(response, endpoint, from_date, to_date, errors, success)
