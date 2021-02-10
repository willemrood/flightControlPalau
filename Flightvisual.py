import pygame as pg

""" This file contains all the visual stuff that is used in the game"""
def SURFCENT(a,b):
    c   = (b[0] - a.get_width()//2, b[1]-a.get_height()//2)
    return c


pg.init()
#universal stuff
reso   = (1280, 720)
middle = (640,360)
icon   = pg.image.load("icon.png")

#for the menuloop
mcolor      = (255,255,0)
lcolor      = (0,0,210)
lfont       = pg.font.SysFont("calibri", 32, True)
mfont       = pg.font.SysFont("calibri", 80, True)
menubg      = pg.image.load("menu.jpg")
menubg      = pg.transform.scale(menubg,reso)
menubgrect  = menubg.get_rect()
starttxt    = mfont.render("START GAME", False, mcolor)
startpos    = SURFCENT(starttxt,(640,550))
abouttxt    = mfont.render("ABOUT", False, mcolor)
aboutpos    = (25,635)
lboardtxt   = mfont.render("LEADERBOARD", False, lcolor)
lboardpos   = SURFCENT(lboardtxt,(640,50))
lboardleft  = 250
lboardright = 800

#for the aboutloop
aboutbg      = pg.image.load("palau1.jpg")
aboutbg      = pg.transform.scale(aboutbg,reso)
aboutbgrect  = aboutbg.get_rect()
storytxt     = pg.image.load("story.png")
storypos     = SURFCENT(storytxt,(640,300))
controls     = pg.image.load("controls.png")
controlsrect = controls.get_rect()
controlspos  = SURFCENT(controls,(640,600))
backtxt      = mfont.render("BACK", False, mcolor)
backpos      = (10,10)

#for the gameloop
gcolor     = (255,255,0)
linecolor  = (255,255,255)
gfont       = pg.font.SysFont("calibri", 30, True)
gamebg     = pg.image.load("Palau.jpg")
gamebg     = pg.transform.scale(gamebg, reso)
gamebgrect = gamebg.get_rect()
cloud      = pg.image.load("cloud.png")
p1         = pg.image.load("A330.png")
p2         = pg.image.load("Challenger350.png")
p3         = pg.image.load("A380.png")
p1         = pg.transform.rotate(p1, 180)
p2         = pg.transform.rotate(p2, 180)
p3         = pg.transform.rotate(p3, 180)


#for the dead/score
dcolor      = (255,255,0)
deadbg      = pg.image.load("palau2.jpg")
deadbg      = pg.transform.scale(deadbg,reso)
deadbgrect  = deadbg.get_rect()
entertxt    = lfont.render("PRESS ENTER TO CONTINUE", False, dcolor)
enterpos    = SURFCENT(entertxt,(640,600))
nohscoretxt = lfont.render("NO HIGHSCORE, TRY AGAIN", False, dcolor)
nohscorepos =  SURFCENT(nohscoretxt, (640,350))
nametxt     = lfont.render("ENTER YOUR NAME:", False, dcolor)
namepos     = SURFCENT(nametxt, (640,350))

pg.quit()
del lfont, mfont, gfont #otherwise wont restart