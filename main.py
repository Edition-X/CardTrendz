#!/usr/bin/env python3
from SplinterlandsSDK import Api
from beem.blockchain import Blockchain
from beem import Hive
from datetime import datetime, timedelta
import pytz
import json


def _store_purchase_data(trx_info, card_data):
    items = json.loads(trx_info["data"])

    for item in (items if isinstance(items, list) else [items]):
        if "cards" not in item:
            continue
        card_uids = [(card,) for card in item["cards"]]
        for card_uid in card_uids:
            card_data.add(tuple(sorted({"card_uid": card_uid, "price": item["price"],
                                        "created_date": trx_info["created_date"], "trx_id": trx_info["id"]}.items())))

    return card_data


def _check_transaction_success(trx_id, card_data):
    api = Api()
    data = api.get_transaction(trx_id)

    if "trx_info" in data and data["trx_info"]["success"]:
        card_data = _store_purchase_data(data["trx_info"], card_data)
        return True, card_data
    return False, card_data


def _get_start_block(blockchain, time_unit, time_amount):
    x_time_ago = datetime.now(pytz.UTC) - timedelta(**{time_unit: time_amount})
    return blockchain.get_estimated_block_num(x_time_ago)


def get_blocks_from_last_x_days_and_filter(filter_value, time_unit, time_amount):
    # Instantiate Hive and Blockchain
    h = Hive("https://api.hive.blog")
    blockchain = Blockchain(blockchain_instance=h)

    start_block_num = _get_start_block(blockchain, time_unit, time_amount)
    current_block_num = blockchain.get_current_block_num()

    # List to store processed items
    card_data = set()

    # Get blocks from the last x days
    for block in blockchain.blocks(start=start_block_num, stop=current_block_num):
        # Parse the block to check the operations
        unverified_transactions = []
        for transaction in block["transactions"]:
            for operation in transaction["operations"]:
                if operation["type"] == "custom_json_operation" and operation["value"].get("id") == filter_value:
                    # Parse JSON from string
                    json_data = json.loads(operation["value"]["json"])
                    # Process each item
                    unverified_transactions += [item.split('-')[0] for item in json_data["items"]]

                    for transaction_id in unverified_transactions:
                        # Check if the transaction was successful
                        success, card_data = _check_transaction_success(transaction_id, card_data)
                        print(f"Transaction {'was' if success else 'was not'} successful.")
                        if success:
                            print(card_data)


def main():
    get_blocks_from_last_x_days_and_filter("sm_market_purchase", "hours", 1)


if __name__ == "__main__":
    main()
