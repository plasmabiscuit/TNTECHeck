# Grants.gov Common Types Relevant to Opportunity/Package Workflows

This file distills the `GrantsCommonTypes` page to the types you are most likely to need when validating opportunity/package request payloads and responses.

## Enumerated / coded types
| Type | Rules / valid values |
|---|---|
| `OpportunityCategoryType` | `D` Discretionary, `M` Mandatory, `C` Continuation, `E` Earmark, `O` Other |
| `SubmissionMethodType` | `PDF`, `Workspace`, `S2S`, `Third Party S2S` |
| `OperationStatusType` | `Success`, `Partial`, `Fail` |
| `GrantsGovApplicationStatusType` | `Receiving`, `Received`, `Processing`, `Validated`, `Rejected with Errors`, `Download Preparation`, `Received by Agency`, `Agency Tracking Number Assigned` |
| `AORStatusType` | `AUTHORIZED`, `UNAUTHORIZED` |
| `YesNoType` | `Y`, `N` |
| `ActiveExclusionsType` | `Yes`, `No`, `Not Available` |
| `DelinquentFederalDebtType` | `Yes`, `No`, `Not Available` |

## Identifier / code formats
| Type | Rules |
|---|---|
| `PackageIDType` | Valid format `PKG########` where `#` is numeric only |
| `FundingOpportunityNumberType` | Uppercase letters, numeric, and hyphens; max length 40 |
| `CompetitionIDType` | Uppercase letters, numeric, and hyphens; max length 40; no whitespace |
| `CompetitionTitleType` | cannot begin with whitespace; no newline; max length 255 |
| `CFDANumberType` | valid format `##.###`; numeric only; no whitespace |
| `GrantsGovTrackingNumberType` | valid format `GRANTxxxxxxxx` where `x` is numeric only |
| `DUNSType` | alphanumeric; first 9 characters numeric; min length 9, max 13 |
| `UEIType` | alphanumeric; fixed length 12 |
| `UserIDType` | spaces and non-whitespace characters allowed; invalid: line feeds, tabs, carriage returns |
| `TokenIdType` | min length 1; max length 2000 |
| `MessageCodeType` | numeric; min length 2; max length 2 |

## String/date helpers
| Type | Rules |
|---|---|
| `MMDDYYYYFwdSlashType` | `MM/DD/YYYY` format; no whitespace |
| `YYYYDateType` | numeric; max length 4 |
| `FileNameType` | no leading whitespace; no newline; max length 255 |
| `FileExtensionType` | no leading whitespace; no newline; max length 15 |
| `FileContentIdType` | no leading whitespace; no newline; max length 255 |
| `StringWithoutNewLine255Type` | no leading whitespace; no newline; max length 255 |
| `StringWithoutNewLine250Type` | no leading whitespace; no newline; max length 250 |
| `StringWithoutNewLine130Type` | no leading whitespace; no newline; max length 130 |
| `StringWithoutNewLine512Type` | no leading whitespace; no newline; max length 512 |
| `StringMin1Max240Type` | min 1; max 240 |
| `StringMin1Max255Type` | min 1; max 255 |
| `StringMin1Max250Type` | min 1; max 250 |
| `StringMin1Max2000Type` | min 1; max 2000 |
| `StringMin1Max2500Type` | min 1; max 2500 |
| `StringMin1Max4000Type` | min 1; max 4000 |
| `StringMin1Max18000Type` | min 1; max 18000 |
| `FullNameType` | min 1; max 240 |
| `AgencyContactInfoType` | min 1; max 2000 |
| `AgencyNotesType` | min 1; max 2048 |
| `StatusDetailType` | min 1 (additional max-length detail is not fully shown in the page excerpt) |

## Numeric string helpers
| Type | Rules |
|---|---|
| `Number4DigitsType` | numeric; max length 4 |
| `Number8DigitsType` | numeric; max length 8 |
| `Number8DigitsOrUnboundedType` | numeric; max length 8 or unbounded semantics per schema naming |
| `Number15DigitsType` | numeric; max length 15 |
| `Number18DigitsType` | numeric; max length 18 |
| `Number20DigitsType` | numeric; max length 20 |
