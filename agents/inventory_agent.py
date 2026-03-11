from db.database import SessionLocal
from sqlalchemy.orm import Session
from models.models import Products
from state.agentstate import GroceryState


def db_inventory_node(state: GroceryState) -> GroceryState:

    db: Session = SessionLocal()

    try:
        mcp = state.get("mcp_command", {})
        params = mcp.get("parameters", {})
        product_name = params.get("product", "")
        if not product_name:
            product_name = params.get("query", "")

        if not product_name:
            return {"inventory_result": {"error": "Product not provided"}}

        product = (
            db.query(Products).filter(Products.name.ilike(f"%{product_name}%")).first()
        )

        if not product:
            return {
                "inventory_result": {
                    "status": "not_found",
                    "message": f"{product_name} not available",
                }
            }

        return {
            "inventory_result": {
                "name": product.name,
                "price": product.price,
                "stock": product.stock,
                "aisle": product.aisle,
            }
        }

    except Exception as e:
        return {"inventory_result": {"error": str(e)}}

    finally:
        db.close()


# for multiple


# def db_inventory_node(state: GroceryState) -> GroceryState:

#     db = SessionLocal()

#     try:
#         mcp = state.get("mcp_command", {})
#         product_name = mcp.get("parameters", {}).get("product", "")

#         if not product_name:
#             return {"inventory_result": {"error": "Product not provided"}}

#         products = (
#             db.query(Products).filter(Products.name.ilike(f"%{product_name}%")).all()
#         )

#         if not products:
#             return {
#                 "inventory_result": {
#                     "status": "not_found",
#                     "message": f"{product_name} not available",
#                 }
#             }

#         return {
#             "inventory_result": [
#                 {"name": p.name, "price": p.price, "stock": p.stock, "aisle": p.aisle}
#                 for p in products
#             ]
#         }

#     except Exception as e:
#         return {"inventory_result": {"error": str(e)}}

#     finally:
#         db.close()
