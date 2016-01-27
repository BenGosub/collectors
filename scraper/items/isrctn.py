# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import sqlalchemy as sa
from scrapy import Field

from .. import utils
from .base import Base


# Module API

class Isrctn(Base):

    # Config

    primary_key = 'isrctn_id'
    updated_key = 'last_edited'

    # General

    isrctn_id = Field()
    doi_isrctn_id = Field()
    title = Field()
    condition_category = Field()
    date_applied = Field(parser=utils.isrctn.parse_date, type=sa.Date)
    date_assigned = Field(parser=utils.isrctn.parse_date, type=sa.Date)
    last_edited = Field(parser=utils.isrctn.parse_date, type=sa.Date)
    prospective_retrospective = Field()
    overall_trial_status = Field()
    recruitement_status = Field()
    plain_english_summary = Field()
    trial_website = Field()

    # Contant information

    type = Field()
    primary_contact = Field()
    orcid_id = Field()
    contact_details = Field()

    # Additional identifiers

    eudract_number = Field()
    clinicaltrials_gov_number = Field()
    protocol_serial_number = Field()

    # Study information

    scientific_title = Field()
    acronym = Field()
    study_hypothesis = Field()
    ethics_approval = Field()
    study_design = Field()
    primary_study_design = Field()
    secondary_study_design = Field()
    trial_setting = Field()
    trial_type = Field()
    patient_information_sheet = Field()
    condition = Field()
    intervention = Field()
    intervention_type = Field()
    phase = Field()
    drug_names = Field()
    primary_outcome_measures = Field()
    secondary_outcome_measures = Field()
    overall_trial_start_date = Field()
    overall_trial_end_date = Field()
    reason_abandoned = Field()

    # Eligability

    participant_inclusion_criteria = Field()
    participant_type = Field()
    age_group = Field()
    gender = Field()
    target_number_of_participants = Field()
    participant_exclusion_criteria = Field()
    recruitment_start_date = Field()
    recruitment_end_date = Field()

    # Locations

    countries_of_recruitment = Field()
    trial_participating_centre = Field()

    # Sponsor information

    organisation = Field()
    sponsor_details = Field()
    sponsor_type = Field()
    website = Field()

    # Funders

    funder_type = Field()
    funder_name = Field()
    alternative_name_s_ = Field()
    funding_body_type = Field()
    funding_body_subtype = Field()
    location = Field()

    # Result and publications

    publication_and_dissemination_plan = Field()
    intention_to_publish_date = Field()
    participant_level_data = Field()
    results_basic_reporting = Field()
    publication_summary = Field()
    publication_citations = Field()

    # Additional files

    # ...

    # Editorial notes

    # ...
