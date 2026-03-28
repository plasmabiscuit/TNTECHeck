# NIH RePORTER Project API Markdown Conversion Pack

This pack converts the uploaded **Data Elements for RePORTER Project API** PDF into developer-oriented Markdown references for dashboard and query-builder work.

## Source facts

- Source document title: `Data Elements for RePORTER Project API`
- PDF length: **51 pages**
- Project API field definitions captured: **92**
- Top-level fields and objects: **44**
- Object attributes: **48**
- Spending categories captured from Appendix I: **326**
- Administrative IC code rows captured from Appendix II: **29**
- Latest version in PDF: **2.2** on **07/18/2025**

## What is in this pack

- `RePORTER_Project_API_Field_Catalog.md`
- `RePORTER_Project_API_Query_Map.md`
- `RePORTER_Project_API_Spending_Categories_FY2024.md`
- `RePORTER_Project_API_Admin_IC_Codes.md`

## Structure of the API dictionary

The PDF defines each data element using these columns: business name, definition, type, `PayloadCriteriaName`, `APIResponseName`, `APIIncludeFieldName`, and `ExPORTERColumn`.
Object fields such as `Organization`, `Principal Investigator`, `Program Officer`, `Study Section`, `Funding ICs`, and `Project Number Components Split` have nested object-attribute records rather than flat scalar fields.

## Recommended dashboard starter fields

- Core IDs and grant numbers: `appl_id`, `project_num`, `core_project_num`, `project_serial_num`, `subproject_id`
- Funding analysis: `fiscal_year`, `award_amount`, `direct_cost_amt`, `indirect_cost_amt`, `funding_mechanism`, `AgencyIcFundings.total_cost`
- Institution and org matching: `Organization.org_name`, `Organization.org_state`, `Organization.org_city`, `Organization.org_ueis`, `Organization.org_duns`, `Organization.org_ipf_code`
- PI and staffing analysis: `PrincipalInvestigators.full_name`, `PrincipalInvestigators.profile_id`, `ProgramOfficers.full_name`, `contact_pi_name`
- Portfolio/topic analysis: `project_title`, `abstract_text`, `terms`, `pref_terms`, `spending_categories_desc`, `covid_response`
- Review / award structure: `FullStudySection.name`, `ProjectNumSplit.*`, `is_active`, `is_new`

## Latest version history from the PDF

| Version | Date | Detail |
|---|---|---|
| `1.0` | 10/08/2021 | Quyin Fan Initial version |
| `1.1` | 12/06/2021 | Quyin Fan Fix CFDA type, add UEI, primary UEI, primary DUNS, and category 3265 |
| `1.2` | 01/12/2022 | Quin Fan Append IC values |
| `1.3` | 02/28/2022 | Quyin Fan Update Award notice date and award amount sample payload criteria |
| `1.4` | 03/10/2022 | Quyin Fan Add information for date_added data element |
| `1.5` | 03/21/2022 | Quyin Fan Update definition for Active Project indicator and Newly added project indicator |
| `1.6` | 05/10/2022 | Quyin Fan Update project title definition |
| `1.7` | 09/21/2022 | Quyin Fan Add note on funding mechanism search value ‘Other’ |
| `1.8` | 12/05/2022 | Chidambaram Muthappan Modify sub-section title for ‘Record Added Date’ |
| `1.9` | 08/09/2023 | Angkana Saparakpanya Update FOA label to Opportunity Number |
| `2.0` | 08/11/2023 | Angkana Saparakpanya Update definition of Award Type 4C/4N |
| `2.1` | 04/23/2025 | Angkana Saparakpanya Update list of Spending Categories available in FY2023 |
| `2.2` | 07/18/2025 | Angkana Saparakpanya Update list of Spending Categories available in FY2024 and ExPORTER Column label from ‘CFDA_CODE’ to ‘ASSISTANCE_LISTING_NUMBER’ |