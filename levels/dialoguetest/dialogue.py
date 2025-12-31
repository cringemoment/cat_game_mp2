from src.dialogue.dialogueobject import *

default = Dialogue([
    DialogueBox ("sprites/players/axodialogue1.png", "Alright, I know it's been a while since your last mission, so we're going to have you two complete a basic mission to get back up to speed."),
    DialogueBox("sprites/players/missioncontrol1.png", "Your goal is to get the candy currently in the hands of a five-year-old baby."),  #Mission Control
    DialogueBox("sprites/players/catdialogue1.png", "So... we're taking candy from a baby."), #Dude 1
    DialogueBox("sprites/players/missioncontrol1.png", "HEY! He's not a baby any more."), #Mission Control

    DialogueBox("sprites/players/catdialogue1.png", "And he can be a real pain sometimes..."),
    DialogueBox("sprites/players/catdialogue1.png", "Just like his father!!"), #Dude 1
    DialogueBox("sprites/players/catdialogue1.png", "Didn't know you had a kid."), # Dude 1
    DialogueBox("sprites/players/missioncontrol1.png", "What?"), #Mission Control
    DialogueBox("sprites/players/catdialogue1.png", "What?"), #Dude 1
    DialogueBox("sprites/players/missioncontrol1.png", "For the record, the kid's my brother's son."), #Mission Control
    DialogueBox("sprites/players/catdialogue1.png", "Does your brother know he's here?"), #Dude 1
    DialogueBox("sprites/players/missioncontrol1.png", "Enough questions, just complete this so we can move on to the important mission!"), #Mission Control
])

lookingfor = Dialogue([
    DialogueBox("sprites/players/axodialogue1.png", "I don't see it, do you?"), #Dude 1
    DialogueBox("sprites/players/axodialogue1.png", "No..."), #Dude 2
    DialogueBox("sprites/players/axodialogue1.png", "What are you guys looking for?"), #Mission Control
    DialogueBox("sprites/players/axodialogue1.png", "Our stuff."), #Dude 1
    DialogueBox("sprites/players/axodialogue1.png", "Stuff? What stuff?"), #Mission Control
    DialogueBox("sprites/players/axodialogue1.png", "You know, our equipment."), #Dude 1
    DialogueBox("sprites/players/axodialogue1.png", "You have everything you need."), #Mission Control
    DialogueBox("sprites/players/axodialogue1.png", "What about our guns?"), #Dude 1
])

helloyellowguy = Dialogue([
    DialogueBox("sprites/players/axodialogue1.png", "Hello, little guy!"),
    DialogueBox("sprites/players/axodialogue1.png", "I don't think boxes can talk...")
])

dialogues = {
    "default": default,
    "secondroomdialogue": lookingfor,
    "helloyellowguy": helloyellowguy
}
