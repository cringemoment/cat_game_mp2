from src.renderer.spriteobject import Animation

idleanimation = Animation([
    "sprites/players/catidle1.png",
    "sprites/players/catidle2.png"
], 0.3)

idle2 = Animation([
    "sprites/players/axoidle1.png",
    "sprites/players/axoidle2.png"
], 0.3)

runninganim = Animation([
    "sprites/players/catrun1.png",
    "sprites/players/catrun2.png",
    "sprites/players/catrun3.png",
    "sprites/players/catrun4.png",
], 0.1)

runninganim2 = Animation([
    "sprites/players/axorun1.png",
    "sprites/players/axorun2.png",
    "sprites/players/axorun3.png",
    "sprites/players/axorun4.png",
], 0.1)

crouch = Animation([
    "sprites/players/catcrouch1.png",
    "sprites/players/catcrouch2.png",
    "sprites/players/catcrouch3.png",
    "sprites/players/catcrouch4.png",
    "sprites/players/catcrouch5.png",
    "sprites/players/catcrouch6.png",
    "sprites/players/catcrouch7.png",
], 0.01)

test_spritelist = {
"default": idleanimation,
"crouchanim": crouch,
"crouch": "sprites/players/catcrouch.png",
"running": runninganim
}

test_controller_spritelist = {
"default": idle2,
"crouchanim": "sprites/players/axocrouch.png",
"crouch": "sprites/players/axocrouch.png",
"running": runninganim2
}
