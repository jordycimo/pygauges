import pygame, os, math

# (version text)
vtext = "PyGauges V0"

# pygame setup
pygame.init()
screen = pygame.display.set_mode((320,480))
clock = pygame.time.Clock()
running = True
font = pygame.font.Font(os.path.join('src','Heavitas.ttf'), 12)

# class representing dashboard gauge
class gauge:
    def __init__(self,glyph,min,max,length):
        self.glyph = glyph # the glyph on the gauge, ie: temperature, oil, or battery.
        self.value = 0
        self.min = min
        self.max = max
        self.length = length

# create two gauges. they will occupy 240 pixels of the total vertical space each

gauge1 = gauge(pygame.image.load(os.path.join('src','temp.gif')),
               15,  # in my program, i want the value to directly reflect the angle of the needle.
               165, # i like the look of 15deg - 165deg. at least, to represent the temperature.
               40)  # 40 is nice for this resolution/arrangement

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # clear screen
    screen.fill("black")

    # --render--
    # version text because it looks cool as fuck
    for c in vtext:
        text_surface = font.render(c, False, (100,100,100))
        screen.blit(text_surface, (0,vtext.index(c)*15))

    # gauge 1

    #needle
    gauge1.value *= math.pi/180 #  convert to radians
    endpos = (180-math.cos(gauge1.value)*40),140-(math.sin(gauge1.value)*40) # (too long to explain, its trig)
    pygame.draw.line(screen,(255,0,0),(180,140),endpos,4) # draw it

    #center
    pygame.draw.circle(screen,(100,100,100),(180,140),10)

    # update
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
