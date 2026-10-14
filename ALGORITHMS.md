
# T-Instant — Algorithm Documentation

## 1. Dutch Auction Simulation

### Objective
To simulate periodic matching of buy and sell orders at compatible prices.

### Workflow
1. Generate simulated buy and sell orders.
2. Validate available cash and stocks.
3. Sort buy orders by descending price.
4. Sort sell orders by ascending price.
5. Match orders when buy price >= sell price.
6. Calculate the transaction quantity.
7. Calculate the transaction price.
8. Update remaining order quantities.
9. Carry unfilled orders into future auctions.
10. Remove orders exceeding the participation limit.

### Pricing Formula

Transaction Price = (Buy Price + Sell Price) / 2

Transaction Quantity = min(Buy Quantity, Sell Quantity)

### Outputs
- Matched transactions
- Transaction quantities
- Average transaction price
- Remaining order backlog

---

## 2. Corporate Actions Simulation

### Objective
To model dividend payments and related wallet operations.

### Workflow
1. Announce the dividend.
2. Check issuer bank funding.
3. Transfer funding into the issuer wallet.
4. Verify dividend requirements.
5. Suspend auctions.
6. Process manufactured dividends.
7. Distribute shareholder dividends.
8. Resume auctions.
9. Report final balances.

### Dividend Formula

Gross Dividend = Shares Held × Dividend Rate

Tax = Gross Dividend × Tax Rate

Net Dividend = Gross Dividend − Tax

The example implementation uses a 15% tax rate
for wallets classified as taxable.

### Outputs
- Shareholder payments
- Manufactured dividend transfers
- Updated wallet cash balances

---

## 3. Short Selling Simulation

### Objective
To explore the matching of securities lending and borrowing requests.

### Workflow
1. Generate short-selling and lending orders.
2. Identify active orders.
3. Check cash margin requirements.
4. Identify eligible lending orders.
5. Group orders by borrowing fee and loan period.
6. Evaluate loan-period compatibility.
7. Match lending and borrowing quantities.
8. Update wallet balances and securities.
9. Record loan and transaction details.

### Margin Formula

Required Margin = Order Price × Quantity × 10%

### Outputs
- Matched securities
- Loan quantities
- Borrowing fee information
- Loan durations
- Updated wallet information

---

## 4. Margin Finance Simulation

### Objective
To simulate financing support for auction-based buy orders.

### Workflow
1. Generate buy orders.
2. Assign orders to auction periods.
3. Calculate order execution prices.
4. Check trading or margin wallet cash balances.
5. Determine financing requirements.
6. Check finance-provider liquidity.
7. Allocate available financing.
8. Route accepted orders to the relevant execution workflow.
9. Record executed transactions.
10. Calculate prices for subsequent auctions.

### Financing Formula

Order Cost = Order Quantity × Final Price

Margin Required = max(0, Order Cost − Available Wallet Cash)

### Tick Price Statistics

Average Price = Sum of Transaction Prices / Number of Transactions

Highest Price = Maximum Transaction Price

Lowest Price = Minimum Transaction Price

Median Price = Median of Transaction Prices

### Outputs
- Auction-level transactions
- Updated cash balances
- Margin debt records
- Finance-provider available cash
- Tick-price statistics

---

## Development Status

These four modules represent independent experimental
implementations.

They are not yet connected through a shared trading
engine, central ledger, or persistent database.

Before production use, the models would require
additional accounting validation, error handling,
testing, risk controls, security review, and
financial-domain verification.
