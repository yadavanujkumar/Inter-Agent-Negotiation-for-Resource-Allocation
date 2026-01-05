# Integration Guide for Multi-Agent Frameworks

This guide explains how to integrate the bilateral negotiation system with AutoGen or CrewAI frameworks.

## 🔌 AutoGen Integration

### Overview
AutoGen is a framework by Microsoft Research for building multi-agent applications with conversable agents.

### Integration Steps

1. **Install AutoGen**
```bash
pip install pyautogen
```

2. **Configure LLM Backend**
```python
config_list = [{
    "model": "gpt-4",
    "api_key": os.environ["OPENAI_API_KEY"]
}]
```

3. **Create AutoGen Agents**
```python
from autogen import AssistantAgent, UserProxyAgent
from negotiation_sim import NegotiationOffer, BUYER_SYSTEM_MESSAGE, SELLER_SYSTEM_MESSAGE

# Create Buyer Agent with AutoGen
buyer_agent = AssistantAgent(
    name="Buyer_Agent",
    system_message=BUYER_SYSTEM_MESSAGE,
    llm_config={"config_list": config_list, "temperature": 0.7}
)

# Create Seller Agent with AutoGen
seller_agent = AssistantAgent(
    name="Seller_Agent",
    system_message=SELLER_SYSTEM_MESSAGE,
    llm_config={"config_list": config_list, "temperature": 0.7}
)
```

4. **Use Pydantic Schema for Validation**
```python
# Parse agent responses through Pydantic schema
def validate_offer(response_text: str) -> NegotiationOffer:
    # Extract JSON from agent response
    import json
    import re
    
    # Find JSON object in response
    json_match = re.search(r'\{[^}]+\}', response_text)
    if json_match:
        json_str = json_match.group(0)
        return NegotiationOffer.from_json_str(json_str)
    raise ValueError("No valid offer found in response")
```

5. **Run Group Chat**
```python
from autogen import GroupChat, GroupChatManager

# Create group chat
groupchat = GroupChat(
    agents=[buyer_agent, seller_agent],
    messages=[],
    max_round=10
)

manager = GroupChatManager(
    groupchat=groupchat,
    llm_config={"config_list": config_list}
)

# Start negotiation
buyer_agent.initiate_chat(
    manager,
    message="Let's negotiate GPU compute hours. I need 100 hours."
)
```

## 🚢 CrewAI Integration

### Overview
CrewAI is a framework for orchestrating role-playing AI agents to work together on complex tasks.

### Integration Steps

1. **Install CrewAI**
```bash
pip install crewai
```

2. **Create CrewAI Agents**
```python
from crewai import Agent, Task, Crew
from negotiation_sim import NegotiationOffer, BUYER_SYSTEM_MESSAGE, SELLER_SYSTEM_MESSAGE

# Create Buyer Agent with CrewAI
buyer_agent = Agent(
    role='Buyer Agent',
    goal='Minimize cost while securing GPU compute hours',
    backstory=BUYER_SYSTEM_MESSAGE,
    verbose=True,
    allow_delegation=False
)

# Create Seller Agent with CrewAI
seller_agent = Agent(
    role='Seller Agent',
    goal='Maximize revenue while meeting reservation price',
    backstory=SELLER_SYSTEM_MESSAGE,
    verbose=True,
    allow_delegation=False
)
```

3. **Define Negotiation Tasks**
```python
# Buyer's task
buyer_task = Task(
    description="""
    Negotiate the purchase of 100 GPU compute hours.
    Your maximum budget is $500 per hour.
    Respond using JSON format: {"offer_price": <price>, "quantity": 100, 
    "reasoning": "<reason>", "is_final_offer": <bool>}
    """,
    agent=buyer_agent,
    expected_output="A negotiated price and agreement"
)

# Seller's task
seller_task = Task(
    description="""
    Negotiate the sale of GPU compute hours.
    Your minimum reservation price is $350 per hour.
    Respond using JSON format: {"offer_price": <price>, "quantity": 100,
    "reasoning": "<reason>", "is_final_offer": <bool>}
    """,
    agent=seller_agent,
    expected_output="A negotiated price and agreement"
)
```

4. **Create and Run Crew**
```python
# Create the negotiation crew
negotiation_crew = Crew(
    agents=[buyer_agent, seller_agent],
    tasks=[buyer_task, seller_task],
    verbose=True
)

# Execute negotiation
result = negotiation_crew.kickoff()
print(result)
```

## 📝 Custom Message Handlers

### AutoGen Message Handler
```python
def handle_autogen_message(message: str, tracker: NegotiationTracker):
    """Process AutoGen agent messages"""
    try:
        offer = validate_offer(message)
        tracker.add_offer(sender_name, offer)
        
        # Check for stalemate
        if tracker.detect_stalemate():
            return propose_mediator_compromise(tracker)
        
        return offer
    except Exception as e:
        print(f"Error parsing offer: {e}")
        return None
```

### CrewAI Result Parser
```python
def parse_crewai_result(result: str) -> NegotiationOffer:
    """Parse CrewAI task results"""
    # Extract JSON from result
    import json
    import re
    
    json_match = re.search(r'\{[^}]+\}', result)
    if json_match:
        return NegotiationOffer.from_json_str(json_match.group(0))
    
    raise ValueError("Could not parse CrewAI result")
```

## 🔄 State Management

### Tracking Negotiation State
```python
from negotiation_sim import NegotiationTracker

# Initialize tracker
tracker = NegotiationTracker()

# After each agent response
def process_agent_response(agent_name: str, response: str):
    offer = validate_offer(response)
    tracker.add_offer(agent_name, offer)
    
    # Check conditions
    if tracker.detect_stalemate():
        return "STALEMATE", None
    
    # Check if agreement reached
    if offer.is_final_offer:
        return "FINAL", offer
    
    return "CONTINUE", offer
```

## 🎨 Visualization Integration

```python
from negotiation_sim import plot_negotiation_path

# After negotiation completes
def finalize_negotiation(tracker: NegotiationTracker):
    # Generate visualization
    plot_negotiation_path(tracker, "results/negotiation.png")
    
    # Get summary statistics
    final_price = tracker.history[-1]['price']
    rounds = tracker.rounds
    
    return {
        "success": True,
        "final_price": final_price,
        "rounds": rounds,
        "visualization": "results/negotiation.png"
    }
```

## 🧪 Testing Your Integration

```python
def test_integration():
    """Test the framework integration"""
    
    # 1. Test schema validation
    offer = NegotiationOffer(
        offer_price=425.0,
        quantity=100,
        reasoning="Test offer",
        is_final_offer=False
    )
    assert offer.offer_price == 425.0
    
    # 2. Test JSON serialization
    json_str = offer.to_json_str()
    parsed = NegotiationOffer.from_json_str(json_str)
    assert parsed.offer_price == offer.offer_price
    
    # 3. Test tracker
    tracker = NegotiationTracker()
    tracker.add_offer("Test_Agent", offer)
    assert tracker.rounds == 1
    
    print("✓ All integration tests passed!")
```

## 🚀 Production Considerations

### 1. Error Handling
```python
try:
    offer = validate_offer(agent_response)
except ValidationError as e:
    # Handle invalid offers
    logger.error(f"Invalid offer: {e}")
    return request_new_offer()
```

### 2. Timeout Management
```python
import signal
from contextlib import contextmanager

@contextmanager
def timeout(seconds):
    def timeout_handler(signum, frame):
        raise TimeoutError("Negotiation timeout")
    
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)

# Use timeout
with timeout(300):  # 5 minutes
    result = run_negotiation()
```

### 3. Logging
```python
import logging

logging.basicConfig(
    filename='negotiation.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Log all offers
logger.info(f"Offer from {agent_name}: {offer.to_json_str()}")
```

## 📚 Additional Resources

- **AutoGen Documentation**: https://microsoft.github.io/autogen/
- **CrewAI Documentation**: https://docs.crewai.com/
- **Pydantic Documentation**: https://docs.pydantic.dev/
- **Game Theory Primer**: See README.md

## 💡 Examples

See the included example files:
- `example_schema_usage.py` - Pydantic schema examples
- `example_mediator.py` - Mediator intervention demo
- `negotiation_sim.py` - Complete simulation

---

For questions or issues, please open an issue on GitHub.
