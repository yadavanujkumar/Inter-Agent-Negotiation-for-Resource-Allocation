#!/usr/bin/env python3
"""
Example: Mediator Intervention Scenario

This script demonstrates a negotiation scenario where the Mediator
must intervene due to a stalemate.
"""

from negotiation_sim import (
    NegotiationOffer, 
    NegotiationTracker, 
    plot_negotiation_path,
    BuyerAgent,
    SellerAgent,
    MediatorAgent
)


def main():
    """Demonstrate mediator intervention in a stalemate"""
    
    print("=" * 80)
    print("MEDIATOR INTERVENTION DEMONSTRATION")
    print("=" * 80)
    print()
    
    # Initialize tracker and agents
    tracker = NegotiationTracker()
    buyer = BuyerAgent(max_budget=500.0)
    seller = SellerAgent(min_price=350.0)
    mediator = MediatorAgent()
    
    print(f"Agents initialized:")
    print(f"  - {buyer.name}: Max budget ${buyer.max_budget}/hour")
    print(f"  - {seller.name}: Min price ${seller.min_price}/hour")
    print(f"  - {mediator.name}: Monitors for stalemates")
    print()
    
    quantity = 100
    
    # Simulate a stalemate scenario
    print("Simulating negotiation with minimal price movements...")
    print("-" * 80)
    print()
    
    # Round 1-3: Agents get close
    offers = [
        ("Buyer_Agent", 428.0, "Initial offer near middle ground"),
        ("Seller_Agent", 432.0, "Counter-offer with small gap"),
        ("Buyer_Agent", 429.0, "Small increment"),
        ("Seller_Agent", 431.0, "Small decrement"),
        ("Buyer_Agent", 429.5, "Tiny increment - stalemate forming"),
        ("Seller_Agent", 430.5, "Tiny decrement - stalemate forming"),
        ("Buyer_Agent", 429.8, "Another tiny increment"),
        ("Seller_Agent", 430.2, "Another tiny decrement"),
    ]
    
    for i, (agent, price, reasoning) in enumerate(offers, 1):
        offer = NegotiationOffer(
            offer_price=price,
            quantity=quantity,
            reasoning=reasoning,
            is_final_offer=False
        )
        tracker.add_offer(agent, offer)
        print(f"Round {i}: {agent}")
        print(f"  Price: ${price}")
        print(f"  Reasoning: {reasoning}")
        
        # Check for stalemate after round 5
        if i >= 5 and tracker.detect_stalemate():
            print()
            print("=" * 80)
            print("⚠️  STALEMATE DETECTED!")
            print("=" * 80)
            print()
            print("Analysis:")
            print(f"  - Rounds without progress: {i}")
            print(f"  - Price change over last 5 rounds: <2%")
            print(f"  - Current gap: ${abs(offers[i-1][1] - offers[i-2][1]):.2f}")
            print()
            
            # Get last buyer and seller prices
            last_buyer_price = next(
                (o[1] for o in reversed(offers[:i]) if "Buyer" in o[0]),
                429.8
            )
            last_seller_price = next(
                (o[1] for o in reversed(offers[:i]) if "Seller" in o[0]),
                430.2
            )
            
            print("Mediator Intervention:")
            print(f"  Last Buyer offer: ${last_buyer_price}")
            print(f"  Last Seller offer: ${last_seller_price}")
            
            # Calculate compromise
            compromise = (last_buyer_price + last_seller_price) / 2
            print(f"  Proposed compromise: ${compromise:.2f}")
            print()
            
            # Mediator proposes compromise
            mediator_offer = NegotiationOffer(
                offer_price=compromise,
                quantity=quantity,
                reasoning=f"Mediator intervention: Split-the-difference compromise at ${compromise:.2f}. "
                          f"This is exactly halfway between your positions and ensures fairness.",
                is_final_offer=False
            )
            tracker.add_offer("Mediator_Agent", mediator_offer)
            
            print(f"Round {i+1}: Mediator_Agent")
            print(f"  Price: ${compromise:.2f}")
            print(f"  Reasoning: {mediator_offer.reasoning}")
            print()
            
            print("=" * 80)
            print("✓ Mediator successfully proposes fair compromise")
            print("✓ Both parties accept the middle-ground solution")
            print("=" * 80)
            print()
            
            # Show final statistics
            print("Final Agreement:")
            print(f"  Price: ${compromise:.2f} per GPU hour")
            print(f"  Quantity: {quantity} hours")
            print(f"  Total cost: ${compromise * quantity:.2f}")
            print(f"  Buyer savings from max: ${(buyer.max_budget - compromise) * quantity:.2f}")
            print(f"  Seller gain above min: ${(compromise - seller.min_price) * quantity:.2f}")
            print()
            
            # Generate visualization
            plot_negotiation_path(tracker, "mediator_example.png")
            print("📊 Visualization saved to: mediator_example.png")
            print()
            
            break
        print()
    
    print("=" * 80)
    print("DEMONSTRATION COMPLETE")
    print("=" * 80)
    print()
    print("Key Takeaways:")
    print("  1. Stalemate detected when price changes < 2% over 5 rounds")
    print("  2. Mediator proposes 'Split the Difference' compromise")
    print("  3. Compromise is exactly halfway between last offers")
    print("  4. Both parties benefit equally from the resolution")
    print("  5. Pareto optimal outcome achieved through mediation")
    print()


if __name__ == "__main__":
    main()
