def apply_motion(character, motion_type, duration):
    """Automate motion for a character."""
    motions = {
        "walk": f"{character} walks for {duration} seconds.",
        "wave": f"{character} waves for {duration} seconds.",
        "jump": f"{character} jumps for {duration} seconds."
    }
    return motions.get(motion_type, "Unknown motion type")