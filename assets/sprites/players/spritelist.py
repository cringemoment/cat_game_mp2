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

test_spritelist = {
"default": idleanimation,
"crouch": "sprites/players/catcrouch.png",
"running": runninganim
}

test_controller_spritelist = {
"default": idle2,
"crouch": "sprites/players/axocrouch.png",
"running": runninganim2
}
