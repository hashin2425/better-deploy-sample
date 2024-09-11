import json
from typing import Dict, List, Optional
import azure.functions as func


def load_database(file_path: str) -> List[Dict]:
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def find_product(products: List[Dict], product_id: int) -> Optional[Dict]:
    return next((item for item in products if item["id"] == product_id), None)


def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        product_id = req.params.get("id")

        if not product_id or not product_id.isdigit():
            return func.HttpResponse("Invalid id", status_code=400)

        product_id = int(product_id)
        items = load_database("./database/items.json")
        product = find_product(items, product_id)

        if product is None:
            return func.HttpResponse("Product not found", status_code=404)

        return func.HttpResponse(json.dumps(product), mimetype="application/json")

    except Exception as e:
        return func.HttpResponse(f"Internal server error: {str(e)}", status_code=500)
