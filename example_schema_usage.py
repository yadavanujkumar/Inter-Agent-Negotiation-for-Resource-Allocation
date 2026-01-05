#!/usr/bin/env python3
"""
Example: Using the Pydantic Schema for Negotiation

This script demonstrates how to use the NegotiationOffer schema
for structured communication between agents.
"""

from negotiation_sim import NegotiationOffer
import json


def main():
    """Demonstrate Pydantic schema usage"""
    
    print("=" * 70)
    print("PYDANTIC SCHEMA DEMONSTRATION")
    print("=" * 70)
    print()
    
    # Example 1: Create a valid offer
    print("Example 1: Creating a valid offer")
    print("-" * 70)
    
    buyer_offer = NegotiationOffer(
        offer_price=420.50,
        quantity=100,
        reasoning="This price aligns with our budget constraints and market research.",
        is_final_offer=False
    )
    
    print("Python Object:")
    print(f"  Price: ${buyer_offer.offer_price}")
    print(f"  Quantity: {buyer_offer.quantity} hours")
    print(f"  Reasoning: {buyer_offer.reasoning}")
    print(f"  Final Offer: {buyer_offer.is_final_offer}")
    print()
    
    print("JSON Representation:")
    print(f"  {buyer_offer.to_json_str()}")
    print()
    
    # Example 2: Parse JSON into schema
    print("\nExample 2: Parsing JSON into validated schema")
    print("-" * 70)
    
    json_offer = """{
        "offer_price": 455.75,
        "quantity": 150,
        "reasoning": "Counter-offer considering operational costs and demand.",
        "is_final_offer": false
    }"""
    
    print("Raw JSON:")
    print(f"  {json_offer}")
    print()
    
    seller_offer = NegotiationOffer.from_json_str(json_offer)
    print("Parsed and Validated:")
    print(f"  Price: ${seller_offer.offer_price}")
    print(f"  Quantity: {seller_offer.quantity} hours")
    print(f"  Reasoning: {seller_offer.reasoning}")
    print()
    
    # Example 3: Validation in action
    print("\nExample 3: Schema validation (negative price)")
    print("-" * 70)
    
    try:
        invalid_offer = NegotiationOffer(
            offer_price=-100.0,  # Invalid: negative price
            quantity=100,
            reasoning="This will fail validation",
            is_final_offer=False
        )
    except Exception as e:
        print(f"✓ Validation Error Caught: {type(e).__name__}")
        print(f"  Message: {str(e)}")
    print()
    
    # Example 4: Validation in action
    print("\nExample 4: Schema validation (zero quantity)")
    print("-" * 70)
    
    try:
        invalid_offer = NegotiationOffer(
            offer_price=400.0,
            quantity=0,  # Invalid: must be > 0
            reasoning="This will also fail validation",
            is_final_offer=False
        )
    except Exception as e:
        print(f"✓ Validation Error Caught: {type(e).__name__}")
        print(f"  Message: {str(e)}")
    print()
    
    # Example 5: Communication protocol
    print("\nExample 5: Agent-to-Agent communication simulation")
    print("-" * 70)
    
    # Buyer creates offer
    buyer_msg = NegotiationOffer(
        offer_price=380.0,
        quantity=100,
        reasoning="Initial offer based on market analysis",
        is_final_offer=False
    )
    
    print("Buyer Agent sends:")
    print(f"  {buyer_msg.to_json_str()}")
    print()
    
    # Seller receives and creates counter-offer
    seller_response = NegotiationOffer(
        offer_price=470.0,
        quantity=100,
        reasoning="Counter-offer reflecting infrastructure costs",
        is_final_offer=False
    )
    
    print("Seller Agent responds:")
    print(f"  {seller_response.to_json_str()}")
    print()
    
    # Calculate the gap
    price_gap = seller_response.offer_price - buyer_msg.offer_price
    print(f"Current negotiation gap: ${price_gap:.2f}")
    print()
    
    print("=" * 70)
    print("✓ Pydantic schema ensures type-safe communication!")
    print("=" * 70)


if __name__ == "__main__":
    main()
