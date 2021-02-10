"""
FLIGHT CONTROL

COMMENTS
- Flightvisual contains most of all the visual stuff that is used, apart from constantly changing surfaces like the score and timing.
- Flightfunctions contains functions for; spawning of planes and clouds, checking proximity of two points, and landing of the planes.
- further comments are within the code itself, at the end there's another comment box with closing remarks.
"""

import random as rnd
import numpy as np
import pygame as pg
import Flightfunctions as ff
import Flightvisual as fv

pg.init()
music = pg.mixer.music.load("ellavater.mp3")
volumemusic = 0.2
pg.mixer.music.set_volume(volumemusic)
explosion = pg.mixer.Sound("explosion.wav")
screen = pg.display.set_mode(fv.reso)
pg.display.set_caption("Flightcontrol Palau")
pg.display.set_icon(fv.icon)
lfont = pg.font.SysFont("calibri", 30, True) # menufont
gfont = pg.font.SysFont("calibri", 30, True) # gamefont

# loading the scores from data file
scorefile = open("highscores.dat","r")
lines = scorefile.readlines()
scores=[]
for line in lines:
    if len(line.strip())!=0:
        columns = line.split(";")
        name = columns[0].strip()
        score = columns[1].strip()
        scores.append([name,score])
scorefile.close()
scores=np.array(scores)

# Timing: check the closing remarks for my opinion on pg.get_ticks....
Hz = 30    # the set refresh rate, seems to run pretty stable across the board..
dt = 1/Hz  # duration of one frame

# initiate loops, starting with the menu
run       = True
menuloop  = True
aboutloop = False
gameloop  = False
scoreloop = False

while run:
    pg.mixer.music.play(-1)
# =======The menuloop
    while menuloop:
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    run      = False
                    menuloop = False
                if event.key == pg.K_RETURN:
                    menuloop = False
                    gameloop = True
            if event.type == pg.MOUSEBUTTONDOWN:
                c = pg.mouse.get_pos()
                if 423<c[0]<854 and 518<c[1]<569:
                    menuloop = False
                    gameloop = True
                if 20<c[0]<265 and 645<c[1]<695:
                    menuloop = False
                    aboutloop = True
        # blitting
        screen.blit(fv.menubg, fv.menubgrect)  # background
        screen.blit(fv.starttxt, fv.startpos)  # startgame
        screen.blit(fv.abouttxt, fv.aboutpos)  # About
        screen.blit(fv.lboardtxt,fv.lboardpos) # leaderboard
        n=1
        for i in range(10): #entries of said leaderboard
            entry = lfont.render(str(n)+" "+str(scores[i][0])+" "+str(scores[i][1]) , False, fv.lcolor)
            if i<5:
                screen.blit(entry, (fv.lboardleft,100+i*50))
            else:
                screen.blit(entry, (fv.lboardright,100+(i-5)*50))
            n+=1
        pg.display.flip()

#========The Aboutloop
    while aboutloop:
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    menuloop  = True
                    aboutloop = False
            if event.type == pg.MOUSEBUTTONDOWN:
                c = pg.mouse.get_pos()
                if 15<c[0]<185 and 15<c[1]<65: #clicking on back
                    menuloop = True
                    aboutloop = False
        # blitting
        screen.blit(fv.aboutbg, fv.aboutbgrect)  # background
        screen.blit(fv.controls, fv.controlspos) # controls image
        screen.blit(fv.storytxt, fv.storypos)    # backstory image
        screen.blit(fv.backtxt, fv.backpos)      # back to menu button
        pg.display.flip()

# =======The gameloop
# as a reminder, here's the contents of the planes and clouds arrays:
#planes: 0:type 1:rectangle 2:centerloc 3:hitbox 4:velocity vector 5:velocity multiplier 6:angle 7:lines 8:scale 9:collideable 10: points
#clouds: 0:rectangle 1:centerloc 2:velocity vector 3:angle
    if gameloop: #init for the game
        t0          = 0.001*pg.time.get_ticks()
        speed       = 1 #arrow keys to enhance the gamespeed!!
        tgame       = 0
        score       = 0
        detail      = 15 #refinement of the paths being drawn. lower is more accurate but more jittery to follow... 15 works quite well
        planeid     = 0
        planes      = np.array([ff.PLANE()])
        clouds      = []
        c1, c2      = 0, 0
        hold        = False
        drawpath    = False
        difficulty  = 1
        spawnplane  = rnd.randint(3*Hz,20*Hz) #Random spawn of a new plane
        spawncloud  = 60*Hz #spawn first cloud after 1 minute

    while gameloop:
        t = 0.001*pg.time.get_ticks()  #as said, only the gameloop needs fixed timestep
        if t-t0 >= dt:
            t0=t
            tgame += (speed * dt)  # seconds
            if difficulty == 1 and score > 1000:
                difficulty = 2
            if difficulty == 2 and score > 2500:
                difficulty = 3
            if difficulty == 3 and score > 5000:
                difficulty = 4
            if difficulty == 4 and score > 7500:
                difficulty = 5    
            if difficulty == 5 and score > 10000:
                difficulty = 6
            if difficulty == 6 and score > 12500:
                difficulty = 7
            if difficulty == 7 and score > 15000:
                difficulty = 8    
            score += 2*difficulty * dt * speed  # guaranteed points per second, avoids equalling scores in leaderboard

            # spawn of new plane
            spawnplane -= 1 * speed
            if spawnplane < 0:
                #three levels:
                spawnplane = rnd.randint(3 * Hz, (20/difficulty) * Hz)  # new spawn between 2 and 20/difficulty seconds
                planes = np.vstack((planes, ff.PLANE()))  # appends new spawn to planes array

            # spawn of a possible cloud
            spawncloud -=1
            if spawncloud<0:
                if len(clouds) > 0:
                    spawncloud = rnd.randint(30*Hz,60*Hz)
                    clouds = np.vstack((clouds, ff.CLOUD()))
                if len(clouds) == 0: #this one has to be second, since
                    spawncloud = rnd.randint(30*Hz,60*Hz)
                    clouds = np.array([ff.CLOUD()])

            # mother loop for planes
            for i in range(len(planes[:, 0])):
                # collision detection
                for j in range(i+1,len(planes[:, 0])):
                    if planes[i,9] and planes[j,9]: #only checking for collidable planes!
                        if ff.PCL(planes[i, 2],planes[j, 2],planes[i, 3]+planes[j, 3]):
                            gameloop = False
                            scoreloop = True
                            explosion.play()
                #out of bounds detection. range is 800 since the planes spawn in at around 750.
                if planes[i,9]: #only planes that are "in the air".
                    if not ff.PCL(planes[i,2],fv.middle,800):
                        scoreloop = True
                        gameloop  = False

                # Arrival at the runway using APPROACH function
                if planes[i,9] and ff.APP(planes[i,2],planes[i,6]):
                    if i == planeid:
                        drawpath    = False   #removes the ability to extend the path after landing...
                    planes[i,9] = False   #set plane to not collidable
                    score += planes[i,10] #adding points to total
                    planes[i,7] = []      #clearing the path
                    planes[i, 4], planes[i, 6] = ff.DRC(planes[i, 1].center, fv.middle) #directing plane to the middle

                # editing the scale for landed planes
                if not planes[i,9]:
                    planes[i,8] -= 0.003*speed * planes[i,5]*dt #lineair, exponential didn't work that well..

                # editing the velocity, angles and delete the closest point within range.
                if planes[i,9] and len(planes[i, 7]) > 0:
                    planes[i, 4], planes[i, 6] = ff.DRC(planes[i, 1].center, planes[i, 7][0])
                    if ff.PCL(planes[i, 1].center, planes[i, 7][0], detail):
                        del planes[i, 7][0]

                # movement of the planes, could also be done with np calc outside of the loop, however you cant call ".center"..
                planes[i, 2][0] += planes[i, 4][0] * speed * planes[i,5] *dt
                planes[i, 2][1] += planes[i, 4][1] * speed * planes[i,5] *dt
                planes[i, 1].center = planes[i, 2]

                # excluding planes that have landed from blitting
                if not planes[i,9] and planes[i,0] != 0 and ff.PCL(planes[i,2],fv.middle,10) :
                    planes[i,0]=0 #planetype is set to zero, and there's no blitting command for zero.

            # movement of the clouds
            if len(clouds) > 0:
                for i in range(len(clouds)):
                    clouds[i,1][0] += clouds[i,2][0] * speed*dt*60 #60 seemed like a decent fixed speed
                    clouds[i,1][1] += clouds[i,2][1] * speed*dt*60
                    clouds[i,0].center = clouds[i,1]

            # Drawing the flight paths, so rightmouse should be held down
            if hold:
                # this is to determine which plane is clicked:
                for i in range(len(planes[:, 0])):
                    # click within a certain range (30) of the center of the plane
                    if not drawpath and planes[i,9] and ff.PCL(c1, planes[i, 2], 30):
                        planes[i, 7] = []  # first reset or empty the previous drawn path
                        planeid = i  # this is the identifier of where to append the path tuples
                        drawpath = True
                if drawpath:
                    c2 = pg.mouse.get_pos()
                    # if next mouse pos is further than 'detail' pixels, a new pathpoint is appended
                    if not ff.PCL(c1, c2, detail):
                        planes[planeid, 7].append(c2)
                        c1 = c2 #oldposition is replaced by newposition

            # loading the visual stuff, these change in the game, so can't be loaded from fv.
            speedtxt = gfont.render("Speed: "  + str(speed)+ "x", False, fv.gcolor)
            timetxt  = gfont.render("Time:   " + str(int(tgame)), False, fv.gcolor)
            scoretxt = gfont.render("Score:  " + str(int(score)), False, fv.gcolor)

            # blitting
            screen.blit(fv.gamebg, fv.gamebgrect)
            # drawing the stored lines per plane in planes array
            for i in range(len(planes[:, 0])):
                for j in range(len(planes[i, 7]) - 1):
                    pg.draw.line(screen, fv.linecolor, planes[i, 7][j], planes[i, 7][j + 1], 2)
            # text objects
            screen.blit(speedtxt, (5, 5 ))
            screen.blit(timetxt,  (5, 30))
            screen.blit(scoretxt, (5, 55))
            #blitting the angled and resized planes
            for i in range(len(planes)):
                if planes[i,0]==1:
                    p1r = pg.transform.rotozoom(fv.p1, planes[i, 6],planes[i,8])
                    planes[i,1] = p1r.get_rect()     #stores the new surface in the planes table
                    planes[i,1].center = planes[i,2] #sets the center of the new surface
                    screen.blit(p1r, planes[i, 1])
                if planes[i,0]==2:
                    p2r = pg.transform.rotozoom(fv.p2, planes[i, 6],planes[i,8])
                    planes[i,1] = p2r.get_rect()     #stores the new surface in the planes table
                    planes[i,1].center = planes[i,2] #sets the center of the new surface
                    screen.blit(p2r, planes[i, 1])
                if planes[i,0]==3:
                    p3r = pg.transform.rotozoom(fv.p3, planes[i, 6],planes[i,8])
                    planes[i,1] = p3r.get_rect()     #stores the new surface in the planes table
                    planes[i,1].center = planes[i,2] #sets the center of the new surface
                    screen.blit(p3r, planes[i, 1])
            # blitting the clouds
            for i in range(len(clouds)):
                cloudr = pg.transform.rotate(fv.cloud,clouds[i,3])
                clouds[i,0] = cloudr.get_rect()
                clouds[i,0].center = clouds[i,1]
                screen.blit(cloudr,clouds[i,0])
            pg.display.flip()

            #check for events
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        menuloop = True
                        gameloop = False
                    if event.key == pg.K_LEFT and speed > 1:
                        speed -= (speed // 2)
                    if event.key == pg.K_RIGHT and speed < 4:
                        speed += speed
                if event.type == pg.MOUSEBUTTONDOWN:
                    hold = True
                    c1   = pg.mouse.get_pos() #first press
                if event.type == pg.MOUSEBUTTONUP:
                    hold     = False
                    drawpath = False
                if event.type == pg.QUIT:
                    run      = False
                    menuloop = False
                    gameloop = False

#======= The scoreloop (or deadloop)
    if scoreloop:
        total = 0
        step  = score/(150)
        typedname = " "
        appendname = False
        score = int(score) #rounding off the score

    while scoreloop:
        if total<int(score):
            total+=step #adding up the score

        # blitting
        scoretxt    = lfont.render(str(int(total)), False, fv.dcolor)
        inputtxt    = lfont.render(typedname, False, fv.dcolor)
        screen.blit(fv.deadbg, fv.deadbgrect)
        if score>int(scores[9][1]):
            screen.blit(fv.nametxt , fv.namepos)
            screen.blit(inputtxt, fv.SURFCENT( inputtxt, (640,450)))
        else:
            screen.blit(fv.nohscoretxt , fv.nohscorepos)
        screen.blit(scoretxt, fv.SURFCENT(scoretxt, (640,200)))
        screen.blit(fv.entertxt, fv.enterpos)
        pg.display.flip()

        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN and len(typedname)>0:
                    menuloop = True
                    scoreloop = False
                    appendname = True
                if event.unicode.isalpha():
                    typedname += event.unicode
                if event.key == pg.K_SPACE:
                    typedname += " "
                if event.key == pg.K_BACKSPACE:
                    typedname = typedname[:-1]

        if appendname and score>int(scores[9][1]):
            for i in range(len(scores[:,1])):
                if score>int(scores[i,1]):
                    scores = np.insert(scores,i,[typedname,int(score)],0)
                    appendname = False
                    break
pg.quit()
del lfont, gfont

# write newly generated table back to file
scorefile = open("highscores.dat","w")
for i in range(len(scores)):
    line = str(scores[i,0]) + ";" + str(scores[i,1]) + "\n"
    scorefile.write(line)
scorefile.close()

""" Closing remarks
pg.get_ticks():
    the resolution of pg.get_ticks() for simple games/loops is not
    accurate enough. for instance: the pendulum assignment (for me) really inaccurate.
    Because it ran at +-800Hz, the dt was 0.00125. whilst the resolution of pg.get_ticks()
    stops at 0.001 or 0.002. which is why I used the time library for that assignment.
    But due to lack of support for mac(?) I stuck with pg.get_ticks() for compatibility reasons.
    So for faster laptops and desktops it's advisible to use an alternate for pg.get_ticks()
    (I rock an i7-8750H)

Use of stackoverflow:
    Basicly the only real thing I "borrowed" from stackoverflow was:
    "if event.unicode.isalpha():
                    typedname += event.unicode"
    Which is a really neat and clean way of getting user input in pygame.
    My first solution was having an if statement for every individual keypress..
    which made the code about 25*2 lines too long. (it worked though!)

Images used ingame:
    the images of Palau were pulled from google images, as were the planes.
    The images for the controls and backstory were made with photoshop.
    The satellite view of the game was also made with photoshop, you can still
    see some of the gridlines from apple maps.
"""