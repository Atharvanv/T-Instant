
# ⚡ T-Instant
### Algorithmic Trading Infrastructure | Auction-Based Execution & Financial Operations

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Status](https://img.shields.io/badge/Status-Research%20Prototype-orange?style=for-the-badge)
![Algorithms](https://img.shields.io/badge/Algorithms-4-blue?style=for-the-badge)
![Domain](https://img.shields.io/badge/Domain-FinTech-008080?style=for-the-badge)

---

## 📌 Overview

**T-Instant** is a Python-based prototype exploring algorithmic trading infrastructure, periodic auction execution, corporate actions, securities lending, short selling, and margin financing.

The project includes four standalone simulation algorithms designed to explore important processes in a financial trading ecosystem.

The objective is to demonstrate how different financial operations can be represented through transparent, rule-based Python implementations.

> **Project scope:** These algorithms are educational and research prototypes. They are not connected to live exchanges, brokerages, or payment networks.

---

## 🧠 Core Algorithms

| # | Algorithm | Description |
|---|-----------|-------------|
| 01 | Dutch Auction | Periodic order matching, price discovery, and backlog management |
| 02 | Corporate Actions | Dividend processing, tax deductions, and manufactured dividends |
| 03 | Short Selling | Securities lending, borrowing, collateral checks, and order matching |
| 04 | Margin Finance | Financing facilities, wallet funding, and auction-based execution |

---

## 🔹 01 — Dutch Auction Algorithm

**File:** `dutch_auction.py`

Simulates periodic trading auctions using generated buy and sell orders.

### Key Features
- Randomized buy and sell order generation
- Price-priority sorting
- Buy/sell order matching
- Transaction price calculation
- Partial order execution
- Backlog management across auctions
- Automatic removal of expired backlog orders
- Transaction quantity and price reporting

### Auction Simulation
- 3 auctions per day
- 3 simulated trading days
- 9 auctions in total

**Output:** Transaction records, remaining orders, total traded quantity, backlog quantities, and average transaction prices.

---

## 🔹 02 — Corporate Actions Algorithm

**File:** `corporate_actions.py`

Simulates dividend-related corporate actions across trading and margin wallets.

### Key Features
- Dividend announcements
- Issuer fund availability checks
- Dividend funding
- Temporary auction suspension
- Dividend distribution to shareholders
- Configurable taxable and non-taxable treatment
- Manufactured dividend processing for short positions
- Wallet balance reporting

**Output:** Initial balances, dividend events, payment notifications, manufactured dividend transfers, and updated wallet balances.

---

## 🔹 03 — Short Selling Algorithm

**File:** `short_selling.py`

Explores securities borrowing and lending workflows through simulated orders.

### Key Features
- Randomized short-selling and lending orders
- Securities-specific price ranges
- Cash margin verification
- Loan-period compatibility checks
- Lending and borrowing order matching
- Partial order fulfillment
- Loan record creation
- Transaction reporting

**Output:** Generated orders, matched securities-lending transactions, quantities, borrowing fees, and loan durations.

---

## 🔹 04 — Margin Finance Algorithm

**File:** `margin_finance.py`

Explores financing arrangements for buy orders across trading and margin wallets.

### Key Features
- Trading and margin wallet simulation
- Finance-provider liquidity checks
- Margin funding calculations
- Auction-based order processing
- Average, highest, lowest, and median tick-price calculations
- Transaction recording
- Debt and wallet balance updates
- Order rejection when financing is insufficient

**Output:** Auction orders, transaction details, tick-price statistics, wallet balances, financing balances, and transaction counts.

---

## 🏗️ Conceptual Architecture

```text
                     T-INSTANT
                         |
                 Trading Operations
                         |
           +-------------+-------------+
           |                           |
    Auction Execution            Financial Services
           |                           |
     Dutch Auction          +----------+----------+
                            |          |          |
                        Corporate    Short      Margin
                         Actions    Selling     Finance
                            |          |          |
                        Dividends    Lending    Funding
```

Each algorithm is currently implemented as a standalone simulation. The architecture above illustrates their conceptual relationship rather than an implemented integration.

---

## 🛠️ Technology Stack

- **Language:** Python 3
- **Data processing:** Pandas
- **Financial calculations:** Python Decimal
- **Statistical calculations:** Python Statistics
- **Simulation:** Python Random
- **Date and time:** Python Datetime

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/T-Instant.git
cd T-Instant
```

Replace `YOUR_USERNAME` with your GitHub username.

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it:

**Windows**
```powershell
.venv\Scripts\Activate.ps1
```

**macOS / Linux**
```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the algorithms

**Dutch Auction**
```bash
python dutch_auction.py
```

**Corporate Actions**
```bash
python corporate_actions.py
```

**Short Selling**
```bash
python short_selling.py
```

**Margin Finance**
```bash
python margin_finance.py
```

---

## 📊 Simulation Notes

The algorithms use generated sample data rather than live market data.

- Simulation results may differ between executions.
- Wallet balances and prices are illustrative.
- Individual modules are not yet integrated into one trading system.
- Auction behavior and financial operations are simplified.
- The code is not designed for production trading or regulatory compliance.

---

## 🔭 Future Development

Potential future enhancements include:

- Unified trading and wallet architecture
- Integrated order management
- Persistent transaction storage
- Automated testing and validation
- Event-driven auction processing
- Portfolio risk monitoring
- Market data integration
- Performance benchmarking

---

## ⚠️ Disclaimer

T-Instant is a software research and simulation project.

The implementations are intended for educational, experimental, and technical demonstration purposes only.

They should not be used for real-money trading, investment execution, custody, or financial settlement without substantial additional development, validation, security controls, and applicable regulatory review.

---

## 🤝 Contributions

Suggestions, technical discussions, bug reports, and improvements are welcome through GitHub Issues and Pull Requests.

---

### ⚡ T-Instant
**Exploring Auction-Based Trading and Financial Infrastructure Through Python**
