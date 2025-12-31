from src.dialogue.dialogueobject import *

default = Dialogue([
    DialogueBox ("sprites/players/missioncontrol.png", "Alright, I know it's been a while since your last mission, so we're going to have you two complete a basic mission to get back up to speed."),
    DialogueBox("sprites/players/missioncontrol.png", "Your goal is to get the candy currently in the hands of a five-year-old child."),  #Mission Control
    DialogueBox("sprites/players/catdialogue.png", "So... we're taking candy from a baby."), #Dude 1
    DialogueBox("sprites/players/missioncontrol.png", "HEY! He's not a baby any more."), #Mission Control

    DialogueBox("sprites/players/missioncontrol.png", "And he can be a real pain sometimes..."),#Mission Control
    DialogueBox("sprites/players/missioncontrol.png", "Just like his father..."), #Mission Control
    DialogueBox("sprites/players/catsmug.png", "Didn't know you had a kid."), # Dude 1
    DialogueBox("sprites/players/missioncontrol.png", "What?"), #Mission Control
    DialogueBox("sprites/players/catdialogue.png", "What?"), #Dude 1
    DialogueBox("sprites/players/missioncontrol.png", "For the record, the kid's my brother's son."), #Mission Control
    DialogueBox("sprites/players/catdialogue.png", "Does your brother know he's here?"), #Dude 1
    DialogueBox("sprites/players/missioncontrol.png", "Enough questions, just complete this so we can move on to the important mission!"), #Mission Control
])

lookingfor = Dialogue([
    DialogueBox("sprites/players/catdialogue.png", "I don't see it, do you?"), #Dude 1
    DialogueBox("sprites/players/axolotldialogue.png", "No..."), #Dude 2
    DialogueBox("sprites/players/missioncontrol.png", "What are you guys looking for?"), #Mission Control
    DialogueBox("sprites/players/axolotldialogue.png", "Our stuff."), #Dude 1
    DialogueBox("sprites/players/missioncontrol.png", "Stuff? What stuff?"), #Mission Control
    DialogueBox("sprites/players/catdialogue.png", "You know, our equipment."), #Dude 1
    DialogueBox("sprites/players/missioncontrol.png", "You have everything you need."), #Mission Control
    DialogueBox("sprites/players/axolotldialogue.png", "What about our guns?"), #Dude 1
])

helloyellowguy = Dialogue([
    DialogueBox("sprites/players/axolotldialogue.png", "Hello, little guy!"),
    DialogueBox("sprites/players/axolotldialogue.png", "I don't think boxes can talk...")
])

dialogues = {
    "default": default,
    "secondroomdialogue": lookingfor,
    "helloyellowguy": helloyellowguy
}
