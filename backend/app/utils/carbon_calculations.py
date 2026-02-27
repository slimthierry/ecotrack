"""
Helper functions for carbon calculation conversions and comparisons.
"""

# Average annual CO2 per capita (global average is about 4.7 tonnes, EU ~6.8, US ~15.5)
GLOBAL_AVERAGE_DAILY_KG = 12.88  # ~4700 kg / 365 days
EU_AVERAGE_DAILY_KG = 18.63  # ~6800 kg / 365 days
US_AVERAGE_DAILY_KG = 42.47  # ~15500 kg / 365 days

# One mature tree absorbs approximately 22 kg CO2 per year
TREE_ANNUAL_ABSORPTION_KG = 22.0

# Average car emits about 0.21 kg CO2 per km
CAR_EMISSION_PER_KM = 0.21


def kg_to_trees_equivalent(carbon_kg: float) -> float:
    """
    Convert kg of CO2 to the number of trees needed to absorb
    that amount in one year.
    """
    if carbon_kg <= 0:
        return 0.0
    return round(carbon_kg / TREE_ANNUAL_ABSORPTION_KG, 2)


def kg_to_driving_km(carbon_kg: float) -> float:
    """
    Convert kg of CO2 to equivalent driving distance in km.
    """
    if carbon_kg <= 0:
        return 0.0
    return round(carbon_kg / CAR_EMISSION_PER_KM, 1)


def format_carbon(carbon_kg: float) -> str:
    """
    Format carbon amount with appropriate unit (g, kg, or tonnes).
    """
    if carbon_kg < 0.001:
        return "0 g CO2"
    elif carbon_kg < 1.0:
        return f"{carbon_kg * 1000:.0f} g CO2"
    elif carbon_kg < 1000.0:
        return f"{carbon_kg:.2f} kg CO2"
    else:
        return f"{carbon_kg / 1000:.2f} tonnes CO2"


def compare_to_average(
    daily_carbon_kg: float, region: str = "global"
) -> dict:
    """
    Compare a user's daily carbon footprint to regional averages.
    Returns a dict with comparison percentage and message.
    """
    averages = {
        "global": GLOBAL_AVERAGE_DAILY_KG,
        "eu": EU_AVERAGE_DAILY_KG,
        "us": US_AVERAGE_DAILY_KG,
    }

    average = averages.get(region.lower(), GLOBAL_AVERAGE_DAILY_KG)

    if average == 0:
        percentage = 0.0
    else:
        percentage = (daily_carbon_kg / average) * 100

    if percentage < 50:
        level = "excellent"
        message = f"Your carbon footprint is {100 - percentage:.0f}% below the {region} average. Excellent work!"
    elif percentage < 80:
        level = "good"
        message = f"Your carbon footprint is {100 - percentage:.0f}% below the {region} average. Good job!"
    elif percentage < 100:
        level = "average"
        message = f"Your carbon footprint is close to the {region} average. Small changes can help!"
    elif percentage < 150:
        level = "above_average"
        message = f"Your carbon footprint is {percentage - 100:.0f}% above the {region} average. Consider reducing high-impact activities."
    else:
        level = "high"
        message = f"Your carbon footprint is {percentage - 100:.0f}% above the {region} average. Check our tips for ways to reduce it."

    return {
        "daily_carbon_kg": round(daily_carbon_kg, 2),
        "average_daily_kg": round(average, 2),
        "percentage_of_average": round(percentage, 1),
        "level": level,
        "message": message,
    }


def calculate_eco_score(total_carbon_saved: float, streak_days: int, achievements_count: int) -> int:
    """
    Calculate an eco score (0-100) based on user's overall performance.
    Factors: carbon saved, streak consistency, and achievements.
    """
    # Carbon saved component (0-40 points): 1 point per 25kg saved, max 40
    carbon_points = min(int(total_carbon_saved / 25), 40)

    # Streak component (0-30 points): 1 point per day, max 30
    streak_points = min(streak_days, 30)

    # Achievement component (0-30 points): 3 points per achievement, max 30
    achievement_points = min(achievements_count * 3, 30)

    return min(carbon_points + streak_points + achievement_points, 100)
