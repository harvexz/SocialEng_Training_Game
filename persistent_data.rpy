init python:
    import csv
    import os
    import platform
    import sys

    def get_user_data_directory():
        """
        Returns a platform-specific directory where the game can save data files.
        
        Returns:
            str: Path to an appropriate directory for saving game data
        """
        try:
            system = platform.system()
            
            # Print debug info to the Ren'Py log
            print(f"System detected: {system}")
            
            if system == "Windows":
                # On Windows, use AppData/Roaming
                path = os.path.join(os.environ.get("APPDATA", ""), "CyberCorpGame")
                print(f"Windows path: {path}")
                return path
            elif system == "Darwin":  # macOS
                # On macOS, use ~/Library/Application Support or ~/Documents
                home = os.path.expanduser("~")
                app_support = os.path.join(home, "Library", "Application Support", "CyberCorpGame")
                documents = os.path.join(home, "Documents", "CyberCorpGame")
                
                print(f"macOS paths: App Support={app_support}, Documents={documents}")
                
                # Try to create app_support first, fall back to documents if needed
                try:
                    if not os.path.exists(app_support):
                        print(f"Creating directory: {app_support}")
                        os.makedirs(app_support)
                    return app_support
                except OSError as e:
                    print(f"Error creating App Support directory: {e}")
                    if not os.path.exists(documents):
                        print(f"Creating directory: {documents}")
                        os.makedirs(documents)
                    return documents
            else:  # Linux and others
                # On Linux, use ~/.local/share
                home = os.path.expanduser("~")
                data_dir = os.path.join(home, ".local", "share", "CyberCorpGame")
                
                print(f"Linux/other path: {data_dir}")
                
                if not os.path.exists(data_dir):
                    print(f"Creating directory: {data_dir}")
                    os.makedirs(data_dir)
                return data_dir
        except Exception as e:
            # If anything unexpected happens, fall back to a directory we know exists
            print(f"Unexpected error in get_user_data_directory: {e}")
            fallback_dir = os.path.dirname(config.savedir)
            print(f"Using fallback directory: {fallback_dir}")
            return fallback_dir

    if not hasattr(persistent, "game_progress") or persistent.game_progress is None:
        persistent.game_progress = {
            "current_level": "tutorial",  # Defaults to tutorial on first launch
            "completed_levels": [],
            "score": 0,
            "level_status": "",
            "replay_status": "",
            "levels_played": 0,
            "tutorial_seen": False,
            "temp_level": None  # Used to store the original level when playing a previous level
        }
    
    # Initialize achievements if not already present
    if not hasattr(persistent, "achievements") or persistent.achievements is None:
        persistent.achievements = {
            "quick_thinker": False,  # For making fast decisions
            "vigilant_observer": False,  # For correctly identifying multiple phishing attempts
            "security_expert": False,  # For completing all levels
            "perfect_score": False,  # For getting a perfect score on any level
            "level_three_master": False,  # For getting Expert rank in level 3
            "physical_security_expert": False,  # For successfully identifying and reporting a tailgating attempt in Level 4
            "detail_oriented": False   # For accurately remembering details about the intruder in Level 4
        }
    else:
        # Remove outdated achievements if they exist
        if "security_responder" in persistent.achievements:
            del persistent.achievements["security_responder"]
        if "defense_master" in persistent.achievements:
            del persistent.achievements["defense_master"]
    
    # Initialize rank data if not already present
    if not hasattr(persistent, "rank_data") or persistent.rank_data is None:
        persistent.rank_data = {
            "current_rank": "Novice",  # Novice, Intermediate, Expert, Elite
            "rank_thresholds": {
                "Novice": 0,
                "Intermediate": 50,
                "Expert": 100,
                "Elite": 275,
                "Master": 350,
                "Hacker": 600
            }
        }

    if not hasattr(persistent, "emails") or persistent.emails is None:
        persistent.all_emails_correct = False
        persistent.emails = [
            {
                "from": "Cyber Security Team <security@cybercorp.com>",
                "subject": "CyberCorp Security News - Best Practices & Updates",
                "body": "Dear CyberCorp Team,\n\nWelcome to this month's CyberCorp Security Newsletter. Our goal is to keep you informed about the latest security trends, threats, and best practices to help protect both our company and your personal information.\n\n**Key Updates:**\n\n1. **Our Official URLs:**\n   - https://www.cybercorp.com\n   - https://portal.cybercorp.com\n\n2. **Recognizing Genuine Emails:**\n   - Official CyberCorp emails will always come from '@cybercorp.com' domains.\n   - For security-related emails, look for addresses like 'security@cybercorp.com' or 'it-support@cybercorp.com'.\n\n3. **Security Tips:**\n   - Never click on suspicious links or download unexpected attachments.\n   - Always verify the sender's email address carefully.\n   - If in doubt, report suspicious emails to security@cybercorp.com.\n\nStay vigilant, and thank you for helping keep CyberCorp secure.\n\nBest regards,\nCyber Security Team",
                "is_phishing": False,
                "difficulty_level": 1,
                "is_external": False,
                "error_hint": "This is a legitimate security newsletter from the company domain with good security tips."
            },
            {
                "from": "IT Support <it-support@cybercorp.com>",
                "subject": "Your Password Will Expire Soon!",
                "body": "Dear user,\n\nWe have detected that your current password is set to expire within the next 24 hours. To maintain uninterrupted access to your account, please follow the link below to reset your password immediately:\n\n[www.cybercorp-security.com/reset-password]\n\nFailure to update your password may result in restricted access to key systems. If you believe this message was sent in error, contact IT Support directly.\n\nStay secure,\nIT Support Team",
                "is_phishing": True,
                "difficulty_level": 2,
                "is_external": False,
                "error_hint": "Check the URL! The domain is cybercorp-security.com, not cybercorp.com. Legitimate password resets come from the company domain."
            },
            {
                "from": "John.Doe@cybercorp.com",
                "subject": "Project Updates",
                "body": "Hey,\n\nI've compiled the latest updates on the project, including changes to the timeline and deliverables. Please review the attached document and let me know your thoughts before our next team meeting.\n\nThanks,\nJohn",
                "is_phishing": False,
                "difficulty_level": 1,
                "is_external": False,
                "error_hint": "This is a normal internal email from a coworker with appropriate context. No suspicious links or attachments are mentioned."
            },
            {
                "from": "HR Department <hr@cybercorp.com>",
                "subject": "Urgent: Employee Benefits Update",
                "body": "Dear CyberCorp Employee,\n\nDue to recent changes in our benefits provider's policies, we require all employees to review and acknowledge the updated terms. Please download the attached document and sign electronically by tomorrow:\n\n[hr-cybercorp.com/login]\n\nFailure to comply may affect your eligibility for certain benefits. If you have questions, please reach out to the HR team.\n\nBest regards,\nHR Department",
                "is_phishing": True,
                "difficulty_level": 3,
                "is_external": False,
                "error_hint": "Notice the suspicious link domain (hr-cybercorp.com instead of cybercorp.com) and the urgency creating pressure to act quickly."
            },
            {
                "from": "Marketing <newsletter@trustedsource.com>",
                "subject": "Company News - January Edition",
                "body": "Hello Team,\n\nWe're excited to share the January edition of the CyberCorp newsletter! Inside, you'll find highlights of recent company initiatives, employee achievements, and upcoming events. Stay informed and connected with your colleagues across departments.\n\nBest,\nThe Marketing Team",
                "is_phishing": False,
                "difficulty_level": 1,
                "is_external": True,
                "error_hint": "While this is from an external email, it's a trusted partner domain with no suspicious links or requests for action."
            },
            {
                "from": "Security Alert <alerts@cybercorp-security.com>",
                "subject": "Unusual Login Attempt Detected",
                "body": "Dear Employee,\n\nWe've identified an unusual login attempt to your CyberCorp account from an unfamiliar device located in a different region. For your security, we recommend verifying your account activity immediately by clicking the link below:\n\n[cybercorp-security.com/verify]\n\nIf this was not you, please secure your account promptly to prevent unauthorized access.\n\nRegards,\nCyberCorp Security Team",
                "is_phishing": True,
                "difficulty_level": 4,
                "is_external": False,
                "error_hint": "This uses fear tactics and urgency to trick you. The domain (cybercorp-security.com) is not the legitimate company domain."
            },
            {
                "from": "CEO <michael.smith@cybercorp.com>",
                "subject": "Quick Request - Urgent",
                "body": "Hi,\n\nI'm currently in a meeting and need you to process an urgent wire transfer for a new vendor. Please don't delay, as it's time-sensitive. Here are the payment details:\n\n[Vendor Payment Information]\n\nLet me know once it's done.\n\nThanks,\nMichael",
                "is_phishing": True,
                "difficulty_level": 5,
                "is_external": False,
                "error_hint": "CEO fraud! This uses authority and urgency to bypass normal financial controls. CEOs don't typically request urgent wire transfers via email."
            },
            {
                "from": "Jane.Doe@trustedpartner.com",
                "subject": "Meeting Rescheduled",
                "body": "Hello,\n\nI wanted to inform you that the meeting scheduled for tomorrow has been rescheduled to next Monday at 2 PM. Please update your calendar accordingly.\n\nIf this new time conflicts with your availability, let me know.\n\nBest regards,\nJane",
                "is_phishing": False,
                "difficulty_level": 1,
                "is_external": True,
                "error_hint": "This is a routine scheduling email with no suspicious requests, links, or urgency."
            },
            {
                "from": "Admin <admin@cybercorp-secure.com>",
                "subject": "Important Security Patch Required",
                "body": "Dear User,\n\nA critical security vulnerability has been identified in our system. To protect your data, it's imperative that you install the latest security patch immediately:\n\n[cybercorp-secure.com/update]\n\nFailure to apply this patch could result in compromised account security. Contact the IT Help Desk if you need assistance.\n\nRegards,\nIT Admin",
                "is_phishing": True,
                "difficulty_level": 3,
                "is_external": False,
                "error_hint": "The domain (cybercorp-secure.com) isn't the company domain. IT departments don't ask you to download 'security patches' via email links."
            },
            {
                "from": "Payroll Department <payroll@cybercorp.com>",
                "subject": "Your Payslip for January",
                "body": "Dear [Employee Name],\n\nYour January payslip is now available on the employee portal. To view your payslip, please log in using the following secure link:\n\n[www.cybercorp.com/employee-portal]\n\nIf you encounter any issues accessing your payslip, contact the Payroll Department for support.\n\nBest regards,\nPayroll Team",
                "is_phishing": False,
                "difficulty_level": 2,
                "is_external": False,
                "error_hint": "This is legitimate - the sender is from the company domain and the link points to the official company website."
            },
            {
                "from": "Help Desk <support@cybercorp.com>",
                "subject": "Mailbox Full: Action Required",
                "body": "Dear User,\n\nYour mailbox has reached 95% of its storage capacity. To avoid disruption in receiving future emails, please click the link below to manage your mailbox:\n\n[support-cybercorp.com/clean-mailbox]\n\nFailure to act may result in undelivered messages. Contact IT Support if you need assistance.\n\nBest,\nIT Help Desk",
                "is_phishing": True,
                "difficulty_level": 4,
                "is_external": False,
                "error_hint": "While the email appears to be from the company domain, the link is suspicious (support-cybercorp.com, not cybercorp.com)."
            }
        ]


    def save_progress():
        """Saves game progress automatically."""
        # Update rank based on score
        update_rank()
        # Check for achievements
        check_achievements()
        renpy.save_persistent()  # Save changes
        try:
            log_data() # Exports to csv
        except Exception as e:
            # Log the error but don't crash the game if writing fails
            error_msg = str(e)
            if "Read-only file system" in error_msg or "Permission denied" in error_msg:
                renpy.notify("Note: Could not save analytics data due to file permissions. Your game progress is still saved.")
            else:
                renpy.notify("Note: Analytics data could not be saved. Your game progress is still saved.")
            print(f"Error logging data: {e}")
    

    def update_rank():
        """Updates the player's rank based on their score."""
        score = persistent.game_progress["score"]

        if score >= persistent.rank_data["rank_thresholds"]["Hacker"]:
            persistent.rank_data["current_rank"] = "Hacker"
        elif score >= persistent.rank_data["rank_thresholds"]["Master"]:
            persistent.rank_data["current_rank"] = "Master"
        elif score >= persistent.rank_data["rank_thresholds"]["Elite"]:
            persistent.rank_data["current_rank"] = "Elite"
        elif score >= persistent.rank_data["rank_thresholds"]["Expert"]:
            persistent.rank_data["current_rank"] = "Expert"
        elif score >= persistent.rank_data["rank_thresholds"]["Intermediate"]:
            persistent.rank_data["current_rank"] = "Intermediate"
        else:
            persistent.rank_data["current_rank"] = "Novice"
    

    def check_achievements():
        """Checks and updates achievements based on game progress."""
        # Check for security expert achievement
        if len(persistent.game_progress["completed_levels"]) >= 3:
            if not persistent.achievements["security_expert"]:
                persistent.achievements["security_expert"] = True
                renpy.notify("Achievement Unlocked: Security Expert!")
        
        # Check for level three master achievement
        if "third_level" in persistent.game_progress["completed_levels"] and persistent.rank_data["current_rank"] == "Expert":
            if not persistent.achievements["level_three_master"]:
                persistent.achievements["level_three_master"] = True
                renpy.notify("Achievement Unlocked: Level Three Master!")
    

    def log_data():
        """Logs player data to CSV."""
        try:
            # Get the user-specific data directory
            data_dir = get_user_data_directory()
            
            # Create the directory if it doesn't exist
            if not os.path.exists(data_dir):
                try:
                    os.makedirs(data_dir)
                    print(f"Created data directory: {data_dir}")
                except Exception as e:
                    print(f"Error creating data directory: {e}")
                    raise
            
            # Create the filepath in the user's data directory
            filepath = os.path.join(data_dir, "player_data.csv")
            print(f"Attempting to write to: {filepath}")
            
            # Check if the file exists and create header if it doesn't
            file_exists = os.path.isfile(filepath)
            
            # Try to open and write to the file
            try:
                with open(filepath, "a", newline="") as file:
                    writer = csv.writer(file)
                    
                    # Write header if this is a new file
                    if not file_exists:
                        writer.writerow([
                            "Level", 
                            "Score", 
                            "Status",
                            "Replay Status",
                            "Rank"
                        ])
                    
                    # Write the player data
                    writer.writerow([
                        persistent.game_progress["current_level"],
                        persistent.game_progress["score"],
                        persistent.game_progress["level_status"],
                        persistent.game_progress["replay_status"],
                        persistent.rank_data["current_rank"]
                    ])
                print(f"Successfully wrote data to {filepath}")
            except Exception as e:
                print(f"Error writing to CSV file {filepath}: {e}")
                raise
                
        except Exception as e:
            # Print the error for debugging but allow the game to continue
            print(f"Error in log_data: {e}")
            raise  # Re-raise to be caught by save_progress
    

    def check_email(reported_as_phishing):
        """
        Handles reporting as phising or not
        Marks the email as read and (if correct) answered_correctly
        If every email is answered correctly, level 2 is completed
        !!!May want to move to script.rpy!!!
        """
        max_difficulty = 5
        email = persistent.emails[selected_email_index]
        difficulty = email.get("difficulty_level", 1)  # gets difficulty, defult to 1
        email["read"] = True
        all_correct = persistent.all_emails_correct
        
        if reported_as_phishing == email["is_phishing"]:
            if not email.get("scored", False):  # only get points if not already scored
                renpy.notify("Correct! You scored {} points.".format(difficulty))
                persistent.game_progress["score"] += difficulty  # score based on difficulty
                email["scored"] = True
            else:
                renpy.notify("Correct! No points scored for reapeated answers.")
            email["answered_correctly"] = True
            
            # Check for vigilant observer achievement
            correct_count = sum(1 for e in persistent.emails if e.get("answered_correctly", False))
            if correct_count >= 5 and not persistent.achievements["vigilant_observer"]:
                persistent.achievements["vigilant_observer"] = True
                renpy.notify("Achievement Unlocked: Vigilant Observer!")
        else:
            penalty = max_difficulty - difficulty
            error_hint = email.get("error_hint", "Always check the sender and content carefully.")
            renpy.notify("Incorrect. This email was " + ("safe." if not email["is_phishing"] else "a phishing attempt!") + " {} points lost. \n{}. Try that one again!".format(penalty, error_hint))
            persistent.game_progress["score"] -= penalty  # score loss based on difficulty 
            email["answered_correctly"] = False
        
        # persistent.emails[selected_email_index]["checked"] = True  # replaced by email["read"] = True (keeping incase)
        persistent.game_progress["level_status"] = "email check"
        save_progress()

        # check if all emails answered correctly
        all_correct = True
        for e in persistent.emails:
            if not e.get("answered_correctly", False):
                all_correct = False
                break
        if all_correct:
            renpy.notify("All emails have been correctly identified. Level complete!")
            # call the level_complete label
            persistent.all_emails_correct = all_correct
            
            # Check for perfect score achievement
            if all(e.get("scored", False) for e in persistent.emails) and not persistent.achievements["perfect_score"]:
                persistent.achievements["perfect_score"] = True
                renpy.notify("Achievement Unlocked: Perfect Score!")
                
            renpy.call_in_new_context("level_complete")
            
    
    def award_quick_thinker():
        """Awards the Quick Thinker achievement for making fast decisions."""
        if not persistent.achievements["quick_thinker"]:
            persistent.achievements["quick_thinker"] = True
            renpy.notify("Achievement Unlocked: Quick Thinker!")
            save_progress()

    def reset_email_status():
        """Resets the status of all emails when replaying Level 2."""
        if hasattr(persistent, "emails") and persistent.emails:
            for email in persistent.emails:
                if "read" in email:
                    del email["read"]
                if "answered_correctly" in email:
                    del email["answered_correctly"]
                if "scored" in email:
                    del email["scored"]
            
            # Reset the all_emails_correct flag
            persistent.all_emails_correct = False
            renpy.notify("Email status has been reset for replay")

    def delete_analytics_data():
        """
        Utility function to delete the analytics data file.
        This can be exposed through a settings menu if needed.
        
        Returns:
            bool: True if the file was deleted successfully, False otherwise
        """
        try:
            data_dir = get_user_data_directory()
            filepath = os.path.join(data_dir, "player_data.csv")
            
            if os.path.exists(filepath):
                os.remove(filepath)
                print(f"Deleted analytics data file: {filepath}")
                renpy.notify("Analytics data has been deleted.")
                return True
            else:
                print(f"No analytics data file found at: {filepath}")
                renpy.notify("No analytics data found to delete.")
                return False
        except Exception as e:
            print(f"Error deleting analytics data: {e}")
            renpy.notify("Error deleting analytics data. See log for details.")
            return False
