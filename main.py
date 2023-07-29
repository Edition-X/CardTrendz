#!/usr/bin/env python3
from SplinterlandsSDK import Api
from beem.blockchain import Blockchain
from beem import Hive
from datetime import datetime, timedelta
import pytz
import json

card_data = []

def _store_purchase_data(trx_info):
    raw_items = trx_info["data"]
    created_date = trx_info["created_date"]
    items = json.loads(raw_items)
    card_uid = items["cards"]
    # card_id = carduid[0].split('-')[1]  # Split the card id string by '-' and get the 2nd part
    price = items["price"]  # Extract the price
    trx_id = trx_info["id"]
    card_data.append({"card_uid": card_uid, "price": price, "created_date": created_date, "trx_id": trx_id})

def _check_transaction_success(trx_id):
    api = Api()
    data = api.get_transaction(trx_id)
    if "trx_info" in data:
        if data["trx_info"]["success"] == True:
            # _store_purchase_data(data["trx_info"]["data"], data["trx_info"]["created_date"])
            _store_purchase_data(data["trx_info"])
            return True
    return False

def get_blocks_from_last_x_days_and_filter(filter_value, days):
    # Instantiate Hive and Blockchain
    h = Hive("https://api.hive.blog")
    blockchain = Blockchain(blockchain_instance=h)

    # Calculate the date for x days ago
    x_days_ago = datetime.now(pytz.UTC) - timedelta(days=days)

    # Estimate the block number for x days ago
    start_block_num = blockchain.get_estimated_block_num(x_days_ago)

    # Get the current block number
    current_block_num = blockchain.get_current_block_num()

    # List to store processed items
    unverified_transactions = []

    # Get blocks from the last x days
    for block in blockchain.blocks(start=start_block_num, stop=current_block_num):
        # Parse the block to check the operations
        for transaction in block["transactions"]:
            for operation in transaction["operations"]:
                if operation["type"] == "custom_json_operation" and "id" in operation["value"] and operation["value"]["id"] == filter_value:
                    # Parse JSON from string
                    json_data = json.loads(operation["value"]["json"])
                    # Process each item
                    for item in json_data["items"]:
                        # Split the string by '-' and keep the first part
                        transaction_id = item.split('-')[0]
                        # Add processed item to the new list
                        unverified_transactions.append(transaction_id)
                    # print(json.dumps(operation, indent=4))  # print out full content of each block
                    # print(new_items)  # print the new list of items
                    for transaction_id in unverified_transactions:
                        # Check if the transaction was successful
                        if _check_transaction_success(transaction_id):
                            # Do something
                            print("Transaction was successful")
                            print(card_data)
                        else:
                            # Do something else
                            print("Transaction was not successful")

# Test the function
get_blocks_from_last_x_days_and_filter("sm_market_purchase", 1)

