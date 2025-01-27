init python:
    import csv
    import os

    if not hasattr(persistent, "game_progress") or persistent.game_progress is None:
        persistent.game_progress = {
            "current_level": "tutorial",  # Defaults to tutorial on first launch
            "completed_levels": [],
            "score": 0,
            "level_status": "",
            "replay_status": "",
            "levels_played": 0,
            "tutorial_seen": False
        }


    def save_progress():
        """Saves game progress automatically."""
        renpy.save_persistent()  # Save changes
        log_data() # Exports to csv
    

    def log_data():
        """Logs player data to CSV."""

        filepath = os.path.join(config.basedir, "player_data.csv")
        
        with open(filepath, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([
                persistent.game_progress["current_level"],
                persistent.game_progress["score"],
                persistent.game_progress["level_status"],
                persistent.game_progress["replay_status"]
            ])
