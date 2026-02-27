from app.utils.emission_factors import get_emission_factor


def calculate_carbon(
    category: str, sub_category: str, quantity: float, unit: str
) -> float:
    """
    Calculate carbon emissions in kg CO2e for a given activity.

    Args:
        category: The activity category (transport, food, energy, purchase).
        sub_category: The specific sub-category (car, beef, electricity, etc.).
        quantity: The amount of the activity.
        unit: The unit of measurement (should match the emission factor unit).

    Returns:
        Carbon emissions in kg CO2e.

    Raises:
        ValueError: If the category/sub_category combination is not found.
    """
    factor_data = get_emission_factor(category, sub_category)

    if factor_data is None:
        raise ValueError(
            f"No emission factor found for category='{category}', "
            f"sub_category='{sub_category}'. "
            f"Check available categories and sub-categories."
        )

    factor = factor_data["factor"]
    expected_unit = factor_data["unit"]

    # Validate that units are compatible
    if unit.lower() != expected_unit.lower():
        # Try to handle common unit conversions
        carbon_kg = _convert_and_calculate(factor, quantity, unit, expected_unit)
    else:
        carbon_kg = quantity * factor

    return round(max(carbon_kg, 0.0), 4)


def _convert_and_calculate(
    factor: float, quantity: float, provided_unit: str, expected_unit: str
) -> float:
    """
    Handle basic unit conversions when the user provides a different unit
    than the emission factor expects.
    """
    conversions = {
        ("mi", "km"): 1.60934,
        ("miles", "km"): 1.60934,
        ("lb", "kg"): 0.453592,
        ("lbs", "kg"): 0.453592,
        ("gal", "L"): 3.78541,
        ("gallons", "L"): 3.78541,
        ("ft3", "m3"): 0.0283168,
    }

    conversion_key = (provided_unit.lower(), expected_unit.lower())
    conversion_factor = conversions.get(conversion_key)

    if conversion_factor is not None:
        converted_quantity = quantity * conversion_factor
        return converted_quantity * factor

    # If no conversion found, use the quantity as-is with a warning
    return quantity * factor
