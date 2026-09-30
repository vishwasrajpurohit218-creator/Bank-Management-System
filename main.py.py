# This program checks a transaction in the gateway, bank and ledger
# and tells us if there is any problem with the settlement.

gateway_data = {
    "TXN1001": {
        "date": "2026-09-20",
        "amount": 1500,
        "status": "PROCESSED"
    },
    "TXN1002": {
        "date": "2026-09-20",
        "amount": 2500,
        "status": "PROCESSED"
    },
    "TXN1003": {
        "date": "2026-09-21",
        "amount": 3200,
        "status": "FAILED"
    },
    "TXN1004": {
        "date": "2026-09-21",
        "amount": 1800,
        "status": "PROCESSED"
    },
    "TXN1005": {
        "date": "2026-09-22",
        "amount": 5000,
        "status": "PROCESSED"
    }
}


# Sample bank records
bank_data = {
    "TXN1001": {
        "date": "2026-09-20",
        "amount": 1500,
        "status": "SETTLED"
    },
    "TXN1002": {
        "date": "2026-09-20",
        "amount": 2500,
        "status": "PENDING"
    },
    "TXN1003": {
        "date": "2026-09-21",
        "amount": 3200,
        "status": "NOT_RECEIVED"
    },
    "TXN1004": {
        "date": "2026-09-21",
        "amount": 1800,
        "status": "SETTLED"
    },
    "TXN1005": {
        "date": "2026-09-22",
        "amount": 5000,
        "status": "PENDING"
    }
}


# Sample ledger records
ledger_data = {
    "TXN1001": {
        "date": "2026-09-20",
        "amount": 1500,
        "status": "RECORDED"
    },
    "TXN1002": {
        "date": "2026-09-20",
        "amount": 2500,
        "status": "RECORDED"
    },
    "TXN1003": {
        "date": "2026-09-21",
        "amount": 3200,
        "status": "NOT_RECORDED"
    },
    "TXN1004": {
        "date": "2026-09-21",
        "amount": 1800,
        "status": "RECORDED"
    },
    "TXN1005": {
        "date": "2026-09-22",
        "amount": 5000,
        "status": "RECORDED"
    }
}


def trace_transaction(transaction_id):
    """Check one transaction in all three records."""

    print("\n" + "=" * 55)
    print("             TRANSACTION SETTLEMENT REPORT")
    print("=" * 55)

    gateway = gateway_data.get(transaction_id)
    bank = bank_data.get(transaction_id)
    ledger = ledger_data.get(transaction_id)

    # Check if the transaction is present
    if gateway is None:
        print("\nTransaction ID not found.")
        print("Please check the Transaction ID and try again.")
        return

    print("\nTransaction ID :", transaction_id)
    print("Date           :", gateway["date"])
    print("Amount         :", gateway["amount"])

    # Gateway details
    print("\n--- Gateway Record ---")
    print("Status :", gateway["status"])
    print("Amount :", gateway["amount"])
    print("Date   :", gateway["date"])

    # Bank details
    print("\n--- Bank Record ---")

    if bank:
        print("Status :", bank["status"])
        print("Amount :", bank["amount"])
        print("Date   :", bank["date"])
    else:
        print("Bank record not found.")

    # Ledger details
    print("\n--- Ledger Record ---")

    if ledger:
        print("Status :", ledger["status"])
        print("Amount :", ledger["amount"])
        print("Date   :", ledger["date"])
    else:
        print("Ledger record not found.")

    problems = []

    # Check gateway status
    if gateway["status"] != "PROCESSED":
        problems.append("Gateway did not process the transaction.")

    # Check bank status
    if bank is None:
        problems.append("Bank record is missing.")
    elif bank["status"] == "PENDING":
        problems.append("Bank settlement is still pending.")
    elif bank["status"] == "NOT_RECEIVED":
        problems.append("Bank did not receive the transaction.")

    # Check ledger status
    if ledger is None:
        problems.append("Ledger record is missing.")
    elif ledger["status"] == "NOT_RECORDED":
        problems.append("Transaction is not recorded in the ledger.")

    # Compare the amounts
    if bank is not None:
        if gateway["amount"] != bank["amount"]:
            problems.append("Gateway and bank amounts do not match.")

    if ledger is not None:
        if gateway["amount"] != ledger["amount"]:
            problems.append("Gateway and ledger amounts do not match.")

    # Compare the dates
    if bank is not None:
        if gateway["date"] != bank["date"]:
            problems.append("Gateway and bank dates do not match.")

    if ledger is not None:
        if gateway["date"] != ledger["date"]:
            problems.append("Gateway and ledger dates do not match.")

    # Display the final result
    print("\n--- Settlement Explanation ---")

    if not problems:
        print("Settlement completed successfully.")
        print("Gateway, bank, and ledger records are consistent.")
    else:
        print("Settlement requires attention.")
        print("\nException List:")

        for problem in problems:
            print("-", problem)

    print("\n" + "=" * 55)


def search_by_date(search_date):
    """Find transactions made on a particular date."""

    found = False

    print("\n" + "=" * 55)
    print("TRANSACTIONS FOR DATE:", search_date)
    print("=" * 55)

    for transaction_id, transaction in gateway_data.items():

        if transaction["date"] == search_date:
            found = True

            print(
                transaction_id,
                "| Amount:", transaction["amount"],
                "| Status:", transaction["status"]
            )

    if not found:
        print("No transactions found for this date.")


def main():

    print("\n" + "=" * 55)
    print("              SETTLEMENT Q&A AGENT")
    print("=" * 55)

    print("\nThis program traces transactions across:")
    print("1. Gateway")
    print("2. Bank")
    print("3. Ledger")

    while True:

        print("\n" + "-" * 55)
        print("MENU")
        print("-" * 55)
        print("1. Search Transaction")
        print("2. Search Transactions by Date")
        print("3. Exit")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":

            transaction_id = input(
                "\nEnter Transaction ID: "
            ).strip().upper()

            trace_transaction(transaction_id)

        elif choice == "2":

            search_date = input(
                "\nEnter date (YYYY-MM-DD): "
            ).strip()

            search_by_date(search_date)

        elif choice == "3":

            print("\nThank you for using Settlement Q&A Agent.")
            print("Program ended.")
            break

        else:

            print("\nInvalid choice.")
            print("Please enter 1, 2, or 3.")


# Start the program
if __name__ == "__main__":
    main()