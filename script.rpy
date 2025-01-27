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

    # Show a background. This uses a placeholder by default, but you can
    # add a file (named either "bg room.png" or "bg room.jpg") to the
    # images directory to show it.

    scene bg personal_office

    # This shows a character sprite. A placeholder is used, but you can
    # replace it by adding a file named "eileen happy.png" to the images
    # directory.

    "Welcome to the game, I hope you're ready to start!!"

    show player happy

    # These display lines of dialogue.

    #player "You've created a new Ren'Py game."

    #player "Once you add a story, pictures, and music, you can release it to the world!"

    #show player shock

    menu:
        "I'm ready":
            if not persistent.game_progress["tutorial_seen"]:
                $ persistent.game_progress["tutorial_seen"] = True
                $ save_progress()
                $ persistent.game_progress["current_level"] = "first_level"  # Set next level
            return
        
        "Wait im confused... say that again":
            jump tutorial

    # This ends the game.

    return



label level_complete:
    # Updating data for analysis and game save
    ## Updates for level completed

    "Level Complete!"
    if persistent.game_progress["current_level"] not in persistent.game_progress["completed_levels"]:
        $ persistent.game_progress["completed_levels"].append(persistent.game_progress["current_level"])
        $ persistent.game_progress["score"] += 20 # Add to score
        $ persistent.game_progress["replay_status"] = "not replay"
    else:
        $ persistent.game_progress["replay_status"] = "replay"
        $ persistent.game_progress["score"] += 1 # Add to score
    
    $ persistent.game_progress["level_status"] = "complete"
    $ save_progress()
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

    networker "Hey there! Sorry to bother you. I’m Alex from IT. We’ve got a critical server issue and I need access to the server room right away."

    menu:
        "Oh, sure! Let me unlock it for you.":  
            jump access_granted

        "I don’t recognize you. Can I see your ID?":
            jump request_id

        "We usually get emails about IT maintenance. I didn’t see one. Who sent you?":
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
    show player shock
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

        "That’s fine, just give me your name and I’ll check the employee database.":  
            jump check_database


label verify_story:

    show networker happy

    networker "Oh, right! Yeah, you wouldn’t have seen the email yet, it was just sent out. Mike from IT Security asked me to come fix it."

    menu:
        "Okay, let me just call Mike to confirm.":  
            jump call_supervisor

        "That makes sense. I'll let you in.":  
            jump access_granted


label deny_access:

    show networker angry

    networker "Look, I don’t have time for this. The server is down and it’s costing the company money. Just let me in!"

    menu:
        "I’m following protocol. You need to verify your identity first.":  
            jump insist_policy

        "Fine, go ahead.":  
            jump access_granted


label check_database:

    show player happy

    player "Give me a second, I’ll look you up in the employee database."

    show networker sad

    networker "Uh… you know what? I just remembered, I need to check something outside first. I’ll be back."

    show player happy

    "You watch as the 'IT technician' quickly walks away. Something felt off about that encounter."

    "CONGRATULATIONS! You stopped a potential social engineering attack by verifying identity."
    
    jump level_complete

    return


label call_supervisor:

    show player happy

    player "I’ll just give Mike a quick call to confirm you’re supposed to be here."

    show networker sad

    networker "Uh… you know what? Never mind. I think I got the wrong department."

    "The supposed IT worker quickly exits the building."

    "GREAT JOB! You followed security procedures and prevented an unauthorized entry attempt."

    jump level_complete

    return

label insist_policy:

    show networker angry

    networker "This is ridiculous! I’ll report you for slowing down IT work!"

    player "Go ahead. I’ll be happy to explain my actions to my supervisor."

    "The person storms off angrily. Later, IT confirms they never sent anyone, meaning you just stopped an attempted breach."

    "EXCELLENT WORK! You enforced security policies and protected company assets."

    jump level_complete

    return

