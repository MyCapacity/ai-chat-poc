# Ratings model data schema

| Field Name | Type | Mode | Description |
|------------|------|------|-------------|
| Property | STRING | NULLABLE | Name or identifier of the casino property |
| PatronId | INTEGER | NULLABLE | Unique identifier for the casino patron/player |
| SignupPropertyid | INTEGER | NULLABLE | ID of the property where the patron initially signed up |
| GamingDate | DATE | NULLABLE | Date when the gaming activity occurred |
| GamingDateMonth | DATE | NULLABLE | First day of the month for the gaming activity (used for partitioning) |
| CasinoLocationDescription | STRING | NULLABLE | Name or description of the specific casino location |
| GameName | STRING | NULLABLE | Name of the specific game played |
| GamingActivityCode | STRING | NULLABLE | Code identifying the type of gaming activity |
| GamingProductType | STRING | NULLABLE | Category or type of gaming product (e.g., slots, table games) |
| ActualWin | NUMERIC | NULLABLE | Actual amount won by the patron |
| turnover | NUMERIC | NULLABLE | Total amount wagered by the patron |
| buyin | NUMERIC | NULLABLE | Amount of money initially purchased for gaming |
| AverageBet | NUMERIC | NULLABLE | Average amount bet per game or session |
| TheoreticalWin | NUMERIC | NULLABLE | Expected win amount based on game odds |
| GrossRevenue | NUMERIC | NULLABLE | Total revenue generated from the gaming activity |
| NetRevenue | NUMERIC | NULLABLE | Revenue after deductions and adjustments |
| PointsEarned | INTEGER | NULLABLE | Loyalty points earned during the gaming session |
| SecondsPLayed | FLOAT | NULLABLE | Duration of play in seconds |

