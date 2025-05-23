﻿################################################################################
## Initialization
################################################################################

init offset = -1


################################################################################
## Styles
################################################################################

style default:
    properties gui.text_properties()
    language gui.language

style input:
    properties gui.text_properties("input", accent=True)
    adjust_spacing False

style hyperlink_text:
    properties gui.text_properties("hyperlink", accent=True)
    hover_underline True

style gui_text:
    properties gui.text_properties("interface")


style button:
    properties gui.button_properties("button")

style button_text is gui_text:
    properties gui.text_properties("button")
    yalign 0.5


style label_text is gui_text:
    properties gui.text_properties("label", accent=True)

style prompt_text is gui_text:
    properties gui.text_properties("prompt")


style bar:
    ysize gui.bar_size
    left_bar Frame("gui/bar/left.png", gui.bar_borders, tile=gui.bar_tile)
    right_bar Frame("gui/bar/right.png", gui.bar_borders, tile=gui.bar_tile)

style vbar:
    xsize gui.bar_size
    top_bar Frame("gui/bar/top.png", gui.vbar_borders, tile=gui.bar_tile)
    bottom_bar Frame("gui/bar/bottom.png", gui.vbar_borders, tile=gui.bar_tile)

style scrollbar:
    ysize gui.scrollbar_size
    base_bar Frame("gui/scrollbar/horizontal_[prefix_]bar.png", gui.scrollbar_borders, tile=gui.scrollbar_tile)
    thumb Frame("gui/scrollbar/horizontal_[prefix_]thumb.png", gui.scrollbar_borders, tile=gui.scrollbar_tile)

style vscrollbar:
    xsize gui.scrollbar_size
    base_bar Frame("gui/scrollbar/vertical_[prefix_]bar.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile)
    thumb Frame("gui/scrollbar/vertical_[prefix_]thumb.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile)

style slider:
    ysize gui.slider_size
    base_bar Frame("gui/slider/horizontal_[prefix_]bar.png", gui.slider_borders, tile=gui.slider_tile)
    thumb "gui/slider/horizontal_[prefix_]thumb.png"

style vslider:
    xsize gui.slider_size
    base_bar Frame("gui/slider/vertical_[prefix_]bar.png", gui.vslider_borders, tile=gui.slider_tile)
    thumb "gui/slider/vertical_[prefix_]thumb.png"


style frame:
    padding gui.frame_borders.padding
    background Frame("gui/frame.png", gui.frame_borders, tile=gui.frame_tile)



################################################################################
## In-game screens
################################################################################


## Say screen ##################################################################
##
## The say screen is used to display dialogue to the player. It takes two
## parameters, who and what, which are the name of the speaking character and
## the text to be displayed, respectively. (The who parameter can be None if no
## name is given.)
##
## This screen must create a text displayable with id "what", as Ren'Py uses
## this to manage text display. It can also create displayables with id "who"
## and id "window" to apply style properties.
##
## https://www.renpy.org/doc/html/screen_special.html#say

screen say(who, what):

    window:
        id "window"

        if who is not None:

            window:
                id "namebox"
                style "namebox"
                text who id "who"

        text what id "what"


    ## If there's a side image, display it above the text. Do not display on the
    ## phone variant - there's no room.
    if not renpy.variant("small"):
        add SideImage() xalign 0.0 yalign 1.0


## Make the namebox available for styling through the Character object.
init python:
    config.character_id_prefixes.append('namebox')

style window is default
style say_label is default
style say_dialogue is default
style say_thought is say_dialogue

style namebox is default
style namebox_label is say_label


style window:
    xalign 0.5
    xfill True
    yalign gui.textbox_yalign
    ysize gui.textbox_height

    background Image("gui/textbox.png", xalign=0.5, yalign=1.0)

style namebox:
    xpos gui.name_xpos
    xanchor gui.name_xalign
    xsize gui.namebox_width
    ypos gui.name_ypos
    ysize gui.namebox_height

    background Frame("gui/namebox.png", gui.namebox_borders, tile=gui.namebox_tile, xalign=gui.name_xalign)
    padding gui.namebox_borders.padding

style say_label:
    properties gui.text_properties("name", accent=True)
    xalign gui.name_xalign
    yalign 0.5

style say_dialogue:
    properties gui.text_properties("dialogue")

    xpos gui.dialogue_xpos
    xsize gui.dialogue_width
    ypos gui.dialogue_ypos

    adjust_spacing False

## Input screen ################################################################
##
## This screen is used to display renpy.input. The prompt parameter is used to
## pass a text prompt in.
##
## This screen must create an input displayable with id "input" to accept the
## various input parameters.
##
## https://www.renpy.org/doc/html/screen_special.html#input

screen input(prompt):
    style_prefix "input"

    window:

        vbox:
            xanchor gui.dialogue_text_xalign
            xpos gui.dialogue_xpos
            xsize gui.dialogue_width
            ypos gui.dialogue_ypos

            text prompt style "input_prompt"
            input id "input"

style input_prompt is default

style input_prompt:
    xalign gui.dialogue_text_xalign
    properties gui.text_properties("input_prompt")

style input:
    xalign gui.dialogue_text_xalign
    xmaximum gui.dialogue_width


## Choice screen ###############################################################
##
## This screen is used to display the in-game choices presented by the menu
## statement. The one parameter, items, is a list of objects, each with caption
## and action fields.
##
## https://www.renpy.org/doc/html/screen_special.html#choice

screen choice(items):
    style_prefix "choice"

    vbox:
        for i in items:
            textbutton i.caption action i.action


style choice_vbox is vbox
style choice_button is button
style choice_button_text is button_text

style choice_vbox:
    xalign 0.5
    ypos 805
    yanchor 0.5

    spacing gui.choice_spacing

style choice_button is default:
    properties gui.button_properties("choice_button")

style choice_button_text is default:
    properties gui.text_properties("choice_button")


## Quick Menu screen ###########################################################
##
## The quick menu is displayed in-game to provide easy access to the out-of-game
## menus.

screen quick_menu():

    ## Ensure this appears on top of other screens.
    zorder 100

    if quick_menu:

        hbox:
            style_prefix "quick"

            xalign 0.5
            yalign 1.0

            textbutton _("Back") action Rollback()
            textbutton _("History") action ShowMenu('history')
            #textbutton _("Skip") action Skip() alternate Skip(fast=True, confirm=True)
            textbutton _("Auto") action Preference("auto-forward", "toggle")
            textbutton _("Help") action ShowMenu('help')
            #textbutton _("Save") action ShowMenu('save')
            #textbutton _("Q.Save") action QuickSave()
            #textbutton _("Q.Load") action QuickLoad()
            #textbutton _("Prefs") action ShowMenu('preferences')


## This code ensures that the quick_menu screen is displayed in-game, whenever
## the player has not explicitly hidden the interface.
init python:
    config.overlay_screens.append("quick_menu")

default quick_menu = True

style quick_button is default
style quick_button_text is button_text

style quick_button:
    properties gui.button_properties("quick_button")

style quick_button_text:
    properties gui.text_properties("quick_button")


################################################################################
## Main and Game Menu Screens
################################################################################

## Navigation screen ###########################################################
##
## This screen is included in the main and game menus, and provides navigation
## to other menus, and to start the game.

screen navigation():

    vbox:
        style_prefix "navigation"

        xpos gui.navigation_xpos
        yalign 0.5

        spacing gui.navigation_spacing

        if main_menu:

            textbutton _("Start") action Start()

        else:

            textbutton _("History") action ShowMenu("history")

            textbutton _("Save") action ShowMenu("save")

        textbutton _("Load") action ShowMenu("load")

        textbutton _("Preferences") action ShowMenu("preferences")

        if _in_replay:

            textbutton _("End Replay") action EndReplay(confirm=True)

        elif not main_menu:

            textbutton _("Main Menu") action MainMenu()

        textbutton _("About") action ShowMenu("about")

        if renpy.variant("pc") or (renpy.variant("web") and not renpy.variant("mobile")):

            ## Help isn't necessary or relevant to mobile devices.
            textbutton _("Help") action ShowMenu("help")

        if renpy.variant("pc"):

            ## The quit button is banned on iOS and unnecessary on Android and
            ## Web.
            textbutton _("Quit") action Quit(confirm=not main_menu)


style navigation_button is gui_button
style navigation_button_text is gui_button_text

style navigation_button:
    size_group "navigation"
    properties gui.button_properties("navigation_button")

style navigation_button_text:
    properties gui.text_properties("navigation_button")


## Main Menu screen ############################################################
##
## Used to display the main menu when Ren'Py starts.
##
## https://www.renpy.org/doc/html/screen_special.html#main-menu

screen main_menu():

    ## This ensures that any other menu screen is replaced.
    tag menu

    add gui.main_menu_background

    frame:
        xalign 0.99
        yalign 0.02
        background "#00000088"
        padding (10, 5)
        text "Score: [persistent.game_progress['score']]" color "#FFFFFF"
    
    vbox:
            xalign 0.5
            yalign 0.4
            spacing 20

            if persistent.game_progress and "current_level" in persistent.game_progress:
                # $ persistent.game_progress["current_level"] = "second_level"  # For testing use - change for specific level
                if persistent.game_progress["tutorial_seen"]:
                    textbutton "Continue" action Start(persistent.game_progress["current_level"]) text_style "main_menu_text"
                else:
                    textbutton "Play Now" action Start(persistent.game_progress["current_level"]) text_style "main_menu_text"             
            else:
                textbutton "Continue" action NullAction() text_style "main_menu_text"
            textbutton "Play Previous Levels" action Show("level_select") text_style "main_menu_text"
            textbutton "View Stats" action Show("stats_screen") text_style "main_menu_text"
            textbutton "Replay Tutorial" action Start("tutorial") text_style "main_menu_text"
            textbutton "Quit" action Quit(confirm=True) text_style "main_menu_text"


style main_menu_frame is empty
style main_menu_vbox is vbox
style main_menu_text is gui_text
style main_menu_title is main_menu_text
style main_menu_version is main_menu_text

style main_menu_frame:
    xsize 420
    yfill True

    background "gui/overlay/main_menu.png"

style main_menu_vbox:
    xalign 1.0
    xoffset -30
    xmaximum 1200
    yalign 1.0
    yoffset -30

style main_menu_text:
    properties gui.text_properties("main_menu", accent=True)
    font "gui/fonts/LEMONMILK-Medium.otf"
    size 32
    color "#000000"
    hover_color "#535353"

style main_menu_title:
    properties gui.text_properties("title")

style main_menu_version:
    properties gui.text_properties("version")


## Game Menu screen ############################################################
##
## This lays out the basic common structure of a game menu screen. It's called
## with the screen title, and displays the background, title, and navigation.
##
## The scroll parameter can be None, or one of "viewport" or "vpgrid".
## This screen is intended to be used with one or more children, which are
## transcluded (placed) inside it.

screen game_menu(title, scroll=None, yinitial=0.0, spacing=0):

    style_prefix "game_menu"

    if main_menu:
        add gui.main_menu_background
    else:
        add gui.game_menu_background

    frame:
        style "game_menu_outer_frame"

        hbox:

            ## Reserve space for the navigation section.
            frame:
                style "game_menu_navigation_frame"

            frame:
                style "game_menu_content_frame"

                if scroll == "viewport":

                    viewport:
                        yinitial yinitial
                        scrollbars "vertical"
                        mousewheel True
                        draggable True
                        pagekeys True

                        side_yfill True

                        vbox:
                            spacing spacing

                            transclude

                elif scroll == "vpgrid":

                    vpgrid:
                        cols 1
                        yinitial yinitial

                        scrollbars "vertical"
                        mousewheel True
                        draggable True
                        pagekeys True

                        side_yfill True

                        spacing spacing

                        transclude

                else:

                    transclude

    use navigation

    textbutton _("Return"):
        style "return_button"

        action Return()

    label title

    if main_menu:
        key "game_menu" action ShowMenu("main_menu")


style game_menu_outer_frame is empty
style game_menu_navigation_frame is empty
style game_menu_content_frame is empty
style game_menu_viewport is gui_viewport
style game_menu_side is gui_side
style game_menu_scrollbar is gui_vscrollbar

style game_menu_label is gui_label
style game_menu_label_text is gui_label_text

style return_button is navigation_button
style return_button_text is navigation_button_text

style game_menu_outer_frame:
    bottom_padding 45
    top_padding 180

    background "gui/overlay/game_menu.png"

style game_menu_navigation_frame:
    xsize 420
    yfill True

style game_menu_content_frame:
    left_margin 60
    right_margin 30
    top_margin 15

style game_menu_viewport:
    xsize 1380

style game_menu_vscrollbar:
    unscrollable gui.unscrollable

style game_menu_side:
    spacing 15

style game_menu_label:
    xpos 75
    ysize 180

style game_menu_label_text:
    size gui.title_text_size
    color gui.accent_color
    yalign 0.5

style return_button:
    xpos gui.navigation_xpos
    yalign 1.0
    yoffset -45


## About screen ################################################################
##
## This screen gives credit and copyright information about the game and Ren'Py.
##
## There's nothing special about this screen, and hence it also serves as an
## example of how to make a custom screen.

screen about():

    tag menu

    ## This use statement includes the game_menu screen inside this one. The
    ## vbox child is then included inside the viewport inside the game_menu
    ## screen.
    use game_menu(_("About"), scroll="viewport"):

        style_prefix "about"

        vbox:

            label "[config.name!t]"
            text _("Version [config.version!t]\n")

            ## gui.about is usually set in options.rpy.
            if gui.about:
                text "[gui.about!t]\n"

            text _("Made with {a=https://www.renpy.org/}Ren'Py{/a} [renpy.version_only].\n\n[renpy.license!t]")


style about_label is gui_label
style about_label_text is gui_label_text
style about_text is gui_text

style about_label_text:
    size gui.label_text_size


## Load and Save screens #######################################################
##
## These screens are responsible for letting the player save the game and load
## it again. Since they share nearly everything in common, both are implemented
## in terms of a third screen, file_slots.
##
## https://www.renpy.org/doc/html/screen_special.html#save https://
## www.renpy.org/doc/html/screen_special.html#load

screen save():

    tag menu

    use file_slots(_("Save"))


screen load():

    tag menu

    use file_slots(_("Load"))


screen file_slots(title):

    default page_name_value = FilePageNameInputValue(pattern=_("Page {}"), auto=_("Automatic saves"), quick=_("Quick saves"))

    use game_menu(title):

        fixed:

            ## This ensures the input will get the enter event before any of the
            ## buttons do.
            order_reverse True

            ## The page name, which can be edited by clicking on a button.
            button:
                style "page_label"

                key_events True
                xalign 0.5
                action page_name_value.Toggle()

                input:
                    style "page_label_text"
                    value page_name_value

            ## The grid of file slots.
            grid gui.file_slot_cols gui.file_slot_rows:
                style_prefix "slot"

                xalign 0.5
                yalign 0.5

                spacing gui.slot_spacing

                for i in range(gui.file_slot_cols * gui.file_slot_rows):

                    $ slot = i + 1

                    button:
                        action FileAction(slot)

                        has vbox

                        add FileScreenshot(slot) xalign 0.5

                        text FileTime(slot, format=_("{#file_time}%A, %B %d %Y, %H:%M"), empty=_("empty slot")):
                            style "slot_time_text"

                        text FileSaveName(slot):
                            style "slot_name_text"

                        key "save_delete" action FileDelete(slot)

            ## Buttons to access other pages.
            vbox:
                style_prefix "page"

                xalign 0.5
                yalign 1.0

                hbox:
                    xalign 0.5

                    spacing gui.page_spacing

                    textbutton _("<") action FilePagePrevious()
                    key "save_page_prev" action FilePagePrevious()

                    if config.has_autosave:
                        textbutton _("{#auto_page}A") action FilePage("auto")

                    if config.has_quicksave:
                        textbutton _("{#quick_page}Q") action FilePage("quick")

                    ## range(1, 10) gives the numbers from 1 to 9.
                    for page in range(1, 10):
                        textbutton "[page]" action FilePage(page)

                    textbutton _(">") action FilePageNext()
                    key "save_page_next" action FilePageNext()

                if config.has_sync:
                    if CurrentScreenName() == "save":
                        textbutton _("Upload Sync"):
                            action UploadSync()
                            xalign 0.5
                    else:
                        textbutton _("Download Sync"):
                            action DownloadSync()
                            xalign 0.5


style page_label is gui_label
style page_label_text is gui_label_text
style page_button is gui_button
style page_button_text is gui_button_text

style slot_button is gui_button
style slot_button_text is gui_button_text
style slot_time_text is slot_button_text
style slot_name_text is slot_button_text

style page_label:
    xpadding 75
    ypadding 5

style page_label_text:
    textalign 0.5
    layout "subtitle"
    hover_color gui.hover_color

style page_button:
    properties gui.button_properties("page_button")

style page_button_text:
    properties gui.text_properties("page_button")


## Preferences screen ##########################################################
##
## The preferences screen allows the player to configure the game to better suit
## themselves.
##
## https://www.renpy.org/doc/html/screen_special.html#preferences

screen preferences():

    tag menu

    use game_menu(_("Preferences"), scroll="viewport"):

        vbox:

            hbox:
                box_wrap True

                if renpy.variant("pc") or renpy.variant("web"):

                    vbox:
                        style_prefix "radio"
                        label _("Display")
                        textbutton _("Window") action Preference("display", "window")
                        textbutton _("Fullscreen") action Preference("display", "fullscreen")

                vbox:
                    style_prefix "check"
                    label _("Skip")
                    textbutton _("Unseen Text") action Preference("skip", "toggle")
                    textbutton _("After Choices") action Preference("after choices", "toggle")
                    textbutton _("Transitions") action InvertSelected(Preference("transitions", "toggle"))

                ## Additional vboxes of type "radio_pref" or "check_pref" can be
                ## added here, to add additional creator-defined preferences.

            null height (4 * gui.pref_spacing)

            hbox:
                style_prefix "slider"
                box_wrap True

                vbox:

                    label _("Text Speed")

                    bar value Preference("text speed")

                    label _("Auto-Forward Time")

                    bar value Preference("auto-forward time")

                vbox:

                    if config.has_music:
                        label _("Music Volume")

                        hbox:
                            bar value Preference("music volume")

                    if config.has_sound:

                        label _("Sound Volume")

                        hbox:
                            bar value Preference("sound volume")

                            if config.sample_sound:
                                textbutton _("Test") action Play("sound", config.sample_sound)


                    if config.has_voice:
                        label _("Voice Volume")

                        hbox:
                            bar value Preference("voice volume")

                            if config.sample_voice:
                                textbutton _("Test") action Play("voice", config.sample_voice)

                    if config.has_music or config.has_sound or config.has_voice:
                        null height gui.pref_spacing

                        textbutton _("Mute All"):
                            action Preference("all mute", "toggle")
                            style "mute_all_button"


style pref_label is gui_label
style pref_label_text is gui_label_text
style pref_vbox is vbox

style radio_label is pref_label
style radio_label_text is pref_label_text
style radio_button is gui_button
style radio_button_text is gui_button_text
style radio_vbox is pref_vbox

style check_label is pref_label
style check_label_text is pref_label_text
style check_button is gui_button
style check_button_text is gui_button_text
style check_vbox is pref_vbox

style slider_label is pref_label
style slider_label_text is pref_label_text
style slider_slider is gui_slider
style slider_button is gui_button
style slider_button_text is gui_button_text
style slider_pref_vbox is pref_vbox

style mute_all_button is check_button
style mute_all_button_text is check_button_text

style pref_label:
    top_margin gui.pref_spacing
    bottom_margin 3

style pref_label_text:
    yalign 1.0

style pref_vbox:
    xsize 338

style radio_vbox:
    spacing gui.pref_button_spacing

style radio_button:
    properties gui.button_properties("radio_button")
    foreground "gui/button/radio_[prefix_]foreground.png"

style radio_button_text:
    properties gui.text_properties("radio_button")

style check_vbox:
    spacing gui.pref_button_spacing

style check_button:
    properties gui.button_properties("check_button")
    foreground "gui/button/check_[prefix_]foreground.png"

style check_button_text:
    properties gui.text_properties("check_button")

style slider_slider:
    xsize 525

style slider_button:
    properties gui.button_properties("slider_button")
    yalign 0.5
    left_margin 15

style slider_button_text:
    properties gui.text_properties("slider_button")

style slider_vbox:
    xsize 675


## History screen ##############################################################
##
## This is a screen that displays the dialogue history to the player. While
## there isn't anything special about this screen, it does have to access the
## dialogue history stored in _history_list.
##
## https://www.renpy.org/doc/html/history.html

screen history():

    tag menu

    ## Avoid predicting this screen, as it can be very large.
    predict False

    use game_menu(_("History"), scroll=("vpgrid" if gui.history_height else "viewport"), yinitial=1.0, spacing=gui.history_spacing):

        style_prefix "history"

        for h in _history_list:

            window:

                ## This lays things out properly if history_height is None.
                has fixed:
                    yfit True

                if h.who:

                    label h.who:
                        style "history_name"
                        substitute False

                        ## Take the color of the who text from the Character, if
                        ## set.
                        if "color" in h.who_args:
                            text_color h.who_args["color"]

                $ what = renpy.filter_text_tags(h.what, allow=gui.history_allow_tags)
                text what:
                    substitute False

        if not _history_list:
            label _("The dialogue history is empty.")


## This determines what tags are allowed to be displayed on the history screen.

define gui.history_allow_tags = { "alt", "noalt", "rt", "rb", "art" }


style history_window is empty

style history_name is gui_label
style history_name_text is gui_label_text
style history_text is gui_text

style history_label is gui_label
style history_label_text is gui_label_text

style history_window:
    xfill True
    ysize gui.history_height

style history_name:
    xpos gui.history_name_xpos
    xanchor gui.history_name_xalign
    ypos gui.history_name_ypos
    xsize gui.history_name_width

style history_name_text:
    min_width gui.history_name_width
    textalign gui.history_name_xalign

style history_text:
    xpos gui.history_text_xpos
    ypos gui.history_text_ypos
    xanchor gui.history_text_xalign
    xsize gui.history_text_width
    min_width gui.history_text_width
    textalign gui.history_text_xalign
    layout ("subtitle" if gui.history_text_xalign else "tex")

style history_label:
    xfill True

style history_label_text:
    xalign 0.5


## Help screen #################################################################
##
## A screen that gives information about key and mouse bindings. It uses other
## screens (keyboard_help, mouse_help, and gamepad_help) to display the actual
## help.

screen help():

    tag menu

    default device = "keyboard"

    use game_menu(_("Help"), scroll="viewport"):

        style_prefix "help"

        vbox:
            spacing 23

            hbox:

                textbutton _("Keyboard") action SetScreenVariable("device", "keyboard")
                textbutton _("Mouse") action SetScreenVariable("device", "mouse")

                if GamepadExists():
                    textbutton _("Gamepad") action SetScreenVariable("device", "gamepad")

            if device == "keyboard":
                use keyboard_help
            elif device == "mouse":
                use mouse_help
            elif device == "gamepad":
                use gamepad_help


screen keyboard_help():

    hbox:
        label _("Enter")
        text _("Advances dialogue and activates the interface.")

    hbox:
        label _("Space")
        text _("Advances dialogue without selecting choices.")

    hbox:
        label _("Arrow Keys")
        text _("Navigate the interface.")

    hbox:
        label _("Escape")
        text _("Accesses the game menu.")

    hbox:
        label _("Ctrl")
        text _("Skips dialogue while held down.")

    hbox:
        label _("Tab")
        text _("Toggles dialogue skipping.")

    hbox:
        label _("Page Up")
        text _("Rolls back to earlier dialogue.")

    hbox:
        label _("Page Down")
        text _("Rolls forward to later dialogue.")

    hbox:
        label "H"
        text _("Hides the user interface.")

    hbox:
        label "S"
        text _("Takes a screenshot.")

    hbox:
        label "V"
        text _("Toggles assistive {a=https://www.renpy.org/l/voicing}self-voicing{/a}.")

    hbox:
        label "Shift+A"
        text _("Opens the accessibility menu.")


screen mouse_help():

    hbox:
        label _("Left Click")
        text _("Advances dialogue and activates the interface.")

    hbox:
        label _("Middle Click")
        text _("Hides the user interface.")

    hbox:
        label _("Right Click")
        text _("Accesses the game menu.")

    hbox:
        label _("Mouse Wheel Up")
        text _("Rolls back to earlier dialogue.")

    hbox:
        label _("Mouse Wheel Down")
        text _("Rolls forward to later dialogue.")


screen gamepad_help():

    hbox:
        label _("Right Trigger\nA/Bottom Button")
        text _("Advances dialogue and activates the interface.")

    hbox:
        label _("Left Trigger\nLeft Shoulder")
        text _("Rolls back to earlier dialogue.")

    hbox:
        label _("Right Shoulder")
        text _("Rolls forward to later dialogue.")

    hbox:
        label _("D-Pad, Sticks")
        text _("Navigate the interface.")

    hbox:
        label _("Start, Guide, B/Right Button")
        text _("Accesses the game menu.")

    hbox:
        label _("Y/Top Button")
        text _("Hides the user interface.")

    textbutton _("Calibrate") action GamepadCalibrate()


style help_button is gui_button
style help_button_text is gui_button_text
style help_label is gui_label
style help_label_text is gui_label_text
style help_text is gui_text

style help_button:
    properties gui.button_properties("help_button")
    xmargin 12

style help_button_text:
    properties gui.text_properties("help_button")

style help_label:
    xsize 375
    right_padding 30

style help_label_text:
    size gui.text_size
    xalign 1.0
    textalign 1.0



################################################################################
## Additional screens
################################################################################


## Confirm screen ##############################################################
##
## The confirm screen is called when Ren'Py wants to ask the player a yes or no
## question.
##
## https://www.renpy.org/doc/html/screen_special.html#confirm

screen confirm(message, yes_action, no_action):

    ## Ensure other screens do not get input while this screen is displayed.
    modal True

    zorder 200

    style_prefix "confirm"

    add "gui/overlay/confirm.png"

    frame:

        vbox:
            xalign .5
            yalign .5
            spacing 45

            label _(message):
                style "confirm_prompt"
                xalign 0.5

            hbox:
                xalign 0.5
                spacing 150

                textbutton _("Yes") action yes_action
                textbutton _("No") action no_action

    ## Right-click and escape answer "no".
    key "game_menu" action no_action


style confirm_frame is gui_frame
style confirm_prompt is gui_prompt
style confirm_prompt_text is gui_prompt_text
style confirm_button is gui_medium_button
style confirm_button_text is gui_medium_button_text

style confirm_frame:
    background Frame([ "gui/confirm_frame.png", "gui/frame.png"], gui.confirm_frame_borders, tile=gui.frame_tile)
    padding gui.confirm_frame_borders.padding
    xalign .5
    yalign .5

style confirm_prompt_text:
    textalign 0.5
    layout "subtitle"

style confirm_button:
    properties gui.button_properties("confirm_button")

style confirm_button_text:
    properties gui.text_properties("confirm_button")


## Skip indicator screen #######################################################
##
## The skip_indicator screen is displayed to indicate that skipping is in
## progress.
##
## https://www.renpy.org/doc/html/screen_special.html#skip-indicator

screen skip_indicator():

    zorder 100
    style_prefix "skip"

    frame:

        hbox:
            spacing 9

            text _("Skipping")

            text "▸" at delayed_blink(0.0, 1.0) style "skip_triangle"
            text "▸" at delayed_blink(0.2, 1.0) style "skip_triangle"
            text "▸" at delayed_blink(0.4, 1.0) style "skip_triangle"


## This transform is used to blink the arrows one after another.
transform delayed_blink(delay, cycle):
    alpha .5

    pause delay

    block:
        linear .2 alpha 1.0
        pause .2
        linear .2 alpha 0.5
        pause (cycle - .4)
        repeat


style skip_frame is empty
style skip_text is gui_text
style skip_triangle is skip_text

style skip_frame:
    ypos gui.skip_ypos
    background Frame("gui/skip.png", gui.skip_frame_borders, tile=gui.frame_tile)
    padding gui.skip_frame_borders.padding

style skip_text:
    size gui.notify_text_size

style skip_triangle:
    ## We have to use a font that has the BLACK RIGHT-POINTING SMALL TRIANGLE
    ## glyph in it.
    font "DejaVuSans.ttf"


## Notify screen ###############################################################
##
## The notify screen is used to show the player a message. (For example, when
## the game is quicksaved or a screenshot has been taken.)
##
## https://www.renpy.org/doc/html/screen_special.html#notify-screen

screen notify(message):

    zorder 100
    style_prefix "notify"

    frame at notify_appear:
        text "[message!tq]" size 24  # Increased text size

    timer 6.25 action Hide('notify')  # Increased from 3.25 to 6.25 seconds


transform notify_appear:
    on show:
        alpha 0
        linear .25 alpha 1.0
    on hide:
        linear .5 alpha 0.0


style notify_frame is empty
style notify_text is gui_text

style notify_frame:
    ypos gui.notify_ypos

    background Frame("gui/notify.png", gui.notify_frame_borders, tile=gui.frame_tile)
    padding gui.notify_frame_borders.padding

style notify_text:
    properties gui.text_properties("notify")
    size 24  # Explicitly set size here as well


## NVL screen ##################################################################
##
## This screen is used for NVL-mode dialogue and menus.
##
## https://www.renpy.org/doc/html/screen_special.html#nvl


screen nvl(dialogue, items=None):

    window:
        style "nvl_window"

        has vbox:
            spacing gui.nvl_spacing

        ## Displays dialogue in either a vpgrid or the vbox.
        if gui.nvl_height:

            vpgrid:
                cols 1
                yinitial 1.0

                use nvl_dialogue(dialogue)

        else:

            use nvl_dialogue(dialogue)

        ## Displays the menu, if given. The menu may be displayed incorrectly if
        ## config.narrator_menu is set to True.
        for i in items:

            textbutton i.caption:
                action i.action
                style "nvl_button"

    add SideImage() xalign 0.0 yalign 1.0


screen nvl_dialogue(dialogue):

    for d in dialogue:

        window:
            id d.window_id

            fixed:
                yfit gui.nvl_height is None

                if d.who is not None:

                    text d.who:
                        id d.who_id

                text d.what:
                    id d.what_id


## This controls the maximum number of NVL-mode entries that can be displayed at
## once.
define config.nvl_list_length = gui.nvl_list_length

style nvl_window is default
style nvl_entry is default

style nvl_label is say_label
style nvl_dialogue is say_dialogue

style nvl_button is button
style nvl_button_text is button_text

style nvl_window:
    xfill True
    yfill True

    background "gui/nvl.png"
    padding gui.nvl_borders.padding

style nvl_entry:
    xfill True
    ysize gui.nvl_height

style nvl_label:
    xpos gui.nvl_name_xpos
    xanchor gui.nvl_name_xalign
    ypos gui.nvl_name_ypos
    yanchor 0.0
    xsize gui.nvl_name_width
    min_width gui.nvl_name_width
    textalign gui.nvl_name_xalign

style nvl_dialogue:
    xpos gui.nvl_text_xpos
    xanchor gui.nvl_text_xalign
    ypos gui.nvl_text_ypos
    xsize gui.nvl_text_width
    min_width gui.nvl_text_width
    textalign gui.nvl_text_xalign
    layout ("subtitle" if gui.nvl_text_xalign else "tex")

style nvl_thought:
    xpos gui.nvl_thought_xpos
    xanchor gui.nvl_thought_xalign
    ypos gui.nvl_thought_ypos
    xsize gui.nvl_thought_width
    min_width gui.nvl_thought_width
    textalign gui.nvl_thought_xalign
    layout ("subtitle" if gui.nvl_text_xalign else "tex")

style nvl_button:
    properties gui.button_properties("nvl_button")
    xpos gui.nvl_button_xpos
    xanchor gui.nvl_button_xalign

style nvl_button_text:
    properties gui.text_properties("nvl_button")


## Bubble screen ###############################################################
##
## The bubble screen is used to display dialogue to the player when using speech
## bubbles. The bubble screen takes the same parameters as the say screen, must
## create a displayable with the id of "what", and can create displayables with
## the "namebox", "who", and "window" ids.
##
## https://www.renpy.org/doc/html/bubble.html#bubble-screen

screen bubble(who, what):
    style_prefix "bubble"

    window:
        id "window"

        if who is not None:

            window:
                id "namebox"
                style "bubble_namebox"

                text who:
                    id "who"

        text what:
            id "what"

style bubble_window is empty
style bubble_namebox is empty
style bubble_who is default
style bubble_what is default

style bubble_window:
    xpadding 30
    top_padding 5
    bottom_padding 5

style bubble_namebox:
    xalign 0.5

style bubble_who:
    xalign 0.5
    textalign 0.5
    color "#000"

style bubble_what:
    align (0.5, 0.5)
    text_align 0.5
    layout "subtitle"
    color "#000"

define bubble.frame = Frame("gui/bubble.png", 55, 55, 55, 95)
define bubble.thoughtframe = Frame("gui/thoughtbubble.png", 55, 55, 55, 55)

define bubble.properties = {
    "bottom_left" : {
        "window_background" : Transform(bubble.frame, xzoom=1, yzoom=1),
        "window_bottom_padding" : 27,
    },

    "bottom_right" : {
        "window_background" : Transform(bubble.frame, xzoom=-1, yzoom=1),
        "window_bottom_padding" : 27,
    },

    "top_left" : {
        "window_background" : Transform(bubble.frame, xzoom=1, yzoom=-1),
        "window_top_padding" : 27,
    },

    "top_right" : {
        "window_background" : Transform(bubble.frame, xzoom=-1, yzoom=-1),
        "window_top_padding" : 27,
    },

    "thought" : {
        "window_background" : bubble.thoughtframe,
    }
}

define bubble.expand_area = {
    "bottom_left" : (0, 0, 0, 22),
    "bottom_right" : (0, 0, 0, 22),
    "top_left" : (0, 22, 0, 0),
    "top_right" : (0, 22, 0, 0),
    "thought" : (0, 0, 0, 0),
}



################################################################################
## Mobile Variants
################################################################################

style pref_vbox:
    variant "medium"
    xsize 675

## Since a mouse may not be present, we replace the quick menu with a version
## that uses fewer and bigger buttons that are easier to touch.
screen quick_menu():
    variant "touch"

    zorder 100

    if quick_menu:

        hbox:
            style_prefix "quick"

            xalign 0.5
            yalign 1.0

            textbutton _("Back") action Rollback()
            textbutton _("Skip") action Skip() alternate Skip(fast=True, confirm=True)
            textbutton _("Auto") action Preference("auto-forward", "toggle")
            textbutton _("Menu") action ShowMenu()


style window:
    variant "small"
    background "gui/phone/textbox.png"

style radio_button:
    variant "small"
    foreground "gui/phone/button/radio_[prefix_]foreground.png"

style check_button:
    variant "small"
    foreground "gui/phone/button/check_[prefix_]foreground.png"

style nvl_window:
    variant "small"
    background "gui/phone/nvl.png"

style main_menu_frame:
    variant "small"
    background "gui/phone/overlay/main_menu.png"

style game_menu_outer_frame:
    variant "small"
    background "gui/phone/overlay/game_menu.png"

style game_menu_navigation_frame:
    variant "small"
    xsize 510

style game_menu_content_frame:
    variant "small"
    top_margin 0

style pref_vbox:
    variant "small"
    xsize 600

style bar:
    variant "small"
    ysize gui.bar_size
    left_bar Frame("gui/phone/bar/left.png", gui.bar_borders, tile=gui.bar_tile)
    right_bar Frame("gui/phone/bar/right.png", gui.bar_borders, tile=gui.bar_tile)

style vbar:
    variant "small"
    xsize gui.bar_size
    top_bar Frame("gui/phone/bar/top.png", gui.vbar_borders, tile=gui.bar_tile)
    bottom_bar Frame("gui/phone/bar/bottom.png", gui.vbar_borders, tile=gui.bar_tile)

style scrollbar:
    variant "small"
    ysize gui.scrollbar_size
    base_bar Frame("gui/phone/scrollbar/horizontal_[prefix_]bar.png", gui.scrollbar_borders, tile=gui.scrollbar_tile)
    thumb Frame("gui/phone/scrollbar/horizontal_[prefix_]thumb.png", gui.scrollbar_borders, tile=gui.scrollbar_tile)

style vscrollbar:
    variant "small"
    xsize gui.scrollbar_size
    base_bar Frame("gui/phone/scrollbar/vertical_[prefix_]bar.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile)
    thumb Frame("gui/phone/scrollbar/vertical_[prefix_]thumb.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile)

style slider:
    variant "small"
    ysize gui.slider_size
    base_bar Frame("gui/phone/slider/horizontal_[prefix_]bar.png", gui.slider_borders, tile=gui.slider_tile)
    thumb "gui/phone/slider/horizontal_[prefix_]thumb.png"

style vslider:
    variant "small"
    xsize gui.slider_size
    base_bar Frame("gui/phone/slider/vertical_[prefix_]bar.png", gui.vslider_borders, tile=gui.slider_tile)
    thumb "gui/phone/slider/vertical_[prefix_]thumb.png"

style slider_vbox:
    variant "small"
    xsize None

style slider_slider:
    variant "small"
    xsize 900


## Score Bar screen ############################################################
##
## Used to displays current level and score.

screen top_bar():
    frame:
        xalign 0.01
        yalign 0.02
        background "#00000088"
        padding (15, 10)  # Increased padding for a bigger frame
        text "Score: [persistent.game_progress['score']]" color "#FFFFFF" size 28  # Increased text size from default to 28
        #text "Level: [persistent.game_progress['current_level']] | Score: [persistent.game_progress['score']]" color "#FFFFFF"


## Level Selection screen ############################################################
##
## Used to allow players to replay any completed level.

screen level_select():
    tag menu
    
    # Store the current level before navigating to a previous level
    python:
        if not hasattr(store, "original_level"):
            store.original_level = persistent.game_progress["current_level"]
        
        # Function to get a formatted level name
        def get_formatted_level_name(level_id):
            if level_id == "tutorial":
                return "Tutorial"
            elif level_id == "first_level":
                return "Level 1: The Networker"
            elif level_id == "second_level":
                return "Level 2: Check your mail!"
            elif level_id == "third_level":
                return "Level 3: Insider Threat"
            elif level_id == "fourth_level":
                return "Level 4: Physical Security - Tailgating"
            else:
                return level_id
    
    add "images/bg personal_office.png"
    
    frame:
        xalign 0.5
        yalign 0.5
        xsize 900
        ysize 630
        background "#000000ff"
        padding (30, 30)
        
        vbox:
            spacing 20
            xfill True
            
            text "Play Previous Levels" size 40 xalign 0.5 color "#FFFFFF"
            
            null height 10
            
            # Current level indicator
            frame:
                background "#FFFFFF22"
                padding (15, 15)
                xfill True
                
                vbox:
                    spacing 5
                    xalign 0.5
                    
                    $ formatted_current_level = get_formatted_level_name(persistent.game_progress["current_level"])
                    text "Current Level: [formatted_current_level]" size 20 color "#FFFFFF" xalign 0.5
                    text "You will return to this level after playing a previous level" size 16 color "#CCCCCC" xalign 0.5
            
            null height 10
            
            # Level selection area with scrollbar
            frame:
                background "#FFFFFF22"
                padding (20, 20)
                xfill True
                ysize 350  # Fixed height for scrollable area
                
                viewport:
                    scrollbars "vertical"
                    mousewheel True
                    draggable True
                    yinitial 0.0
                    xfill True
                    
                    vbox:
                        spacing 15
                        xfill True
                        
                        text "Available Levels" size 24 color "#FFFFFF" bold True xalign 0.5
                        
                        null height 10
                        
                        # Tutorial is always available
                        frame:
                            background "#333333"
                            padding (15, 15)
                            xfill True
                            
                            hbox:
                                spacing 20
                                xfill True
                                
                                vbox:
                                    xsize 600
                                    spacing 5
                                    
                                    text "Tutorial" size 22 color "#FFFFFF" bold True
                                    text "Learn the basics of the game" size 16 color "#CCCCCC"
                                
                                button:
                                    xalign 1.0
                                    yalign 0.5
                                    action [SetVariable("persistent.game_progress['temp_level']", persistent.game_progress["current_level"]), 
                                            Start("tutorial")]
                                    
                                    frame:
                                        background "#0099cc"
                                        padding (15, 10)
                                        hover_background "#66c1e0"
                                        
                                        text "Play" size 18 color "#FFFFFF"
                        
                        # Level 1 is always available
                        frame:
                            background "#333333"
                            padding (15, 15)
                            xfill True
                            
                            hbox:
                                spacing 20
                                xfill True
                                
                                vbox:
                                    xsize 600
                                    spacing 5
                                    
                                    text "Level 1: The Networker" size 22 color "#FFFFFF" bold True
                                    text "Learn to identify and respond to social engineering attempts" size 16 color "#CCCCCC"
                                
                                button:
                                    xalign 1.0
                                    yalign 0.5
                                    action [SetVariable("persistent.game_progress['temp_level']", persistent.game_progress["current_level"]), 
                                            Start("first_level")]
                                    
                                    frame:
                                        background "#0099cc"
                                        padding (15, 10)
                                        hover_background "#66c1e0"
                                        
                                        text "Play" size 18 color "#FFFFFF"
                        
                        # Level 2 is available if Level 1 is completed
                        if "first_level" in persistent.game_progress["completed_levels"]:
                            frame:
                                background "#333333"
                                padding (15, 15)
                                xfill True
                                
                                hbox:
                                    spacing 20
                                    xfill True
                                    
                                    vbox:
                                        xsize 600
                                        spacing 5
                                        
                                        text "Level 2: Check Your Mail!" size 22 color "#FFFFFF" bold True
                                        text "Identify and report phishing emails" size 16 color "#CCCCCC"
                                    
                                    button:
                                        xalign 1.0
                                        yalign 0.5
                                        action [SetVariable("persistent.game_progress['temp_level']", persistent.game_progress["current_level"]), 
                                                Function(reset_email_status),
                                                Start("second_level")]
                                        
                                        frame:
                                            background "#0099cc"
                                            padding (15, 10)
                                            hover_background "#66c1e0"
                                            
                                            text "Play" size 18 color "#FFFFFF"
                        
                        # Level 3 is available if Level 2 is completed
                        if "second_level" in persistent.game_progress["completed_levels"]:
                            frame:
                                background "#333333"
                                padding (15, 15)
                                xfill True
                                
                                hbox:
                                    spacing 20
                                    xfill True
                                    
                                    vbox:
                                        xsize 600
                                        spacing 5
                                        
                                        text "Level 3: Insider Threat" size 22 color "#FFFFFF" bold True
                                        text "Navigate complex security scenarios and respond to insider threats" size 16 color "#CCCCCC"
                                    
                                    button:
                                        xalign 1.0
                                        yalign 0.5
                                        action [SetVariable("persistent.game_progress['temp_level']", persistent.game_progress["current_level"]), 
                                                Start("third_level")]
                                        
                                        frame:
                                            background "#0099cc"
                                            padding (15, 10)
                                            hover_background "#66c1e0"
                                            
                                            text "Play" size 18 color "#FFFFFF"
                        
                        # Level 4 is available if Level 3 is completed
                        if "third_level" in persistent.game_progress["completed_levels"]:
                            frame:
                                background "#333333"
                                padding (15, 15)
                                xfill True
                                
                                hbox:
                                    spacing 20
                                    xfill True
                                    
                                    vbox:
                                        xsize 600
                                        spacing 5
                                        
                                        text "Level 4: Physical Security - Tailgating" size 22 color "#FFFFFF" bold True
                                        text "Learn to identify and respond to physical security threats like tailgating" size 16 color "#CCCCCC"
                                    
                                    button:
                                        xalign 1.0
                                        yalign 0.5
                                        action [SetVariable("persistent.game_progress['temp_level']", persistent.game_progress["current_level"]), 
                                                Start("fourth_level")]
                                        
                                        frame:
                                            background "#0099cc"
                                            padding (15, 10)
                                            hover_background "#66c1e0"
                                            
                                            text "Play" size 18 color "#FFFFFF"
            
            null height 10
            
            # Return button
            button:
                xalign 0.5
                action Return()
                
                frame:
                    background "#555555"
                    padding (20, 10)
                    hover_background "#777777"
                    
                    text "Return to Main Menu" size 20 color "#FFFFFF"

## Email Inbox Interface Screen ############################################################
##
## Used to display fake emails.

# Define the resizable background with rounded corners
image email_window = Frame("gui/email_assets/email_window.png", 20, 20, 20, 20)
image email_hover_rec = Frame("gui/email_assets/email_hover_rec.png", 20, 20, 20, 20)
image email_rec = Frame("gui/email_assets/email_rec.png", 20, 20, 20, 20)

screen email_inbox():
    modal True  # Ensures player must interact with this screen before continuing

    # Initialize selected_email_index if not defined
    default selected_email_index = -1

    frame:
        xsize 800
        ysize 500
        padding (20, 20)
        align (0.5, 0.5)
        background "email_window"  # Use the defined Frame as the background

        vbox:
            spacing 20
            xalign 0.5

            text "Inbox" size 40 bold True color "#000000"  # Title

            viewport:
                scrollbars "vertical"
                draggable True
                mousewheel True
                xsize 750
                ysize 400

                vbox:
                    spacing 10

                    if persistent.all_emails_correct:
                        timer 0.01 action [Hide("email_inbox")]
                    else:
                        for i, email in enumerate(persistent.emails):
                            $ is_selected = (i == selected_email_index)
                            $ answered_correctly = persistent.emails[i].get("answered_correctly", False)

                            button:
                                xsize 700
                                background "email_rec"
                                hover_background "email_hover_rec"  # Changes background on hover
                                padding (15, 10)
                                action [SetVariable("selected_email_index", i), Show("email_view")]

                                hbox:
                                    spacing 10
                                    xalign 0.0

                                    # Indicator Dot
                                    if answered_correctly:
                                        add Solid("#b5b5b5", xsize=15, ysize=15)  # Gray dot for correct (also increased)
                                        
                                        # Add a stamp-like indicator for what user selected (Safe or Phishing)
                                        frame:
                                            xsize 100
                                            ysize 45
                                            xalign 0.0
                                            xoffset 0
                                            padding (3, 3)
                                            margin (0, 0, 0, 0)
                                            
                                            # Red "PHISHING" or green "SAFE" indicator based on email type
                                            if email.get("is_phishing", False) == True:
                                                background Frame("#FFFFFF", Borders(2, 2, 2, 2))
                                                foreground Frame("#FF000055", Borders(2, 2, 2, 2))
                                                transform:
                                                    rotate 12  
                                                    text "PHISHING" size 18 color "#CC0000" bold True xalign 0.5 yalign 0.5 font "gui/fonts/LEMONMILK-Medium.otf" text_align 0.5 line_leading 0
                                            else:

                                                background Frame("#FFFFFF", Borders(2, 2, 2, 2))
                                                foreground Frame("#00AA0055", Borders(3, 3, 3, 3))
                                                transform:
                                                    rotate 12
                                                    text "SAFE" size 18 color "#008800" bold True xalign 0.5 yalign 0.5 font "gui/fonts/LEMONMILK-Medium.otf" text_align 0.5 line_leading 0
                                    else:
                                        add Solid("#0000FF", xsize=15, ysize=15)  # Blue dot

                                    vbox:
                                        spacing 5
                                        text "From: [email['from']]" size 20 bold True color "#000000"
                                        text "[email['subject']]" size 16 color "#000000"




## Individual Email Interface Screen ############################################################
##
## Used to display individual emails.

screen email_view():
    modal True
    frame:
        xsize 800
        ysize 500
        padding (20, 20)
        background "email_window" 
        align (0.5, 0.5)

        vbox:
            xalign 0.5
            spacing 20

            viewport:
                scrollbars "vertical"
                draggable True
                mousewheel True
                xsize 750
                ysize 450

                vbox:
                    spacing 10
                    xalign 0.5

                    # Display Email Header
                    text "To: You" size 20 bold True color "#555555" kerning 1.5
                    text "From: [persistent.emails[selected_email_index]['from']]" size 20 bold True color "#555555" kerning 1.5
                    text "Subject: [persistent.emails[selected_email_index]['subject']]" size 20 bold True color "#555555" kerning 1.5
                    text "[persistent.emails[selected_email_index]['body']]" size 16 color "#222222" kerning 1.5

                    hbox:
                        spacing 20
                        xalign 0.5

                        textbutton "Report as Phishing":
                            action [Function(check_email, True), Hide("email_view")]
                        
                        textbutton "Mark as Safe":
                            action [Function(check_email, False), Hide("email_view")]
                        
                        textbutton "Close":
                            action Hide("email_view")

## Phone Interface Screen ############################################################
##
## Used for the phone call challenge in level 3.

image phone_bg = Frame("gui/phone_assets/phone_bg.png", 20, 20, 20, 20)

screen phone_interface():
    modal False  # Changed to False to allow clicking anywhere to progress
    frame:
        xsize 400
        ysize 700
        background "phone_bg"
        align (0.75, 0.5)

        vbox:
            spacing 15
            xalign 0.5
            yalign 0.5

            text "Incoming Call" size 24 xalign 0.5 color "#000000"
            text "Unknown Number" size 20 xalign 0.5 color "#000000"
            
            null height 20
            
            text "Call in progress..." size 18 xalign 0.5 color "#555555"
            
            null height 150  # Increased to move button down
            
            hbox:
                spacing 30
                xalign 0.5
                
                imagebutton:
                    idle "gui/phone_assets/end_call.png"
                    hover "gui/phone_assets/end_call_hover.png"
                    action Show("end_call_confirmation")
                    tooltip "End Call"

## End Call Confirmation Screen ############################################################
##
## Confirmation dialog for ending a phone call.

screen end_call_confirmation():
    modal True
    zorder 200
    
    frame:
        xalign 0.5
        yalign 0.5
        xsize 500
        ysize 250
        background "#FFFFFF"
        
        vbox:
            spacing 20
            xalign 0.5
            yalign 0.5
            
            text "Are you sure you want to end the call?" size 22 xalign 0.5 color "#000000"
            text "You could be hanging up on a legitimate caller." size 18 xalign 0.5 color "#555555"
            
            null height 20
            
            hbox:
                spacing 50
                xalign 0.5
                
                textbutton "End Call":
                    action [Hide("end_call_confirmation"), Return()]
                
                textbutton "Continue Call":
                    action Hide("end_call_confirmation")

## Chat Interface Screen ############################################################
##
## Used for the chat challenge in level 3.

image chat_bg = Frame("gui/chat_assets/chat_bg.png", 20, 20, 20, 20)
image chat_bubble_them = Frame("gui/chat_assets/chat_bubble_them.png", 20, 20, 20, 20)
image chat_bubble_you = Frame("gui/chat_assets/chat_bubble_you.png", 20, 20, 20, 20)

screen chat_interface():
    modal False  # Allow clicking anywhere to progress
    frame:
        xsize 700
        ysize 500
        background "email_window"  # Use the same background as email for consistency
        align (0.5, 0.3)  # Move up by 300 pixels as requested
        
        vbox:
            spacing 10
            xalign 0.5
            yalign 0.0
            
            # Header with improved formatting
            text "Chat with Sarah - Finance" size 20 bold True color "#555555" kerning 1.5 xalign 0.5
            
            null height 10
            
            viewport:
                id "chat_viewport"
                xsize 670  # Reduced width to add padding from scrollbar
                ysize 400
                scrollbars "vertical"
                mousewheel True
                draggable True
                yinitial 1.0  # Start at the bottom
                
                vbox:
                    spacing 15
                    xfill True
                    
                    # Initial message from Sarah
                    frame:
                        background "#EEEEEE"  # Grey box for Sarah's messages
                        xsize 500
                        xalign 0.0
                        padding (15, 10)
                        
                        vbox:
                            spacing 5
                            text "Hi there! I'm working on reconciling some accounts and need the latest financial report for project Falcon. Can you send it to me?" size 16 color "#000000"
                            text "Sarah" size 12 color "#888888" xalign 0.0
                    
                    # Display all messages in the conversation history
                    if "_chat_history" in globals() and _chat_history:
                        for msg in _chat_history:
                            if msg["sender"] == "you":
                                frame:
                                    background "#0099cc"  # Blue box for your messages
                                    xsize 500
                                    xalign 1.0
                                    padding (15, 10)
                                    
                                    vbox:
                                        spacing 5
                                        text msg["text"] size 16 color "#FFFFFF"
                                        text "You" size 12 color "#DDDDDD" xalign 1.0
                            else:
                                frame:
                                    background "#EEEEEE"  # Grey box for Sarah's messages
                                    xsize 500
                                    xalign 0.0
                                    padding (15, 10)
                                    
                                    vbox:
                                        spacing 5
                                        text msg["text"] size 16 color "#000000"
                                        text "Sarah" size 12 color "#888888" xalign 0.0

## Chat Exit Confirmation Screen ############################################################
##
## Confirmation dialog for exiting a chat.

screen chat_exit_confirmation():
    modal True
    zorder 200
    
    frame:
        xalign 0.5
        yalign 0.5
        xsize 500
        ysize 250
        background "#FFFFFF"
        
        vbox:
            spacing 20
            xalign 0.5
            yalign 0.5
            
            text "Are you sure you want to exit this chat?" size 22 xalign 0.5 color "#000000"
            text "You may need to verify the sender's identity first." size 18 xalign 0.5 color "#555555"
            
            null height 20
            
            hbox:
                spacing 50
                xalign 0.5
                
                textbutton "Exit Chat":
                    action [Hide("chat_exit_confirmation"), Return()]
                
                textbutton "Continue Chat":
                    action Hide("chat_exit_confirmation")

## Document Interface Screen ############################################################
##
## Used for the document review challenge in level 3.

image document_bg = Frame("gui/document_assets/document_bg.png", 20, 20, 20, 20)

screen document_interface():
    modal False  # Allow clicking anywhere to progress
    frame:
        xsize 800
        ysize 500  # Reduced height for invoice document
        background "document_bg"
        align (0.5, 0.4)  # Moved up to avoid menu overlap
        
        vbox:
            spacing 10
            xalign 0.5
            yalign 0.5
            
            frame:
                background "#FFFFFF"
                xsize 750
                ysize 400  # Reduced height
                padding (20, 20)
                
                vbox:
                    spacing 10
                    
                    text "INVOICE" size 30 bold True xalign 0.5 color "#000000"
                    
                    null height 5  # Reduced spacing
                    
                    grid 2 4:
                        xfill True
                        spacing 10
                        
                        text "Invoice #:" size 16 bold True color "#000000"
                        text "INV-29384-XZ" size 16 color "#000000"
                        
                        text "Date:" size 16 bold True color "#000000"
                        text "October 15, 2023" size 16 color "#000000"
                        
                        text "Bill To:" size 16 bold True color "#000000"
                        text "CyberCorp Inc." size 16 color "#000000"
                        
                        text "Amount Due:" size 16 bold True color "#000000"
                        text "$12,450.00" size 16 color "#000000"
                    
                    null height 10  # Reduced spacing
                    
                    text "Payment Instructions:" size 18 bold True color "#000000"
                    text "Please remit payment to:" size 16 color "#000000"
                    text "Bank: First National Bank" size 16 color "#000000"
                    text "Account: 9834-5678-1234" size 16 color "#000000"
                    text "Routing: 021-456-789" size 16 color "#000000"
                    
                    null height 10  # Reduced spacing
                    
                    text "Note: Due to recent system changes, please use the new banking details above." size 14 italic True color "#FF0000"

## Score Panel Screen ############################################################
##
## Used to display the player's score and rank.

screen score_panel():
    frame:
        xalign 0.99
        yalign 0.1
        background "#00000088"
        padding (15, 10)
        
        vbox:
            spacing 5
            
            text "Score: [persistent.game_progress['score']]" color "#FFFFFF" size 20
            
            $ player_score = persistent.game_progress['score']
            
            if player_score >= 100:
                $ player_rank = "Expert"
            elif player_score >= 50:
                $ player_rank = "Intermediate"
            else:
                $ player_rank = "Novice"
                
            text "Rank: [player_rank]" color "#FFFFFF" size 18
            
            # Progress bar to next rank
            if player_rank == "Novice":
                $ progress_value = float(player_score) / 50.0
                $ next_rank = "Intermediate"
            elif player_rank == "Intermediate":
                $ progress_value = float(player_score - 50) / 50.0
                $ next_rank = "Expert"
            else:
                $ progress_value = 1.0
                $ next_rank = "Elite"
                
            text "Progress to [next_rank]:" color "#FFFFFF" size 14
            bar value progress_value range 1.0 xsize 150 ysize 10

## Stats Screen ############################################################
##
## Used to display player achievements and progress statistics.

screen stats_screen():
    tag menu
    
    add "images/bg personal_office.png"
    
    frame:
        xalign 0.5
        yalign 0.5
        xsize 900
        ysize 600
        background "#000000ff"
        padding (30, 30)
        
        vbox:
            spacing 20
            
            text "Player Statistics" size 40 xalign 0.5 color "#FFFFFF"
            
            null height 10
            
            hbox:
                spacing 40
                
                # Left column - Score and Rank
                vbox:
                    spacing 15
                    xsize 400
                    
                    text "Score and Rank" size 24 color "#FFFFFF" bold True
                    
                    frame:
                        background "#FFFFFF22"
                        padding (15, 15)
                        
                        vbox:
                            spacing 10
                            
                            text "Current Score: [persistent.game_progress['score']]" size 18 color "#FFFFFF"
                            text "Current Rank: [persistent.rank_data['current_rank']]" size 18 color "#FFFFFF"
                            
                            null height 5
                            
                            text "Progress to Next Rank:" size 16 color "#FFFFFF"
                            
                            $ current_rank = persistent.rank_data['current_rank']
                            $ score = persistent.game_progress['score']
                            
                            if current_rank == "Master" or current_rank == "Hacker":
                                $ progress_value = 1.0
                                $ next_rank = "Max rank"
                                $ points_needed = 0
                            elif current_rank == "Elite":
                                $ progress_value = float(score) / 350.0
                                $ next_rank = "Master"
                                $ points_needed = 350 - score
                            elif current_rank == "Expert":
                                $ progress_value = float(score) / 275
                                $ next_rank = "Elite"
                                $ points_needed = 275 - score
                            elif current_rank == "Intermediate":
                                $ progress_value = float(score) / 100
                                $ next_rank = "Expert"
                                $ points_needed = 100 - score
                            else:
                                $ progress_value = float(score) / 50.0
                                $ next_rank = "Intermediate"
                                $ points_needed = 50 - score
                            
                            bar value progress_value range 1.0 xsize 350 ysize 15
                            text "[points_needed] points needed for [next_rank]" size 14 color "#FFFFFF"
                    
                    null height 10
                    
                    text "Completed Levels" size 24 color "#FFFFFF" bold True
                    
                    frame:
                        background "#FFFFFF22"
                        padding (15, 15)
                        
                        vbox:
                            spacing 5
                            
                            if len(persistent.game_progress["completed_levels"]) == 0:
                                text "No levels completed yet" size 18 color "#FFFFFF"
                            else:
                                for level in persistent.game_progress["completed_levels"]:
                                    text "• [level]" size 18 color "#FFFFFF"
                
                # Right column - Achievements
                vbox:
                    spacing 15
                    xsize 400
                    
                    text "Achievements" size 24 color "#FFFFFF" bold True
                    
                    frame:
                        background "#FFFFFF22"
                        padding (15, 15)
                        
                        vbox:
                            spacing 10
                            
                            $ achievement_count = sum(1 for a in persistent.achievements.values() if a)
                            $ total_achievements = len(persistent.achievements)
                            
                            text "Unlocked: [achievement_count]/[total_achievements]" size 18 color "#FFFFFF"
                            
                            null height 10
                            
                            for name, unlocked in persistent.achievements.items():
                                hbox:
                                    spacing 10
                                    
                                    if unlocked:
                                        add "gui/button/check_selected_foreground.png" zoom 0.5
                                    else:
                                        add "gui/button/check_foreground.png" zoom 0.5
                                    
                                    if name == "quick_thinker":
                                        text "Quick Thinker - Make fast decisions under pressure" size 16 color "#FFFFFF"
                                    elif name == "vigilant_observer":
                                        text "Vigilant Observer - Correctly identify multiple phishing attempts" size 16 color "#FFFFFF"
                                    elif name == "security_expert":
                                        text "Security Expert - Complete all levels" size 16 color "#FFFFFF"
                                    elif name == "perfect_score":
                                        text "Perfect Score - Get a perfect score on any level" size 16 color "#FFFFFF"
                                    elif name == "level_three_master":
                                        text "Level Three Master - Achieve Expert rank in Level 3" size 16 color "#FFFFFF"
                                    elif name == "physical_security_expert":
                                        text "Physical Security Expert - Successfully identify and report a tailgating attempt" size 16 color "#FFFFFF"
                                    elif name == "detail_oriented":
                                        text "Detail Oriented - Accurately remember details about an intruder" size 16 color "#FFFFFF"
                                    elif name == "security_responder":
                                        text "Security Responder - Excel at the Level 4 Security Defense Game" size 16 color "#FFFFFF"
                                    elif name == "defense_master":
                                        text "Defense Master - Prevent all attacks in the Level 4 Security Defense Game" size 16 color "#FFFFFF"
            
            null height 20
            
            # Return button
            button:
                xalign 0.5
                action Return()
                
                frame:
                    background "#555555"
                    padding (20, 10)
                    hover_background "#777777"
                    
                    text "Return to Main Menu" size 20 color "#FFFFFF"

## Countdown Timer Screen ############################################################
##
## Used for timed challenges in level 3.

screen countdown_timer(duration):
    zorder 100
    
    default timer_value = duration
    default timer_bar_value = 1.0
    
    timer 0.1 repeat True action If(
        timer_active,
        [
            SetScreenVariable("timer_value", timer_value - 0.1),
            SetScreenVariable("timer_bar_value", timer_value / duration),
            If(
                timer_value <= 0,
                [
                    SetVariable("timer_active", False),
                    Hide("countdown_timer"),
                    Jump("timeout_handler")
                ]
            )
        ],
        NullAction()
    )
    
    frame:
        xalign 0.5
        yalign 0.05
        background "#00000088"
        padding (20, 15)  # Increased padding
        
        vbox:
            spacing 8  # Increased spacing
            xalign 0.5
            
            text "Time Remaining: {:.1f}".format(timer_value) color "#FFFFFF" size 24 xalign 0.5  # Increased text size
            
            bar value timer_bar_value range 1.0 xsize 250 ysize 20  # Larger bar
            
            if timer_value <= 5.0:
                text "Hurry!" color "#FF0000" size 22 xalign 0.5  # Increased warning text size

## Legal Document Interface Screen ############################################################
##
## Used for the legal document challenge in level 3.

image legal_document_bg = Frame("gui/document_assets/document_bg.png", 20, 20, 20, 20)

screen legal_document_interface():
    modal False  # Allow clicking anywhere to progress
    frame:
        xsize 800
        ysize 600
        background "legal_document_bg"
        align (0.5, 0.3)  # Moved up by 200 pixels as requested
        
        vbox:
            spacing 15
            xalign 0.5
            yalign 0.5
            
            frame:
                background "#FFFFFF"
                xsize 750
                ysize 500
                padding (20, 20)
                
                viewport:
                    scrollbars "vertical"
                    mousewheel True
                    draggable True
                    xfill True
                    yfill True
                    
                    vbox:
                        spacing 10
                        
                        text "NON-DISCLOSURE AGREEMENT" size 30 bold True xalign 0.5 color "#000000"
                        
                        null height 10
                        
                        text "This Non-Disclosure Agreement (the \"Agreement\") is entered into by and between:" size 16 color "#000000"
                        text "CyberCorp Inc. (\"Company\") and the undersigned Employee (\"Recipient\")" size 16 color "#000000"
                        
                        null height 20
                        
                        text "1. Confidential Information" size 18 bold True color "#000000"
                        text "Recipient agrees to maintain all Confidential Information in strict confidence and to not disclose such information to any third party. Recipient further agrees to grant CyberCorp access to all personal accounts and devices for security verification purposes." size 16 color "#000000"
                        
                        null height 10
                        
                        text "2. Term" size 18 bold True color "#000000"
                        text "This Agreement shall remain in effect for a period of five (5) years from the date of execution, regardless of employment status with the Company." size 16 color "#000000"
                        
                        null height 10
                        
                        text "3. Intellectual Property" size 18 bold True color "#000000"
                        text "Recipient agrees to assign all rights to any intellectual property created during or after employment with CyberCorp to the Company." size 16 color "#000000"
                        
                        null height 10
                        
                        text "4. Governing Law" size 18 bold True color "#000000"
                        text "This Agreement shall be governed by the laws of the jurisdiction of CyberCorp's choosing." size 16 color "#000000"
                        
                        null height 20
                        
                        text "By signing below, Recipient acknowledges having read and understood this Agreement and agrees to be bound by its terms." size 14 italic True color "#000000"
                        
                        null height 10
                        
                        text "URGENT: Please sign and return immediately to maintain project access." size 14 bold True color "#FF0000"

## Email Compose Screen ############################################################
##
## Used for composing emails in Level 4.

screen email_compose():
    modal False
    frame:
        xsize 800
        ysize 500
        background "gui/document_assets/document_bg.png"
        align (0.5, 0.5)
        
        vbox:
            spacing 15
            xalign 0.5
            yalign 0.5
            xfill True
            
            frame:
                background "#FFFFFF"
                xsize 750
                ysize 450
                padding (20, 20)
                
                vbox:
                    spacing 10
                    xfill True
                    
                    frame:
                        background "#F0F0F0"
                        padding (10, 10)
                        xfill True
                        
                        vbox:
                            spacing 5
                            xfill True
                            
                            hbox:
                                spacing 10
                                text "To:" size 16 color "#000000" bold True
                                text "security@cybercorp.com" size 16 color "#000000"
                            
                            hbox:
                                spacing 10
                                text "From:" size 16 color "#000000" bold True
                                text "you@cybercorp.com" size 16 color "#000000"
                            
                            hbox:
                                spacing 10
                                text "Subject:" size 16 color "#000000" bold True
                                if "email_content" in globals() and email_content.startswith("Subject:"):
                                    $ subject = email_content.split("\n")[0].replace("Subject: ", "")
                                    text "[subject]" size 16 color "#000000"
                                else:
                                    text "Potential Security Concern" size 16 color "#000000"
                    
                    null height 10
                    
                    frame:
                        background "#FFFFFF"
                        xfill True
                        yfill True
                        padding (10, 10)
                        
                        viewport:
                            scrollbars "vertical"
                            mousewheel True
                            draggable True
                            xfill True
                            yfill True
                            
                            vbox:
                                spacing 10
                                xfill True
                                
                                if "email_content" in globals():
                                    $ body = "\n".join(email_content.split("\n")[1:]) if "\n" in email_content else email_content
                                    text "[body]" size 16 color "#000000"
                                else:
                                    text "Email content will appear here." size 16 color "#000000"

## ID Card Screen ############################################################
##
## Used for displaying ID cards in Level 4.

image id_card = Composite(
    (400, 200),
    (0, 0), "gui/document_assets/document_bg.png",
    (20, 20), Text("CYBERCORP", size=24, color="#000000", bold=True),
    (20, 60), Text("EMPLOYEE IDENTIFICATION", size=16, color="#000000"),
    (20, 100), Text("Name: Alice Johnson", size=14, color="#000000"),
    (20, 120), Text("ID: 78291", size=14, color="#000000"),
    (20, 140), Text("Department: IT Security", size=14, color="#000000"),
    (20, 160), Text("Access Level: B", size=14, color="#000000"),
    (20, 180), Text("Issue Date: 01/15/2025", size=14, color="#000000"),
    (250, 50), "gui/document_assets/id_photo.png"
)
