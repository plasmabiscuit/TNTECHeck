# College Scorecard Markdown Conversion Pack for Dashboard Development

This pack converts the uploaded College Scorecard data dictionary workbook into dashboard-oriented Markdown references.

## Source workbook facts

- Workbook title: COLLEGE SCORECARD
- Release note in README sheet: Released March 23, 2026
- Source workbook used for conversion: `CollegeScorecardDataDictionary.xlsx`
- Institution-level dictionary entries consolidated: **3308**
- Field-of-study dictionary entries consolidated: **178**
- Institution-level coverage map rows: **3308**
- Field-of-study coverage map rows: **178**

## What was normalized during conversion

- Continuation rows containing coded values were attached to their parent variable.
- Newlines in field descriptions were preserved as HTML line breaks for Markdown readability.
- Cohort availability was merged in so each field record includes historical coverage context where possible.

- Four legacy institution variables in the dictionary were not present in the institution cohort maps and therefore have blank coverage fields: `D150_4_AIANOld`, `D150_4_HISPOld`, `D150_L4_AIANOld`, and `D150_L4_HISPOld`.
- Institution-level and field-of-study records were split because they serve different dashboard surfaces.

## Files in this pack

- `CollegeScorecard_Institution_Core.md`
- `CollegeScorecard_Institution_Outcomes.md`
- `CollegeScorecard_FieldOfStudy.md`
- `CollegeScorecard_Cohort_Coverage.md`

## Category counts

- `root`: 6
- `school`: 50
- `admissions`: 32
- `student`: 131
- `academics`: 247
- `cost`: 85
- `aid`: 111
- `completion`: 1367
- `earnings`: 185
- `repayment`: 1094
- `programs` (field of study): 178

## Recommended dashboard starter domains

For a TTU-first grant data dashboard, the highest-value starting domains are usually:
- Institutional identity and descriptors: `id`, `ope6_id`, `school.name`, `school.state`, `school.locale`, `school.carnegie_*`, `school.minority_serving.*`
- Student body and pipeline: `student.size`, `student.demographics.*`, `student.retention_rate.*`, `student.fafsa_sent.*`
- Academic supply / program mix: `program.*`, `program_percentage.*`, and field-of-study `cip_4_digit.*`
- Affordability and debt: `cost.*`, `aid.*`
- Proposal-grade outcomes: `completion.*`, `earnings.*`, `repayment.*`

## Latest workbook changes called out in the ChangeLog

- **All dates** — `Most_Recent_Inst_Cohort_Map`: Note that any changes referenced as changes in the "institution_cohort_map" tab were also made for the "most_recent_inst_cohort_map" tab.
- **March 23, 2026** — `Institution_Data_Dictionary`:  Added entries for EARN_THR_STATE and EARN_THR_NAT
- **Same release block** — `Institution_Cohort_Map`: Updated entries with new values due to data refresh and added entries for EARN_THR_STATE and EARN_THR_NAT.
- **Same release block** — `FieldOfStudy_Data_Dictionary`: Added entries for EARN_COUNT_WNE_4YR_NAT, EARN_MDN_4YR_NAT, EARN_P25_4YR_NAT, EARN_P75_4YR_NAT
- **Same release block** — `FieldOfStudy_Cohort_Map`: Updated entries with new values due to data refresh and added entries for EARN_COUNT_WNE_4YR_NAT, EARN_MDN_4YR_NAT, EARN_P25_4YR_NAT, EARN_P75_4YR_NAT
- **November 17, 2025** — `Institution_Cohort_Map`: Updated entries with new values due to data refresh
- **Same release block** — `FieldOfStudy_Cohort_Map`: Updated entries with new values due to data refresh
- **April 23, 2025** — `Glossary`: Added a definition for "NA"
- **Same release block** — `Institution_Data_Dictionary`: Added entry for SCORECARD_SECTOR
- **Same release block** — `Institution_Cohort_Map`: Updated entries with new values due to data refresh and added entry for SCORECARD_SECTOR
- **January 16, 2025** — `Institution_Cohort_Map`: Updated entries with new values due to data refresh
- **Same release block** — `FieldOfStudy_Cohort_Map`: Updated entries with new values due to data refresh

## Glossary terms copied from workbook

| Term | Description | Notes |
|---|---|---|
| `Acad yr` | Academic Year; differs by institution, but generally the period from September to June (e.g., AcadYr 2013-14 = 9/1/2013 - 5/31/2014) | Referenced in the data cohort map |
| `AY` | Award Year (e.g. AY 2013-14 = 7/1/2013-6/30/2014) | Referenced in the data cohort map |
| `CY` | Calendar Year (e.g. CY 2014 = 1/1/14-12/31/14) | Referenced in the data cohort map |
| `DCY` | IPEDS Data Collection Year (e.g., DCY2013-14 = the 2013-14 IPEDS collection) | Referenced in the data cohort map |
| `FSA` | Federal Student Aid | In the data dictionary, an "FSA" value in the “Source” field indicates that the data element described is derived from the FSA Data Center (https://studentaid.ed.gov/sa/data-center) or FSA Postsecondary Education Participant System (https://www2.ed.gov/offices/OSFAP/PEPS/dataextracts.html) |
| `FY` | Fiscal Year (e.g. FY 2014= 10/1/13-9/30/14) | Referenced in the data cohort map |
| `IPEDS` | Integrated Postsecondary Education Data System | An "IPEDS" value in the "Source" field indicates that the data element described is derived from IPEDS (http://nces.ed.gov/ipeds/Home/UseTheData) or taken from the College Navigator (http://nces.ed.gov/collegenavigator/) |
| `NA` | Not available | Used in the *_Cohort_Map tabs of this document. Data for this metric are unavailable for all institutions in the indicated data file. |
| `NSLDS` | National Student Loan Data System | NSLDS is the U.S. Department of Education's central database for student aid, a value of “NSLDS” in the “Source” field of the data dictionary indicates that the data element described is derived from NSLDS |
| `OPE` | Office of Postsecondary Education | In the data dictionary, a value of "OPE" in the "Source" field indicates that the data element described is derived from the Department's Office of Postsecondary Education Eligibility Matrix (https://www2.ed.gov/about/offices/list/ope/idues/eligibility.html#tips. ) |
| `Treasury` | U. S. Department of Treasury | A value of "Treasury" in the "Source" field of the data dictionary indicates that the data element described was calculated by the Department of Treasury with data derived from NSLDS combined with data from IRS tax records or data from the U.S. Census Bureau |
| `ED` | U.S. Department of Education | In the data dictionary, a value of "ED" in the "Source" field indicates that the data element described is derived from http://sites.ed.gov/whhbcu/one-hundred-and-five-historically-black-colleges-and-universities/ |
| `PEPS` | FSA Postsecondary Education Participant System | Referenced in the data cohort map |
| `CIP` | Classification of Instructional Programs | Referenced in the data cohort map. |
| `DOL` | Department of Labor | In the data dictionary, a value of "DOL" in the "Source" field indicates that the data element described is derived from the Department of Labor Workforce Innovation and Opportunity Act approved training provider list. |
| `ACS` | Census American Community Survey | Referenced in the data cohort map |

## Practical use notes

- Use the `Developer Name` column as the main dashboard parameter inventory.
- Use the raw `Variable` column when matching against downloadable all-data files or source documentation.
- Use the coverage file before building trend charts; not every metric exists across the full history.
- Many proposal tables will need both institution-level and field-of-study variables, so keep the institution and program files paired during implementation.
