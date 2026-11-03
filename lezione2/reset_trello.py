"""Riporta la board "Lista della spesa" allo stato iniziale: liste vuote.

Cancella tutte le card delle liste TRELLO_LIST_ID e TRELLO_LIST_ID_DONE.
Uso, dalla root della repo:

    .venv/bin/python lezione2/reset_trello.py          # mostra cosa cancellerebbe
    .venv/bin/python lezione2/reset_trello.py --yes    # cancella davvero
"""

import os
import sys

import requests
from dotenv import load_dotenv

API = "https://api.trello.com/1"


def main() -> None:
    load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env"))
    auth = {"key": os.environ["TRELLO_API_KEY"], "token": os.environ["TRELLO_TOKEN"]}
    list_ids = [v for v in (os.getenv("TRELLO_LIST_ID"), os.getenv("TRELLO_LIST_ID_DONE")) if v]
    confirm = "--yes" in sys.argv

    total = 0
    for list_id in list_ids:
        lst = requests.get(f"{API}/lists/{list_id}", params={**auth, "fields": "name"}, timeout=30)
        lst.raise_for_status()
        cards = requests.get(f"{API}/lists/{list_id}/cards", params={**auth, "fields": "name"}, timeout=30)
        cards.raise_for_status()
        print(f"{lst.json()['name']}: {len(cards.json())} card")
        for card in cards.json():
            total += 1
            if confirm:
                requests.delete(f"{API}/cards/{card['id']}", params=auth, timeout=30).raise_for_status()
            print(f"  {'cancellata' if confirm else 'da cancellare'}: {card['name']}")

    if not confirm and total:
        print("\nNiente cancellato: rilancia con --yes per svuotare le liste.")
    elif total == 0:
        print("Board già vuota.")


if __name__ == "__main__":
    main()
