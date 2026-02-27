"""
Eco tips organized by category with potential carbon savings.
"""

ECO_TIPS: list[dict] = [
    # Transport tips
    {
        "title": "Cycle to work",
        "description": "Switching from driving to cycling for a 10km commute saves about 2.1 kg CO2 per trip. Over a year, that is over 500 kg saved.",
        "category": "transport",
        "potential_savings_kg": 2.1,
    },
    {
        "title": "Take public transit",
        "description": "Taking the bus instead of driving solo cuts your per-km emissions by over 50%. Trains are even better at 80% reduction.",
        "category": "transport",
        "potential_savings_kg": 1.2,
    },
    {
        "title": "Carpool with colleagues",
        "description": "Sharing a ride with just one other person halves your per-person transport emissions instantly.",
        "category": "transport",
        "potential_savings_kg": 1.05,
    },
    {
        "title": "Work from home one day a week",
        "description": "Eliminating one commute day per week can save 200-400 kg CO2 per year depending on your distance.",
        "category": "transport",
        "potential_savings_kg": 4.2,
    },
    {
        "title": "Consider an electric vehicle",
        "description": "Electric cars produce about 75% less CO2 per km compared to conventional cars when accounting for grid mix.",
        "category": "transport",
        "potential_savings_kg": 1.57,
    },
    # Food tips
    {
        "title": "Try Meatless Monday",
        "description": "Replacing one beef meal per week with a vegetarian option saves about 25 kg CO2 per meal. That is over 1,300 kg per year.",
        "category": "food",
        "potential_savings_kg": 25.3,
    },
    {
        "title": "Choose chicken over beef",
        "description": "Chicken produces about 75% less CO2 than beef per kg. A simple protein swap makes a big difference.",
        "category": "food",
        "potential_savings_kg": 20.1,
    },
    {
        "title": "Buy local and seasonal produce",
        "description": "Locally sourced, seasonal food avoids the high emissions from refrigerated transport and heated greenhouses.",
        "category": "food",
        "potential_savings_kg": 1.5,
    },
    {
        "title": "Reduce food waste",
        "description": "About 8-10% of global emissions come from food waste. Plan meals and use leftovers to cut your share.",
        "category": "food",
        "potential_savings_kg": 3.0,
    },
    {
        "title": "Try a vegan meal",
        "description": "A vegan meal produces about 50% less CO2 than a vegetarian meal and 95% less than a beef-based meal.",
        "category": "food",
        "potential_savings_kg": 0.8,
    },
    # Energy tips
    {
        "title": "Switch to LED bulbs",
        "description": "LED bulbs use 75% less energy than incandescent bulbs. Replacing 10 bulbs saves about 100 kWh per year.",
        "category": "energy",
        "potential_savings_kg": 23.3,
    },
    {
        "title": "Lower your thermostat by 1 degree",
        "description": "Reducing heating by just 1 degree C can save about 300 kg CO2 per year for an average home.",
        "category": "energy",
        "potential_savings_kg": 300.0,
    },
    {
        "title": "Unplug standby electronics",
        "description": "Standby power accounts for 5-10% of residential energy use. Use power strips to easily cut phantom loads.",
        "category": "energy",
        "potential_savings_kg": 50.0,
    },
    {
        "title": "Air dry your laundry",
        "description": "Skipping the dryer for one load saves about 2.4 kg CO2. Air drying 100 loads per year saves 240 kg.",
        "category": "energy",
        "potential_savings_kg": 2.4,
    },
    {
        "title": "Switch to a green energy provider",
        "description": "Renewable energy tariffs can reduce your electricity carbon footprint by up to 100%.",
        "category": "energy",
        "potential_savings_kg": 1000.0,
    },
    # Purchase tips
    {
        "title": "Buy second-hand clothing",
        "description": "Second-hand clothing avoids the 10 kg CO2 per item from manufacturing. Thrift shopping is both eco and budget friendly.",
        "category": "purchase",
        "potential_savings_kg": 10.0,
    },
    {
        "title": "Repair instead of replace",
        "description": "Repairing electronics instead of buying new saves an average of 50 kg CO2 per device.",
        "category": "purchase",
        "potential_savings_kg": 50.0,
    },
    {
        "title": "Choose durable products",
        "description": "Buying higher quality items that last twice as long effectively halves the manufacturing emissions per year of use.",
        "category": "purchase",
        "potential_savings_kg": 15.0,
    },
    {
        "title": "Borrow or rent rarely-used items",
        "description": "Tools, party supplies, and sporting equipment can be borrowed instead of bought, avoiding manufacturing emissions entirely.",
        "category": "purchase",
        "potential_savings_kg": 20.0,
    },
]


def get_tips_by_category(category: str) -> list[dict]:
    """Get eco tips filtered by category."""
    return [tip for tip in ECO_TIPS if tip["category"] == category.lower()]


def get_random_tips(count: int = 3) -> list[dict]:
    """Get a selection of random eco tips."""
    import random
    return random.sample(ECO_TIPS, min(count, len(ECO_TIPS)))


def get_all_tips() -> list[dict]:
    """Get all eco tips."""
    return ECO_TIPS
