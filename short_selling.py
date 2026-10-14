# -*- coding: utf-8 -*-
"""
Created on Wed Oct 14 11:40:21 2026

@author: Radhey
"""

import datetime
from decimal import Decimal
from random import randint, uniform, choice


# Existing classes and methods remain the same
class Order:
    def __init__(self, order_id, security_id, quantity, price, order_type,
                 min_loan_period=None, max_borrow_fee=None, expiry=None,
                 available=True):
        self.order_id = order_id
        self.security_id = security_id
        self.quantity = quantity
        self.price = price
        self.order_type = order_type
        self.min_loan_period = min_loan_period
        self.max_borrow_fee = max_borrow_fee
        self.expiry = expiry
        self.available = available
        self.timestamp = datetime.datetime.now()


class Wallet:
    def __init__(self, cash):
        self.cash = Decimal(cash)
        self.stocks = {}
        self.loans = []

    def has_sufficient_cash(self, required_cash):
        return self.cash >= required_cash

    def update_cash(self, amount):
        self.cash += Decimal(amount)

    def update_stock(self, security_id, quantity):
        if security_id in self.stocks:
            self.stocks[security_id] += quantity
        else:
            self.stocks[security_id] = quantity


class ShortSellingEngine:
    def __init__(self, wallet):
        self.orders = []
        self.borrow_records = []
        self.auction_engine = AuctionEngine()
        self.wallet = wallet
        self.transactions = []

    def add_order(self, order: Order):
        self.orders.append(order)

    def process_orders(self):
        active_short_sells = [
            order for order in self.orders
            if order.available and order.order_type == "SHORT_SELL"
        ]

        active_lend_orders = [
            order for order in self.orders
            if order.available and order.order_type == "LEND"
        ]

        for order in active_short_sells:
            required_cash = (
                Decimal(order.price)
                * Decimal(order.quantity)
                * Decimal(0.10)
            )  # 10% margin

            if not self.wallet.has_sufficient_cash(required_cash):
                self.notify_short_seller(order)
                continue

            self.wallet.update_cash(-required_cash)

            eligible_lend_orders = [
                lend for lend in active_lend_orders
                if lend.quantity <= self.wallet.stocks.get(lend.security_id, 0)
                and lend.security_id == order.security_id
            ]

            lend_groups = {}
            for lend in eligible_lend_orders:
                key = (lend.max_borrow_fee, lend.min_loan_period)

                if key not in lend_groups:
                    lend_groups[key] = []

                lend_groups[key].append(lend)

            borrow_groups = {}
            for sell in active_short_sells:
                key = (sell.max_borrow_fee, sell.min_loan_period)

                if key not in borrow_groups:
                    borrow_groups[key] = []

                borrow_groups[key].append(sell)

            lend_keys = sorted(lend_groups.keys(), reverse=True)
            borrow_keys = sorted(borrow_groups.keys(), reverse=True)

            for borrow_key in borrow_keys:
                for lend_key in lend_keys:
                    if lend_key[1] >= borrow_key[1]:  # Loan period check
                        lend_orders = lend_groups[lend_key]
                        borrow_orders = borrow_groups[borrow_key]

                        for lend_order in lend_orders:
                            for borrow_order in borrow_orders:
                                if lend_order.quantity > 0 and borrow_order.quantity > 0:
                                    quantity_traded = min(
                                        lend_order.quantity,
                                        borrow_order.quantity
                                    )

                                    lend_order.quantity -= quantity_traded
                                    borrow_order.quantity -= quantity_traded

                                    self.wallet.update_stock(
                                        lend_order.security_id,
                                        -quantity_traded
                                    )

                                    self.wallet.update_cash(
                                        quantity_traded * lend_order.price
                                    )

                                    self.wallet.loans.append((
                                        lend_order.security_id,
                                        quantity_traded,
                                        lend_key[0],
                                        lend_key[1]
                                    ))

                                    transaction_price = lend_order.price

                                    # Record the transaction details
                                    self.transactions.append({
                                        'security_id': lend_order.security_id,
                                        'quantity': quantity_traded,
                                        'price': transaction_price,
                                        'fee': lend_key[0],
                                        'duration': lend_key[1],
                                    })

                                    print(
                                        f"Traded {quantity_traded} shares of "
                                        f"{lend_order.security_id} at price "
                                        f"{transaction_price}"
                                    )

                                    print(
                                        f"Lend record created for "
                                        f"{lend_order.security_id}, "
                                        f"quantity: {quantity_traded}"
                                    )

                                    print(
                                        f"Borrow record created for "
                                        f"{borrow_order.security_id}, "
                                        f"quantity: {quantity_traded}"
                                    )

    def notify_short_seller(self, order: Order):
        print(
            f"Notify short seller: Order ID {order.order_id} "
            f"has insufficient cash"
        )


class AuctionEngine:
    def route_order(self, order: Order):
        print(f"Routing order ID {order.order_id} to auction engine")

    def complete_auction(self):
        print("Auction completed")


# Generate random orders with different price ranges for different security IDs
def generate_random_orders(num_orders):
    orders = []

    securities = {
        "AAPL": (90, 110),
        "MSFT": (520, 540),
        "GOOGL": (2100, 2250),
        "AMZN": (999, 1010),
        "TSLA": (95, 102),
        "NFLX": (450, 470),
        "FB": (270, 280),
        "NVDA": (150, 160),
    }

    order_types = ["SHORT_SELL", "LEND"]

    for i in range(1, num_orders + 1):
        order_type = choice(order_types)
        security_id = choice(list(securities.keys()))
        quantity = randint(1000, 20000)
        price_range = securities[security_id]

        price = round(
            Decimal(uniform(*price_range)),
            2
        )

        min_loan_period = randint(5, 10)

        max_borrow_fee = round(
            Decimal(uniform(0.01, 0.1)),
            2
        )

        expiry = "10 minutes"

        order = Order(
            order_id=i,
            security_id=security_id,
            quantity=quantity,
            price=price,
            order_type=order_type,
            min_loan_period=min_loan_period,
            max_borrow_fee=max_borrow_fee,
            expiry=expiry
        )

        orders.append(order)

    return orders


# Sample wallet
wallet = Wallet(cash=Decimal('1000000'))

wallet.update_stock("AAPL", 15000)
wallet.update_stock("MSFT", 10000)
wallet.update_stock("GOOGL", 12000)
wallet.update_stock("AMZN", 8000)
wallet.update_stock("TSLA", 5000)
wallet.update_stock("NFLX", 7000)
wallet.update_stock("FB", 9000)
wallet.update_stock("NVDA", 6000)


# Create an instance of ShortSellingEngine
short_engine = ShortSellingEngine(wallet)


# Generate 100 random orders and add them to the engine
random_orders = generate_random_orders(10)

for order in random_orders:
    short_engine.add_order(order)


# Display the generated orders
print("\nGenerated Orders:")

for order in random_orders:
    print(
        f"Order ID: {order.order_id}, "
        f"Security ID: {order.security_id}, "
        f"Quantity: {order.quantity}, "
        f"Price: {order.price}, "
        f"Order Type: {order.order_type}, "
        f"Min Loan Period: {order.min_loan_period}, "
        f"Max Borrow Fee: {order.max_borrow_fee}, "
        f"Expiry: {order.expiry}"
    )


# Process the orders
short_engine.process_orders()


# Display the transaction details
print("\nTransactions")

for transaction in short_engine.transactions:
    print(
        f"Security ID: {transaction['security_id']}, "
        f"Quantity: {transaction['quantity']}, "
        f"Price: {transaction['price']}, "
        f"Fee: {transaction['fee']}, "
        f"Duration: {transaction['duration']}"
    )