# Data Sources

### Financial Institutions & Vendors

Capital One
- Checking + Credit Cards + Savings
- CSV downloads available
- PDFs monthly
- Can export 25 months in past up to one year per download (Credit)
- Can download checking & savings transactions from past two years

Amazon
- Order history & subscriptions
- CSVs available
- Data request fulfilled with lengthy SLA 1-2 weeks
  - Maybe option to convert to business account for better reports
- Contains all historical data from creation of account-10 years+
---
### File Formats 
- CSV
  - Clean 
- PDF
  - Statements mostly
  - No multi-account PDFs, each account can produce it's own statment PDFs
  - Amazon reports are thorough but must be requested via data request
---
### Expected Transaction Fields
Capital One Credit
- Transaction Date	
- Posted Date	
- Card No.	
- Description	
- Category	
- Debit	
- Credit
Capital One Checking/Savings
- Account Number	
- Transaction Date	
- Transaction Amount	
- Transaction Type	
- Transaction Description	
- Balance

Amazon
- Website	
- Order ID	
- Order Date	
- Purchase Order Number	
- Currency	
- Unit Price	
- Unit Price Tax	
- Shipping Charge	
- Total Discounts	
- Total Owed	
- Shipment Item Subtotal	
- Shipment Item Subtotal Tax	
- ASIN	
- Product Condition	Quantity	
- Payment Instrument Type	
- Order Status	
- Shipment Status	
- Ship Date	
- Shipping Option	
- Shipping Address	
- Billing Address	
- Carrier Name & Tracking Number	
- Product Name	
- Gift Message	
- Gift Sender Name	
- Gift Recipient Contact Details	
- Item Serial Number

Categories don't seem to change too often & some of the Amazon reports will have some noise

---
### Volume & History
- \# of accounts: Approx. 6, more vendors/banks/cards to be added later on
- One credit card is primary account and will have roughly 100-200 transactions per month
- Amazon will have payments from credit accounts I'm not even tracking nor own, but will strongly correlate with main credit card
- Will have data from past 2 years approx., unless banks can provide reports from further back
---
### Non-Bank Inputs
- Aformentioned Amazon reports will be critical as it is one of the main vendors (Must Have)
- Receipts (photos or PDFs) (Must Have)
- Cash Transactions (Manual) (Future)
- Spending Tracking (Future)
---
### Constraints & Red Lines
- Local first
- Self-hosted MVP
- Cloud future, but must take encryption and secure approach