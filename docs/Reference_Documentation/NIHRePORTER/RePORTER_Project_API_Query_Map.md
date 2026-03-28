# NIH RePORTER Project API Query Map

This file is focused on query-building rather than raw field definitions.

## Payload criteria inventory

| PayloadCriteriaName | Fields Using It | Example / Note |
|---|---|---|
| `abstracttext` | `abstract_text` | (e. g. { "criteria": { advanced_text_search: { operator: "and", search_field: "projecttitle,abstracttext,terms", "search_text": "brain disorder" } } } ) |
| `activity_code` | `ProjectNumSplit.activity_code` | (e.g. {"criteria": { project_num_split: { appl_type_code: "1", activity_code: "F32", ic_code: "HL", serial_num: "149210", support_year: "01", full_support_year: "01A1", suffix_code: "A1" } } } e.g. {"criteria": { activity_codes:["P20","R35"] } } ) |
| `activity_codes` | `ProjectNumSplit.activity_code`, `activity_code` | (e.g. {"criteria": { project_num_split: { appl_type_code: "1", activity_code: "F32", ic_code: "HL", serial_num: "149210", support_year: "01", full_support_year: "01A1", suffix_code: "A1" } } } e.g. {"criteria": { activity_codes:["P20","R35"] } } ) |
| `agencies` | `AgencyIcAdmin.abbreviation`, `AgencyIcFundings.code`, `AgencyIcFundings.total_cost`, `agency_code` |  |
| `any_name` | `PrincipalInvestigators.middle_name` | (e.g. {"criteria": {"pi_names": [{"any_name": ""}, {"middle_name": "William"}] } }) |
| `appl_ids` | `appl_id` |  |
| `award_amount_range` | `award_amount` | (e.g. { "criteria": { "award_amount_range": { "min_amount": 0, "max_amount": 50000000 } } } ) |
| `award_notice_date` | `award_notice_date` | (e.g. { "criteria": {"award_notice_date":{ "from_date":"2021-02- 17", "to_date":"2022-02-17" } }} ) |
| `award_types` | `ProjectNumSplit.appl_type_code`, `award_type` |  |
| `cong_dists` | `cong_dist` |  |
| `covid_response` | `covid_response` |  |
| `date_added` | `date_added` |  |
| `dept_types` | `Organization.dept_type` |  |
| `exclude_subprojects` | `subproject_id` |  |
| `first_name` | `PrincipalInvestigators.first_name`, `ProgramOfficers.first_name` | (e.g. {"criteria": {"pi_names": [{"any_name": ""}, {"first_name": "John"}] } }) |
| `fiscal_years` | `fiscal_year` |  |
| `full_support_year` | `ProjectNumSplit.full_support_year` | (e.g. { "criteria": { project_num_split: { appl_type_code: "1", activity_code: "F32", ic_code: "HL", serial_num: "149210", support_year: "01", full_support_year: "01A1", suffix_code: "A1" } } } ) |
| `funding_mechanism` | `mechanism_code_dc` |  |
| `ic_code` | `ProjectNumSplit.ic_code` | (e.g. { "criteria": { project_num_split: { appl_type_code: "1", activity_code: "F32", ic_code: "HL", serial_num: "149210", support_year: "01", full_support_year: "01A1", suffix_code: "A1" } } } ) |
| `include_active_projects` | `is_active` |  |
| `is_agency_admin` | `AgencyIcAdmin` |  |
| `is_agency_funding` | `AgencyIcFundings` |  |
| `last_name` | `PrincipalInvestigators.last_name`, `ProgramOfficers.last_name` | (e.g. {"criteria": {"pi_names": [{"any_name": ""}, {"last_name": "Welch"}] } } |
| `middle_name` | `ProgramOfficers.middle_name` | (e. g. {"criteria": {"po_names": [{"any_name": ""}, {"middle_name": "William"} ] } } ) |
| `multi_pi_only` | `PrincipalInvestigators` |  |
| `newly_added_projects_only` | `is_new` |  |
| `opportunity_number` | `opportunity_number` |  |
| `org_cities` | `Organization.org_city` |  |
| `org_countries` | `Organization.org_country` |  |
| `org_names` | `Organization.org_name` |  |
| `org_names_exact_match` | `Organization.org_name` |  |
| `org_states` | `Organization.org_state` |  |
| `organization_type` | `OrganizationType` |  |
| `pi_names` | `PrincipalInvestigators.full_name`, `PrincipalInvestigators`, `contact_pi_name` |  |
| `pi_profile_ids` | `PrincipalInvestigators.profile_id` |  |
| `po_names` | `ProgramOfficers.full_name`, `ProgramOfficers` |  |
| `project_end_date` | `project_end_date` |  |
| `project_num_split` | `ProjectNumSplit` |  |
| `project_nums` | `core_project_num`, `project_num` |  |
| `project_start_date` | `project_start_date` |  |
| `projecttitle` | `project_title` | (e. g. {"criteria": { advanced_text_search: { operator: "and", search_field: "projecttitle,abstracttext,terms", "search_text": "brain disorder" } } } ) |
| `serial_num` | `ProjectNumSplit.serial_num`, `project_serial_num` | (e.g. { "criteria": { project_num_split: { appl_type_code: "1", activity_code: "F32", ic_code: "HL", serial_num: "149210", support_year: "01", full_support_year: "01A1", suffix_code: "A1" } } } ) |
| `spending_categories` | `spending_categories_desc` |  |
| `sub_project_only` | `subproject_id` |  |
| `suffix_code` | `ProjectNumSplit.suffix_code` | (e.g. { "criteria": { project_num_split: { appl_type_code: "1", activity_code: "F32", ic_code: "HL", serial_num: "149210", support_year: "01", full_support_year: "01A1", suffix_code: "A1" } } } ) |
| `support_year` | `ProjectNumSplit.support_year` | (e.g. { "criteria": { project_num_split: { appl_type_code: "1", activity_code: "F32", ic_code: "HL", serial_num: "149210", support_year: "01", full_support_year: "01A1", suffix_code: "A1" } } } ) |
| `terms` | `pref_terms` | (e. g. { "criteria": { advanced_text_search: { operator: "and", search_field: "projecttitle,abstracttext,terms", "search_text": "brain disorder" } } } ) |

## Include field inventory

| APIIncludeFieldName | Returned Paths | Notes |
|---|---|---|
| `AbstractText` | `abstract_text` |  |
| `ActivityCode` | `activity_code` |  |
| `AgencyCode` | `agency_code` |  |
| `AgencyIcAdmin` | `AgencyIcAdmin.abbreviation`, `AgencyIcAdmin.code`, `AgencyIcAdmin.name`, `AgencyIcAdmin` | Object with attributes: `abbreviation`, `code`, `name` |
| `AgencyIcFundings` | `AgencyIcFundings.abbreviation`, `AgencyIcFundings.code`, `AgencyIcFundings.fy`, `AgencyIcFundings.name`, `AgencyIcFundings.total_cost`, `AgencyIcFundings` | Object with attributes: `abbreviation`, `code`, `fy`, `name`, `total_cost` |
| `ApplId` | `appl_id` |  |
| `ArraFunded` | `arra_funded` |  |
| `AwardAmount` | `award_amount` |  |
| `AwardNoticeDate` | `award_notice_date` |  |
| `AwardType` | `award_type` |  |
| `BudgetEnd` | `budget_end` |  |
| `BudgetStart` | `budget_start` |  |
| `CfdaCode` | `cfda_code` |  |
| `CongDist` | `cong_dist` |  |
| `ContactPiName` | `contact_pi_name` |  |
| `CoreProjectNum` | `core_project_num` |  |
| `CovidResponse` | `covid_response` |  |
| `DateAdded` | `date_added` |  |
| `DirectCostAmt` | `direct_cost_amt` |  |
| `FiscalYear` | `fiscal_year` |  |
| `FullStudySection` | `FullStudySection.group`, `FullStudySection.name`, `FullStudySection.sra_designator_code`, `FullStudySection.sra_flex_code`, `FullStudySection.srg_code`, `FullStudySection.srg_flex`, `FullStudySection` | Object with attributes: `group`, `name`, `sra_designator_code`, `sra_flex_code`, `srg_code`, `srg_flex` |
| `FundingMechanism` | `funding_mechanism` |  |
| `IndirectCostAmt` | `indirect_cost_amt` |  |
| `IsActive` | `is_active` |  |
| `IsNew` | `is_new` |  |
| `MechanismCodeDc` | `mechanism_code_dc` |  |
| `OpportunityNumber` | `opportunity_number` |  |
| `Organization` | `Organization.dept_type`, `Organization.external_org_id`, `Organization.org_city`, `Organization.org_country`, `Organization.org_duns`, `Organization.org_fips`, `Organization.org_ipf_code`, `Organization.org_name`, `Organization.org_state`, `Organization.org_ueis`, `Organization.org_zipcode`, `Organization.primary_duns`, `Organization.primary_uei`, `Organization` | Object with attributes: `dept_type`, `external_org_id`, `org_city`, `org_country`, `org_duns`, `org_fips`, `org_ipf_code`, `org_name`, `org_state`, `org_ueis`, `org_zipcode`, `primary_duns`, `primary_uei` |
| `OrganizationType` | `OrganizationType.code`, `OrganizationType.is_other`, `OrganizationType.name`, `OrganizationType` | Object with attributes: `code`, `is_other`, `name` |
| `PhrText` | `phr_text` |  |
| `PrefTerms` | `pref_terms` |  |
| `PrincipalInvestigators` | `PrincipalInvestigators.first_name`, `PrincipalInvestigators.full_name`, `PrincipalInvestigators.is_contact_pi`, `PrincipalInvestigators.last_name`, `PrincipalInvestigators.middle_name`, `PrincipalInvestigators.profile_id`, `PrincipalInvestigators.title`, `PrincipalInvestigators` | Object with attributes: `first_name`, `full_name`, `is_contact_pi`, `last_name`, `middle_name`, `profile_id`, `title` |
| `ProgramOfficers` | `ProgramOfficers.first_name`, `ProgramOfficers.full_name`, `ProgramOfficers.last_name`, `ProgramOfficers.middle_name`, `ProgramOfficers` | Object with attributes: `first_name`, `full_name`, `last_name`, `middle_name` |
| `ProjectDetailUrl` | `project_detail_url` |  |
| `ProjectEndDate` | `project_end_date` |  |
| `ProjectNum` | `project_num` |  |
| `ProjectNumSplit` | `ProjectNumSplit.activity_code`, `ProjectNumSplit.appl_type_code`, `ProjectNumSplit.full_support_year`, `ProjectNumSplit.ic_code`, `ProjectNumSplit.serial_num`, `ProjectNumSplit.suffix_code`, `ProjectNumSplit.support_year`, `ProjectNumSplit` | Object with attributes: `activity_code`, `appl_type_code`, `full_support_year`, `ic_code`, `serial_num`, `suffix_code`, `support_year` |
| `ProjectSerialNum` | `project_serial_num` |  |
| `ProjectStartDate` | `project_start_date` |  |
| `ProjectTitle` | `project_title` |  |
| `SpendingCategories` | `spending_categories` |  |
| `SpendingCategoriesDesc` | `spending_categories_desc` |  |
| `SubprojectId` | `subproject_id` |  |
| `Terms` | `terms` |  |

## Non-filterable / include-only fields

| Path | Name | Reason |
|---|---|---|
| `AgencyIcAdmin.code` | IC Code | No usable `PayloadCriteriaName` is defined in the PDF. |
| `AgencyIcAdmin.name` | IC Name | No usable `PayloadCriteriaName` is defined in the PDF. |
| `arra_funded` | ARRA Indicator | No usable `PayloadCriteriaName` is defined in the PDF. |
| `budget_start` | Budget Start Date | No usable `PayloadCriteriaName` is defined in the PDF. |
| `budget_end` | Budget End Date | No usable `PayloadCriteriaName` is defined in the PDF. |
| `cfda_code` | CFDA Code | No usable `PayloadCriteriaName` is defined in the PDF. |
| `OrganizationType.name` | Generic Name for Institution Type | No usable `PayloadCriteriaName` is defined in the PDF. |
| `OrganizationType.code` | Generic Name for Institution Type Code | No usable `PayloadCriteriaName` is defined in the PDF. |
| `OrganizationType.is_other` | Other Generic Institution Type | No usable `PayloadCriteriaName` is defined in the PDF. |
| `AgencyIcFundings.fy` | Fiscal Year | No usable `PayloadCriteriaName` is defined in the PDF. |
| `AgencyIcFundings.name` | IC Name | No usable `PayloadCriteriaName` is defined in the PDF. |
| `AgencyIcFundings.abbreviation` | IC Name Abbreviation | No usable `PayloadCriteriaName` is defined in the PDF. |
| `funding_mechanism` | Funding Mechanism | No usable `PayloadCriteriaName` is defined in the PDF. |
| `spending_categories` | NIH Spending Categories Code | No usable `PayloadCriteriaName` is defined in the PDF. |
| `Organization` | Organization | No usable `PayloadCriteriaName` is defined in the PDF. |
| `Organization.org_duns` | DUNS | No usable `PayloadCriteriaName` is defined in the PDF. |
| `Organization.org_ueis` | Unique Entity Identifier | No usable `PayloadCriteriaName` is defined in the PDF. |
| `Organization.primary_duns` | Primary DUNS | No usable `PayloadCriteriaName` is defined in the PDF. |
| `Organization.primary_uei` | Primary UEI | No usable `PayloadCriteriaName` is defined in the PDF. |
| `Organization.org_fips` | FIPS | No usable `PayloadCriteriaName` is defined in the PDF. |
| `Organization.org_ipf_code` | Institution Profile (IPF) Number | No usable `PayloadCriteriaName` is defined in the PDF. |
| `Organization.org_zipcode` | Organization ZIP Code | No usable `PayloadCriteriaName` is defined in the PDF. |
| `Organization.external_org_id` | External Organization ID | No usable `PayloadCriteriaName` is defined in the PDF. |
| `phr_text` | Public Health Relevance | No usable `PayloadCriteriaName` is defined in the PDF. |
| `PrincipalInvestigators.is_contact_pi` | Principal Investigator of Contact | No usable `PayloadCriteriaName` is defined in the PDF. |
| `PrincipalInvestigators.title` | Title of Principal Investigator | No usable `PayloadCriteriaName` is defined in the PDF. |
| `FullStudySection` | Study Section | No usable `PayloadCriteriaName` is defined in the PDF. |
| `FullStudySection.srg_code` | Scientific Review Group (SRG) | No usable `PayloadCriteriaName` is defined in the PDF. |
| `FullStudySection.name` | Study Section Name | No usable `PayloadCriteriaName` is defined in the PDF. |
| `FullStudySection.srg_flex` | Scientific Review Group Flex Code | No usable `PayloadCriteriaName` is defined in the PDF. |
| `FullStudySection.sra_designator_code` | Scientific Review Administrator Designator Code | No usable `PayloadCriteriaName` is defined in the PDF. |
| `FullStudySection.sra_flex_code` | Scientific Review Administrator Flex Code | No usable `PayloadCriteriaName` is defined in the PDF. |
| `FullStudySection.group` | Study Section Group | No usable `PayloadCriteriaName` is defined in the PDF. |
| `direct_cost_amt` | Total of Direct Cost Funding | No usable `PayloadCriteriaName` is defined in the PDF. |
| `indirect_cost_amt` | Total of Indirect Cost Funding | No usable `PayloadCriteriaName` is defined in the PDF. |
| `terms` | RCDC Thesaurus Terms | No usable `PayloadCriteriaName` is defined in the PDF. |
| `project_detail_url` | Project Details Page URL | No usable `PayloadCriteriaName` is defined in the PDF. |