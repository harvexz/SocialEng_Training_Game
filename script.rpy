# The script of the game goes in this file.

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
    
    # Timer scoring function
    python:
        def timer_score(response_time, score_variable):
            """
            Calculates and adds score based on response time.
            
            Args:
                base_points: Base points for the correct answer
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
    
    # Initialize _last_choice variable for chat interface
    $ _last_choice = ""
    
    show screen chat_interface
    with dissolve
    
    # Initialize timer variables
    $ timer_duration = 20.0  # 20 seconds for chat
    $ timer_active = True
    $ start_time = renpy.time.time()
    
    show screen countdown_timer(timer_duration)
    
    "Sarah_Finance" "Hi there! I'm working on reconciling some accounts and need the latest financial report for project Falcon. Can you send it to me?"
    
    menu:
        "Sure, I'll email it right away.":
            $ timer_active = False
            hide screen countdown_timer
            $ response_time = renpy.time.time() - start_time
            $ _last_choice = "Sure, I'll email it right away."
            
            # No points for this option
            jump chat_continue
            
        "I don't think I'm supposed to have access to that. Are you sure you have the right person?":
            $ response_time = renpy.time.time() - start_time
            $ _last_choice = "I don't think I'm supposed to have access to that. Are you sure you have the right person?"
            $ timer_score(5, response_time, "chat_score")
            jump chat_verify_person
            
        "Can you tell me which specific report you need?":
            $ response_time = renpy.time.time() - start_time
            $ _last_choice = "Can you tell me which specific report you need?"
            $ timer_score(3, response_time, "chat_score")
            jump chat_verify_report
            
        "Time's up!":
            $ timer_active = False
            hide screen countdown_timer
            jump chat_timeout

label chat_timeout:
    "Sarah_Finance" "Hello? Are you there? This is really urgent - I need that report ASAP!"
    
    menu:
        "Sorry, I was away from my desk. I'll send it right away.":
            jump chat_continue
        "I need to verify who you are first before sharing any reports.":
            $ chat_score += 8  # Slightly lower score for delayed response
            jump chat_verify_person

label chat_verify_person:
    # Update chat messages
    $ _last_sarah_message = "Oh, sorry! I thought you were on the finance team. But since you're not, could you forward me the contact info for someone who might have access?"
    
    hide screen chat_interface
    show screen chat_interface
    
    "Sarah_Finance" "Oh, sorry! I thought you were on the finance team. But since you're not, could you forward me the contact info for someone who might have access?"
    
    menu:
        "Sure, let me find someone for you.":
            $ _last_choice = "Sure, let me find someone for you."
            hide screen chat_interface
            show screen chat_interface
            jump chat_continue
            
        "I can check the company directory for you, but may I ask which department you're with?":
            $ _last_choice = "I can check the company directory for you, but may I ask which department you're with?"
            $ chat_score += 5
            $ renpy.notify("+5 points for verifying identity")
            hide screen chat_interface
            show screen chat_interface
            jump chat_verify_department
            
        "You should be able to find that in the company directory. Is there a reason you're asking me?":
            $ _last_choice = "You should be able to find that in the company directory. Is there a reason you're asking me?"
            $ chat_score += 8
            $ renpy.notify("+8 points for questioning suspicious behavior")
            hide screen chat_interface
            show screen chat_interface
            jump chat_suspicious
    
label chat_verify_department:
    # Update chat messages
    $ _last_sarah_message = "I'm with the finance team, but I'm new and still learning who handles what. I have a deadline this afternoon and my manager is out."
    
    hide screen chat_interface
    show screen chat_interface
    
    "Sarah_Finance" "I'm with the finance team, but I'm new and still learning who handles what. I have a deadline this afternoon and my manager is out."
    
    menu:
        "I understand. Let me help you find the right contact.":
            $ _last_choice = "I understand. Let me help you find the right contact."
            hide screen chat_interface
            show screen chat_interface
            jump chat_continue
            
        "What's your manager's name? Maybe I can help you reach them.":
            $ _last_choice = "What's your manager's name? Maybe I can help you reach them."
            $ chat_score += 5
            $ renpy.notify("+5 points for further verification")
            hide screen chat_interface
            show screen chat_interface
            jump chat_verify_manager
            
        "I'll need to verify your request through proper channels first.":
            $ _last_choice = "I'll need to verify your request through proper channels first."
            $ chat_score += 10
            $ renpy.notify("+10 points for following security protocol")
            hide screen chat_interface
            show screen chat_interface
            jump chat_success
    
label chat_verify_manager:
    # Update chat messages
    $ _last_sarah_message = "It's... um... John. But he's in meetings all day and unreachable. This is really urgent."
    
    hide screen chat_interface
    show screen chat_interface
    
    "Sarah_Finance" "It's... um... John. But he's in meetings all day and unreachable. This is really urgent."
    
    menu:
        "Okay, I'll try to help you out.":
            $ _last_choice = "Okay, I'll try to help you out."
            hide screen chat_interface
            show screen chat_interface
            jump chat_continue
            
        "That's strange, the finance department manager is actually Michelle, not John.":
            $ _last_choice = "That's strange, the finance department manager is actually Michelle, not John."
            $ chat_score += 10
            $ renpy.notify("+10 points for catching the lie")
            hide screen chat_interface
            show screen chat_interface
            jump chat_success
            
        "Let me check with HR to confirm you're a new hire before I share any information.":
            $ _last_choice = "Let me check with HR to confirm you're a new hire before I share any information."
            $ chat_score += 10
            $ renpy.notify("+10 points for thorough verification")
            hide screen chat_interface
            show screen chat_interface
            jump chat_success

label chat_verify_report:
    "Sarah_Finance" "The Q3 financial summary for Project Falcon. It should have all the budget allocations and expense reports."
    
    menu:
        "I'll look for it and send it over.":
            jump chat_continue
        "That contains sensitive information. Can you tell me why you need it?":
            $ chat_score += 5
            jump chat_verify_reason
        "Let me check if you're authorized to receive that report.":
            $ chat_score += 8
            jump chat_verify_authorization
    
label chat_verify_reason:
    "Sarah_Finance" "My manager asked me to review the expenses for any discrepancies before the board meeting tomorrow."
    
    menu:
        "That makes sense. I'll send it right away.":
            jump chat_continue
        "Which board meeting? I don't recall one being scheduled for tomorrow.":
            $ chat_score += 10
            jump chat_success
        "I'll need your manager to request this directly or approve your request via email.":
            $ chat_score += 10
            jump chat_success
    
label chat_verify_authorization:
    "Sarah_Finance" "Of course, I understand. But please hurry, this is time-sensitive. My employee ID is SF-29384 if that helps."
    
    menu:
        "Thanks, that's all I needed. I'll send the report shortly.":
            jump chat_continue
        "Let me verify that ID with the system first.":
            $ chat_score += 10
            jump chat_success
        "Can you also provide your company email so I can verify?":
            $ chat_score += 5
            jump chat_verify_email
    
label chat_verify_email:
    "Sarah_Finance" "It's sarah.j@financeteam-cybercorp.com"
    
    menu:
        "Thanks, I'll send the report to that email.":
            jump chat_continue
        "Our company email format is firstname.lastname@cybercorp.com. That doesn't look right.":
            $ chat_score += 10
            jump chat_success
        "Let me double-check that email in the directory.":
            $ chat_score += 8
            jump chat_success
    
label chat_suspicious:
    "Sarah_Finance" "I'm having trouble with the directory system. Plus, this is urgent and I thought you might be able to help me quickly."
    
    menu:
        "I understand. Let me see what I can do.":
            jump chat_continue
        "I'm going to check with the finance department directly to confirm this request.":
            $ chat_score += 10
            jump chat_success
        "Can you tell me more about Project Falcon? Just to make sure we're talking about the same thing.":
            $ chat_score += 8
            jump chat_verify_project
    
label chat_verify_project:
    "Sarah_Finance" "It's the new product development initiative... with the... marketing components and international expansion."
    
    menu:
        "That sounds right. I'll help you out.":
            jump chat_continue
        "Project Falcon is actually our internal infrastructure upgrade, not a product development initiative.":
            $ chat_score += 10
            jump chat_success
        "Let me verify this with the project manager before sharing any documents.":
            $ chat_score += 8
            jump chat_success
    
label chat_continue:
    "Sarah_Finance" "Great! You can just send it to my email: sarah.j@financeteam-cybercorp.com. Or upload it to this secure link: [file-share.cyber-docs.net/upload]"
    
    menu:
        "I'll email it to you right away.":
            jump chat_fail
        "I'll upload it to the link you provided.":
            jump chat_fail
        "I'll need to share this through our official company channels only.":
            $ chat_score += 10
            jump chat_success
    
label chat_fail:
    hide screen chat_interface
    
    "You shared sensitive financial information with an unverified person."
    "This was a social engineering attempt. 'Sarah' doesn't actually work in the finance department."
    "Confidential company information has now been compromised."
    
    $ persistent.game_progress["score"] -= 10
    $ save_progress()
    
    "Chat Challenge: FAILED"
    "Let's continue to the final challenge."
    
    jump document_challenge
    
label chat_success:
    hide screen chat_interface
    
    "After your questioning, 'Sarah' suddenly goes offline."
    "You report the suspicious chat to the security team, who confirm it came from outside the company network."
    
    "EXCELLENT WORK! You protected sensitive company information from a social engineering attack."
    
    $ persistent.game_progress["score"] += chat_score
    $ save_progress()
    
    "Chat Challenge: PASSED (Score: [chat_score])"
    "Let's continue to the final challenge."
    
    jump document_challenge

label document_challenge:
    scene bg office
    show screen top_bar
    show player happy
    with fade
    
    "You receive an email with an attached document that requires your urgent review and approval."
    
    show screen document_interface
    with dissolve
    
    # Initialize timer variables
    $ timer_duration = 25.0  # 25 seconds for document review
    $ timer_active = True
    $ start_time = renpy.time.time()
    
    show screen countdown_timer(timer_duration)
    
    "The document appears to be an invoice from a regular vendor, but something seems off about it."
    
    menu:
        "Check the sender's email address":
            $ response_time = renpy.time.time() - start_time
            $ timer_score(5, response_time, "document_score")
            "The email is from 'billing@venndor-invoices.com' instead of the usual 'accounting@vendor.com'"
            jump document_continue
            
        "Review the invoice details":
            $ response_time = renpy.time.time() - start_time
            $ timer_score(3, response_time, "document_score")
            "The invoice number format is different from previous ones, and the bank account details don't match your records."
            jump document_continue
            
        "Check both the sender and invoice details":
            $ response_time = renpy.time.time() - start_time
            $ timer_score(10, response_time, "document_score")
            "Both the sender's email address and invoice details appear suspicious and don't match previous legitimate communications."
            jump document_continue
            
        "Time's up!":
            $ timer_active = False
            hide screen countdown_timer
            jump document_timeout

label document_timeout:
    "You receive a follow-up email: 'Please process this invoice immediately to avoid late fees.'"
    
    menu:
        "Process the payment quickly since it's urgent":
            jump document_fail
        "Take time to verify the invoice details first":
            $ document_score += 5  # Reduced score for delayed verification
            jump document_verify_accounting

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
    "You reply to the email requesting additional verification."
    
    "Sender" "Please process the payment immediately to avoid late fees. Our accounting system is currently down, so we can't provide additional documentation right now."
    
    menu:
        "Process the payment since they can't provide documentation":
            jump document_fail
        "Insist on proper verification before processing":
            $ document_score += 10
            jump document_success
        "Escalate to your manager for guidance":
            $ document_score += 8
            jump document_escalate
    
label document_escalate:
    "Your Manager" "Good catch. This looks suspicious. Let's contact our vendor through our established channels to verify."
    
    "After contacting the real vendor, they confirm they did not send this invoice and have not changed their banking details."
    
    "WELL DONE! You prevented a fraudulent payment by escalating appropriately."
    
    $ persistent.game_progress["score"] += document_score + 5
    $ save_progress()
    
    "Document Challenge: PASSED (Score: [document_score + 5])"
    
    jump level_three_complete
    
label document_fail:
    hide screen document_interface
    
    "You processed a fraudulent invoice without proper verification."
    "This was a social engineering attempt designed to trick you into sending money to a fraudulent account."
    "Company funds have now been compromised."
    
    $ persistent.game_progress["score"] -= 15
    $ save_progress()
    
    "Document Challenge: FAILED"
    
    jump level_three_complete
    
label document_success:
    hide screen document_interface
    
    "You contact the vendor using your existing contact information, not the details in the email."
    "They confirm they did not send this invoice and have not changed their banking details."
    
    "EXCELLENT WORK! You prevented a fraudulent payment by following proper verification procedures."
    
    $ persistent.game_progress["score"] += document_score + 10
    $ save_progress()
    
    "Document Challenge: PASSED (Score: [document_score + 10])"
    
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
    
    "Welcome to the Security Breach Response Challenge!"
    "In this simulation, you'll need to protect your company's network from cyber attacks."
    
    "Here's how it works:"
    "1. Vulnerabilities will appear on different network nodes."
    "2. Click on vulnerable nodes to patch them before attackers can exploit them."
    "3. If an attacker reaches a vulnerable node, you'll lose points."
    "4. The challenge lasts for 60 seconds."
    
    "Are you ready to defend your network?"
    
    menu:
        "I'm ready!":
            jump security_game_start
        "Show me the tutorial first":
            jump security_game_tutorial
    
label security_game_tutorial:
    "Tutorial: Security Breach Response"
    
    "Network Nodes: These represent your company's computers and servers."
    "Vulnerabilities: These appear as yellow warning symbols on nodes."
    "Attackers: These appear as red dots moving toward vulnerable nodes."
    "Patching: Click on a vulnerable node to patch it and earn points."
    
    "The faster you patch vulnerabilities, the more points you'll earn."
    "If an attacker reaches a vulnerable node before you patch it, you'll lose points."
    
    "Ready to start now?"
    
    menu:
        "Let's go!":
            jump security_game_start
        "I need more time to prepare":
            "Take your time. Security is important!"
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
    
    # Show the game screen
    show screen security_breach_game
    
    # Wait for the game to complete (60 seconds)
    $ renpy.pause(60.0, hard=True)
    
    hide screen security_breach_game
    
    jump security_game_results
    
label security_game_results:
    scene bg office
    show screen top_bar
    show player happy
    with fade
    
    "Security Breach Response Challenge Complete!"
    
    "Your Results:"
    "Score: [security_game_score] points"
    "Vulnerabilities Patched: [vulnerabilities_patched]"
    "Attacks Prevented: [attacks_prevented]"
    "Attacks Succeeded: [attacks_succeeded]"
    
    # Calculate efficiency ratio if any vulnerabilities were patched
    if vulnerabilities_patched > 0:
        $ efficiency = float(attacks_prevented) / vulnerabilities_patched * 100
        $ efficiency_text = "{:.1f}%".format(efficiency)
        "Efficiency Rating: [efficiency_text]"
    
    if security_game_score >= 100:
        "EXCELLENT WORK! You're a cybersecurity expert!"
        # Award achievement
        if not persistent.achievements.get("security_responder", False):
            $ persistent.achievements["security_responder"] = True
            $ renpy.notify("Achievement Unlocked: Security Responder!")
    elif security_game_score >= 50:
        "GOOD JOB! Your quick responses protected the network."
    else:
        "KEEP PRACTICING! Security requires constant vigilance."
    
    # Add the security game score to the persistent score
    $ persistent.game_progress["score"] += security_game_score
    $ save_progress()
    
    "Remember these key lessons:"
    "1. Always verify the identity of anyone requesting sensitive information."
    "2. Never share passwords or credentials, even with IT staff."
    "3. Use established company channels for sharing sensitive documents."
    "4. When in doubt, escalate to your manager or security team."
    "5. Respond quickly to security vulnerabilities before they can be exploited."
    
    # Use the existing level_complete label
    jump level_complete