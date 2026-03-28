# Urban Colleges Endpoint Inventory

This inventory is derived from the endpoint table exposed in the Urban-maintained **R package** repository README. It is one of the most practical sources for seeing the available **college-university** endpoints in compact form.

## Legend

- **Level**: top-level section in the API
- **Source**: underlying data source in Urban's portal
- **Topic**: endpoint/topic name
- **Subtopic**: required path disaggregator(s), if any
- **Main Filters**: key filters surfaced in the endpoint table
- **Years Available**: years reported by the Urban R package docs at the time of capture

## College-university endpoints

| Level | Source | Topic | Subtopic | Main Filters | Years Available |
|---|---|---|---|---|---|
| college-university | campus | crime | hate-crimes | NA | 2005–2021 |
| college-university | eada | institutional-characteristics | NA | year | 2002–2021 |
| college-university | fsa | 90-10-revenue-percentages | NA | year | 2014–2021 |
| college-university | fsa | campus-based-volume | NA | year | 2001–2021 |
| college-university | fsa | financial-responsibility | NA | year | 2006–2016 |
| college-university | fsa | grants | NA | year | 1999–2021 |
| college-university | fsa | loans | NA | year | 1999–2021 |
| college-university | ipeds | academic-libraries | NA | year | 2013–2020 |
| college-university | ipeds | academic-year-room-board-other | NA | year | 1999–2021 |
| college-university | ipeds | academic-year-tuition-prof-program | NA | year | 1986–2008, 2010–2021 |
| college-university | ipeds | academic-year-tuition | NA | year | 1986–2021 |
| college-university | ipeds | admissions-enrollment | NA | year | 2001–2022 |
| college-university | ipeds | admissions-requirements | NA | year | 1990–2022 |
| college-university | ipeds | completers | NA | year | 2011–2022 |
| college-university | ipeds | completions-cip-2 | NA | year | 1991–2022 |
| college-university | ipeds | completions-cip-6 | NA | year | 1983–2022 |
| college-university | ipeds | directory | NA | year | 1980, 1984–2022 |
| college-university | ipeds | enrollment-full-time-equivalent | NA | year, level_of_study | 1997–2021 |
| college-university | ipeds | enrollment-headcount | NA | year, level_of_study | 1996–2021 |
| college-university | ipeds | fall-enrollment | age, sex | year, level_of_study | 1991, 1993, 1995, 1997, 1999–2020 |
| college-university | ipeds | fall-enrollment | race, sex | year, level_of_study | 1986–2022 |
| college-university | ipeds | fall-enrollment | residence | year | 1986, 1988, 1992, 1994, 1996, 1998, 2000–2020 |
| college-university | ipeds | fall-retention | NA | year | 2003–2020 |
| college-university | ipeds | finance | NA | year | 1979, 1983–2017 |
| college-university | ipeds | grad-rates-200pct | NA | year | 2007–2017 |
| college-university | ipeds | grad-rates-pell | NA | year | 2015–2017 |
| college-university | ipeds | grad-rates | NA | year | 1996–2017 |
| college-university | ipeds | institutional-characteristics | NA | year | 1980, 1984–2022 |
| college-university | ipeds | outcome-measures | NA | year | 2015–2021 |
| college-university | ipeds | program-year-room-board-other | NA | year | 1999–2021 |
| college-university | ipeds | program-year-tuition-cip | NA | year | 1987–2021 |
| college-university | ipeds | salaries-instructional-staff | NA | year | 1980, 1984, 1985, 1987, 1989–1999, 2001–2022 |
| college-university | ipeds | salaries-noninstructional-staff | NA | year | 2012–2022 |
| college-university | ipeds | sfa-all-undergraduates | NA | year | 2007–2021 |
| college-university | ipeds | sfa-by-living-arrangement | NA | year | 2008–2021 |
| college-university | ipeds | sfa-by-tuition-type | NA | year | 1999–2021 |
| college-university | ipeds | sfa-ftft | NA | year | 1999–2021 |
| college-university | ipeds | sfa-grants-and-net-price | NA | year | 2008–2021 |
| college-university | ipeds | student-faculty-ratio | NA | year | 2009–2020 |
| college-university | nacubo | endowments | NA | year | 2012–2022 |
| college-university | nccs | 990-forms | NA | year | 1993–2016 |
| college-university | nhgis | census-1990 | NA | year | 1980, 1984–2022 |
| college-university | nhgis | census-2000 | NA | year | 1980, 1984–2022 |
| college-university | nhgis | census-2010 | NA | year | 1980, 1984–2022 |
| college-university | scorecard | default | NA | year | 1996–2020 |
| college-university | scorecard | earnings | NA | year | 2003–2014, 2018 |
| college-university | scorecard | institutional-characteristics | NA | year | 1996–2020 |
| college-university | scorecard | repayment | NA | year | 2007–2016 |
| college-university | scorecard | student-characteristics | aid-applicants | year | 1997–2016 |
| college-university | scorecard | student-characteristics | home-neighborhood | year | 1997–2016 |

## Endpoints most relevant to TNTECHeck

### First-priority institutional profile endpoints
- `ipeds/directory`
- `ipeds/institutional-characteristics`
- `ipeds/admissions-enrollment`
- `ipeds/admissions-requirements`

### First-priority student profile / pipeline endpoints
- `ipeds/enrollment-headcount`
- `ipeds/enrollment-full-time-equivalent`
- `ipeds/fall-enrollment/race/sex`
- `ipeds/fall-enrollment/age/sex`
- `ipeds/fall-enrollment/residence`

### First-priority program production endpoints
- `ipeds/completions-cip-6`
- `ipeds/completions-cip-2`
- `ipeds/completers`

### First-priority student success / attainment endpoints
- `ipeds/fall-retention`
- `ipeds/grad-rates`
- `ipeds/grad-rates-200pct`
- `ipeds/outcome-measures`

### First-priority affordability / aid endpoints
- `ipeds/academic-year-tuition`
- `ipeds/program-year-tuition-cip`
- `ipeds/sfa-ftft`
- `ipeds/sfa-grants-and-net-price`
- `ipeds/sfa-all-undergraduates`

### Useful context / supplemental endpoints
- `scorecard/default`
- `scorecard/repayment`
- `scorecard/earnings`
- `scorecard/student-characteristics/aid-applicants`
- `nacubo/endowments`
- `fsa/grants`
- `fsa/loans`
- `campus/crime/hate-crimes`

## Caveats

1. **Years vary heavily by endpoint.**  
   You cannot assume that all endpoint families support the same year range.

2. **Some endpoints have required subtopics.**  
   Example: `fall-enrollment/race/sex` and `fall-enrollment/age/sex`.

3. **Not all useful metrics are raw one-field pulls.**  
   Some proposal-ready indicators require combining multiple endpoints or computing derived metrics.

4. **Urban exposes both IPEDS and Scorecard slices.**  
   Do not casually combine them without documenting source provenance and year semantics.
