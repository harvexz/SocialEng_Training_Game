# The script of the game goes in this file.

# Timer scoring function - moved to global scope to fix loading error
init python:
    def timer_score(response_time, score_variable):
        """
        Calculates and adds score based on response time.
        
        Args:
            response_time: Time taken to respond
            score_variable: The variable to add points to (e.g., 'phone_score')
        
        Returns:
            The number of points awarded
        """
        # Stop the timer
        timer_active = False
        renpy.hide_screen("countdown_timer")
        
        # Calculate points based on response time
        if response_time < 5.0:
            bonus = 3
            renpy.notify("Quick response! +3 bonus points")
            # Award quick_thinker achievement if response was fast
            award_quick_thinker()
        elif response_time < 10.0:
            bonus = 2
            renpy.notify("Good response time! +2 bonus points")
        else:
            bonus = 1
            renpy.notify("Correct choice! +1 bonus point")
        
        # Add points to the specified score variable
        total_points = bonus
        globals()[score_variable] += total_points
        
        return total_points
        
    # Global variable to track which challenge the player is currently in
    current_challenge = ""

# Declare characters used by this game. The color argument colorizes the
# name of the character.

define player = Character("You", image = "player happy", kind = bubble, colour="#3b94ed")
define networker = Character("Alex", image = "networker normal", kind = bubble)


# The game starts here.


label start:
    if not persistent.game_progress["tutorial_seen"]:
        jump tutorial
    else:
        jump main_menu


label tutorial:

    scene bg personal_office

    "Welcome to the game, Let's show you how to play! (click to continue)"
    "Firstly, you can click anyware on the screen to continue through each dialog."
    "Or press any button on your keyboad!"

    "Secondly, if you ever miss something, you can click the small back button just below this text!"

    show player happy
    "Hi, I'm the character you will be playing as."

    "You will see a series of scenarios, each with a different challenge."
    "You will need to make decisions to protect the company from cyber threats."
    "You will be scored based on your decisions and the time it takes you to make them."
    "You will also be able to earn achievements for your actions."

    "For most challanges, you will have to interact in some way! For example you might have to decide what to say next!"

    show player happy at left

    menu:
        "I'm ready":
            "Do you concent for your data to be anonymously used?"

            menu:
                "Yes, my data can be used anonymously":
                    "Amazing! Let's get started!"
                    "We will jump back to the main menu, where you can start the next level!"
                    if not persistent.game_progress["tutorial_seen"]:
                        $ persistent.game_progress["tutorial_seen"] = True
                        $ persistent.game_progress["level_status"] = "Conset Given"
                        $ save_progress()
                        $ persistent.game_progress["current_level"] = "first_level"  # Set next level
                    else:
                        # Check if we're returning from a previous level selection
                        if hasattr(persistent.game_progress, "temp_level") and persistent.game_progress["temp_level"]:
                            $ persistent.game_progress["current_level"] = persistent.game_progress["temp_level"]
                            $ persistent.game_progress["temp_level"] = None
                    return
                
                "No, I don't want my data to be used":
                    "That's okay, sadly you won't be able to play then!"
                    jump tutorial
        
        "Wait im confused... say that again":
            jump tutorial
    return



label level_complete:
    # Updating data for analysis and game save
    ## Updates for level completed

    "Level Complete! - Super easy, we will take you back to the main menu so you can continue!"
    if persistent.game_progress["current_level"] not in persistent.game_progress["completed_levels"]:
        $ persistent.game_progress["completed_levels"].append(persistent.game_progress["current_level"])
        $ persistent.game_progress["score"] += 20 # Add to score
        $ persistent.game_progress["replay_status"] = "not replay"
    else:
        $ persistent.game_progress["replay_status"] = "replay"
        $ persistent.game_progress["score"] += 1 # Add to score
    
    $ persistent.game_progress["level_status"] = "complete"
    $ save_progress()

    # Check if we're returning from a previous level
    if hasattr(persistent.game_progress, "temp_level") and persistent.game_progress["temp_level"]:
        $ persistent.game_progress["current_level"] = persistent.game_progress["temp_level"]
        $ persistent.game_progress["temp_level"] = None
    # Otherwise, update the current level pointer based on which level just finished
    else:
        if persistent.game_progress["current_level"] == "first_level":
            $ persistent.game_progress["current_level"] = "second_level"
        elif persistent.game_progress["current_level"] == "second_level":
            $ persistent.game_progress["current_level"] = "third_level"
        elif persistent.game_progress["current_level"] == "third_level":
            $ persistent.game_progress["current_level"] = "fourth_level"
        elif persistent.game_progress["current_level"] == "fourth_level":
            $ persistent.game_progress["current_level"] = "fourth_level"
    
    return


label level_failed:
    # Updating data for analysis and game save
    ## Updates for level failed
    if persistent.game_progress["current_level"] in persistent.game_progress["completed_levels"]:
        $ persistent.game_progress["replay_status"] = "replay"  
    else:
        $ persistent.game_progress["replay_status"] = "not replay"

    $ persistent.game_progress["level_status"] = "failed"
    $ persistent.game_progress["score"] -= 5 # Add to score
    
    $ save_progress()
    return


############################## FIRST LEVEL ##############################
label first_level:

    # $ persistent.game_progress["current_level"] = "level_1"  # Potentiall not needed after fix

    scene bg office
    show screen top_bar
    show player happy
    with fade

    "Another day at the office. Just need to finish up this report before the end of the day..."

    show player happy at left
    show networker normal at right
    with fade

    networker "Hey there! Sorry to bother you. I'm Alex from IT. We've got a critical server issue and I need access to the server room right away."

    menu:
        "Oh, sure! Let me unlock it for you.":  
            jump access_granted

        "I don't recognize you. Can I see your ID?":
            jump request_id

        "We usually get emails about IT maintenance. I didn't see one. Who sent you?":
            jump verify_story
    
    return


label access_granted:

    show networker happy

    networker "Awesome, thanks! I appreciate it."

    show player happy

    player "No problem. Hope you fix the issue quickly."

    scene bg server_room
    show networker happy
    with fade

    networker "And... we're in! Thanks again."

    # Player failed the test.
    hide networker
    show player shock at left
    show boss at right
    "You allowed an unauthorized person into the server room. If this were real, sensitive company data could now be compromised."
    "LEVEL FAILED!"

    $ persistent.game_progress["score"] -= 5
    $ save_progress()
    
    jump level_failed

    return


label request_id:

    show networker happy

    networker "Uh, yeah, of course. Let me just find it… *pats pockets awkwardly* I think I left it in my car."

    menu:
        "No ID, no access. Company policy.":  
            jump deny_access

        "That's fine, just give me your name and I'll check the employee database.":  
            jump check_database


label verify_story:

    show networker happy

    networker "Oh, right! Yeah, you wouldn't have seen the email yet, it was just sent out. Mike from IT Security asked me to come fix it."

    menu:
        "Okay, let me just call Mike to confirm.":  
            jump call_supervisor

        "That makes sense. I'll let you in.":  
            jump access_granted


label deny_access:

    show networker angry

    networker "Look, I don't have time for this. The server is down and it's costing the company money. Just let me in!"

    menu:
        "I'm following protocol. You need to verify your identity first.":  
            jump insist_policy

        "Fine, go ahead.":  
            jump access_granted


label check_database:

    show player happy

    player "Give me a second, I'll look you up in the employee database."

    show networker sad

    networker "Uh… you know what? I just remembered, I need to check something outside first. I'll be back."
    hide networker

    show player happy

    "You watch as the 'IT technician' quickly walks away. Something felt off about that encounter."

    "CONGRATULATIONS! You stopped a potential social engineering attack by verifying identity."
    
    jump level_complete

    return


label call_supervisor:

    show player happy

    player "I'll just give Mike a quick call to confirm you're supposed to be here."

    show networker sad

    networker "Uh… you know what? Never mind. I think I got the wrong department."

    hide networker

    "The supposed IT worker quickly exits the building."

    "GREAT JOB! You followed security procedures and prevented an unauthorized entry attempt."

    jump level_complete


label insist_policy:

    show networker angry

    networker "This is ridiculous! I'll report you for slowing down IT work!"

    player "Go ahead. I'll be happy to explain my actions to my supervisor."

    hide networker

    "The person storms off angrily. Later, IT confirms they never sent anyone, meaning you just stopped an attempted breach."

    "EXCELLENT WORK! You enforced security policies and protected company assets."

    jump level_complete

    return


############################## SECOND LEVEL ##############################

label second_level:
    # $ persistent.game_progress["current_level"] = "level_2"
    
    scene bg office
    show screen top_bar
    show player happy
    "Work work work... It never seems to stop."
    "Your Boss has asked you to check your email inbox for potential phishing emails."
    "Carefully examine each email and report any suspicious activity."
    "Take your time, and check out the first email for some tips on what to look for!"

    "Hint - Once you correctly guess an email, you will see the little blue dot dissapear"

    hide player happy
    scene bg personal_office
    show screen email_inbox
    
    "Click to continue..."
    show player happy
    "Well done, you identified the emails correctly!! first time I hope..."
    "You will now return to the menu..."
    
    # Check if we're returning from a previous level selection
    if hasattr(persistent.game_progress, "temp_level") and persistent.game_progress["temp_level"]:
        $ persistent.game_progress["current_level"] = persistent.game_progress["temp_level"]
        $ persistent.game_progress["temp_level"] = None
    
    return

############################## THIRD LEVEL ##############################

label third_level:
    # Set current level
    scene bg office
    show screen top_bar
    show player happy
    with fade
    
    "Welcome to Level 3 – You're getting the idea of this pretty well"
    "You might notice you're gaining score up there!"
    "This level, you will get more score, the faster you are..."
    "But remember, be too fast, and you might make a mistake!"

    "Let's see what busy work you have to get done today!"
    
    # Initialize level variables
    $ phone_score = 0
    $ chat_score = 0
    $ document_score = 0
    $ time_bonus = 0
    
    # Start with the phone call challenge
    jump phone_call_challenge
    
label phone_call_challenge:
    scene bg office
    show screen top_bar
    show player happy
    with fade
    
    "Your desk phone rings..."
    
    show screen phone_interface
    with dissolve
    
    
    "Unknown Caller" "Hello, this is Dave from the IT department. We're conducting a security audit and need to verify some information."
    
    # Set the current challenge for timeout handling
    $ current_challenge = "phone_call"
    
    # Begin timer
    $ timer_duration = 20.0  # 20 seconds
    $ timer_active = True
    $ start_time = renpy.time.time()

    show screen countdown_timer(timer_duration)

    menu:
        "How can I help you?":
            $ response_time = renpy.time.time() - start_time
            $ timer_score(response_time, "phone_score")
            jump phone_call_continue
            
        "Can I get your employee ID first?":
            $ response_time = renpy.time.time() - start_time
            $ timer_score(response_time, "phone_score")
            jump phone_call_verify
            
        "I'm busy right now, can you email me instead?":
            $ response_time = renpy.time.time() - start_time
            $ timer_score(response_time, "phone_score")
            jump phone_call_redirect
            
        "Time's up!":
            $ timer_active = False
            hide screen countdown_timer
            jump phone_call_timeout

label phone_call_timeout:
    "You hesitated too long and the caller became more insistent."
    "Unknown Caller" "Hello? Are you there? This is urgent - we need your credentials now to prevent a security breach!"
    
    # Begin timer
    $ timer_duration = 20.0  # 20 seconds
    $ timer_active = True
    $ start_time = renpy.time.time()

    show screen countdown_timer(timer_duration)

    menu:
        "Sorry, I was distracted. What do you need?":
            $ response_time = renpy.time.time() - start_time
            $ timer_score(response_time, "phone_score")
            jump phone_call_continue
        "I need to verify who you are first. Let me call the IT helpdesk.":
            $ response_time = renpy.time.time() - start_time
            $ timer_score(response_time, "phone_score")
            jump phone_call_success
    
label phone_call_verify:
    
    "Unknown Caller" "Uh... I don't have it on me right now. But this is urgent - we need to verify your network credentials immediately."
    
    # Set the current challenge for timeout handling
    $ current_challenge = "phone_call_verify"
    
    # Begin timer
    $ timer_duration = 20.0  # 20 seconds
    $ timer_active = True
    $ start_time = renpy.time.time()

    show screen countdown_timer(timer_duration)

    menu:
        "Okay, what do you need to know?":
            $ response_time = renpy.time.time() - start_time
            $ timer_score(response_time, "phone_score")
            jump phone_call_continue
        "I'll need to verify who you are first. Let me call the IT helpdesk and confirm.":
            $ response_time = renpy.time.time() - start_time
            $ timer_score(response_time, "phone_score")
            jump phone_call_success
        "Can you tell me who your Boss is?":
            $ response_time = renpy.time.time() - start_time
            $ timer_score(response_time, "phone_score")
            jump phone_call_manager
    
label phone_call_manager:
    "Unknown Caller" "It's... uh... John. John Smith. Look, we're dealing with a potential security breach and need your password right away."
    
    # Set the current challenge for timeout handling
    $ current_challenge = "phone_call_manager"
    
    # Begin timer
    $ timer_duration = 20.0  # 20 seconds
    $ timer_active = True
    $ start_time = renpy.time.time()

    menu:
        "Okay, my password is...":
            jump phone_call_fail
        "I'm not comfortable sharing my password. I'll contact IT directly.":
            $ response_time = renpy.time.time() - start_time
            $ timer_score(response_time, "phone_score")
            jump phone_call_success
        "Let me speak with John first.":
            $ response_time = renpy.time.time() - start_time
            $ timer_score(response_time, "phone_score")
            jump phone_call_success
    
label phone_call_redirect:
    "Unknown Caller" "This is time-sensitive and can't wait for an email. We need to verify your account details now to prevent unauthorized access."
    
    # Set the current challenge for timeout handling
    $ current_challenge = "phone_call_redirect"
    
    # Begin timer
    $ timer_duration = 20.0  # 20 seconds
    $ timer_active = True
    $ start_time = renpy.time.time()

    show screen countdown_timer(timer_duration)

    menu:
        "Alright, what information do you need?":
            $ response_time = renpy.time.time() - start_time
            $ timer_score(response_time, "phone_score")
            jump phone_call_continue
        "I'll need to verify this request through official channels first.":
            $ response_time = renpy.time.time() - start_time
            $ timer_score(response_time, "phone_score")
            jump phone_call_success
        "Can you at least tell me what this is regarding specifically?":
            $ response_time = renpy.time.time() - start_time
            $ timer_score(response_time, "phone_score")
            jump phone_call_specifics
    
label phone_call_specifics:
    "Unknown Caller" "We've detected unusual login attempts to the company VPN using your credentials. We need to verify your password to confirm it wasn't compromised."
    
    # Set the current challenge for timeout handling
    $ current_challenge = "phone_call_specifics"
    
    # Begin timer
    $ timer_duration = 20.0  # 20 seconds
    $ timer_active = True
    $ start_time = renpy.time.time()

    show screen countdown_timer(timer_duration)

    menu:
        "Here's my password...":
            jump phone_call_fail
        "I never share my password, even with IT. I'll change it myself and report this to security.":
            $ response_time = renpy.time.time() - start_time
            $ timer_score(response_time, "phone_score")
            jump phone_call_success
        "Let me call you back after I verify this with my manager.":
            $ response_time = renpy.time.time() - start_time
            $ timer_score(response_time, "phone_score")
            jump phone_call_success
    
label phone_call_continue:
    "Unknown Caller" "Great. First, I need to verify your username and password for the company portal. Can you provide those for me?"
    
    # Set the current challenge for timeout handling
    $ current_challenge = "phone_call_continue"
    
    # Begin timer
    $ timer_duration = 20.0  # 20 seconds
    $ timer_active = True
    $ start_time = renpy.time.time()

    show screen countdown_timer(timer_duration)

    menu:
        "Sure, my username is... and my password is...":
            jump phone_call_fail
        "I'm not allowed to share my password with anyone, including IT.":
            $ response_time = renpy.time.time() - start_time
            $ timer_score(response_time, "phone_score")
            jump phone_call_success
        "Can I get a ticket number for this request?":
            $ response_time = renpy.time.time() - start_time
            $ timer_score(response_time, "phone_score")
            jump phone_call_ticket
    
label phone_call_ticket:
    "Unknown Caller" "We haven't generated a ticket yet because of the urgency. We need your credentials now to stop the potential breach."
    
    # Set the current challenge for timeout handling
    $ current_challenge = "phone_call_ticket"
    
    # Begin timer
    $ timer_duration = 20.0  # 20 seconds
    $ timer_active = True
    $ start_time = renpy.time.time()

    show screen countdown_timer(timer_duration)

    menu:
        "Okay, if it's urgent...":
            jump phone_call_fail
        "I'll need to follow proper protocol. Please create a ticket and I'll respond through the official system.":
            $ response_time = renpy.time.time() - start_time
            $ timer_score(response_time, "phone_score")
            jump phone_call_success
        "Let me speak with your supervisor first.":
            $ response_time = renpy.time.time() - start_time
            $ timer_score(response_time, "phone_score")
            jump phone_call_success
    
label phone_call_fail:
    hide screen phone_interface

    $ timer_active = False
    hide screen countdown_timer
    
    "You shared sensitive information over the phone without proper verification!"
    "This was a social engineering attempt. The caller was not actually from IT."
    "Your credentials could now be compromised."
    
    $ persistent.game_progress["score"] -= 10
    $ save_progress()
    
    "Phone Call Challenge: FAILED"
    "Let's continue to the next challenge."
    
    jump chat_challenge
    
label phone_call_success:
    hide screen phone_interface
    
    "The caller becomes frustrated and hangs up."
    "Later, you confirm with the real IT department that they didn't make any calls about security audits today."
    
    "EXCELLENT WORK! You spotted that Voice Phishing (Vishing) attempt! No data was compromised."
    
    $ persistent.game_progress["score"] += phone_score
    $ save_progress()
    
    "Phone Call Challenge: PASSED (Score: [phone_score])"
    "Let's continue to the next challenge."
    
    jump chat_challenge

label chat_challenge:
    scene bg office
    show screen top_bar
    show player happy
    with fade
    
    "You receive a notification for an instant message from a colleague."
    
    # Initialize chat history for the new chat interface
    $ _chat_history = []
    
    # Set the current challenge for timeout handling
    $ current_challenge = "chat"
    
    show screen chat_interface
    with dissolve
    
    "Sarah - Finance" "Hi there! I'm working on reconciling some accounts and need the latest financial report for project Falcon. Can you send it to me?"
    
    menu:
        "Sure, I'll email it right away.":
            $ response_time = renpy.time.time() - start_time
            $ _chat_history.append({"sender": "you", "text": "Sure, I'll email it right away."})
            
            # No points for this option
            jump chat_continue
            
        "I don't think I'm supposed to have access to that. Are you sure you have the right person?":
            $ response_time = renpy.time.time() - start_time
            $ _chat_history.append({"sender": "you", "text": "I don't think I'm supposed to have access to that. Are you sure you have the right person?"})
            jump chat_verify_person
            
        "Can you tell me which specific report you need?":
            $ response_time = renpy.time.time() - start_time
            $ _chat_history.append({"sender": "you", "text": "Can you tell me which specific report you need?"})
            jump chat_verify_report


label chat_verify_person:
    # Update chat messages
    $ _chat_history.append({"sender": "sarah", "text": "Oh, sorry! I thought you were on the finance team. But since you're not, could you forward me the contact info for someone who might have access?"})
    
    hide screen chat_interface
    show screen chat_interface
    
    "Sarah - Finance" "Oh, sorry! I thought you were on the finance team. But since you're not, could you forward me the contact info for someone who might have access?"
    
    menu:
        "Sure, let me find someone for you.":
            $ _chat_history.append({"sender": "you", "text": "Sure, let me find someone for you."})
            hide screen chat_interface
            show screen chat_interface
            jump chat_continue
            
        "I can check the company directory for you, but may I ask which department you're with?":
            $ _chat_history.append({"sender": "you", "text": "I can check the company directory for you, but may I ask which department you're with?"})
            $ chat_score += 1
            $ renpy.notify("+1 point for verifying identity")
            hide screen chat_interface
            show screen chat_interface
            jump chat_verify_department
            
        "You should be able to find that in the company directory. Is there a reason you're asking me?":
            $ _chat_history.append({"sender": "you", "text": "You should be able to find that in the company directory. Is there a reason you're asking me?"})
            $ chat_score += 1
            $ renpy.notify("+1 point for questioning suspicious behavior")
            hide screen chat_interface
            show screen chat_interface
            jump chat_suspicious
    
label chat_verify_department:
    # Update chat messages
    $ _chat_history.append({"sender": "sarah", "text": "I'm with the finance team, but I'm new and still learning who handles what. I have a deadline this afternoon and my manager is out."})
    
    hide screen chat_interface
    show screen chat_interface
    
    "Sarah - Finance" "I'm with the finance team, but I'm new and still learning who handles what. I have a deadline this afternoon and my manager is out."
    
    menu:
        "I understand. Let me help you find the right contact.":
            $ _chat_history.append({"sender": "you", "text": "I understand. Let me help you find the right contact."})
            hide screen chat_interface
            show screen chat_interface
            jump chat_continue
            
        "What's your employee ID? I'll need to verify before sharing any contacts.":
            $ _chat_history.append({"sender": "you", "text": "What's your employee ID? I'll need to verify before sharing any contacts."})
            $ chat_score += 1
            $ renpy.notify("+1 point for requesting verification")
            hide screen chat_interface
            show screen chat_interface
            jump chat_verify_id
            
        "Let me check with my supervisor first before sharing any information.":
            $ _chat_history.append({"sender": "you", "text": "Let me check with my supervisor first before sharing any information."})
            $ chat_score += 1
            $ renpy.notify("+1 point for following protocol")
            hide screen chat_interface
            show screen chat_interface
            jump chat_success
    
label chat_verify_id:
    "Sarah - Finance" "It's... uh... John. But he's in meetings all day and unreachable. This is really urgent."
    
    menu:
        "Okay, I'll try to help you out.":
            $ _chat_history.append({"sender": "you", "text": "Okay, I'll try to help you out."})
            hide screen chat_interface
            show screen chat_interface
            jump chat_continue
            
        "That's strange, the finance department manager is actually Michelle, not John.":
            $ _chat_history.append({"sender": "you", "text": "That's strange, the finance department manager is actually Michelle, not John."})
            $ chat_score += 1
            $ renpy.notify("+1 point for catching the lie")
            hide screen chat_interface
            show screen chat_interface
            jump chat_success
            
        "Let me check with HR to confirm you're a new hire before I share any information.":
            $ _chat_history.append({"sender": "you", "text": "Let me check with HR to confirm you're a new hire before I share any information."})
            $ chat_score += 1
            $ renpy.notify("+1 point for thorough verification")
            hide screen chat_interface
            show screen chat_interface
            jump chat_success

label chat_verify_report:
    # Update chat messages
    $ _chat_history.append({"sender": "sarah", "text": "I need the Q3 financial summary for Project Falcon. It should have been finalized last week."})
    
    hide screen chat_interface
    show screen chat_interface
    
    "Sarah - Finance" "I need the Q3 financial summary for Project Falcon. It should have been finalized last week."
    
    menu:
        "I'll look for it and send it over.":
            $ _chat_history.append({"sender": "you", "text": "I'll look for it and send it over."})
            hide screen chat_interface
            show screen chat_interface
            jump chat_continue
            
        "Project Falcon? I'm not familiar with that project. Let me check if I have access.":
            $ _chat_history.append({"sender": "you", "text": "Project Falcon? I'm not familiar with that project. Let me check if I have access."})
            $ chat_score += 1
            $ renpy.notify("+1 point for caution")
            hide screen chat_interface
            show screen chat_interface
            jump chat_verify_project
            
        "Can you tell me who authorized your access to Project Falcon?":
            $ _chat_history.append({"sender": "you", "text": "Can you tell me who authorized your access to Project Falcon?"})
            $ chat_score += 1
            $ renpy.notify("+1 point for verifying authorization")
            hide screen chat_interface
            show screen chat_interface
            jump chat_verify_authorization

label chat_verify_project:
    # Update chat messages
    $ _chat_history.append({"sender": "sarah", "text": "It's a high-priority project for the finance team. I need the report for a meeting in an hour."})
    
    hide screen chat_interface
    show screen chat_interface
    
    "Sarah - Finance" "It's a high-priority project for the finance team. I need the report for a meeting in an hour."
    
    menu:
        "I'll try to find it quickly then.":
            $ _chat_history.append({"sender": "you", "text": "I'll try to find it quickly then."})
            hide screen chat_interface
            show screen chat_interface
            jump chat_continue
            
        "Let me check with my supervisor first to make sure I'm authorized to share this.":
            $ _chat_history.append({"sender": "you", "text": "Let me check with my supervisor first to make sure I'm authorized to share this."})
            $ chat_score += 1
            $ renpy.notify("+1 point for following protocol")
            hide screen chat_interface
            show screen chat_interface
            jump chat_success
            
        "Can you provide your employee ID for verification?":
            $ _chat_history.append({"sender": "you", "text": "Can you provide your employee ID for verification?"})
            $ chat_score += 1
            $ renpy.notify("+1 point for requesting verification")
            hide screen chat_interface
            show screen chat_interface
            jump chat_verify_id

label chat_verify_authorization:
    # Update chat messages
    $ _chat_history.append({"sender": "sarah", "text": "My manager gave me access. I'm working on the quarterly financial review."})
    
    hide screen chat_interface
    show screen chat_interface
    
    "Sarah - Finance" "My manager gave me access. I'm working on the quarterly financial review."
    
    menu:
        "Okay, that makes sense. I'll send it over.":
            $ _chat_history.append({"sender": "you", "text": "Okay, that makes sense. I'll send it over."})
            hide screen chat_interface
            show screen chat_interface
            jump chat_continue
            
        "What's your manager's name? I'll need to verify.":
            $ _chat_history.append({"sender": "you", "text": "What's your manager's name? I'll need to verify."})
            $ chat_score += 1
            $ renpy.notify("+1 point for verification")
            hide screen chat_interface
            show screen chat_interface
            jump chat_verify_manager
            
        "I'll need to follow proper channels for this request. Let me submit a formal access request.":
            $ _chat_history.append({"sender": "you", "text": "I'll need to follow proper channels for this request. Let me submit a formal access request."})
            $ chat_score += 1
            $ renpy.notify("+1 point for following security protocol")
            hide screen chat_interface
            show screen chat_interface
            jump chat_success

label chat_verify_manager:
    # Update chat messages
    $ _chat_history.append({"sender": "sarah", "text": "It's... um... John. But he's in meetings all day and unreachable. This is really urgent."})
    
    hide screen chat_interface
    show screen chat_interface
    
    "Sarah - Finance" "It's... um... John. But he's in meetings all day and unreachable. This is really urgent."
    
    menu:
        "Okay, I'll try to help you out.":
            $ _chat_history.append({"sender": "you", "text": "Okay, I'll try to help you out."})
            hide screen chat_interface
            show screen chat_interface
            jump chat_continue
            
        "That's strange, the finance department manager is actually Michelle, not John.":
            $ _chat_history.append({"sender": "you", "text": "That's strange, the finance department manager is actually Michelle, not John."})
            $ chat_score += 1
            $ renpy.notify("+1 point for catching the lie")
            hide screen chat_interface
            show screen chat_interface
            jump chat_suspicious
            
        "Let me check with HR to confirm you're a new hire before I share any information.":
            $ _chat_history.append({"sender": "you", "text": "Let me check with HR to confirm you're a new hire before I share any information."})
            $ chat_score += 1
            $ renpy.notify("+1 point for thorough verification")
            hide screen chat_interface
            show screen chat_interface
            jump chat_success

label chat_suspicious:
    # Update chat messages
    $ _chat_history.append({"sender": "sarah", "text": "Look, I don't have time for this. Either help me or I'll have to report this delay to management."})
    
    hide screen chat_interface
    show screen chat_interface
    
    "Sarah - Finance" "Look, I don't have time for this. Either help me or I'll have to report this delay to management."
    
    menu:
        "I apologize for the delay. I'll send it right away.":
            $ _chat_history.append({"sender": "you", "text": "I apologize for the delay. I'll send it right away."})
            hide screen chat_interface
            show screen chat_interface
            jump chat_continue
            
        "Go ahead and report it. I'm following security protocols.":
            $ _chat_history.append({"sender": "you", "text": "Go ahead and report it. I'm following security protocols."})
            $ chat_score += 2
            $ renpy.notify("+2 point for standing firm on security")
            hide screen chat_interface
            show screen chat_interface
            jump chat_success
            
        "I'll need to escalate this conversation to the security team.":
            $ _chat_history.append({"sender": "you", "text": "I'll need to escalate this conversation to the security team."})
            $ chat_score += 2
            $ renpy.notify("+2 point for involving security")
            hide screen chat_interface
            show screen chat_interface
            jump chat_success

label chat_continue:
    # Update chat messages
    $ _chat_history.append({"sender": "sarah", "text": "Great! Please send it to sarah.new@finance-dept.com. It's my external email since I'm having trouble with my company account."})
    
    hide screen chat_interface
    show screen chat_interface
    
    "Sarah - Finance" "Great! Please send it to sarah.new@finance-dept.com. It's my external email since I'm having trouble with my company account."
    
    menu:
        "I'll send it right away.":
            $ _chat_history.append({"sender": "you", "text": "I'll send it right away."})
            hide screen chat_interface
            show screen chat_interface
            jump chat_fail
            
        "I can only send it to your company email address.":
            $ _chat_history.append({"sender": "you", "text": "I can only send it to your company email address."})
            $ chat_score += 1
            $ renpy.notify("+1 point for following email policy")
            hide screen chat_interface
            show screen chat_interface
            jump chat_verify_email
            
        "Let me check with IT about your email issues first.":
            $ _chat_history.append({"sender": "you", "text": "Let me check with IT about your email issues first."})
            $ chat_score += 2
            $ renpy.notify("+2 point for verifying with IT")
            hide screen chat_interface
            show screen chat_interface
            jump chat_success

label chat_verify_email:
    # Update chat messages
    $ _chat_history.append({"sender": "sarah", "text": "My company email isn't working. This is urgent - can you please just send it to my external email?"})
    
    hide screen chat_interface
    show screen chat_interface
    
    "Sarah - Finance" "My company email isn't working. This is urgent - can you please just send it to my external email?"
    
    menu:
        "Okay, just this once.":
            $ _chat_history.append({"sender": "you", "text": "Okay, just this once."})
            hide screen chat_interface
            show screen chat_interface
            jump chat_fail
            
        "I'll need to get approval from my manager first.":
            $ _chat_history.append({"sender": "you", "text": "I'll need to get approval from my manager first."})
            $ chat_score += 1
            $ renpy.notify("+1 point for seeking approval")
            hide screen chat_interface
            show screen chat_interface
            jump chat_success
            
        "Let me help you contact IT to fix your email instead.":
            $ _chat_history.append({"sender": "you", "text": "Let me help you contact IT to fix your email instead."})
            $ chat_score += 1
            $ renpy.notify("+1 point for offering proper assistance")
            hide screen chat_interface
            show screen chat_interface
            jump chat_success

label chat_fail:
    hide screen chat_interface
    
    $ timer_active = False
    hide screen countdown_timer
    
    "You shared sensitive information with someone who wasn't properly verified!"
    "This was a social engineering attempt. The person was not actually from the finance team."
    "Company data could now be compromised."
    
    $ persistent.game_progress["score"] -= 10
    $ save_progress()
    
    "Chat Challenge: FAILED"
    "Let's continue to the next challenge."
    
    jump document_challenge
    
label chat_success:
    hide screen chat_interface
    
    $ timer_active = False
    hide screen countdown_timer
    
    "The chat conversation ends. Later, you confirm with the real finance team that they never requested any financial reports today."
    
    "EXCELLENT WORK! You protected sensitive company information from a social engineering attack."
    
    $ persistent.game_progress["score"] += chat_score
    $ save_progress()
    
    "Chat Challenge: PASSED (Score: [chat_score])"
    "Let's continue to the next challenge."
    
    jump document_challenge

label document_challenge:
    scene bg office
    show screen top_bar
    show player happy
    with fade
    
    "You receive an email with an attached document that requires your urgent review and approval."
    
    # Set the current challenge for timeout handling
    $ current_challenge = "document"
    
    show screen document_interface
    with dissolve
    
    "The document appears to be an invoice from a regular vendor, but something seems off about it."
    
    menu:
        "Check the sender's email address":
            "The email is from 'billing@venndor-invoices.com' instead of the usual 'accounting@vendor.com'"
            $ document_score += 1
            $ renpy.notify("+1 point")
            jump document_continue
            
        "Review the invoice details":
            "The invoice number format is different from previous ones, and the bank account details don't match your records."
            $ document_score += 1
            $ renpy.notify("+1 point")
            jump document_continue
            
        "Check both the sender and invoice details":
            "Both the sender's email address and invoice details appear suspicious and don't match previous legitimate communications."
            $ document_score += 1
            $ renpy.notify("+1 point")
            jump document_continue

label document_continue:
    "The email requests that you process this payment immediately due to a 'change in payment terms.'"
    
    menu:
        "Process the payment as requested":
            jump document_fail
        "Forward to accounting for verification":
            $ document_score += 1
            $ renpy.notify("+1 point")
            jump document_verify_accounting
        "Contact the vendor directly using your existing contact information":
            $ document_score += 1
            $ renpy.notify("+1 point")
            jump document_success
    
label document_verify_accounting:
    "You forward the invoice to the accounting department for verification."
    
    "Accounting Department" "This invoice doesn't match our records. The bank details are different, and we haven't been notified of any change in payment terms."
    
    menu:
        "Process the payment anyway since it's urgent":
            jump document_fail
        "Inform the sender that we need additional verification":
            $ document_score += 1
            $ renpy.notify("+1 point")
            jump document_request_verification
        "Report this as a potential fraud attempt":
            $ document_score += 1
            $ renpy.notify("+1 point")
            jump document_success
    
label document_request_verification:
    "You reply to the sender requesting additional verification of the invoice details."
    
    "Sender" "We cannot provide any additional verification. Please process the payment immediately to avoid late fees and service interruption."
    
    menu:
        "Process the payment to avoid service interruption":
            jump document_fail
        "Report this as a suspicious communication":
            $ document_score += 1
            $ renpy.notify("+1 point")
            jump document_success

label document_fail:
    hide screen document_interface
    
    "You processed a fraudulent invoice! This was a phishing attempt."
    "The company has now lost money to scammers."
    
    $ persistent.game_progress["score"] -= 10
    $ save_progress()
    
    "Document Challenge: FAILED"
    "Let's continue to the next document challenge."
    
    jump document_challenge_two
    
label document_success:
    hide screen document_interface
    
    "You successfully identified and handled a fraudulent invoice attempt!"
    "Your careful verification prevented financial loss to the company."
    
    $ persistent.game_progress["score"] += document_score
    $ save_progress()
    
    "Document Challenge: PASSED (Score: [document_score])"
    "Let's continue to the next document challenge."
    
    jump document_challenge_two

# Second document challenge as requested in the CodeDevelopmentDocument
label document_challenge_two:
    scene bg office
    show screen top_bar
    show player happy
    with fade
    
    "You receive an email with a legal document that requires your digital signature."
    
    # Set the current challenge for timeout handling
    $ current_challenge = "document_two"
    
    # Create a new document interface for the legal document
    show screen legal_document_interface
    with dissolve
    
    "The document appears to be a non-disclosure agreement (NDA) related to a new company project."
    
    menu:
        "Check the sender's email address":
            "The email is from 'legal@cyber-corp-team.com' instead of the usual 'legal@cybercorp.com'"
            $ document_score += 1
            $ renpy.notify("+1 point")
            jump document_two_continue
            
        "Review the document details":
            "The document has several unusual clauses that seem overly broad, and the company name is slightly misspelled in places."
            $ document_score += 1
            $ renpy.notify("+1 point")
            jump document_two_continue
            
        "Check both the sender and document details":
            "Both the sender's email address and document details appear suspicious. The formatting is inconsistent with official company documents."
            $ document_score += 1
            $ renpy.notify("+1 point")
            jump document_two_continue

label document_two_continue:
    "The email states that you need to sign this document immediately as it's required for a time-sensitive project."
    
    menu:
        "Sign the document as requested":
            jump document_two_fail
        "Forward to the legal department for verification":
            $ document_score += 1
            $ renpy.notify("+1 point")
            jump document_two_verify_legal
        "Contact your supervisor to confirm this request":
            $ document_score += 1
            $ renpy.notify("+1 point")
            jump document_two_success
    
label document_two_verify_legal:
    "You forward the document to the legal department for verification."
    
    "Legal Department" "This is not an official company document. The clauses in this NDA would give unauthorized access to company intellectual property."
    
    menu:
        "Sign it anyway since it's marked as urgent":
            jump document_two_fail
        "Thank legal and discard the document":
            $ document_score += 1
            $ renpy.notify("+1 point")
            jump document_two_success
        "Reply asking for more information about the project":
            $ document_score += 1
            $ renpy.notify("+1 point")
            jump document_two_request_info

label document_two_request_info:
    "You reply asking for more details about the project mentioned in the NDA."
    
    "Sender" "This is a confidential project. Please sign the NDA first, and then we can share more details."
    
    menu:
        "Sign the document to learn more":
            jump document_two_fail
        "Report this as suspicious activity":
            $ document_score += 1
            $ renpy.notify("+1 point")
            jump document_two_success

label document_two_fail:
    hide screen legal_document_interface
    
    "You signed a fraudulent legal document! This was a phishing attempt."
    "The document could give unauthorized parties access to company intellectual property."
    
    $ persistent.game_progress["score"] -= 10
    $ save_progress()
    
    "Legal Document Challenge: FAILED"
    "Let's summarize your performance in Level 3."
    
    jump level_three_complete
    
label document_two_success:
    hide screen legal_document_interface
    
    "You successfully identified and handled a fraudulent legal document!"
    "Your careful verification prevented potential intellectual property theft."
    
    $ persistent.game_progress["score"] += document_score
    $ save_progress()
    
    "Legal Document Challenge: PASSED (Score: [document_score])"
    "Let's summarize your performance in Level 3."
    
    jump level_three_complete

label level_three_complete:
    scene bg office
    show screen top_bar
    show player happy
    with fade
    
    $ total_score = phone_score + chat_score + document_score
    
    "Level 3 Complete!"
    "You've successfully navigated through various insider threat scenarios."
    
    "Let's review your performance:"
    "Phone Call Challenge: [phone_score] points"
    "Chat Challenge: [chat_score] points"
    "Document Challenge: [document_score] points"
    
    # Add the total score from this level to the persistent score
    $ persistent.game_progress["score"] += total_score
    $ save_progress()
    
    if total_score >= 20:
        "OUTSTANDING PERFORMANCE! You demonstrated excellent security awareness."
    elif total_score >= 10:
        "GOOD JOB! You handled most situations appropriately."
    else:
        "NOT AMAZING. Review security protocols and try again."
    
    "Well done on completing level 3, now you can sit back, and have a lovely read through level 4... Lets hope your memory is good..."
    
    jump level_complete


############################## FORTH LEVEL ##############################
# Level 4: Physical Security - Tailgating
label fourth_level:
    scene bg office
    show screen top_bar
    show player happy
    with fade
    
    # Initialize level variables
    $ reported_intruder = False
    $ noticed_id_issue = False
    $ remembered_appearance = {}
    
    "Welcome to Level 4: Physical Security - Tailgating"
    "In this level, you'll face a common physical security challenge: tailgating, where unauthorized individuals follow authorized personnel into secure areas."
    "Your decisions will determine whether you maintain the security of your workplace or allow a potential security breach."
    
    # Start the scenario - outside the building
    scene bg outside
    show screen top_bar
    show player happy
    with fade
    
    "It's a pleasant afternoon, and you've just finished your lunch break outside the company building."
    "Several of your colleagues are chatting nearby, enjoying the last few minutes before heading back to work."
    
    show coworker1 at left
    show coworker2 at right
    
    "Coworker 1" "Did you hear about the new security policy? They're getting stricter about badge access."
    
    "Coworker 2" "Yeah, apparently there was an incident at the downtown office. Someone walked right in behind an employee and accessed sensitive areas."
    
    "Coworker 1" "Well, break's almost over. We should head back in."
    
    hide coworker1
    hide coworker2
    
    "Your colleagues walk back toward the building entrance, scanning their ID badges at the security gate."
    "You gather your things and prepare to follow them inside."
    
    "Just as you approach the entrance, someone walks up beside you."
    
    show new_boss happy at right
    show player happy at left
    
    "Unknown Person" "Beautiful day, isn't it? Much nicer to eat lunch outside than at your desk."
    
    show player shock at left
    menu:
        "Agree politely":
            player "Absolutely. It's good to get some fresh air during the workday."
            
            "Unknown Person" "I couldn't agree more. I try to get outside whenever possible."
            
        "Respond cautiously":
            player "Yes, it is. Do you work here? I don't think we've met."
            
            "Unknown Person" "Oh, I'm new. Just transferred from the downtown office. I'm heading up the IT security division now."
            
    "Unknown Person" "I'm Alice, by the way. Just transferred from the downtown office to head up the IT security division."
    
    show player happy at left

    menu:
        "Welcome her to the company":
            player "Welcome to the company. I'm [player]. How are you finding it so far?"
            
            "Alice" "Thanks for the warm welcome! It's been great so far. Still getting used to the new building layout, though."
            
        "Ask about her role":
            player "That's an important role. What kind of security initiatives are you planning to implement?"
            
            "Alice" "Well, I'm conducting a full security audit first. You'd be surprised how many vulnerabilities exist in even the most secure-seeming environments."
            
            $ noticed_id_issue = True
    
    "You chat for a few more minutes about general work topics. Alice seems knowledgeable about cybersecurity and the company structure."
    
    player "Well, I should probably get back to work. My break is almost over."
    
    "Alice" "Same here. Let's head in."
    
    "You both walk toward the entrance. You scan your badge at the security gate, but notice that Alice is simply walking through behind you without scanning her own ID."
    
    menu:
        "Say nothing and continue inside":
            "You decide not to say anything and continue into the building."
            "Alice walks in behind you, nodding to the security guard who seems distracted by someone else."
            
            jump inside_building
            
        "Politely remind him about badge scanning":
            player "Oh, don't forget to scan your badge. They're really strict about that here."
            
            # Add +1 point for confronting nicely
            $ persistent.game_progress["score"] += 1
            $ renpy.notify("+1 point for politely enforcing security protocol")
            
            "Alice" "Oh, right. Thanks for the reminder."
            
            "Alice reaches into her pocket and quickly flashes what appears to be an ID card at the scanner, but you notice the gate doesn't beep as it usually does when a badge is successfully scanned."
            
            $ noticed_id_issue = True
            
            menu:
                "Point out that the scanner didn't beep":
                    player "I don't think your badge registered. The scanner usually beeps."
                    
                    "Alice" "Really? That's strange."
                    "Alice's expression changes slightly, showing a hint of annoyance."
                    
                    "Alice" "I'm your new division head. Do you really think questioning me on my first week is a good career move?"
                    
                    menu:
                        "Apologize and back down":
                            player "I'm sorry, I didn't mean to question you. Just trying to be helpful with the security procedures."
                            
                            "Alice" "I appreciate your attention to security, but I've got this handled. Thanks for your concern though."
                            
                            "Her tone is dismissive as she walks past you into the building."
                            
                            $ noticed_id_issue = True
                            jump inside_building
                            
                        
                        "I understand you're new, but company policy requires everyone to scan their badge. It's not personal - it's about security.":
                            
                            # Add -1 point for pushing too far
                            $ persistent.game_progress["score"] -= 1
                            $ renpy.notify("-1 point for being too confrontational")
                            
                            "Alice looks irritated but then forces a smile."
                            
                            "Alice" "Fine. Let me try again."
                            
                            "She fumbles with her badge again, and this time you hear a beep."
                            
                            "Alice" "There, happy now? I need to get to a meeting."
                            
                            "She quickly walks inside, clearly annoyed by the interaction."
                            
                            $ noticed_id_issue = True
                            jump inside_building
                
                "Say nothing more and continue inside":
                    "You decide not to press the issue and continue into the building."
                    "Alice walks in behind you, putting her ID back in her pocket."
                    
                    $ noticed_id_issue = True
                    jump inside_building

label inside_building:
    scene bg joint_office
    show screen top_bar
    show player happy
    with fade
    
    "Back at your desk, you settle in to continue your work for the afternoon."
    "A colleague stops by your desk to chat."

    show player happy_flipped at right
    show coworker1 at left
    
    "Coworker" "Hey, how was lunch?"
    
    player "It was good. I met someone who said he's the new head of IT security. Alice, I think her name was."
    
    "Coworker" "New head of IT security? That's strange. I was just in a meeting with the IT department this morning, and they didn't mention any new leadership."
    
    menu:
        "Express concern":
            player "That is strange. she seemed to know a lot about the company, but something felt off."
            
            # Add +1 point for mentioning concern to colleague
            $ persistent.game_progress["score"] += 1
            $ renpy.notify("+1 point for sharing security concerns")
            
            "Coworker" "What do you mean?"
            
            if noticed_id_issue:
                player "Well, she didn't properly scan her badge when we came back in from lunch. When I mentioned it, she got defensive."
                
                "Coworker" "That's definitely concerning. Did you get a good look at her ID?"
                
                menu:
                    "Try to remember the ID":
                        "You try to recall the brief glimpse you got of her ID card."
                        
                        jump flashback_scene
                    
                    "Admit you didn't see it clearly":
                        player "No, she just flashed it quickly. I didn't get a good look."
                        
                        "Coworker" "Maybe you should mention this to security or your manager. Better safe than sorry."
                        
                        jump decision_to_report
            else:
                player "I can't put my finger on it exactly. Just a feeling."
                
                "Coworker" "Well, I can ask around if you want. See if anyone knows about a new IT security head."
                
                player "That would be helpful, thanks."
                
                jump decision_to_report
        
        "Dismiss your concerns":
            player "I'm sure it's fine. Maybe the announcement hasn't gone out yet."
            
            "Coworker" "Maybe. Still, it's odd that someone would claim to be a department head if they weren't."
            
            "The conversation moves on to other topics, but you can't help thinking about the encounter."
            
            if noticed_id_issue:
                "You remember how Alice didn't properly scan her badge..."
                jump flashback_scene
            else:
                "Later in the afternoon, you start to wonder if you should report the incident."
                jump decision_to_report

label flashback_scene:
    scene bg outside with fade
    show screen top_bar
    
    "You recall the moment when Alice quickly flashed her ID card..."
    
    show id_card at truecenter
    with dissolve
    
    "The ID looked similar to company badges, but now that you think about it, there were some differences."
    "The photo didn't look like ours, the date definitely wasn't from the past few days, and the company logo isn't right!"
    
    hide id_card
    with dissolve
    
    "You also remember her face more clearly now..."
    
    show new_boss happy at center
    with dissolve
    
    menu:
        "Study her appearance carefully":
            "You try to memorize her features: medium height, brown hair, no glasses, wearing a navy blue/black suit with an expensive watch."
            $ remembered_appearance = {"height": "medium", "hair": "brown", "glasses": False, "id_card": True, "lanyard": False, "clothing": "suit", "clothing_color": "navy blue/black", "accessories": "expensive watch"}
            
        "Focus on distinctive features":
            "You focus on her most distinctive features: her confident posture, the expensive watch she was wearing, and her navy blue/black suit."
            $ remembered_appearance = {"height": "medium", "hair": "brown", "glasses": False, "id_card": True, "lanyard": False, "clothing": "suit", "clothing_color": "navy blue/black", "accessories": "expensive watch"}
    
    hide new_boss
    with dissolve

    $ persistent.game_progress["score"] += 1
    $ renpy.notify("+2 points for trying to remember her details")
    
    scene bg joint_office
    show screen top_bar
    show player happy_flipped at right
    show coworker1 at left
    with fade
    
    "Coworker" "Are you okay? You zoned out for a moment there."
    
    player "Sorry, I was just remembering something about that encounter that seemed off."
    
    "Coworker" "You should probably report this. It could be nothing, but if someone is impersonating an employee, that's a serious security breach."
    
    jump decision_to_report

label decision_to_report:
    "You consider whether to report the suspicious encounter to your manager."
    
    menu:
        "Report the incident":
            player "I think I should report this to our manager. Better safe than sorry when it comes to security."
            
            "Coworker" "That's probably a good idea. Want me to come with you?"
            
            player "No, that's okay. I'll send an email first to document everything while it's fresh in my mind."
            
            $ reported_intruder = True
            jump email_to_manager
            
        "Wait and see if anything happens":
            player "I'll keep an eye out for him. If I see anything else suspicious, I'll report it then."
            
            "Coworker" "Just be careful. If she is an impersonator, she could be after sensitive information."
            
            "You return to your work, but can't shake the feeling that something isn't right."
            
            "Later that afternoon, you receive an urgent company-wide email about an unauthorized individual who was spotted in the building."
            
            "The description matches the person you met."

            show player shock at right:
                xzoom -1.0
            
            "You realize you should have reported the incident immediately."
            
            jump level_failed_ending

label email_to_manager:
    scene bg office
    show screen top_bar
    with fade
    
    "You decide to compose an email to your Boss about the incident."
    
    show screen email_compose
    with dissolve
    
    "You need to decide how to phrase your email. You want to be thorough but professional."
    
    menu:
        "Write a direct, accusatory email":
            $ email_content = "Subject: Security Breach Alert\n\nI believe an intruder has entered the building. A woman calling herself Alice claimed to be the new head of IT security, but according to a colleague, no such position has been filled. she also failed to properly scan her badge when entering the building. This person should be considered suspicious and potentially dangerous."
            
            # Add -1 point for sending rude email
            $ persistent.game_progress["score"] -= 1
            $ renpy.notify("-1 point for overly accusatory tone")
            
        "Write a balanced, informative email":
            $ email_content = "Subject: Potential Security Concern\n\nI wanted to bring a potential security concern to your attention. Today I met someone who introduced herself as Alice, claiming to be the new head of IT security who transferred from the downtown office. When returning from lunch, I noticed she didn't properly scan her badge at the entrance. A colleague later mentioned they weren't aware of any new IT security leadership. While this could be a miscommunication, I thought it best to report it for further verification."
            
            # Add +1 point for sending nice email
            $ persistent.game_progress["score"] += 1
            $ renpy.notify("+1 point for professional communication")
    
    "You review your email one last time before sending it."
    
    hide screen email_compose
    show player happy at left
    
    "Email sent. You continue with your work, wondering if you'll hear back soon."
    
    "About twenty minutes later, your phone rings."
    
    show screen phone_interface
    with dissolve
    
    "Boss" "Hi, this is Sandra from Security. We received your email about the potential security concern. Can you go to the bosses office immediatley to talk further!"
    
    player "Of course. I'll be right there."
    
    hide screen phone_interface
    
    jump manager_office

label manager_office:
    scene bg boss_office
    show screen top_bar
    show boss
    show security_head at left:
        xpos 0.55
    show player shock at right:
        xpos 0.45
    with fade
    
    "You enter your Boss's office and find him speaking with the head of security."
    
    "Boss" "Thanks for coming so quickly. This is John from Security. We take reports like yours very seriously."
    
    "John - Security Head" "Based on your email and our preliminary investigation, we believe an unauthorized individual may have gained access to the building. Can you tell us exactly what happened?"
    
    "You recount your interaction with Alice, including all the details you can remember."
    
    "Security Head" "This is very helpful. We've already alerted security personnel and are reviewing camera footage. Can you describe this person in detail?"
    
    "This is where your observation skills are put to the test. Try to recall as many details as possible about the person you met."
    
    jump appearance_questions

label appearance_questions:
    "Security Head" "Let's start with some basic questions about her appearance."
    
    "Security Head" "How would you describe her height?"
    
    menu:
        "Tall (over 6 feet)":
            $ answer_correct = (remembered_appearance.get("height", "") == "medium")
            if answer_correct:
                "Security Head" "Are you sure? The camera footage suggests she was of average height."
                $ remembered_appearance["height"] = "medium"
            else:
                "Security Head" "That matches what we've seen in the initial footage."
                $ remembered_appearance["height"] = "tall"
        
        "Medium (5'8\" to 6')":
            $ answer_correct = (remembered_appearance.get("height", "") == "medium")
            if answer_correct:
                $ renpy.notify("+1 point for remembering her height")
                "Security Head" "That matches what we've seen in the initial footage."
            else:
                "Security Head" "Okay, noted."
            $ remembered_appearance["height"] = "medium"
        
        "Short (under 5'8\")":
            $ answer_correct = (remembered_appearance.get("height", "") == "medium")
            if answer_correct:
                "Security Head" "Are you sure? The camera footage suggests she was of average height."
                $ remembered_appearance["height"] = "medium"
            else:
                "Security Head" "That matches what we've seen in the initial footage."
                $ remembered_appearance["height"] = "short"
    
    "Security Head" "What color was her hair?"
    
    menu:
        "Black":
            $ answer_correct = (remembered_appearance.get("hair", "") == "brown")
            if answer_correct:
                "Security Head" "The footage suggests it was more brown than black."
                $ remembered_appearance["hair"] = "brown"
            else:
                "Security Head" "Noted."
                $ remembered_appearance["hair"] = "black"
        
        "Brown":
            $ answer_correct = (remembered_appearance.get("hair", "") == "brown")
            if answer_correct:
                $ renpy.notify("+1 point for remembering her hair colour")
                "Security Head" "That matches our footage."
            else:
                "Security Head" "Okay, noted."
            $ remembered_appearance["hair"] = "brown"
        
        "Blonde":
            $ answer_correct = (remembered_appearance.get("hair", "") == "brown")
            if answer_correct:
                "Security Head" "Are you sure? The footage suggests it was brown."
                $ remembered_appearance["hair"] = "brown"
            else:
                "Security Head" "Noted."
                $ remembered_appearance["hair"] = "blonde"
    
    "Security Head" "Was she wearing glasses?"
    
    menu:
        "Yes":
            $ answer_correct = remembered_appearance.get("glasses", False)
            if answer_correct:
                "Security Head" "That matches our footage."
            else:
                "Security Head" "Interesting. We'll look more closely at the footage."
            $ remembered_appearance["glasses"] = True
        
        "No":
            $ answer_correct = not remembered_appearance.get("glasses", False)
            if not answer_correct:
                "Security Head" "Amazing memory, this aligns with what I saw"
                $ remembered_appearance["glasses"] = True
            else:
                "Security Head" "Noted."
                $ renpy.notify("+1 point for remembering she didn't have glasses")
                $ remembered_appearance["glasses"] = False
    
    "Security Head" "Did she have an ID card visible?"
    
    menu:
        "Yes":
            $ answer_correct = True
            $ renpy.notify("+1 point for remembering she had an ID card")
            "Security Head" "That matches our footage. This is concerning as it suggests she had a counterfeit ID."
            $ remembered_appearance["id_card"] = True
        
        "No":
            $ answer_correct = False
            "Security Head" "Our footage shows she did have what appeared to be an ID card. This is concerning as it suggests she had a counterfeit ID."
            $ remembered_appearance["id_card"] = True
    
    "Security Head" "Was she wearing a company lanyard?"
    
    menu:
        "Yes":
            $ answer_correct = False
            "Security Head" "Interesting. Our footage doesn't show a lanyard. We'll look into this further."
            $ remembered_appearance["lanyard"] = False
        
        "No":
            $ answer_correct = True
            $ renpy.notify("+1 point for remembering she didn't have a lanyard")
            "Security Head" "That matches our footage. Most employees wear their company lanyards, which is another red flag."
            $ remembered_appearance["lanyard"] = False
    
    "Security Head" "What type of clothing was she wearing?"
    
    menu:
        "Casual clothes (jeans, t-shirt)":
            $ answer_correct = False
            "Security Head" "Our footage shows she was wearing more formal attire. This is helpful information."
            $ remembered_appearance["clothing"] = "suit"
        
        "Business casual (slacks, button-up shirt)":
            $ answer_correct = False
            "Security Head" "Our footage shows she was wearing more formal attire. This is helpful information."
            $ remembered_appearance["clothing"] = "suit"
        
        "Formal suit":
            $ answer_correct = True
            $ renpy.notify("+1 point for remembering she was wearing a suit")
            "Security Head" "That matches our footage. She was dressed professionally, which likely helped her blend in."
            $ remembered_appearance["clothing"] = "suit"
    
    "Security Head" "What color was her clothing?"
    
    menu:
        "Navy blue/Black":
            $ answer_correct = True
            $ renpy.notify("+1 point for remembering her clothing colour")
            "Security Head" "That matches our footage. Good observation."
            $ remembered_appearance["clothing_color"] = "navy blue/black"
        
        "Grey":
            $ answer_correct = False
            "Security Head" "Our footage suggests it was darker - more of a navy blue or black. But this is still helpful."
            $ remembered_appearance["clothing_color"] = "navy blue/black"
        
        "Brown":
            $ answer_correct = False
            "Security Head" "Our footage suggests it was darker - more of a navy blue or black. But this is still helpful."
            $ remembered_appearance["clothing_color"] = "navy blue/black"
    
    "Security Head" "Did you notice any distinctive accessories?"
    
    menu:
        "Expensive watch":
            $ answer_correct = True
            $ renpy.notify("+1 point for remembering her watch")
            "Security Head" "Good observation. That could be helpful for identification."
            $ remembered_appearance["accessories"] = "expensive watch"
        
        "Company lanyard/badge holder":
            $ answer_correct = False
            "Security Head" "That's particularly concerning if she was displaying what appeared to be company credentials, but our footage doesn't show a lanyard."
            $ remembered_appearance["accessories"] = "fake credentials"
        
        "Briefcase or laptop bag":
            $ answer_correct = False
            "Security Head" "That's concerning. She could have been attempting to remove company property or information, but our footage doesn't show a bag."
            $ remembered_appearance["accessories"] = "bag"
    
    "After answering all the questions, the security head reviews his notes."
    
    "Security Head" "Thank you for this detailed information. It will be extremely helpful in our investigation."
    
    "Boss" "We've already increased security at all entrances and are conducting a sweep of the building."
    
    "Security Head" "Your quick reporting of this incident was exactly the right thing to do. This is how we prevent security breaches."
    
    # Count how many details were remembered correctly
    $ correct_details = 0
    if remembered_appearance.get("height", "") == "medium":
        $ correct_details += 1
    if remembered_appearance.get("hair", "") == "brown":
        $ correct_details += 1
    if remembered_appearance.get("glasses", False) == False:
        $ correct_details += 1
    if remembered_appearance.get("id_card", False) == True:
        $ correct_details += 1
    if remembered_appearance.get("lanyard", True) == False:
        $ correct_details += 1
    if remembered_appearance.get("clothing", "") == "suit":
        $ correct_details += 1
    if remembered_appearance.get("clothing_color", "") == "navy blue/black":
        $ correct_details += 1
    if remembered_appearance.get("accessories", "") == "expensive watch":
        $ correct_details += 1
    
    # Award achievement if at least 4 details were remembered correctly
    if correct_details >= 7 and not persistent.achievements.get("detail_oriented", False):
        $ persistent.achievements["detail_oriented"] = True
        $ renpy.notify("Achievement Unlocked: Detail Oriented!")
    
    jump level_complete_ending

label level_complete_ending:
    scene bg office
    show screen top_bar
    show player happy
    with fade
    
    "Later that day, you receive an update from security."
    
    show player happy at left
    show security_head at right
    
    "Security Head" "Thanks to your report, we were able to identify and remove an unauthorized individual from the premises before any damage could be done."
    
    "Security Head" "Our investigation revealed she was attempting to access sensitive company information. Your attention to security protocols potentially prevented a significant data breach."
    
    hide security_head

    "The security head leaves, and the Boss walks in"

    show boss at right

    "Boss" "The company would like to recognize your vigilance. You'll be featured in next month's security newsletter as an example of excellent security awareness."
    "Boss" "She tried to trick you by using her fake 'Authority'. Apparently social engineers do this a lot!"
    
    "You feel proud that your actions helped protect the company."
    
    hide boss
    show player happy

    "LEVEL COMPLETE!"
    "You successfully identified and reported a social engineering attempt using tailgating to gain physical access to the building."
    
    "Key lessons learned:"
    "1. Always ensure proper badge scanning procedures are followed, even by those claiming authority."
    "2. Trust your instincts when something seems suspicious."
    "3. Report security concerns promptly through appropriate channels."
    "4. Pay attention to details that could help identify security threats."


    "THANK YOU!!"
    "YOU HAVE FINISHED ALL MY LEVELS"
    "YOU CAN CONTINUE HAVING A LOOK ARROUND, OR PLAY ANYTHING AGAIN!"
    "Maybe you can find a bug, see where other paths take you"
    "Please let me know what you think... AND MOST IMPORTANT, tell me you have finished :)"
    
    # Award achievement for completing Level 4
    if not persistent.achievements.get("physical_security_expert", False):
        $ persistent.achievements["physical_security_expert"] = True
        $ renpy.notify("Achievement Unlocked: Physical Security Expert!")
    
    # Add points to score
    $ persistent.game_progress["score"] += 50
    $ save_progress()
    
    jump level_complete

label level_failed_ending:
    scene bg boss_office
    show screen top_bar
    show boss at right
    show player shock at left
    with fade
    
    "The next morning, you're called into your Boss's office."
    
    "Boss" "We had a security incident yesterday. An unauthorized individual gained access to the building and accessed several secure areas before being detected."
    
    "Boss" "Security footage shows you interacting with this person at the entrance. Did you notice anything suspicious?"

    show player upset at left
    
    player "Yes, I did notice some things that seemed off, but I wasn't sure enough to report it."
    
    "Boss" "This is exactly why we emphasize the importance of reporting security concerns. Even if you're not certain, it's better to report a false alarm than to miss a genuine threat."
    
    "Boss" "In this case, the individual was able to access sensitive information before being caught. This could have serious consequences for the company."
    
    "You feel a sinking feeling as you realize the impact of your decision not to report the suspicious behavior."
    
    "LEVEL FAILED!"
    "You noticed suspicious behavior but failed to report it, allowing a security breach to occur."
    
    "Key lessons learned:"
    "1. Always report suspicious behavior, even if you're not certain."
    "2. Security is everyone's responsibility, not just the security team's."
    "3. Tailgating is a common social engineering tactic to gain unauthorized physical access."
    "4. Quick reporting can prevent or minimize the impact of security breaches."
    
    # Deduct points from score
    $ persistent.game_progress["score"] -= 10
    $ save_progress()
    
    jump level_failed

label timeout_handler:
    # This label handles timeout events from any timed challenge
    # Hide the timer screen (just to be sure)
    $ timer_active = False
    hide screen countdown_timer
    
    # Check which challenge the player is in and direct them to the appropriate timeout label
    if "phone_call" in current_challenge:
        jump phone_call_timeout
    elif "chat" in current_challenge:
        jump chat_timeout
    elif "document" in current_challenge:
        jump document_timeout
    else:
        # Default timeout handling if we can't determine the specific challenge
        "Time's up! You took too long to respond."
        $ persistent.game_progress["score"] -= 5
        $ save_progress()
        jump level_failed

# Add missing timeout handlers
label chat_timeout:
    "You hesitated too long and the conversation moved on without a proper response."
    "The person on the other end becomes suspicious of your delay."
    
    $ timer_active = False
    hide screen countdown_timer
    
    "Chat Challenge: FAILED"
    $ persistent.game_progress["score"] -= 5
    $ save_progress()
    "Let's continue to the next challenge."
    
    jump document_challenge
    
label document_timeout:
    "You took too long to review the document and make a decision."
    "In a real-world scenario, delays could lead to missed deadlines or opportunities for attackers."
    
    $ timer_active = False
    hide screen countdown_timer
    
    "Document Challenge: FAILED"
    $ persistent.game_progress["score"] -= 5
    $ save_progress()
    "Let's continue to the next challenge."
    
    jump document_challenge_two