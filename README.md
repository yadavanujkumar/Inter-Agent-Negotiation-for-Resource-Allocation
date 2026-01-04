# Inter-Agent Negotiation for Resource Allocation

A sophisticated **Multi-Agent System (MAS)** implementing bilateral negotiation between specialized agents using game theory principles to achieve Pareto Optimal agreements.

## 🎯 Overview

This project demonstrates a complete bilateral negotiation system where a **Buyer Agent** and **Seller Agent** negotiate the price and quantity of GPU Compute Hours. A **Mediator Agent** monitors the negotiation and intervenes during stalemates to propose fair compromises.

## 🏗️ Architecture

### Agent Roles

1. **Buyer Agent**
   - Goal: Minimize cost
   - Constraint: Maximum budget of $500 per GPU hour
   - Strategy: Start low, gradually increase offers

2. **Seller Agent**
   - Goal: Maximize revenue
   - Constraint: Minimum reservation price of $350 per GPU hour
   - Strategy: Start high, gradually decrease price

3. **Mediator Agent**
   - Role: Stalemate resolution
   - Strategy: Proposes "Split the Difference" compromise
   - Triggers: After 5+ rounds with <2% price change

## 🔧 Technical Implementation

### Structured Communication Schema (Pydantic)

All agent communications use a validated JSON schema:

```python
{
    "offer_price": float,      # Price per GPU compute hour
    "quantity": int,            # Number of hours
    "reasoning": str,           # Justification for offer
    "is_final_offer": bool      # Final offer flag
}
```

### Key Features

- ✅ **Pydantic Validation**: Type-safe, validated communication
- ✅ **Stalemate Detection**: Automatic detection of negotiation deadlocks
- ✅ **Mediator Logic**: "Split the Difference" compromise mechanism
- ✅ **ZOPA Analysis**: Zone of Possible Agreement visualization
- ✅ **Pareto Optimality**: Ensures mutually beneficial outcomes
- ✅ **Visualization**: Beautiful negotiation path charts

## 📦 Installation

### Prerequisites

- Python 3.8+
- pip

### Setup

```bash
# Clone the repository
git clone https://github.com/YOUR-USERNAME/Inter-Agent-Negotiation-for-Resource-Allocation.git
cd Inter-Agent-Negotiation-for-Resource-Allocation

# Install dependencies
pip install -r requirements.txt
```

## 🚀 Usage

### Run the Negotiation Simulation

```bash
python negotiation_sim.py
```

### Expected Output

The script will:
1. Initialize three agents (Buyer, Seller, Mediator)
2. Execute up to 10 negotiation rounds
3. Display all offers with structured JSON
4. Detect stalemates and trigger mediation if needed
5. Generate a visualization (`negotiation_path.png`)
6. Display Pareto optimality analysis

### Example Output

```
================================================================================
BILATERAL NEGOTIATION SYSTEM FOR GPU COMPUTE HOURS
================================================================================

Initializing agents...
✓ Buyer_Agent initialized (Budget: $500.0)
✓ Seller_Agent initialized (Reservation: $350.0)
✓ Mediator_Agent initialized

ROUND 1:
----------------------------------------
Buyer → {"offer_price":370.0,"quantity":100,"reasoning":"Opening offer...","is_final_offer":false}

...

✓ Agreement Status: SUCCESS
✓ Final Price: $432.00 per GPU compute hour
✓ Quantity: 100 hours
✓ Total Cost: $43200.00
✓ PARETO OPTIMAL AGREEMENT ACHIEVED ✓
```

## 📊 Visualization

The system generates a comprehensive negotiation path visualization showing:

- **Buyer offers** (blue line with circles)
- **Seller offers** (red line with squares)
- **Negotiation path** (green dashed line)
- **ZOPA** (Zone of Possible Agreement - shaded green area)
- **Budget constraints** (horizontal reference lines)

> **Note**: The visualization file `negotiation_path.png` is automatically generated when you run the simulation script.

## 🔬 Game Theory Concepts

### Pareto Optimality

An agreement is **Pareto Optimal** when no party can improve their position without making the other party worse off. Our system ensures:

- Final price is within ZOPA ($350-$500)
- Buyer's budget constraint is satisfied
- Seller's reservation price is met
- Both parties benefit from the negotiation

### ZOPA (Zone of Possible Agreement)

The ZOPA is the range where both parties can potentially agree:
- **Lower bound**: $350 (Seller's reservation price)
- **Upper bound**: $500 (Buyer's maximum budget)
- **Overlap**: $150 range for negotiation

### Stalemate Detection

The system detects stalemates using:
- **Threshold**: 5 consecutive rounds
- **Price change**: <2% variation
- **Resolution**: Mediator proposes midpoint compromise

## 🧪 Testing

Run the simulation to verify all components:

```bash
python negotiation_sim.py
```

Check for:
- ✅ Valid Pydantic schema validation
- ✅ Successful agent initialization
- ✅ Structured JSON communication
- ✅ Stalemate detection (if triggered)
- ✅ Mediator intervention (if triggered)
- ✅ Pareto optimal outcome
- ✅ Visualization generation

## 🎓 Educational Value

This project demonstrates:

1. **Multi-Agent Systems**: Autonomous agents with distinct goals
2. **Game Theory**: Nash equilibrium, Pareto optimality, ZOPA
3. **Structured Communication**: Pydantic schemas for type safety
4. **Conflict Resolution**: Mediation strategies
5. **Data Visualization**: matplotlib for insights
6. **Python Best Practices**: Type hints, docstrings, clean code

## 🔌 Framework Integration

The current implementation is framework-agnostic and can be integrated with:

### AutoGen
```python
from autogen import AssistantAgent
# Use the Pydantic schemas and negotiation logic
# with AutoGen's conversational agents
```

### CrewAI
```python
from crewai import Agent, Task
# Integrate the negotiation protocol
# with CrewAI's agent orchestration
```

## 📄 Project Structure

```
Inter-Agent-Negotiation-for-Resource-Allocation/
├── negotiation_sim.py       # Main simulation script
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── LICENSE                   # License information
└── .gitignore               # Git ignore rules
```

## 🤝 Contributing

Contributions are welcome! Areas for enhancement:

- Additional negotiation strategies
- More complex resource types
- Multi-party negotiations
- Machine learning-based agent behaviors
- Real-time visualization
- Integration with actual LLM backends

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Author

**Yadav Anuj Kumar**

## 🙏 Acknowledgments

- Game Theory principles from Von Neumann and Morgenstern
- AutoGen framework by Microsoft Research
- Pydantic for data validation
- matplotlib for visualization

---

**Note**: This implementation demonstrates the complete negotiation protocol with all required components. For production use with actual LLM backends, configure the appropriate API keys for AutoGen or CrewAI frameworks.
