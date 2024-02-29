def calculate_scale_factor(target_zone, reference_zone, reference_factor):
    """
    Calculate the scale factor based on the difference in UTM zones
    """
    # Each UTM zone spans 6 degrees of longitude
    zone_difference = abs(target_zone - reference_zone)

    # Assuming linear relationship between scale factor and zone difference
    scale_factor = reference_factor * (1 + (zone_difference * 0.028))

    return scale_factor

# Example usage:
target_zone = 32752
reference_zone = 32749
reference_factor = 1.25

scale_factor = calculate_scale_factor(target_zone, reference_zone, reference_factor)
print("Adjusted scale factor:", scale_factor)
