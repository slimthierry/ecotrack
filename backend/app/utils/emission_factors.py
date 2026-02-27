"""
Emission factors for carbon footprint calculations.
Values are based on widely cited sources (EPA, DEFRA, IPCC).
All values are in kg CO2e per unit specified.
"""

EMISSION_FACTORS: dict[str, dict[str, dict]] = {
    "transport": {
        "car": {
            "factor": 0.21,
            "unit": "km",
            "description": "Average petrol/diesel car emission per km",
        },
        "bus": {
            "factor": 0.089,
            "unit": "km",
            "description": "Average bus emission per passenger-km",
        },
        "train": {
            "factor": 0.041,
            "unit": "km",
            "description": "Average train emission per passenger-km",
        },
        "plane": {
            "factor": 0.255,
            "unit": "km",
            "description": "Average domestic flight emission per passenger-km",
        },
        "bike": {
            "factor": 0.0,
            "unit": "km",
            "description": "Zero emissions cycling",
        },
        "walk": {
            "factor": 0.0,
            "unit": "km",
            "description": "Zero emissions walking",
        },
        "electric_car": {
            "factor": 0.053,
            "unit": "km",
            "description": "Average electric vehicle emission per km (including grid mix)",
        },
    },
    "food": {
        "beef": {
            "factor": 27.0,
            "unit": "kg",
            "description": "Beef production emissions per kg",
        },
        "chicken": {
            "factor": 6.9,
            "unit": "kg",
            "description": "Chicken production emissions per kg",
        },
        "pork": {
            "factor": 12.1,
            "unit": "kg",
            "description": "Pork production emissions per kg",
        },
        "fish": {
            "factor": 6.1,
            "unit": "kg",
            "description": "Fish production emissions per kg",
        },
        "vegetarian_meal": {
            "factor": 1.7,
            "unit": "meal",
            "description": "Average vegetarian meal emissions",
        },
        "vegan_meal": {
            "factor": 0.9,
            "unit": "meal",
            "description": "Average vegan meal emissions",
        },
    },
    "energy": {
        "electricity": {
            "factor": 0.233,
            "unit": "kWh",
            "description": "Average grid electricity emissions per kWh",
        },
        "natural_gas": {
            "factor": 2.0,
            "unit": "m3",
            "description": "Natural gas combustion emissions per cubic meter",
        },
        "heating_oil": {
            "factor": 2.68,
            "unit": "L",
            "description": "Heating oil combustion emissions per liter",
        },
    },
    "purchase": {
        "clothing": {
            "factor": 10.0,
            "unit": "item",
            "description": "Average clothing item production emissions",
        },
        "electronics": {
            "factor": 50.0,
            "unit": "item",
            "description": "Average electronics item production emissions",
        },
        "furniture": {
            "factor": 30.0,
            "unit": "item",
            "description": "Average furniture item production emissions",
        },
    },
}


def get_emission_factor(category: str, sub_category: str) -> dict | None:
    """Get the emission factor data for a given category and sub-category."""
    category_data = EMISSION_FACTORS.get(category.lower())
    if category_data is None:
        return None
    return category_data.get(sub_category.lower())


def get_all_categories() -> list[str]:
    """Return all available emission factor categories."""
    return list(EMISSION_FACTORS.keys())


def get_sub_categories(category: str) -> list[str]:
    """Return all sub-categories for a given category."""
    category_data = EMISSION_FACTORS.get(category.lower())
    if category_data is None:
        return []
    return list(category_data.keys())
