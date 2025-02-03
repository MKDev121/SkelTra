import pygame as pg
import character
import shared 
import math
# pg setup
pg.init()
screen = pg.display.set_mode((1280, 720))
clock = pg.time.Clock()
running = True
pg.display.set_caption("SkelTra")
char=character.Character()
while running:
    mouse_pos=pg.mouse.get_pos()
    # poll for events
    # pg.QUIT event means the user clicked X to close your window
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type==pg.KEYDOWN:
           if event.key ==pg.K_a:
            char.Body.intial_pos=position=pg.mouse.get_pos()
            name="holder_"+str(len(char.Body.holders))
            shared.current_holder_state=shared.holder_states[0]
            

            keydown=True
        if event.type==pg.MOUSEBUTTONDOWN:
           shared.mouse_down=True
    
    # fill the screen with a color to wipe away anything from last frame
    screen.fill("grey")

    # IO
    if(shared.current_holder_state==shared.holder_states[0]):
       
       scale=mouse_pos-pg.Vector2(char.Body.intial_pos)
       pg.draw.rect(screen,"black",(char.Body.intial_pos,scale))
       pg.draw.rect(screen,"grey",(char.Body.intial_pos+pg.Vector2(10,10),scale-pg.Vector2(20,20)))
       if(shared.mouse_down):
          char.Body.add_holder(name,pos=position,scale=scale)
          shared.current_holder_state=shared.holder_states[1]
          shared.mouse_state="buffer"
    if(shared.mouse_state=="buffer"):
       shared.mouse_down=False
       shared.mouse_state=""
    # RENDER YOUR GAME HERE
    char.load(screen)
    # flip() the display to put your work on screen
    pg.display.flip()
 
    clock.tick(60)  # limits FPS to 60

pg.quit()