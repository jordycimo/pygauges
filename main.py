import pygame, os, numpy

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
    def __init__(self, glyph, min, max, length):
        self.glyph = glyph # the glyph on the gauge, ie: temperature, oil, or battery.
        self.value = 0
        self.min = min
        self.max = max
        self.length = length

# create two gauges. they will occupy 240 pixels of the total vertical space each

gauge1 = gauge(pygame.image.load(os.path.join('src','temp.gif')),
               15,  # in my program, i want the value to directly reflect the angle of the needle.
               165, # i like the look of 15deg - 165deg. at least, to represent the temperature.
               80)  # 80 is nice for this resolution/arrangement

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
        screen.blit(text_surface, (0, vtext.index(c)*15))

    # gauge 1
    gauge1.value = numpy.abs(numpy.sin(pygame.time.get_ticks()/1000)*180)
    print(gauge1.value)

    #needle
    gauge1.value = numpy.clip(gauge1.value, gauge1.min, gauge1.max) # apply min and max
    gauge1.value *= numpy.pi/180 # convert to radians
    endpos = (-(numpy.cos(gauge1.value)*gauge1.length)+180,-(numpy.sin(gauge1.value)*gauge1.length)+140) # to angle
    pygame.draw.line(screen, (255,0,0), (180,140), endpos, 5) # draw it

    #center
    pygame.draw.circle(screen,(100,100,100),(180,140),10)

    #glyph + marks
    screen.blit(gauge1.glyph,(180,150))
    pygame.draw.circle(screen,(0,0,255),(105,120),5) # cold
    pygame.draw.circle(screen,(255,0,0),(255,120),5) # hot

    # update
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
