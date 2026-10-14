# -*- coding: utf-8 -*-
"""
Created on Wed Oct 14 11:45:59 2026

@author: Radhey
"""

import random
from datetime import datetime, timedelta
from statistics import median


class MarginFinance:
    def __init__(self, finance_provider, trading_wallets, margin_wallets, auction_engines):
        self.finance_provider = finance_provider
        self.trading_wallets = trading_wallets
        self.margin_wallets = margin_wallets
        self.auction_engines = auction_engines

    def process_buy_orders(self, buy_orders, initial_auction_prices):
        auction_prices = [initial_auction_prices]

        for auction_index in range(len(self.auction_engines)):
            auction_timeframe = f"{(auction_index * 10)} to {(auction_index + 1) * 10} minutes"

            print(f"\nProcessing Auction {auction_index} ({auction_timeframe})")

            self.process_auction(
                auction_index,
                buy_orders,
                auction_prices[-1]
            )

            if auction_index < len(self.auction_engines) - 1:
                next_auction_prices = self.calculate_next_auction_prices(
                    auction_index
                )

                auction_prices.append(next_auction_prices)

                print(
                    f"Auction {auction_index} Tick Prices: "
                    f"{next_auction_prices}"
                )

    def process_auction(self, auction_index, buy_orders, auction_prices):
        auction_engine = self.auction_engines[auction_index]

        auction_orders = [
            order for order in buy_orders
            if order['auction_index'] == auction_index
        ]

        for order in auction_orders:
            self.process_order(
                order,
                auction_prices,
                auction_engine
            )

        buy_orders[:] = [
            order for order in buy_orders
            if order not in auction_orders
        ]

        # Display orders for the auction
        print(f"Orders in Auction {auction_index}:")

        for order in auction_orders:
            print(
                f"Order ID: {order['id']}, "
                f"Timestamp: {order['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}, "
                f"Wallet ID: {order['wallet_id']}, "
                f"Quantity: {order['quantity']}, "
                f"Price: {order['price']}, "
                f"Final Price: {order['final_price']}"
            )

        print(f"Transactions in Auction {auction_index}:")

        for transaction in auction_engine['transactions']:
            print(
                f"Order ID: {transaction['order_id']}, "
                f"Timestamp: {transaction['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}, "
                f"Final Price: {transaction['final_price']}, "
                f"Total Cost: {transaction['total_cost']}"
            )

    def process_order(self, order, auction_prices, auction_engine):
        order['timestamp'] = datetime.now()

        # Determine the final price for margin finance wallet orders
        if order['wallet_id'].startswith('M') and isinstance(order['price'], str):

            if order['price'] == 'average':
                order['final_price'] = auction_prices[
                    'Average Tick Price Buy Order - Margin Financed'
                ]

            elif order['price'] == 'lowest':
                order['final_price'] = auction_prices[
                    'Lowest Tick Price Buy Order - Margin Financed'
                ]

            elif order['price'] == 'highest':
                order['final_price'] = auction_prices[
                    'Highest Tick Price Buy Order - Margin Financed'
                ]

            elif order['price'] == 'median':
                order['final_price'] = auction_prices[
                    'Median Tick Price Buy Order - Margin Financed'
                ]

        else:
            order['final_price'] = order['price']

        order_cost = order['quantity'] * order['final_price']

        if order['wallet_id'].startswith('T'):
            trading_wallet = self.trading_wallets[order['wallet_id']]

            if trading_wallet['cash'] >= order_cost:
                self.route_to_trading_engine(
                    order,
                    order_cost,
                    auction_engine
                )

            else:
                margin_required = order_cost - trading_wallet['cash']

                if margin_required > 0:
                    if self.is_sufficient_cash_in_facility(margin_required):
                        self.transfer_funds_from_provider(
                            order,
                            order_cost,
                            trading_wallet
                        )

                        self.route_to_auction_engine(
                            order,
                            order_cost,
                            auction_engine
                        )

                    else:
                        self.reject_order(order)

                else:
                    self.reject_order(order)

        elif order['wallet_id'].startswith('M'):
            if order_cost > self.margin_wallets[order['wallet_id']]['cash']:
                margin_required = (
                    order_cost
                    - self.margin_wallets[order['wallet_id']]['cash']
                )

                if self.is_sufficient_cash_in_facility(margin_required):
                    self.finance_provider['available_cash'] -= margin_required

                    self.margin_wallets[
                        order['wallet_id']
                    ]['cash'] += margin_required

                    self.margin_wallets[
                        order['wallet_id']
                    ]['debt'] += margin_required

                else:
                    self.reject_order(order)
                    return

            self.route_to_auction_engine(
                order,
                order_cost,
                auction_engine
            )

    def is_sufficient_cash_in_facility(self, margin_required):
        return (
            self.finance_provider['available_cash']
            >= margin_required
        )

    def transfer_funds_from_provider(self, order, order_cost, trading_wallet):
        margin_required = order_cost - trading_wallet['cash']

        if self.finance_provider['available_cash'] >= margin_required:
            self.finance_provider['available_cash'] -= margin_required

            margin_wallet_id = 'M' + order['wallet_id'][1:]

            self.margin_wallets[
                margin_wallet_id
            ]['cash'] += margin_required

            self.margin_wallets[
                margin_wallet_id
            ]['debt'] += margin_required

        else:
            self.reject_order(order)

    def route_to_trading_engine(self, order, order_cost, auction_engine):
        auction_engine['orders'].append(order)

        auction_engine['transactions'].append({
            'order_id': order['id'],
            'final_price': order['final_price'],
            'total_cost': order_cost,
            'timestamp': order['timestamp']
        })

        self.trading_wallets[
            order['wallet_id']
        ]['cash'] -= order_cost

        self.trading_wallets[
            order['wallet_id']
        ]['securities'].append({
            'type': order['type'],
            'quantity': order['quantity']
        })

        if self.trading_wallets[order['wallet_id']]['cash'] < 0:
            self.trading_wallets[
                order['wallet_id']
            ]['debt'] += abs(
                self.trading_wallets[order['wallet_id']]['cash']
            )

            self.trading_wallets[
                order['wallet_id']
            ]['cash'] = 0

    def route_to_auction_engine(self, order, order_cost, auction_engine):
        auction_engine['orders'].append(order)

        auction_engine['transactions'].append({
            'order_id': order['id'],
            'final_price': order['final_price'],
            'total_cost': order_cost,
            'timestamp': order['timestamp']
        })

        if order['wallet_id'].startswith('T'):
            trading_wallet_cash = self.trading_wallets[
                order['wallet_id']
            ]['cash']

            margin_wallet_id = 'M' + order['wallet_id'][1:]

            self.margin_wallets[
                margin_wallet_id
            ]['cash'] -= (order_cost - trading_wallet_cash)

            self.trading_wallets[
                order['wallet_id']
            ]['cash'] = 0

            self.margin_wallets[
                margin_wallet_id
            ]['securities'].append({
                'type': order['type'],
                'quantity': order['quantity']
            })

            if self.margin_wallets[margin_wallet_id]['cash'] < 0:
                self.margin_wallets[
                    margin_wallet_id
                ]['debt'] += abs(
                    self.margin_wallets[margin_wallet_id]['cash']
                )

                self.margin_wallets[
                    margin_wallet_id
                ]['cash'] = 0

        elif order['wallet_id'].startswith('M'):
            self.margin_wallets[
                order['wallet_id']
            ]['cash'] -= order_cost

            self.margin_wallets[
                order['wallet_id']
            ]['securities'].append({
                'type': order['type'],
                'quantity': order['quantity']
            })

            if self.margin_wallets[order['wallet_id']]['cash'] < 0:
                self.margin_wallets[
                    order['wallet_id']
                ]['debt'] += abs(
                    self.margin_wallets[order['wallet_id']]['cash']
                )

                self.margin_wallets[
                    order['wallet_id']
                ]['cash'] = 0

    def reject_order(self, order):
        print(
            f"Order rejected: {order['id']}. Notify buyer."
        )

    def calculate_next_auction_prices(self, auction_index):
        transactions = self.auction_engines[
            auction_index
        ]['transactions']

        if not transactions:
            return {}

        prices = [
            tx['final_price']
            for tx in transactions
        ]

        next_auction_prices = {
            'Average Tick Price Buy Order - Margin Financed': sum(prices) / len(prices),
            'Highest Tick Price Buy Order - Margin Financed': max(prices),
            'Lowest Tick Price Buy Order - Margin Financed': min(prices),
            'Median Tick Price Buy Order - Margin Financed': median(prices)
        }

        return next_auction_prices


# Generate random buy orders
def generate_buy_orders(
    num_orders,
    trading_wallet_ids,
    margin_wallet_ids,
    order_types,
    price_range,
    quantity_range
):
    buy_orders = []

    for i in range(num_orders):
        wallet_id = random.choice(
            trading_wallet_ids + margin_wallet_ids
        )

        auction_index = random.randint(0, 2)

        price = (
            random.choice([
                'average',
                'lowest',
                'highest',
                'median'
            ])
            if wallet_id.startswith('M') and auction_index > 0
            else round(random.uniform(*price_range), 2)
        )

        order = {
            'id': i + 1,
            'price': price,
            'quantity': random.randint(*quantity_range),
            'wallet_id': wallet_id,
            'type': random.choice(order_types),
            'auction_index': auction_index
        }

        buy_orders.append(order)

    return buy_orders


# Generate wallets
def generate_wallets(num_wallets, cash_range, prefix):
    wallets = {}

    for i in range(num_wallets):
        wallet_id = f"{prefix}{i + 1}"

        wallets[wallet_id] = {
            'cash': random.randint(*cash_range),
            'securities': [],
            'debt': 0
        }

    return wallets


# -----------------------------------------------------
# SAMPLE SIMULATION SETUP
# This section is reconstructed because the screenshots
# stop before the original execution setup.
# -----------------------------------------------------

# Finance provider
finance_provider = {
    'available_cash': 10000000
}

# Generate trading wallets
trading_wallets = generate_wallets(
    num_wallets=10,
    cash_range=(10000, 100000),
    prefix='T'
)

# Generate margin wallets
margin_wallets = generate_wallets(
    num_wallets=10,
    cash_range=(5000, 50000),
    prefix='M'
)

# Create auction engines
auction_engines = [
    {
        'orders': [],
        'transactions': []
    }
    for _ in range(3)
]

# Initial auction prices
initial_auction_prices = {
    'Average Tick Price Buy Order - Margin Financed': 100,
    'Highest Tick Price Buy Order - Margin Financed': 110,
    'Lowest Tick Price Buy Order - Margin Financed': 90,
    'Median Tick Price Buy Order - Margin Financed': 100
}

# Generate buy orders
buy_orders = generate_buy_orders(
    num_orders=30,
    trading_wallet_ids=list(trading_wallets.keys()),
    margin_wallet_ids=list(margin_wallets.keys()),
    order_types=['BUY'],
    price_range=(90, 110),
    quantity_range=(10, 100)
)

# Initialize Margin Finance Engine
margin_finance = MarginFinance(
    finance_provider,
    trading_wallets,
    margin_wallets,
    auction_engines
)

# Display initial balances
print("\nInitial Trading Wallet Balances:")

for wallet_id, wallet in trading_wallets.items():
    print(
        f"Wallet ID: {wallet_id}, "
        f"Cash: {wallet['cash']}, "
        f"Debt: {wallet['debt']}"
    )

print("\nInitial Margin Wallet Balances:")

for wallet_id, wallet in margin_wallets.items():
    print(
        f"Wallet ID: {wallet_id}, "
        f"Cash: {wallet['cash']}, "
        f"Debt: {wallet['debt']}"
    )

print(
    f"\nInitial Finance Provider Available Cash: "
    f"{finance_provider['available_cash']}"
)

# Process buy orders through the auctions
margin_finance.process_buy_orders(
    buy_orders,
    initial_auction_prices
)

# Display final trading wallet balances
print("\nFinal Trading Wallet Balances:")

for wallet_id, wallet in trading_wallets.items():
    print(
        f"Wallet ID: {wallet_id}, "
        f"Cash: {wallet['cash']}, "
        f"Debt: {wallet['debt']}, "
        f"Securities: {wallet['securities']}"
    )

# Display final margin wallet balances
print("\nFinal Margin Wallet Balances:")

for wallet_id, wallet in margin_wallets.items():
    print(
        f"Wallet ID: {wallet_id}, "
        f"Cash: {wallet['cash']}, "
        f"Debt: {wallet['debt']}, "
        f"Securities: {wallet['securities']}"
    )

# Display final finance provider balance
print(
    f"\nFinal Finance Provider Available Cash: "
    f"{finance_provider['available_cash']}"
)

# Display total transactions
total_transactions = sum(
    len(auction['transactions'])
    for auction in auction_engines
)

print(f"\nTotal Transactions: {total_transactions}")

print("\nAll auctions completed.")