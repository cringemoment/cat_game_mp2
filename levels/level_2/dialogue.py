from src.dialogue.dialogueobject import *

default = Dialogue([
    DialogueBox("sprites/players/missioncontrol.png", "we’ve got more information on that trash company, turns out there was more to that investment then just money. Long story short, we suspect that they’ve been collecting trash and shipping it out to MORA. your mission this time is to break into one of the garbage disposal facilities and find out what is being transported, where it’s going, and how it’s getting there"),
    DialogueBox("sprites/players/catdialogue.png", "you’re asking a lot from us"),
    DialogueBox("sprites/players/missioncontrol.png", "it’s pretty basic information, we just want to know what they're doing and where they’re doing it"),
    DialogueBox("sprites/players/catdialogue.png", "oh is that all?"),
    DialogueBox("sprites/players/missioncontrol.png", "… yes?"),
    DialogueBox("sprites/players/catdialogue.png", "i know how this goes, you ask use to do one thing and before we know it we have to go and do a whole bunch of stuff to save the world or whatever"),
    DialogueBox("sprites/players/missioncontrol.png", "yes, that is what we pay you for"),
    DialogueBox("sprites/players/axolotldialogue.png", "i think we need a raise"),
    DialogueBox("sprites/players/missioncontrol.png", "you are literally our best spies, you're already at the top, you can’t get a raise. also this counts as a bonus seeing as you’re retired and we called you back"),
    DialogueBox("sprites/players/catdialogue.png", "meaning…"),
    DialogueBox("sprites/players/missioncontrol.png", "MEANING YOU HAVE ENOUGH MONEY TO NOT COMPLAIN"),
    DialogueBox("sprites/players/missioncontrol.png", "what more do you want?"),
    DialogueBox("sprites/players/catdialogue.png", "i could go for some waffles right now.."),
    DialogueBox("sprites/players/missioncontrol.png", "then you can get some AFTER THE MISSION"),
    DialogueBox("sprites/players/missioncontrol.png", "what did i do to deserve this")

])

end = Dialogue([
    DialogueBox("sprites/players/racoondialogue.png", "it’s an honor to meet with one of our most important investors in person, with your help we’ve been able to achieve things we only dreamed about"),
    DialogueBox("sprites/players/racoondialoguetie.png", "don’t sell yourself short, your company has definitely exceeded expectations. our boss has been very pleased with the materials we’ve received so far"),
    DialogueBox("sprites/players/racoondialogue.png", "is that so? well it’s very good to hear that your investment was worthwhile. now, shall we get down to business?"),
    DialogueBox("sprites/players/missioncontrol.png", "this is it, we need to listen in on this, get closer but stay hidden"),
    DialogueBox("sprites/players/racoondialoguetie.png", "yes, this is our biggest order yet, are we going to ship it in the usual way?"),
    DialogueBox("sprites/players/racoondialogue.png", "yes, the train will leave at 12:00 pm in three days. as for the material, as you may know metal of this quality is hard to come by, not to mention the cables and electronics. we have plans to expand and have already some potential suppliers. however, I am sad to say the cost will be quite large because of the security needed to transport the goods. after all if we are caught it’s over for us and our suppliers."),
    DialogueBox("sprites/players/racoondialoguetie.png", "i understand, we will see what we can do"),
    DialogueBox("sprites/players/racoondialogue.png", "much appreciated"),
    DialogueBox("sprites/players/axolotldialogue.png", "the meeting’s over"),
    DialogueBox("sprites/players/missioncontrol.png", "yes and we still don’t know where they are shipping to. we will most likely need to infiltrate the train"),
    DialogueBox("sprites/players/catdialogue.png", "and by we you mean us"),
    DialogueBox("sprites/players/missioncontrol.png", "yes well, that is your job"),
    DialogueBox("sprites/players/catdialogue.png", "and what will you be doing?"),
    DialogueBox("sprites/players/missioncontrol.png", "i need to find out what station that train is leaving from"),
    DialogueBox("sprites/players/catdialogue.png", "do we get first class tickets?"),
    DialogueBox("sprites/players/missioncontrol.png", "what? no"),
    DialogueBox("sprites/players/catdialogue.png", "but why"),
    DialogueBox("sprites/players/missioncontrol.png", "because it’s most likely a freight train, so there won’t be a first class"),
    DialogueBox("sprites/players/catdialogue.png", "a what?"),
    DialogueBox("sprites/players/missioncontrol.png", "freight train, it’s for carrying cargo"),
    DialogueBox("sprites/players/catdialogue.png", "so what train will we be taking"),
    DialogueBox("sprites/players/missioncontrol.png", "... the freight train"),
    DialogueBox("sprites/players/catdialogue.png", "but we aren’t cargo"),
    DialogueBox("sprites/players/missioncontrol.png", "..."),
    DialogueBox("sprites/players/missioncontrol.png", "why are you like this")

])

dialogues = {
    ".default": default,
    "end": end
}
