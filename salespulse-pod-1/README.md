SalesPulse – Retail Sales Analytics
1. Project Overview
SalesPulse is a small retail sales analytics application developed in Python using Pandas. It analyses a store's sales dataset to understand revenue, valid orders, product performance, regional performance, and data quality.

The application answers these business questions:
- How much revenue did the store generate?
- How many valid orders were received?
- What is the Average Order Value (AOV)?
- Which products generate the highest revenue?
- Which product has the highest quantity sold?
- Which region performs best?
- Which records must be excluded from the analysis?
2. Technologies
- Python 3
- Pandas
- CSV dataset
Install the dependency:
python -m pip install pandas
3. Project Structure
salespulse-pod-1/
├── README.md
├── data/
│   └── sales.csv
├── src/
│   ├── validation.py
│   ├── revenue.py
│   ├── product_analysis.py
│   ├── region_analysis.py
│   └── main.py
├── tests/
│   └── test-cases.md
├── valid_sales.csv
├── invalid_sales.csv
└── sales_report.txt
The Python module names above follow the code used by the project. The three output files are generated when the application runs.
4. Input Dataset
The input file is data/sales.csv. The dataset contains sales information such as Order ID, order date, product name, category, region, quantity, unit price, and unit cost.

The validation module requires these columns:
- OrderID
- ProductName
- Region
- Quantity
- UnitPrice
- UnitCost
5. Data Validation
The application checks sales records for:
- Missing Order IDs.
- Zero or negative quantities.
- Zero or negative unit prices.
- Negative unit costs.
- Missing product names.
- Missing regions.
- Duplicate Order IDs.
Invalid records are not silently deleted. The validation process separates valid and invalid records, adds a ValidationReason to invalid rows, and reports the number of invalid records and the reasons.

For duplicate Order IDs, the current validator flags every row belonging to a duplicated ID. Therefore, the duplicate reason count represents rows flagged, not necessarily the number of distinct duplicate IDs.

A unit cost greater than the unit price can represent a loss-making order. It should not be rejected only because it creates a negative gross profit. The current validation rule rejects negative unit costs; it does not list UnitCost > UnitPrice as an invalid condition.
6. Sales Metrics
The application calculates:
Metric	Formula
Total Revenue	Quantity × UnitPrice, summed across valid rows
Total Valid Orders	Number of valid rows
Average Order Value (AOV)	Total Revenue ÷ Total Valid Orders
Total Quantity Sold	Sum of valid quantities
Estimated Gross Profit	Quantity × (UnitPrice − UnitCost), summed across valid rows


For this assignment, each valid row represents one order.
7. Product Analysis
The application:
- Calculates revenue for each product.
- Displays the top five products by revenue.
- Identifies the product with the highest total quantity sold.
8. Regional Analysis
The application calculates revenue, estimated gross profit, and order count for each region, then identifies the region with the highest revenue.
9. How to Run
Open PowerShell in the project root folder (the folder containing data and src) and run:
python src/main.py
This is the command used for the execution results documented below. Make sure data/sales.csv exists and the required Python modules are inside src.
10. Generated Files
File	Description
valid_sales.csv	Sales records accepted by validation
invalid_sales.csv	Rejected records, including their validation reasons
sales_report.txt	Final text report containing data quality, sales metrics, product and regional analysis, insights, and recommendations


11. Results From the 120-Record Dataset Run
The following values are taken from the execution output supplied for this project.
Data Quality
Metric	Result
Total records	120
Valid records	108
Invalid records	12


Invalid-record reasons reported:
Reason	Rows flagged
Zero or negative Quantity	2
Duplicate Order ID	4
Zero or negative UnitPrice	2
Missing Product Name	1
Missing Region	1
Negative UnitCost	1
Missing Order ID	1


Overall Sales Metrics
Metric	Result
Total revenue	₹23,47,050.00
Total valid orders	108
Average Order Value	₹21,731.94
Total quantity sold	401
Estimated gross profit	₹5,34,850.00
Gross profit margin	22.79%


Top Five Products by Revenue
Rank	Product	Revenue
1	Laptop	₹11,43,000
2	Monitor	₹2,64,100
3	Office Chair	₹2,17,700
4	External SSD	₹1,91,600
5	Mechanical Keyboard	₹1,68,100


The product with the highest quantity sold was Mechanical Keyboard, with 60 units.
Regional Performance
Region	Revenue	Estimated Gross Profit	Valid Orders
West	₹6,51,350	₹1,46,100	28
North	₹5,95,900	₹1,30,050	27
South	₹5,68,000	₹1,45,100	30
East	₹5,31,800	₹1,13,600	23


The highest-revenue region was West.
12. Business Insights
Based on the reported results:
1. Laptop is the leading revenue product, generating ₹11,43,000.
2. Mechanical Keyboard has the highest sales volume, with 60 units sold.
3. West is the strongest region by revenue, generating ₹6,51,350.
4. The overall estimated gross profit margin is 22.79%.
13. Recommendations
1. Maintain sufficient stock of Laptop because it contributes the highest product revenue.
2. Study West's sales performance and identify practices that could help improve revenue in the other regions.
14. GitHub Collaboration
The pod uses one shared GitHub repository managed by the Pod Lead.

Suggested workflow:
1. The Pod Lead creates the repository and invites pod members as collaborators.
2. Each member clones the repository.
3. Each member creates a feature branch for their assigned work.
4. Members commit and push their changes to their own branches.
5. Members create Pull Requests.
6. Another member reviews each Pull Request.
7. The Pod Lead coordinates merging approved changes into main.
Suggested branch names:
- feature/data-validation
- feature/revenue-metrics
- feature/product-analysis
- feature/region-analysis
- feature/integration-report
Do not push all work directly to main.
15. Testing
The required scenarios and expected behaviour are documented in [`tests/test-cases.md`](tests/test-cases.md). The test document separates expected outcomes from actual results; a test should be marked Passed only after it has been executed and verified.
