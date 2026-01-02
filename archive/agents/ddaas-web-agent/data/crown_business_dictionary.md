
# Data Model : Patrons
Path :  ddaastransformdev.AV_PATRON.av_PatronCurrent
Description : contains crown patrons information, only show active patrons (activeflag = 'Y')


# Data Model: Ratings
Path : ddaastransformdev.AI_MODELS.vw_Ratings
Description : Returns patron gaming ratings

Always Use gamingDatemonth in queries. This value has to be the first day of each month

Foreign Key : PatronId (Patrons Model)


# Crown Business Dictionary

| Term | Definition | Example |
|------|------------|---------|
| Tier | loyalty reward Tiers  | MEMBER, SILVER, GOLD, PLATINUM (OR PLAT), BLACK , VIP |
| Patron | customer, player are all interchangable terms, identified by their patronid |  |
| Ratings | a player's gaming or non-gaming ratings  |  |
| Risk Ratings | Risk rating assigned to a player | HIGH, MEDIUM, LOW, CRITICAL|
| PROPERTYID | Location of the crown property, can be one of the following 1 = MELBOURNE , 2 = PERTH , 3 = SYDNEY|
| SITEID | Location of the crown site, can be one of the following 1 = MELBOURNE , 2 = PERTH , 3 = SYDNEY|

