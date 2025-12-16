import pygame, os, numpy

# (config)
config = {}
for l in open("config.cfg").read().removesuffix("\n").split(";"):
    k = l.split("=")
    print(l)
    config[k[0].removesuffix(" ").removeprefix("\n")] = k[1]

vtext = str(config["VERSION"])

# pygame setup
pygame.init()
screen = pygame.display.set_mode((int(config["RESX"]),int(config["RESY"])))
clock = pygame.time.Clock()
running = True
font = pygame.font.Font(os.path.join('src','F25_Bank_Printer_Bold.ttf'), 12)

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

gauge2 = gauge(pygame.image.load(os.path.join('src','volt.gif')),
               1,  # 12 is typical voltage
               23, # same deal
               80) # same length

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # debug stuff -- simulates data for the gauges to display
    if config["DEBUG"]:
        gauge1.value = numpy.abs(numpy.sin(pygame.time.get_ticks()/1000)*165)
        gauge2.value = 12+(numpy.sin(pygame.time.get_ticks()/1000)*10)

    # clear screen
    screen.fill("black")

    # --render--
    # version text because it looks cool as fuck
    for c in vtext:
        text_surface = font.render(c, True, (100,100,100))
        screen.blit(text_surface, (2, vtext.index(c)*10))

    # gauge 1
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
    # end gauge 1



    # gauge 2
    #needle
    gauge2.value = numpy.clip(gauge2.value, gauge2.min, gauge2.max) # apply min and max
    gauge2.value *= numpy.pi/180 # convert to radians
    endpos = (-(numpy.cos(gauge2.value*7.5)*gauge2.length)+180,-(numpy.sin(gauge2.value*7.5)*gauge2.length)+340) # to angle
    pygame.draw.line(screen, (255,0,0), (180,340), endpos, 5) # draw it

    #center
    pygame.draw.circle(screen,(100,100,100),(180,340),10)

    #glyph + marks
    screen.blit(gauge2.glyph,(180,350))
    pygame.draw.circle(screen,(100,100,100),(100,330),5)
    pygame.draw.circle(screen,(100,100,100),(255,330),5)


    # update
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
