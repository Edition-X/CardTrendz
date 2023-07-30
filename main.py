#!/usr/bin/env python3
from SplinterlandsSDK import Api
from beem.blockchain import Blockchain
from beem import Hive
from datetime import datetime, timedelta
import pytz
import json

def _store_purchase_data(trx_info, card_data):
    raw_items = trx_info["data"]
    created_date = trx_info["created_date"]
    items = json.loads(raw_items)
    # If items is a list of dicts, iterate through each item
    if isinstance(items, list):
        for item in items:
            if "cards" in item:
                for card in item["cards"]:
                    card_uid = (card,)
                    price = item["price"]
                    trx_id = trx_info["id"]
                    card_data.add(tuple(sorted({"card_uid": card_uid, "price": price, "created_date": created_date, "trx_id": trx_id}.items())))
    # If items is a dict, proceed as before
    elif isinstance(items, dict):
        if "cards" in items:
            for card in items["cards"]:
                card_uid = (card,)
                price = items["price"]
                trx_id = trx_info["id"]
                card_data.add(tuple(sorted({"card_uid": card_uid, "price": price, "created_date": created_date, "trx_id": trx_id}.items())))
    return card_data

def _check_transaction_success(trx_id, card_data):
    api = Api()
    data = api.get_transaction(trx_id)
    if "trx_info" in data:
        if data["trx_info"]["success"] == True:
            card_data = _store_purchase_data(data["trx_info"], card_data)
            return True, card_data
    return False, card_data

def _get_start_block(blockchain, time_unit, time_amount):
    if time_unit == "days":
        # Calculate the date for x days ago
        x_time_ago = datetime.now(pytz.UTC) - timedelta(days=time_amount)
        # Estimate the block number for x days ago
        start_block_num = blockchain.get_estimated_block_num(x_time_ago)
        return start_block_num
    elif time_unit == "hours":
        # Calculate the date for x hours ago
        x_time_ago = datetime.now(pytz.UTC) - timedelta(hours=time_amount)
        # Estimate the block number for x hours ago
        start_block_num = blockchain.get_estimated_block_num(x_time_ago)
        return start_block_num

def get_blocks_from_last_x_days_and_filter(filter_value, time_unit, time_amount):
    # Instantiate Hive and Blockchain
    h = Hive("https://api.hive.blog")
    blockchain = Blockchain(blockchain_instance=h)

    start_block_num = _get_start_block(blockchain, time_unit, time_amount)

    # Get the current block number
    current_block_num = blockchain.get_current_block_num()

    # List to store processed items
    unverified_transactions = []
    card_data = set()

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
                        success, card_data = _check_transaction_success(transaction_id, card_data)
                        if success:
                            # Do something
                            print("Transaction was successful")
                            print(card_data)
                        else:
                            # Do something else
                            print("Transaction was not successful")

def main():
    get_blocks_from_last_x_days_and_filter("sm_market_purchase", "hours", 1)

if __name__ == "__main__":
    main()

