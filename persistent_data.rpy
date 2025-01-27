init python:
    if not hasattr(persistent, "game_progress") or persistent.game_progress is None:
        persistent.game_progress = {
            "current_level": "tutorial",  # Defaults to tutorial on first launch
            "completed_levels": [],
            "score": 0,
            "tutorial_seen": False
        }

    def save_progress():
        """Saves game progress automatically."""
        renpy.save_persistent()  # Save changes
