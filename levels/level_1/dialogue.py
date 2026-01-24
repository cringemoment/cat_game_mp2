from src.dialogue.dialogueobject import *

default = Dialogue([
    DialogueBox("sprites/players/missioncontrol.png", "time to start the real mission, here’s the overview"),
    DialogueBox("sprites/players/missioncontrol.png","this building in front of you belongs to the evil organization known as ‘MORA’. We have reason to believe that inside there's the outline for something big. Your mission is to break in and take it so we can get an idea of what they're planning."),
    DialogueBox("sprites/players/catdialogue.png", "don't sound very sure of yourself huh"),
    DialogueBox("sprites/players/missioncontrol.png", "what do you mean"),
    DialogueBox("sprites/players/catdialogue.png","we have “reason” to “believe” there's an “outline” for “something”, we needed gat it to get an “idea”"),
    DialogueBox("sprites/players/missioncontrol.png","all right, all right, I get it. listen that’s just what’s written here, i didn’t write the script, okay?"),
    DialogueBox("sprites/players/catdialogue.png", "script? you make it sound like we’re in a movie or something"),
    DialogueBox("sprites/players/axolotldialogue.png", "or a game"),
    DialogueBox("sprites/players/catdialogue.png", "heck ya, like a really cool video game "),
    DialogueBox("sprites/players/missioncontrol.png", "THIS IS NOT A GAME, TAKE THIS SERIOUSLY GUYS"),
    DialogueBox("sprites/players/catdialogue.png", "what do you think is the most epic way to get in the building?"),
    DialogueBox("sprites/players/axolotldialogue.png", "front door"),
    DialogueBox("sprites/players/catdialogue.png", "YES, TO THE FRONT DOOR"),
    DialogueBox("sprites/players/missioncontrol.png", "WAIT"),
    DialogueBox("sprites/players/catdialogue.png", "what"),
    DialogueBox("sprites/players/missioncontrol.png","you will NOT be going through the front door, you'll be going up the side of the building to get to the top level"),
    DialogueBox("sprites/players/catdialogue.png", "sounds boring"),
    DialogueBox("sprites/players/missioncontrol.png","well to bad, you will go up the side of the building, and if anyone asks you two are just window cleaners, okay?"),
    DialogueBox("sprites/players/catdialogue.png", "fine")

])
'''random_window = Dialogue([
    DialogueBox("sprites/player/__.png", "we gotta invest in this stuff early"),
    DialogueBox("sprites/player/__.png", "but the boss said not to spend money on this"),
    DialogueBox("sprites/player/__.png", "we are not spending we’ll be making"),
    DialogueBox("sprites/player/missioncontrol.png", "investing?"),
    DialogueBox("sprites/player/missioncontrol.png", "wait, wait, go back, lets find out what that was"),
    DialogueBox("sprites/player/__.png", "well these graphics are very professional and everything but…"),
    DialogueBox("sprites/player/__.png", "what’s there to talk about? it’s a good offer, we take and make lots of money"),
    DialogueBox("sprites/player/__.png", "the boss would like that"),
    DialogueBox("sprites/player/missioncontrol.png", "invest in what, come on…"),
    DialogueBox("sprites/player/__.png", "let’s do a vote, all in favor?"),
    DialogueBox("sprites/player/__.png", "all right then it’s decided"),
    DialogueBox("sprites/player/missioncontrol.png", "come on come on"),
    DialogueBox("sprites/player/__.png", "we will invest 1 million in the __ company!"),
    DialogueBox("sprites/player/__.png", "YAY"),
    DialogueBox("sprites/player/missioncontrol.png", "huh"),
    DialogueBox("sprites/player/axolotldialogue.png", "well?"),
    DialogueBox("sprites/player/missioncontrol.png", "interesting, i've heard of them, they're new and were looking for investors, didn’t think they'd manage this."),
    DialogueBox("sprites/player/catdialogue.png", "so like are we going to do something"),
    DialogueBox("sprites/player/missioncontrol.png", "not right now, you have more important stuff to do. we’ll save this for later"),
    DialogueBox("sprites/player/catdialogue.png", "maybe we should invest, looks like it’s going to make a lot"),
    DialogueBox("sprites/player/missioncontrol.png", "WHAT?!?!?!?!?"),
    DialogueBox("sprites/player/missioncontrol.png", "IT’S A EVIL ORGANIZATION, WE CAN’T INVEST IN THAT")
])'''
dialogues = {
    "default": default,
    #"random_window": random_window
}
