from src.dialogue.dialogueobject import *

default = Dialogue([
    DialogueBox ("sprites/players/missioncontrol.png", "Alright, I know it's been a while since your last mission, so we're going to have you two complete a basic mission to get back up to speed."),
    DialogueBox("sprites/players/missioncontrol.png", "Your goal is to get the candy currently in the hands of a five-year-old child."),  #Mission Control
    DialogueBox("sprites/players/catdialogue.png", "So... we're taking candy from a baby."), #Dude 1
    DialogueBox("sprites/players/missioncontrolmad.png", "HEY! He's not a baby any more."), #Mission Control

    DialogueBox("sprites/players/missioncontrol.png", "And he can be a real pain sometimes..."),#Mission Control
    DialogueBox("sprites/players/missioncontrol.png", "Just like his father..."), #Mission Control
    DialogueBox("sprites/players/catsmug.png", "Didn't know you had a kid."), # Dude 1
    DialogueBox("sprites/players/missioncontrol.png", "What?"), #Mission Control
    DialogueBox("sprites/players/catdialogue.png", "What?"), #Dude 1
    DialogueBox("sprites/players/missioncontrol.png", "For the record, the kid's my brother's son."), #Mission Control
    DialogueBox("sprites/players/catdialogue.png", "Does your brother know he's here?"), #Dude 1
    DialogueBox("sprites/players/missioncontroldrop.png", "Enough questions, just complete this so we can move on to the important mission!"), #Mission Control
])

lookingfor = Dialogue([
    DialogueBox("sprites/players/catdialogue.png", "I don't see it, do you?"), #Dude 1
    DialogueBox("sprites/players/axolotldialogue.png", "No..."), #Dude 2
    DialogueBox("sprites/players/missioncontrol.png", "What are you guys looking for?"), #Mission Control
    DialogueBox("sprites/players/catdialogue.png", "Our stuff."), #Dude 1
    DialogueBox("sprites/players/missioncontrol.png", "Stuff? What stuff?"), #Mission Control
    DialogueBox("sprites/players/catdialogue.png", "You know, our equipment."), #Dude 1
    DialogueBox("sprites/players/missioncontrol.png", "You have everything you need."), #Mission Control
    DialogueBox("sprites/players/catdialogue.png", "What about our guns?"), #Dude 1
    DialogueBox("sprites/players/missioncontrol.png", "your"), #Mission Control
    DialogueBox("sprites/players/missioncontrol!!.png", "WHAT?!?!"), #Mission Control
    DialogueBox("sprites/players/catlookotherway.png", "guns."),  #Dude 1
    DialogueBox("sprites/players/missioncontrolmad.png", "YOU ARE TAKING CANDY FROM A CHILD"), #Mission Control
    DialogueBox("sprites/players/missioncontrolmad.png", "WHAT DO YOU NEED GUNS FOR!?!"), #Mission Control
    DialogueBox("sprites/players/axolotldialogue.png", "didn't you say he can be a pain..."), #Dude 2
    DialogueBox("sprites/players/missioncontrolmad.png", "NO, NO GUNS"), #Mission Control
    DialogueBox("sprites/players/axolotldialogue.png", "we're not going to hurt him"), #Dude 2
    DialogueBox("sprites/players/catdialogue.png", "ya we can use non-lethal bullets"), #Dude 1
    DialogueBox("sprites/players/missioncontrollines.png", "...non-lethal..."), #Mission Control
    DialogueBox("sprites/players/missioncontrollines.png", "..."), #Mission Control
    DialogueBox("sprites/players/catdialogue.png", "you there?"), #Dude 1
    DialogueBox("sprites/players/missioncontrollines.png", "just..."), #Mission Control
    DialogueBox("sprites/players/missioncontrollines.png", "just do your job please"), #Mission Control
])

helloyellowguy = Dialogue([
    DialogueBox("sprites/players/catdialogue.png", "hey look it’s the baby"),
    DialogueBox("sprites/players/kidwithcandydialogue.png", "I AM NOT A BABY"),
    DialogueBox("sprites/players/catdialogue.png", "that’s a nice lolly pop you got there"),
    DialogueBox("sprites/players/kidwithcandydialogue.png", "hehe, want one? i have a lot more"),
    DialogueBox("sprites/players/catdialogue.png", "really? that’s awfully nice of you, yes please, and one for my friend here if you-"),
    DialogueBox("sprites/players/kidwithcandydialogue.png", "WELL TOO BAD, CUZ THEY’ER ALLLLLL MINE"),
    DialogueBox("sprites/players/axolotldialogue.png", "what a brat"),
    DialogueBox("sprites/players/kidwithcandydialogue.png", "mine, mine, MINE"),
    DialogueBox("sprites/players/catdialogue.png", "isn't it past your bed time?"),
    DialogueBox("sprites/players/kidwithcandydialogue.png", "i don’t have a bed time, i do what i want, and you’re not getting ANY of this candy"),
    DialogueBox("sprites/players/catdialogue.png", "we’ll see about that"),
    DialogueBox("sprites/players/kidwithcandydialogue.png", "you’ll never get it, NEVER"),
    DialogueBox("sprites/players/catdialogue.png", "it would seem he closed the door"),
    DialogueBox("sprites/players/axolotldialogue.png", "we’ll just open it again")
])

end = Dialogue([
    DialogueBox("sprites/players/catdialogue.png", "that's a nice lolly pop you got there"),
    DialogueBox("sprites/players/kidwithcandydialogue.png", "i... uh... there's um.. i have a lot more"),
    DialogueBox("sprites/players/catdialogue.png", "really? don't mind if i do"),
])

dialogues = {
    ".default": default,
    "secondroomdialogue": lookingfor,
    "helloyellowguy": helloyellowguy,
    "end": end
}
