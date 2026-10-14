# -*- coding: utf-8 -*-
"""
Created on Wed Oct 14 11:39:20 2026

@author: Radhey
"""

import random


class CorporateActionsEngine:
    def __init__(self, issuer_wallet, trading_wallets, margin_wallets, shorting_engine):
        self.issuer_wallet = issuer_wallet
        self.trading_wallets = trading_wallets
        self.margin_wallets = margin_wallets
        self.shorting_engine = shorting_engine

    def process_dividend_payment(self, dividend_rate, dividend_date, tax_status):
        # Step 1: Announce the dividend date and time
        self.announce_dividend(dividend_date)

        # Step 2: Issuer transfers funds to issuer wallet
        if not self.transfer_funds_to_issuer_wallet(dividend_rate):
            self.notify_issuer("Insufficient funds in Issuer's bank account.")
            return

        # Step 3: Issuer inputs dividend instructions
        total_shares = self.calculate_total_shares()
        required_funds = total_shares * dividend_rate

        if self.issuer_wallet['cash'] < required_funds:
            self.notify_issuer("Insufficient funds in Issuer's wallet to pay dividends.")
            return

        # Step 4: Corporate actions engine checks for sufficient funds
        self.suspend_auctions()

        # Step 5: Handle manufactured dividends for shorted stocks
        self.shorting_engine.process_manufactured_dividends(dividend_rate)

        # Step 6: Transfer funds to relevant wallets and notify holders
        self.distribute_dividends(dividend_rate, tax_status)
        self.resume_auctions()

        # Print final balances
        self.print_final_balances()

    def announce_dividend(self, dividend_date):
        print(f"Dividend date and time announced: {dividend_date}")

    def transfer_funds_to_issuer_wallet(self, dividend_rate):
        # Simulating fund transfer from issuer's bank account to issuer wallet
        issuer_bank_balance = 1000000  # Example balance
        transfer_amount = self.calculate_total_shares() * dividend_rate

        if issuer_bank_balance >= transfer_amount:
            self.issuer_wallet['cash'] += transfer_amount
            print("Funds transferred from Issuer's bank account to Issuer's wallet.")
            return True
        else:
            return False

    def calculate_total_shares(self):
        total_shares = sum(wallet['shares'] for wallet in self.trading_wallets + self.margin_wallets)
        return total_shares

    def notify_issuer(self, message):
        print(f"Notification to Issuer: {message}")

    def suspend_auctions(self):
        print("Auctions suspended for dividend payment.")

    def resume_auctions(self):
        print("Auctions resumed after dividend payment.")

    def distribute_dividends(self, dividend_rate, tax_status):
        for wallet in self.trading_wallets + self.margin_wallets:
            dividend = wallet['shares'] * dividend_rate
            net_dividend = self.apply_tax(dividend, tax_status)
            wallet['cash'] += net_dividend

            print(
                f"Dividend of {net_dividend} paid to Wallet ID {wallet['id']} "
                f"with {wallet['shares']} shares."
            )

        print("Dividends distributed to all relevant wallets.")

    def apply_tax(self, dividend, tax_status):
        tax_rate = 0.15 if tax_status == 'taxable' else 0.0
        return dividend * (1 - tax_rate)

    def print_final_balances(self):
        print("\nFinal Balances:")

        for wallet in self.trading_wallets:
            print(
                f"Trading Wallet ID {wallet['id']}: "
                f"Cash: {wallet['cash']}, Shares: {wallet['shares']}"
            )

        for wallet in self.margin_wallets:
            print(
                f"Margin Wallet ID {wallet['id']}: "
                f"Cash: {wallet['cash']}, Shares: {wallet['shares']}"
            )

        print(f"Issuer Wallet: Cash: {self.issuer_wallet['cash']}")


class ShortingEngine:
    def __init__(self, short_positions):
        self.short_positions = short_positions

    def process_manufactured_dividends(self, dividend_rate):
        for position in self.short_positions:
            manufactured_dividend = position['borrowed_shares'] * dividend_rate

            net_dividend = self.apply_tax(
                manufactured_dividend,
                position['borrower_tax_status']
            )

            position['borrower_wallet']['cash'] -= net_dividend
            position['lender_wallet']['cash'] += net_dividend

            print(
                f"Manufactured dividend of {net_dividend} transferred from "
                f"borrower ID {position['borrower_wallet']['id']} "
                f"to lender ID {position['lender_wallet']['id']}."
            )

    def apply_tax(self, dividend, tax_status):
        tax_rate = 0.15 if tax_status == 'taxable' else 0.0
        return dividend * (1 - tax_rate)


# Generate sample wallets
def generate_wallets(num_wallets):
    wallets = []

    for i in range(num_wallets):
        wallet = {
            'id': i + 1,
            'shares': random.randint(10, 1000),
            'cash': random.randint(1000, 100000)
        }

        wallets.append(wallet)

    return wallets


# Generate short positions
def generate_short_positions(trading_wallets, margin_wallets, num_positions):
    short_positions = []

    for i in range(num_positions):
        borrower_wallet = random.choice(trading_wallets)
        lender_wallet = random.choice(margin_wallets)
        borrowed_shares = random.randint(10, 50)

        short_position = {
            'id': i + 1,
            'borrowed_shares': borrowed_shares,
            'borrower_wallet': borrower_wallet,
            'lender_wallet': lender_wallet,
            'borrower_tax_status': 'taxable'  # For simplicity, all borrowers are taxable
        }

        short_positions.append(short_position)

    return short_positions


# Example usage with n wallets and m short positions
num_wallets = 100
num_short_positions = 10

issuer_wallet = {'cash': 0}

trading_wallets = generate_wallets(num_wallets // 2)
margin_wallets = generate_wallets(num_wallets // 2)

short_positions = generate_short_positions(
    trading_wallets,
    margin_wallets,
    num_short_positions
)

shorting_engine = ShortingEngine(short_positions)

corporate_actions_engine = CorporateActionsEngine(
    issuer_wallet,
    trading_wallets,
    margin_wallets,
    shorting_engine
)


# Print initial balances
print("Initial Balances:")

for wallet in trading_wallets:
    print(
        f"Trading Wallet ID {wallet['id']}: "
        f"Cash: {wallet['cash']}, Shares: {wallet['shares']}"
    )

for wallet in margin_wallets:
    print(
        f"Margin Wallet ID {wallet['id']}: "
        f"Cash: {wallet['cash']}, Shares: {wallet['shares']}"
    )

print(f"Issuer Wallet: Cash: {issuer_wallet['cash']}")


# Print short positions
print("\nShort Positions:")

for position in short_positions:
    print(
        f"Short Position ID {position['id']}: "
        f"Borrower Wallet ID {position['borrower_wallet']['id']}, "
        f"Lender Wallet ID {position['lender_wallet']['id']}, "
        f"Borrowed Shares: {position['borrowed_shares']}"
    )


# Process a dividend payment with a rate of 2 per share
dividend_rate = 2
dividend_date = '2024-06-30'
tax_status = 'taxable'

corporate_actions_engine.process_dividend_payment(
    dividend_rate,
    dividend_date,
    tax_status
)