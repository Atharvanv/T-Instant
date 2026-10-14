# -*- coding: utf-8 -*-
"""
Created on Wed Oct 14 11:34:12 2026

@author: Radhey
"""

import random
from datetime import datetime, timedelta
import pandas as pd


def generate_orders(num_orders=3, start_time=None, end_time=None, auction_number=1):
    orders = []

    for i in range(num_orders):
        order_id = f"ORD-A{auction_number:02d}-{i+1:03d}"
        price = round(random.uniform(90, 110), 2)
        quantity = random.randint(10, 100)
        timestamp = start_time + timedelta(
            seconds=random.randint(
                0, int((end_time - start_time).total_seconds())
            )
        )
        order_type = random.choice(["Buy", "Sell"])
        cash = random.randint(1000, 20000) if order_type == "Buy" else 0
        stocks = random.randint(50, 500) if order_type == "Sell" else 0

        orders.append({
            "OrderID": order_id,
            "Price": price,
            "Quantity": quantity,
            "Timestamp": timestamp,
            "Type": order_type,
            "Cash": cash,
            "Stocks": stocks
        })

    return orders


def process_auction(orders_df, backlog_df=None, auction_number=1):
    print(f"\n{'='*50}")
    print(f"Processing Auction #{auction_number}")
    print(f"{'='*50}\n")

    # Add 'AuctionsParticipated' column to new orders
    orders_df['AuctionsParticipated'] = 1

    if backlog_df is not None and not backlog_df.empty:
        # Increment 'AuctionsParticipated' for backlog orders
        backlog_df['AuctionsParticipated'] += 1

        # Remove orders that have been in more than 4 auctions
        expired_orders = backlog_df[
            backlog_df['AuctionsParticipated'] > 4
        ]
        backlog_df = backlog_df[
            backlog_df['AuctionsParticipated'] <= 4
        ]

        if not expired_orders.empty:
            print("Expired Orders (removed from backlog):")
            print(expired_orders)
            print("\n")

        df = pd.concat(
            [orders_df, backlog_df],
            ignore_index=True
        )
    else:
        df = orders_df.copy()

    # Filter out invalid orders
    valid_orders = df[
        ((df["Type"] == "Buy") &
         (df["Cash"] >= df["Price"] * df["Quantity"])) |
        ((df["Type"] == "Sell") &
         (df["Stocks"] >= df["Quantity"]))
    ]

    invalid_orders = df[~df.index.isin(valid_orders.index)]

    '''
    print("Invalid Orders (insufficient cash/stocks):")
    print(invalid_orders)
    print("\n")
    '''

    # Sort valid orders
    buy_orders = valid_orders[
        valid_orders["Type"] == "Buy"
    ].sort_values(
        "Price", ascending=False
    ).reset_index(drop=True)

    sell_orders = valid_orders[
        valid_orders["Type"] == "Sell"
    ].sort_values(
        "Price", ascending=True
    ).reset_index(drop=True)

    print("Sorted Buy Orders:")
    print(buy_orders)
    print("\n")

    print("Sorted Sell Orders:")
    print(sell_orders)
    print("\n")

    # Calculate total quantity for Buy and Sell
    total_buy_quantity = buy_orders["Quantity"].sum()
    total_sell_quantity = sell_orders["Quantity"].sum()

    print(f"Total Buy Quantity: {total_buy_quantity}")
    print(f"Total Sell Quantity: {total_sell_quantity}")
    print("\n")

    # Process transactions
    transactions = []
    updated_orders = pd.DataFrame(columns=df.columns)

    buy_index = 0
    sell_index = 0

    while buy_index < len(buy_orders) and sell_index < len(sell_orders):
        buy_order = buy_orders.iloc[buy_index]
        sell_order = sell_orders.iloc[sell_index]

        if sell_order['Price'] > buy_order['Price']:
            break

        transaction_quantity = min(
            buy_order['Quantity'],
            sell_order['Quantity']
        )

        transaction_price = (
            buy_order['Price'] + sell_order['Price']
        ) / 2

        transactions.append({
            "BuyOrderID": buy_order['OrderID'],
            "SellOrderID": sell_order['OrderID'],
            "Quantity": transaction_quantity,
            "Price": transaction_price
        })

        # Update buy order
        buy_orders.at[buy_index, 'Quantity'] -= transaction_quantity
        buy_orders.at[buy_index, 'Cash'] -= (
            transaction_quantity * transaction_price
        )

        # Update sell order
        sell_orders.at[sell_index, 'Quantity'] -= transaction_quantity
        sell_orders.at[sell_index, 'Stocks'] -= transaction_quantity

        if buy_orders.at[buy_index, 'Quantity'] == 0:
            buy_index += 1

        if sell_orders.at[sell_index, 'Quantity'] == 0:
            sell_index += 1

    # Add remaining orders to updated_orders
    updated_orders = pd.concat(
        [
            updated_orders,
            buy_orders[buy_orders['Quantity'] > 0],
            sell_orders[sell_orders['Quantity'] > 0]
        ],
        ignore_index=True
    )

    # Create transactions DataFrame
    transactions_df = pd.DataFrame(transactions)

    print("Transacted Orders:")
    print(transactions_df)

    print("\nUpdated Orders (new backlog):")
    print(updated_orders)

    # Calculate and display total transacted quantity
    total_transacted_qty = (
        transactions_df['Quantity'].sum()
        if not transactions_df.empty else 0
    )
    print(f"\nTotal Transacted Quantity: {total_transacted_qty}")

    # Calculate and display total backlog quantity
    total_backlog_qty = (
        updated_orders['Quantity'].sum()
        if not updated_orders.empty else 0
    )
    print(f"Total Backlog Quantity: {total_backlog_qty}")

    # Display Final Transaction Price (average of all transactions)
    final_transaction_price = (
        transactions_df['Price'].mean()
        if not transactions_df.empty else 0
    )
    print(f"Final Transaction Price: {final_transaction_price:.2f}")

    return updated_orders


# Set up auction times
start_date = datetime(2024, 7, 15, 7, 50)  # July 15, 2024, 7:50 AM

auction_times = [
    (7, 50),   # 7:50 AM
    (12, 0),   # 12:00 PM
    (16, 30)   # 4:30 PM
]

backlog = None
auction_number = 1

for day in range(3):
    for auction_time in auction_times:
        current_auction_time = start_date.replace(
            hour=auction_time[0],
            minute=auction_time[1]
        ) + timedelta(days=day)

        if day == 0 and auction_time == (7, 50):
            previous_auction_time = current_auction_time - timedelta(days=1)
        else:
            previous_index = (
                auction_times.index(auction_time) - 1
            ) % len(auction_times)

            previous_day_offset = 0 if previous_index != 2 else 1

            previous_auction_time = current_auction_time.replace(
                hour=auction_times[previous_index][0],
                minute=auction_times[previous_index][1]
            ) - timedelta(days=previous_day_offset)

        print(f"\n{'='*50}")
        print(f"Auction #{auction_number} at {current_auction_time}")
        print(f"{'='*50}\n")

        # Generate orders for this auction period
        new_orders = generate_orders(
            num_orders=3,
            start_time=previous_auction_time,
            end_time=current_auction_time,
            auction_number=auction_number
        )

        new_orders_df = pd.DataFrame(new_orders)

        print("New Orders for this Auction:")
        print(new_orders_df)
        print("\n")

        '''
        if backlog is not None and not backlog.empty:
            print("Current Backlog:")
            print(backlog)
            print("\n")
        '''

        # Process the auction
        backlog = process_auction(
            new_orders_df,
            backlog,
            auction_number
        )

        auction_number += 1

print("\nAll auctions completed.")