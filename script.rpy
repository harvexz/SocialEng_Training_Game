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
            "Amazing! Let's get started!"
            "We will jump back to the main menu, where you can start the next level!"
            if not persistent.game_progress["tutorial_seen"]:
                $ persistent.game_progress["tutorial_seen"] = True
                $ save_progress()
                $ persistent.game_progress["current_level"] = "first_level"  # Set next level
            else:
                # Check if we're returning from a previous level selection
                if hasattr(persistent.game_progress, "temp_level") and persistent.game_progress["temp_level"]:
                    $ persistent.game_progress["current_level"] = persistent.game_progress["temp_level"]
                    $ persistent.game_progress["temp_level"] = None
            return
        
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
            $ persistent.game_progress["current_level"] = "third_level"
    
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

    return


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
    "Your manager has asked you to check your email inbox for potential phishing emails."
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
    
    # Begin timer
    $ timer_duration = 15.0  # 15 seconds
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
    $ timer_duration = 15.0  # 15 seconds
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
    
    # Begin timer
    $ timer_duration = 15.0  # 15 seconds
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
        "Can you tell me who your manager is?":
            $ response_time = renpy.time.time() - start_time
            $ timer_score(response_time, "phone_score")
            jump phone_call_manager
    
label phone_call_manager:
    "Unknown Caller" "It's... uh... John. John Smith. Look, we're dealing with a potential security breach and need your password right away."
    
    # Begin timer
    $ timer_duration = 15.0  # 15 seconds
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
    
    # Begin timer
    $ timer_duration = 15.0  # 15 seconds
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
    
    # Begin timer
    $ timer_duration = 15.0  # 15 seconds
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
    
    # Begin timer
    $ timer_duration = 15.0  # 15 seconds
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
    
    # Begin timer
    $ timer_duration = 15.0  # 15 seconds
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
    
    "EXCELLENT WORK! You protected your credentials from a social engineering attack."
    
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
            $ chat_score += 5
            $ renpy.notify("+5 points for verifying identity")
            hide screen chat_interface
            show screen chat_interface
            jump chat_verify_department
            
        "You should be able to find that in the company directory. Is there a reason you're asking me?":
            $ _chat_history.append({"sender": "you", "text": "You should be able to find that in the company directory. Is there a reason you're asking me?"})
            $ chat_score += 8
            $ renpy.notify("+8 points for questioning suspicious behavior")
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
            $ chat_score += 10
            $ renpy.notify("+10 points for requesting verification")
            hide screen chat_interface
            show screen chat_interface
            jump chat_verify_id
            
        "Let me check with my supervisor first before sharing any information.":
            $ _chat_history.append({"sender": "you", "text": "Let me check with my supervisor first before sharing any information."})
            $ chat_score += 8
            $ renpy.notify("+8 points for following protocol")
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
            $ chat_score += 10
            $ renpy.notify("+10 points for catching the lie")
            hide screen chat_interface
            show screen chat_interface
            jump chat_success
            
        "Let me check with HR to confirm you're a new hire before I share any information.":
            $ _chat_history.append({"sender": "you", "text": "Let me check with HR to confirm you're a new hire before I share any information."})
            $ chat_score += 10
            $ renpy.notify("+10 points for thorough verification")
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
            $ chat_score += 5
            $ renpy.notify("+5 points for caution")
            hide screen chat_interface
            show screen chat_interface
            jump chat_verify_project
            
        "Can you tell me who authorized your access to Project Falcon?":
            $ _chat_history.append({"sender": "you", "text": "Can you tell me who authorized your access to Project Falcon?"})
            $ chat_score += 8
            $ renpy.notify("+8 points for verifying authorization")
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
            $ chat_score += 10
            $ renpy.notify("+10 points for following protocol")
            hide screen chat_interface
            show screen chat_interface
            jump chat_success
            
        "Can you provide your employee ID for verification?":
            $ _chat_history.append({"sender": "you", "text": "Can you provide your employee ID for verification?"})
            $ chat_score += 8
            $ renpy.notify("+8 points for requesting verification")
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
            $ chat_score += 8
            $ renpy.notify("+8 points for verification")
            hide screen chat_interface
            show screen chat_interface
            jump chat_verify_manager
            
        "I'll need to follow proper channels for this request. Let me submit a formal access request.":
            $ _chat_history.append({"sender": "you", "text": "I'll need to follow proper channels for this request. Let me submit a formal access request."})
            $ chat_score += 10
            $ renpy.notify("+10 points for following security protocol")
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
            $ chat_score += 10
            $ renpy.notify("+10 points for catching the lie")
            hide screen chat_interface
            show screen chat_interface
            jump chat_suspicious
            
        "Let me check with HR to confirm you're a new hire before I share any information.":
            $ _chat_history.append({"sender": "you", "text": "Let me check with HR to confirm you're a new hire before I share any information."})
            $ chat_score += 10
            $ renpy.notify("+10 points for thorough verification")
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
            $ chat_score += 15
            $ renpy.notify("+15 points for standing firm on security")
            hide screen chat_interface
            show screen chat_interface
            jump chat_success
            
        "I'll need to escalate this conversation to the security team.":
            $ _chat_history.append({"sender": "you", "text": "I'll need to escalate this conversation to the security team."})
            $ chat_score += 15
            $ renpy.notify("+15 points for involving security")
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
            $ chat_score += 10
            $ renpy.notify("+10 points for following email policy")
            hide screen chat_interface
            show screen chat_interface
            jump chat_verify_email
            
        "Let me check with IT about your email issues first.":
            $ _chat_history.append({"sender": "you", "text": "Let me check with IT about your email issues first."})
            $ chat_score += 15
            $ renpy.notify("+15 points for verifying with IT")
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
            $ chat_score += 10
            $ renpy.notify("+10 points for seeking approval")
            hide screen chat_interface
            show screen chat_interface
            jump chat_success
            
        "Let me help you contact IT to fix your email instead.":
            $ _chat_history.append({"sender": "you", "text": "Let me help you contact IT to fix your email instead."})
            $ chat_score += 15
            $ renpy.notify("+15 points for offering proper assistance")
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
    
    show screen document_interface
    with dissolve
    
    # Remove timer as requested in the CodeDevelopmentDocument
    
    "The document appears to be an invoice from a regular vendor, but something seems off about it."
    
    menu:
        "Check the sender's email address":
            "The email is from 'billing@venndor-invoices.com' instead of the usual 'accounting@vendor.com'"
            $ document_score += 5
            jump document_continue
            
        "Review the invoice details":
            "The invoice number format is different from previous ones, and the bank account details don't match your records."
            $ document_score += 3
            jump document_continue
            
        "Check both the sender and invoice details":
            "Both the sender's email address and invoice details appear suspicious and don't match previous legitimate communications."
            $ document_score += 10
            jump document_continue

label document_continue:
    "The email requests that you process this payment immediately due to a 'change in payment terms.'"
    
    menu:
        "Process the payment as requested":
            jump document_fail
        "Forward to accounting for verification":
            $ document_score += 5
            jump document_verify_accounting
        "Contact the vendor directly using your existing contact information":
            $ document_score += 10
            jump document_success
    
label document_verify_accounting:
    "You forward the invoice to the accounting department for verification."
    
    "Accounting Department" "This invoice doesn't match our records. The bank details are different, and we haven't been notified of any change in payment terms."
    
    menu:
        "Process the payment anyway since it's urgent":
            jump document_fail
        "Inform the sender that we need additional verification":
            $ document_score += 5
            jump document_request_verification
        "Report this as a potential fraud attempt":
            $ document_score += 10
            jump document_success
    
label document_request_verification:
    "You reply to the sender requesting additional verification of the invoice details."
    
    "Sender" "We cannot provide any additional verification. Please process the payment immediately to avoid late fees and service interruption."
    
    menu:
        "Process the payment to avoid service interruption":
            jump document_fail
        "Report this as a suspicious communication":
            $ document_score += 10
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
    
    # Create a new document interface for the legal document
    show screen legal_document_interface
    with dissolve
    
    "The document appears to be a non-disclosure agreement (NDA) related to a new company project."
    
    menu:
        "Check the sender's email address":
            "The email is from 'legal@cyber-corp-team.com' instead of the usual 'legal@cybercorp.com'"
            $ document_score += 5
            jump document_two_continue
            
        "Review the document details":
            "The document has several unusual clauses that seem overly broad, and the company name is slightly misspelled in places."
            $ document_score += 3
            jump document_two_continue
            
        "Check both the sender and document details":
            "Both the sender's email address and document details appear suspicious. The formatting is inconsistent with official company documents."
            $ document_score += 10
            jump document_two_continue

label document_two_continue:
    "The email states that you need to sign this document immediately as it's required for a time-sensitive project."
    
    menu:
        "Sign the document as requested":
            jump document_two_fail
        "Forward to the legal department for verification":
            $ document_score += 5
            jump document_two_verify_legal
        "Contact your supervisor to confirm this request":
            $ document_score += 10
            jump document_two_success
    
label document_two_verify_legal:
    "You forward the document to the legal department for verification."
    
    "Legal Department" "This is not an official company document. The clauses in this NDA would give unauthorized access to company intellectual property."
    
    menu:
        "Sign it anyway since it's marked as urgent":
            jump document_two_fail
        "Thank legal and discard the document":
            $ document_score += 10
            jump document_two_success
        "Reply asking for more information about the project":
            $ document_score += 5
            jump document_two_request_info

label document_two_request_info:
    "You reply asking for more details about the project mentioned in the NDA."
    
    "Sender" "This is a confidential project. Please sign the NDA first, and then we can share more details."
    
    menu:
        "Sign the document to learn more":
            jump document_two_fail
        "Report this as suspicious activity":
            $ document_score += 10
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
    
    if total_score >= 50:
        "OUTSTANDING PERFORMANCE! You demonstrated excellent security awareness."
    elif total_score >= 30:
        "GOOD JOB! You handled most situations appropriately."
    else:
        "NEEDS IMPROVEMENT. Review security protocols and try again."
    
    "Now, let's test your security response skills with a quick challenge!"
    
    jump start_security_game

# Security Breach Response Mini-Game
label start_security_game:
    scene bg office
    show screen top_bar
    
    "Welcome to the Social Engineering Defense Challenge!"
    "In this simulation, you'll need to protect your company from various social engineering attacks."
    
    "Here's how it works:"
    "1. Social engineering threats will appear on different communication channels (Email, Phone, Social Media)."
    "2. Click on at-risk channels to secure them before attackers can exploit them."
    "3. If an attacker reaches a vulnerable channel, you'll lose points."
    "4. The challenge lasts for 60 seconds."
    
    "Are you ready to defend against social engineering attacks?"
    
    menu:
        "I'm ready!":
            jump security_game_start
        "Show me the tutorial first":
            jump security_game_tutorial
    
label security_game_tutorial:
    "Tutorial: Social Engineering Defense"
    
    "Communication Channels: These represent your company's Email, Phone, and Social Media accounts."
    "Threats: These appear as yellow warning symbols on channels that are at risk."
    "Attackers: These appear as red dots moving toward vulnerable channels, representing phishers, impersonators, and scammers."
    "Defense: Click on a vulnerable channel to secure it and earn points."
    
    "The faster you identify and secure threats, the more points you'll earn."
    "If an attacker reaches a vulnerable channel before you secure it, you'll lose points."
    
    "Ready to start now?"
    
    menu:
        "Let's go!":
            jump security_game_start
        "I need more time to prepare":
            "Take your time. Security awareness is important!"
            jump security_game_tutorial
    
label security_game_start:
    # Initialize game variables
    $ security_game_score = 0
    $ vulnerabilities_patched = 0
    $ attacks_prevented = 0
    $ attacks_succeeded = 0
    $ game_time = 60.0
    $ spawn_timer = 2.0
    $ attacker_timer = 3.0
    $ attackers = []
    
    # Show the game screen - the game will run for 60 seconds
    # The screen itself will handle the timer and jumping to results
    show screen security_breach_game
    
    # This pause is just a fallback in case the screen timer fails
    $ renpy.pause(65.0, hard=True)
    
    jump security_game_results
    
label security_game_results:
    scene bg office
    show screen top_bar
    show player happy
    with fade
    
    "Social Engineering Defense Challenge Complete!"
    
    "Your Results:"
    "Score: [security_game_score] points"
    "Threats Identified: [vulnerabilities_patched]"
    "Attacks Prevented: [attacks_prevented]"
    "Security Breaches: [attacks_succeeded]"
    
    # Calculate efficiency ratio if any vulnerabilities were patched
    if vulnerabilities_patched > 0:
        $ efficiency = float(attacks_prevented) / vulnerabilities_patched * 100
        $ efficiency_text = "{:.1f}%".format(efficiency)
        "Defense Efficiency: [efficiency_text]"
    
    if security_game_score >= 100:
        "EXCELLENT WORK! You're a social engineering defense expert!"
        # Award achievement
        if not persistent.achievements.get("security_responder", False):
            $ persistent.achievements["security_responder"] = True
            $ renpy.notify("Achievement Unlocked: Security Responder!")
    elif security_game_score >= 50:
        "GOOD JOB! Your quick responses protected the company from social engineering attacks."
    else:
        "KEEP PRACTICING! Defending against social engineering requires constant vigilance."
    
    # Add the security game score to the persistent score
    $ persistent.game_progress["score"] += security_game_score
    $ save_progress()
    
    "Remember these key lessons about social engineering defense:"
    "1. Always verify the identity of anyone requesting sensitive information."
    "2. Be suspicious of urgent requests that pressure you to act quickly."
    "3. Use established company channels for sharing sensitive documents."
    "4. When in doubt, escalate to your manager or security team."
    "5. Respond quickly to security threats before they can be exploited."
    
    # Use the existing level_complete label
    jump level_complete