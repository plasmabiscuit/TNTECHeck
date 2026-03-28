# Grants.gov Opportunity-Focused Schemas and Data Elements

This file focuses on the schema/data elements most relevant to **opportunity info**, **package discovery**, and **instruction/package retrieval**.

## 1) Applicant Common Elements (`ApplicantCommonElements-V1.0.xsd`)

### OpportunityFilter
| Sub-element | Type | Rules / Notes |
|---|---|---|
| `FundingOpportunityNumber` | `GrantsCommonElements:FundingOpportunityNumber` | Example shown: `03272012-KJ-SP-MP` |
| `CFDANumber` | `GrantsCommonElements:CFDANumber` | Example shown: `00.000` |
| `CompetitionID` | `GrantsCommonElements:CompetitionID` | Example shown: `03272012-KJ-SP-MP` |

**Business rule:** one sub-element is required.

### SubmissionFilter
| Sub-element | Type | Required? | Notes |
|---|---|---|---|
| `Type` | `ApplicantCommonElements:SubmissionFilterType` | Required | |
| `Value` | `GrantsCommonTypes:StringMin1Max255Type` | Required | |

### SubmissionFilterType valid values
- `FundingOpportunityNumber`
- `GrantsGovTrackingNumber`
- `PackageID`
- `SubmissionTitle`
- `Status`

### OpportunityDetails
This is the return structure used by `GetOpportunityList`.

| Field | Type / format | Notes |
|---|---|---|
| `FundingOpportunityNumber` | `GrantsCommonElements:FundingOpportunityNumber` | |
| `FundingOpportunityTitle` | `GrantsCommonElements:FundingOpportunityTitle` | |
| `CompetitionID` | `GrantsCommonElements:CompetitionID` | |
| `CompetitionTitle` | `GrantsCommonElements:CompetitionTitle` | |
| `PackageID` | `GrantsCommonElements:PackageID` | |
| `CFDADetails` | `ApplicantCommonElements:CFDADetails` | May occur multiple times |
| `OpeningDate` | `date` | Format `YYYY-MM-DD` |
| `ClosingDate` | `date` | Format `YYYY-MM-DD` |
| `OfferingAgency` | `GrantsCommonElements:OfferingAgency` | Example shown: `NIH` |
| `AgencyContactInfo` | `GrantsCommonElements:AgencyContactInfo` | |
| `SchemaURL` | `GrantsCommonElements:SchemaURL` | Example points to applicant package XSD |
| `InstructionsURL` | `GrantsCommonElements:InstructionsURL` | Example points to package instructions doc |
| `IsMultiProject` | `Boolean` | `True/False` |

### SubmissionDetails
| Field | Type / format | Notes |
|---|---|---|
| `GrantsGovTrackingNumber` | `GrantsCommonElements:GrantsGovTrackingNumber` | |
| `AgencyTrackingNumber` | `GrantsCommonElements:AgencyTrackingNumber` | |
| `GrantsGovApplicationStatus` | `GrantsCommonElements:GrantsGovApplicationStatus` | see valid values below |
| `ReceivedDateTime` | `dateTime` | `YYYY-MM-DDThh:mm:ss` |
| `StatusDateTime` | `dateTime` | `YYYY-MM-DDThh:mm:ss` |
| `FundingOpportunityNumber` | `GrantsCommonElements:FundingOpportunityNumber` | |
| `SubmissionTitle` | `GrantsCommonElements:SubmissionTitle` | |
| `PackageID` | `GrantsCommonElements:PackageID` | |
| `CFDADetails.Number` | `GrantsCommonTypes:CFDANumberType` | Example `10.001` |
| `CFDADetails.Title` | `GrantsCommonTypes:StringWithoutNewLine255Type` | Example shown in docs |

---

## 2) Grants Common Elements (`GrantsCommonElements-V1.0.xsd`)

### Core opportunity/package identifiers and descriptors
| Element | Type | Rules / valid values |
|---|---|---|
| `OpportunityID` | `GrantsCommonTypes:Number18DigitType` | |
| `PackageID` | `GrantsCommonTypes:PackageIDType` | |
| `CompetitionID` | `GrantsCommonTypes:CompetitionIDType` | |
| `CompetitionTitle` | `GrantsCommonTypes:CompetitionTitleType` | |
| `FundingOpportunityNumber` | `GrantsCommonTypes:FundingOpportunityNumberType` | |
| `FundingOpportunityTitle` | `GrantsCommonTypes:StringWithoutNewLine255Type` | |
| `CFDANumber` | `GrantsCommonTypes:CFDANumberType` | |
| `CFDADescription` | `GrantsCommonTypes:StringWithoutNewLine255Type` | |
| `AgencyCode` | `GrantsCommonTypes:StringMin1Max255Type` | |
| `AgencyName` | `GrantsCommonTypes:StringMin1Max255Type` | |
| `OfferingAgency` | `GrantsCommonTypes:StringMin1Max255Type` | |
| `AgencyContactInfo` | `GrantsCommonTypes:AgencyContactInfoType` | |

### Dates and URLs
| Element | Type | Rules / notes |
|---|---|---|
| `PostingDate` | `GrantsCommonTypes:MMDDYYYYFwdSlashType` | |
| `ClosingDate` | `GrantsCommonTypes:MMDDYYYYFwdSlashType` | |
| `ArchiveDate` | `GrantsCommonTypes:MMDDYYYYFwdSlashType` | |
| `SchemaURL` | `GrantsCommonTypes:StringWithoutNewLine255Type` | |
| `InstructionsURL` | `GrantsCommonTypes:StringWithoutNewLine255Type` | |
| `LastUpdatedTimestamp` | `dateTime` | |
| `InstructionFileLastUpdatedTimestamp` | `dateTime` | |

### Opportunity category
| Element | Type | Rules / valid values |
|---|---|---|
| `OpportunityCategory` | `GrantsCommonTypes:OpportunityCategoryType` | `D` Discretionary, `M` Mandatory, `C` Continuation, `E` Earmark, `O` Other |
| `OtherOpportunityCategoryExplanation` | `String` | Max length 255; optional |
| `OpportunityCategoryExplanation` | `GrantsCommonTypes:StringMin1Max255Type` | |

### Package/instruction helper structures
| Element | Type | Notes |
|---|---|---|
| `CompetitionInfo` | Complex | contains `CompetitionID` and `CompetitionTitle` |
| `InstructionFileInfo` | Complex | contains `FileName`, `FileExtension`, `FileContentId`, `FileDataHandler` |
| `Attachment` | Complex | contains `FileContentId`, `FileDataHandler` |

### Filters and service plumbing relevant to discovery/workflow
| Element | Type | Notes |
|---|---|---|
| `ExpandedApplicationFilter` | `String` | Valid values include `Status`, `FundingOpportunityNumber`, `CFDANumber`, `SubmissionTitle`, `GrantsGovTrackingNumber`, `OpportunityID`, `AgencyCode`, `CompetitionID`, `PackageID`, `SubmissionMethod` |
| `ApplicationFilter` | Complex | `Filter`, `FilterValue`, `FilterType` with status/opportunity/cfda-based values |
| `CompletionStatus` | `GrantsCommonTypes:OperationStatusType` | |
| `ResponseMessage` | `String` | valid values `Success` / `Failure` |
| `SecurityMessage` | Complex | `MessageCode`, `MessageText` |
| `ErrorDetails` | Complex | `Code`, optional `Message` |

### Application/submission-related helper elements that may still appear in opportunity workflows
| Element | Type | Notes |
|---|---|---|
| `SubmissionMethod` | `GrantsCommonTypes:SubmissionMethodType` | |
| `SubmissionTitle` | `GrantsCommonTypes:StringMin1Max240Type` | |
| `GrantsGovTrackingNumber` | `GrantsCommonTypes:GrantsGovTrackingNumberType` | |
| `AgencyTrackingNumber` | `GrantsCommonTypes:StringMin1Max240Type` | |
| `GrantsGovApplicationStatus` | `GrantsCommonTypes:GrantsGovApplicationStatusType` | |
| `StatusDetail` | `GrantsCommonTypes:StatusDetailType` | |
| `AgencyNotes` | `GrantsCommonTypes:AgencyNotesType` | |

### Applicant/org identity helpers
| Element | Type | Notes |
|---|---|---|
| `UEI` | `GrantsCommonTypes:UEIType` | |
| `DUNS` | `GrantsCommonTypes:DUNSType` | |
| `AORStatus` | `GrantsCommonTypes:AORStatusType` | |
| `AORUserFullName` | `GrantsCommonTypes:FullNameType` | |
| `ActiveExclusions` | `GrantsCommonTypes:ActiveExclusionsType` | |
| `DelinquentFederalDebt` | `GrantsCommonTypes:DelinquentFederalDebtType` | |

---

## 3) High-value fields for opportunity/package + eligibility workflows
If you only wire a first pass, make sure you capture at least:

- `FundingOpportunityNumber`
- `FundingOpportunityTitle`
- `OpportunityID`
- `PackageID`
- `CompetitionID`
- `CompetitionTitle`
- `CFDADetails`
- `OpeningDate`
- `ClosingDate`
- `OfferingAgency`
- `AgencyContactInfo`
- `SchemaURL`
- `InstructionsURL`
- `OpportunityCategory`
- REST detail fields such as `synopsis.applicantTypes`, `synopsis.synopsisDesc`, `synopsisAttachmentFolders`, `alns`
