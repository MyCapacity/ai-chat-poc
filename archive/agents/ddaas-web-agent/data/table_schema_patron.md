# Patron Table Schema
| Column Name | Type | Mode | Description |
|------------|------|------|-------------|
| patronid | INT64 | NULLABLE | Primary identifier for the casino patron |
| signuppropertyid | INT64 | NULLABLE | ID of the casino property where the patron initially registered |
| reportDate | DATE | NULLABLE | Date of the patron record report |
| MelLegacyPatronId | INT64 | NULLABLE | Legacy patron ID from Melbourne casino system |
| PerLegacyPatronId | INT64 | NULLABLE | Legacy patron ID from Perth casino system |
| HomePropertyID | INT64 | NULLABLE | ID of the patron's primary casino property |
| PatronSecurityLevel | INT64 | NULLABLE | Security clearance level assigned to the patron |
| SignupDate | DATETIME | NULLABLE | Date and time when the patron account was created |
| ChannelCode | STRING | NULLABLE | Code indicating the registration channel used |
| Channel | STRING | NULLABLE | Description of the registration channel |
| SignupCustomerStatusCode | STRING | NULLABLE | Code indicating the patron's signup status |
| SignupCustomerStatus | STRING | NULLABLE | Description of the patron's signup status |
| AccountCreationEmployeeId | STRING | NULLABLE | ID of the employee who created the account |
| SourceCode | STRING | NULLABLE | Code indicating the source of the patron referral |
| SourceCodeName | STRING | NULLABLE | Description of the referral source |
| EnrolledFlag | STRING | NULLABLE | Indicates if the patron is enrolled in the loyalty program |
| EnrolledDate | DATETIME | NULLABLE | Date when the patron enrolled in the loyalty program |
| ActiveFlag | STRING | NULLABLE | Indicates if the patron account is currently active |
| DateOfBirth | DATE | NULLABLE | Patron's date of birth |
| Gender | STRING | NULLABLE | Patron's gender |
| FirstName | STRING | NULLABLE | Patron's legal first name |
| MiddleName | STRING | NULLABLE | Patron's legal middle name |
| LastName | STRING | NULLABLE | Patron's legal last name |
| Title | STRING | NULLABLE | Patron's legal title code |
| TitleDescription | STRING | NULLABLE | Description of the patron's legal title |
| Suffix | STRING | NULLABLE | Patron's legal name suffix code |
| SuffixDescription | STRING | NULLABLE | Description of the patron's name suffix |
| PreferredFirstName | STRING | NULLABLE | Patron's preferred first name |
| PreferredLastName | STRING | NULLABLE | Patron's preferred last name |
| PreferredNameFlag | STRING | NULLABLE | Indicates if preferred name should be used |
| PreferredTitle | STRING | NULLABLE | Patron's preferred title code |
| PreferredTitleDescription | STRING | NULLABLE | Description of the patron's preferred title |
| PreferredSuffix | STRING | NULLABLE | Patron's preferred name suffix code |
| PreferredSuffixDescription | STRING | NULLABLE | Description of the patron's preferred suffix |
| CommunicationPreference | STRING | NULLABLE | Patron's preferred communication method |
| CommunicationStatusCode | STRING | NULLABLE | Code indicating communication status |
| CommunicationStatus | STRING | NULLABLE | Description of communication status |
| MailToCode | STRING | NULLABLE | Code indicating mail delivery preferences |
| MailTo | STRING | NULLABLE | Description of mail delivery preferences |
| PreferredContactLanguageCode | STRING | NULLABLE | Code for preferred contact language |
| PreferredContactLanguage | STRING | NULLABLE | Description of preferred contact language |
| EmailFlag | STRING | NULLABLE | Indicates if email communication is allowed |
| SMSFlag | STRING | NULLABLE | Indicates if SMS communication is allowed |
| PromotionalMaterialIndicator | STRING | NULLABLE | Indicates if promotional materials are allowed |
| OccupationCode | STRING | NULLABLE | Code indicating patron's occupation |
| Occupation | STRING | NULLABLE | Description of patron's occupation |
| GamingMachineMailFlag | STRING | NULLABLE | Indicates if gaming machine mail is allowed |
| ResidentialAddressLine1 | STRING | NULLABLE | First line of residential address |
| ResidentialAddressLine2 | STRING | NULLABLE | Second line of residential address |
| ResidentialSuburb | STRING | NULLABLE | Suburb of residential address |
| ResidentialStateCode | STRING | NULLABLE | State code of residential address |
| ResidentialState | STRING | NULLABLE | State name of residential address |
| ResidentialPostcode | STRING | NULLABLE | Postcode of residential address |
| ResidentialCountryCode | STRING | NULLABLE | Country code of residential address |
| ResidentialCountry | STRING | NULLABLE | Country name of residential address |
| ResidentialAddressValidationStatus | STRING | NULLABLE | Status of residential address validation |
| ResidentialDPID | STRING | NULLABLE | Delivery Point Identifier for residential address |
| ResidentialDPIDMatchComment | STRING | NULLABLE | Comments on DPID matching for residential address |
| ResidentialLongitude | FLOAT64 | NULLABLE | Longitude coordinate of residential address |
| ResidentialLatitude | FLOAT64 | NULLABLE | Latitude coordinate of residential address |
| ResidentialDTAddress | STRING | NULLABLE | Delivery Territory address for residential address |
| ResidentialDTSuburb | STRING | NULLABLE | Delivery Territory suburb for residential address |
| ResidentialDTPostcode | STRING | NULLABLE | Delivery Territory postcode for residential address |
| ResidentialDTSortPlan | STRING | NULLABLE | Delivery Territory sort plan for residential address |
| ResidentialDTState | STRING | NULLABLE | Delivery Territory state for residential address |
| ResidentialDTMailBarCode | STRING | NULLABLE | Mail barcode for residential address |
| ResidentialLGANumber | INT64 | NULLABLE | Local Government Area number for residential address |
| ResidentialLGAName | STRING | NULLABLE | Local Government Area name for residential address |
| ResidentialLGAType | STRING | NULLABLE | Local Government Area type code for residential address |
| ResidentialLGATypeDescription | STRING | NULLABLE | Description of Local Government Area type for residential address |
| PostalAddressLine1 | STRING | NULLABLE | First line of postal address |
| PostalAddressLine2 | STRING | NULLABLE | Second line of postal address |
| PostalSuburb | STRING | NULLABLE | Suburb of postal address |
| PostalStateCode | STRING | NULLABLE | State code of postal address |
| PostalState | STRING | NULLABLE | State name of postal address |
| PostalPostcode | STRING | NULLABLE | Postcode of postal address |
| PostalCountryCode | STRING | NULLABLE | Country code of postal address |
| PostalCountry | STRING | NULLABLE | Country name of postal address |
| PostalAddressValidationStatus | STRING | NULLABLE | Status of postal address validation |
| PostalDPID | STRING | NULLABLE | Delivery Point Identifier for postal address |
| PostalDPIDMatchComment | STRING | NULLABLE | Comments on DPID matching for postal address |
| PostalLongitude | FLOAT64 | NULLABLE | Longitude coordinate of postal address |
| PostalLatitude | FLOAT64 | NULLABLE | Latitude coordinate of postal address |
| PostalDTAddress | STRING | NULLABLE | Delivery Territory address for postal address |
| PostalDTSuburb | STRING | NULLABLE | Delivery Territory suburb for postal address |
| PostalDTPostcode | STRING | NULLABLE | Delivery Territory postcode for postal address |
| PostalDTSortPlan | STRING | NULLABLE | Delivery Territory sort plan for postal address |
| PostalDTState | STRING | NULLABLE | Delivery Territory state for postal address |
| PostalDTMailBarCode | STRING | NULLABLE | Mail barcode for postal address |
| PostalLGANumber | INT64 | NULLABLE | Local Government Area number for postal address |
| PostalLGAName | STRING | NULLABLE | Local Government Area name for postal address |
| PostalLGAType | STRING | NULLABLE | Local Government Area type code for postal address |
| PostalLGATypeDescription | STRING | NULLABLE | Description of Local Government Area type for postal address |
| EmailType | STRING | NULLABLE | Type of email address |
| EmailAddress | STRING | NULLABLE | Patron's email address |
| InvalidEmailFlag | STRING | NULLABLE | Indicates if email address is invalid |
| EmailValidationStatus | STRING | NULLABLE | Status of email validation |
| EmailStatus | STRING | NULLABLE | Current status of email address |
| PhoneFlag | STRING | NULLABLE | Indicates if phone contact is allowed |
| Home_PhoneNumber | STRING | NULLABLE | Patron's home phone number |
| Home_InvalidPhoneFlag | STRING | NULLABLE | Indicates if home phone is invalid |
| Home_PhoneValidationStatus | STRING | NULLABLE | Status of home phone validation |
| Home_PhoneStatus | STRING | NULLABLE | Current status of home phone |
| Mobile_PhoneNumber | STRING | NULLABLE | Patron's mobile phone number |
| Mobile_InvalidPhoneFlag | STRING | NULLABLE | Indicates if mobile phone is invalid |
| Mobile_PhoneValidationStatus | STRING | NULLABLE | Status of mobile phone validation |
| Mobile_PhoneStatus | STRING | NULLABLE | Current status of mobile phone |
| Work_PhoneNumber | STRING | NULLABLE | Patron's work phone number |
| Work_InvalidPhoneFlag | STRING | NULLABLE | Indicates if work phone is invalid |
| Work_PhoneValidationStatus | STRING | NULLABLE | Status of work phone validation |
| Work_PhoneStatus | STRING | NULLABLE | Current status of work phone |
| Fax_PhoneNumber | STRING | NULLABLE | Patron's fax number |
| Fax_InvalidPhoneFlag | STRING | NULLABLE | Indicates if fax number is invalid |
| Fax_PhoneValidationStatus | STRING | NULLABLE | Status of fax number validation |
| Fax_PhoneStatus | STRING | NULLABLE | Current status of fax number |
| Alternate_PhoneNumber | STRING | NULLABLE | Patron's alternate phone number |
| Alternate_InvalidPhoneFlag | STRING | NULLABLE | Indicates if alternate phone is invalid |
| Alternate_PhoneValidationStatus | STRING | NULLABLE | Status of alternate phone validation |
| Alternate_PhoneStatus | STRING | NULLABLE | Current status of alternate phone |
| NextTierLockout | STRING | NULLABLE | Indicates if patron is locked from next tier |
| NextTierLockoutReason | STRING | NULLABLE | Reason for next tier lockout |
| Tier | STRING | NULLABLE | Current loyalty program tier |
| BusinessOwnerCode | STRING | NULLABLE | Code indicating business ownership status |
| BusinessOwner | STRING | NULLABLE | Description of business ownership status |
| OwnershipPropertyId | INT64 | NULLABLE | ID of property where business ownership is registered |
| MembershipCodeList | STRING | NULLABLE | List of membership codes |
| PrivilegesLockoutList | STRING | NULLABLE | List of locked privileges |
| ReferredEmployeeID | STRING | NULLABLE | ID of employee who referred the patron |
| Spouse | STRING | NULLABLE | Name of patron's spouse |
| MigratedFlag | STRING | NULLABLE | Indicates if record was migrated from legacy system |
| LoyaltyProgram | STRING | NULLABLE | Name of loyalty program |
| DGNLinkedAccountFlag | STRING | NULLABLE | Indicates if account is linked to DGN |
| CustomerStatusCode | STRING | NULLABLE | Code indicating customer status |
| CustomerStatusName | STRING | NULLABLE | Description of customer status |
| DABInitiatedFlag | STRING | NULLABLE | Indicates if DAB was initiated |
| DeactivatedDate | DATETIME | NULLABLE | Date when account was deactivated |
| SingleNameIndicator | STRING | NULLABLE | Indicates if patron uses single name |
| MemberHubAccessFlag | STRING | NULLABLE | Indicates if patron has MemberHub access |
| Mel_AdministrativeStatus | STRING | NULLABLE | Administrative status at Melbourne casino |
| Per_AdministrativeStatus | STRING | NULLABLE | Administrative status at Perth casino |
| PrimaryPatronCardFlag | STRING | NULLABLE | Indicates if this is the primary patron card |
| JunketOperatorFlag | STRING | NULLABLE | Indicates if patron is a junket operator |
| PASOptionStatus | STRING | NULLABLE | Status of Problematic Alcohol Service options |
| PASDeliveryMethod | STRING | NULLABLE | Method of PAS delivery |
| PASSignupDate | DATE | NULLABLE | Date of PAS signup |
| PASViewedDate | DATE | NULLABLE | Date when PAS was viewed |
| PASCollectedDate | DATE | NULLABLE | Date when PAS was collected |
| Mel_Class | STRING | NULLABLE | Classification at Melbourne casino |
| Mel_StopCode | STRING | NULLABLE | Stop code at Melbourne casino |
| Per_Class | STRING | NULLABLE | Classification at Perth casino |
| Per_StopCode | STRING | NULLABLE | Stop code at Perth casino |
| MergedToPatronID | INT64 | NULLABLE | ID of patron record this was merged into |
| Syd_StopCode | STRING | NULLABLE | Stop code at Sydney casino |
| Syd_AdministrativeStatus | STRING | NULLABLE | Administrative status at Sydney casino |
| CCDate | DATE | NULLABLE | Date of customer contact |
| RowInsertProcessAuditUUID_CC | STRING | NULLABLE | Audit UUID for customer contact insert |
| RowInsertDate_CC | TIMESTAMP | NULLABLE | Timestamp of customer contact insert |
| Mel_PersHostEmpID | STRING | NULLABLE | Melbourne personal host employee ID |
| Mel_PersHostEmpFirstName | STRING | NULLABLE | Melbourne personal host first name |
| Mel_PersHostEmpLastName | STRING | NULLABLE | Melbourne personal host last name |
| Per_PersHostEmpID | STRING | NULLABLE | Perth personal host employee ID |
| Per_PersHostEmpFirstName | STRING | NULLABLE | Perth personal host first name |
| Per_PersHostEmpLastName | STRING | NULLABLE | Perth personal host last name |
| RowInsertProcessAuditUUID_SYCO_MEL | STRING | NULLABLE | Audit UUID for Melbourne SYCO insert |
| RowInsertDate_SYCO_MEL | TIMESTAMP | NULLABLE | Timestamp of Melbourne SYCO insert |
| SYCODATE_MEL | DATE | NULLABLE | Melbourne SYCO date |
| RowInsertProcessAuditUUID_SYCO_PER | STRING | NULLABLE | Audit UUID for Perth SYCO insert |
| RowInsertDate_SYCO_PER | TIMESTAMP | NULLABLE | Timestamp of Perth SYCO insert |
| SYCODATE_PER | DATE | NULLABLE | Perth SYCO date |
| RowInsertProcessAuditUUID_CDWH | STRING | NULLABLE | Audit UUID for CDWH insert |
| RowInsertDate_CDWH | TIMESTAMP | NULLABLE | Timestamp of CDWH insert |
| PrimaryPatronId | INT64 | NULLABLE | Primary patron ID for linked accounts |
| SecondaryAccountReason | STRING | NULLABLE | Reason for secondary account status |
| Mel_CurrentDailyTimeLimit | INT64 | NULLABLE | Current daily time limit at Melbourne casino |
| Mel_CurrentDailyNetLossLimit | NUMERIC | NULLABLE | Current daily net loss limit at Melbourne casino |
| Mel_AnnualLossLimit | NUMERIC | NULLABLE | Annual loss limit at Melbourne casino |
| Per_CurrentDailyTimeLimit | INT64 | NULLABLE | Current daily time limit at Perth casino |
| Per_CurrentDailyNetLossLimit | NUMERIC | NULLABLE | Current daily net loss limit at Perth casino |
| Per_AnnualLossLimit | NUMERIC | NULLABLE | Annual loss limit at Perth casino |
| Alt_SignupDate | DATETIME | NULLABLE | Alternative signup date |
| HostEmployeeId | STRING | NULLABLE | Current host employee ID |
| HostEmployeeFirstName | STRING | NULLABLE | Current host employee first name |
| HostEmployeeLastName | STRING | NULLABLE | Current host employee last name |
| Syd_Class | STRING | NULLABLE | Classification at Sydney casino |
| VisitAcknowledgementStatus | STRING | NULLABLE | Status of visit acknowledgement |
| CountryOfBirthCode | STRING | NULLABLE | Code for country of birth |
| CountryOfBirth | STRING | NULLABLE | Name of country of birth |
| CitizenshipCodes | STRING | NULLABLE | Codes for citizenship(s) |
| Citizenships | STRING | NULLABLE | Description of citizenship(s) |
