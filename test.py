res = 'Here\'s the business logic of the `InvoiceProcessor` class in JSON format:\n\n```json\n{\n  "InvoiceProcessor": {\n    "processInvoice": {\n      "inputs": {\n        "customerId": "String representing the ID of the customer.",\n        "orderId": "String representing the ID of the order."\n      },\n      "process": [\n        {\n          "step": "Retrieve customer information using the customer ID.",\n          "operation": "Get Customer details by ID from CustomerService which returns a Customer object."\n        },\n        {\n          "step": "Retrieve order details using the order ID.",\n          "operation": "Get Order details by ID from OrderService which returns an Order object."\n        },\n        {\n          "step": "Calculate the total order amount.",\n          "operation": "Use Order\'s calculateTotal method which sums item total and tax."\n        },\n        {\n          "step": "Calculate applicable discounts for the order.",\n          "operation": "Use DiscountService\'s calculateDiscount method which checks if customer type is \'VIP\' and order total exceeds 1000, applies a 10% discount."\n        },\n        {\n          "step": "Calculate the final amount after discount.",\n          "operation": "Subtract the discount from the total order amount."\n        },\n        {\n          "step": "Determine if the order requires manual review.",\n          "operation": "Use ReviewService\'s requiresManualReview method which checks if the order total is greater than the customer\'s credit limit."\n        }\n      ],\n      "outputs": {\n        "InvoiceResult": {\n          "Customer ID": "Provided customer ID.",\n          "Order ID": "Provided order ID.",\n          "Total Amount": "Calculated total order amount before discount.",\n          "Discount": "Calculated discount amount.",\n          "Final Amount": "Total amount minus the discount.",\n          "Requires Review": "Boolean indicating if the order needs manual review based on customer credit limit and order total."\n        }\n      }\n    },\n    "relatedEntities": {\n      "Customer": {\n        "attributes": {\n          "customerId": "Unique identifier of the customer",\n          "type": "e.g., VIP",\n          "creditLimit": "Maximum amount of credit allowed"\n        }\n      },\n      "Order": {\n        "attributes": {\n          "orderId": "Unique identifier of the order",\n          "itemTotal": "Total cost of items",\n          "tax": "Tax applied to the order"\n        },\n        "methods": {\n          "calculateTotal": "Calculate sum of itemTotal and tax"\n        }\n      }\n    }\n  }\n}\n```\n\nThe JSON articulates the steps and logic of processing an invoice, including retrieving customer and order information, calculations for total amounts, discounts, and manual review evaluation.'

import json
import re
def extract_json_from_response(response: str) -> dict:
    # Use regex to find the JSON part in the response
    json_pattern = r'```json\n(.*?)\n```'
    match = re.search(json_pattern, response, re.DOTALL)
    
    if match:
        json_str = match.group(1)
        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            print(f"JSON decoding error: {e}")
            return {}
    else:
        print("No JSON found in the response.")
        return {}
# Example usage
if __name__ == "__main__":
    response = res
    extracted_json = extract_json_from_response(response)
    print(json.dumps(extracted_json, indent=2))