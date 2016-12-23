import sys, os
import pygame
from pygame.locals import *
import constants as const
import functions as function
import time
 
if sys.platform == 'win32':
    # On Windows, the best timer is time.clock
    default_timer = time.clock
else:
    # On most other platforms the best timer is time.time
    default_timer = time.time

X=0
Y=1

#-----------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------
class GrfxAsset(object):
    def __init__(self, image, idnum, location):
        #pygame.sprite.Sprite.__init__(self) #call Sprite initializer
        self.image = image          #need to make a copy of the image?
        #self.rect = self.image.get_rect()
        self.id=idnum              #id number for tracking the asset
        self.visible=True          #can we see it?
        self.delay_on=0            #millisecs, used to automatically turn on visibility
        self.rect=location
        self.points=[]             #used to move the image around
        self.speed=25              #millisec, how often does it update?
        self.next_update=0         #once this value is exceeded by the system clock tics then an update occurs and this value is incremented by speed
        self.alpha=255
        self.fadedelta=0            #0 dont change alpha level
        
    def update(self):       
        pass

#-----------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------
class GrfxControl():
    def __init__(self, screen):
        self.asset_list = []
        self.next_id=0
        self.screen=screen

    def add_text(self, text, position, size, font, color, visible=True, justification=0):
        #adds a wrapping text image to the list of graphic objects
        # position = location on the screen
        # size = size of the text box
        # render_textrect(string, font, rect, text_color, background_color, justification=0, transparent=True):
        rendered_text = function.render_textrect(text, font, pygame.Rect(size), color, (0, 0, 0), justification, True)
        asset=GrfxAsset(rendered_text, self.next_id, position)
        if visible:
            asset.alpha=255
        else:
            asset.alpha=0
        self.asset_list.append(asset)
        self.next_id += 1
        return asset.id        

    def load_image(self):
        pass

    def update(self, tics):
        for asset in self.asset_list:
            if tics > asset.next_update:
                asset.next_update = tics + asset.speed
                #update asset stuff
                asset.alpha += asset.fadedelta
                if asset.alpha<0:
                    # maybe check to see if we should auto remove the object once fully faded out <<<<<<<<<<<<<<<<<<<<<<<<<
                    asset.alpha=0
                    asset.fadedelta=0
                if asset.alpha>255:
                    asset.alpha=255
                    asset.fadedelta=0

    def draw(self):
        for asset in self.asset_list:
            asset.image.set_alpha(asset.alpha)
            self.screen.blit(asset.image, asset.rect)

    def fade_in(self, idnum, fadechange=16):
        for asset in self.asset_list:
            if asset.id==idnum:
                asset.fadedelta=fadechange
                print 'fading in {}'.format(idnum)

    def fade_out(self, idnum, fadechange=16):
        for asset in self.asset_list:
            if asset.id==idnum:
                asset.fadedelta=-fadechange
                print 'fading in {}'.format(idnum)

    def remove(self, idnum):
        pass

    def turn_on(self, idnum):
        pass

    def turn_off(self, idnum):
        pass

    def move_to(self, idnum):
        pass

    def list_assets(self):
        for asset in self.asset_list:
            print '{}: loc {}, a:{}'.format(asset.id, asset.rect, asset.alpha)


#-----------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------
def main():
    pygame.init()
    screen = pygame.display.set_mode(const.SCRN_SIZE)
    font=pygame.font.Font('newbaskerville.ttf', 36)
    bkgrnd=pygame.image.load('paper017.jpg')
    grfxs=GrfxControl(screen)

    txt='This is a test!'
    t1=grfxs.add_text(txt, (25,25), (0,0,150,150), font, (96,0,0))
    txt='Brother Jacob returned from a long journey feeling very sick. The doctor suspects that he has a case of scurvy.'
    t2=grfxs.add_text(txt, (25,250), (0,0,500,350), font, (0,0,96),2)

    clock = pygame.time.Clock()
    running=True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                running = False
            elif event.type == KEYDOWN and event.key == K_SPACE:
                grfxs.fade_out(default_timer())
                #print '{}'.format(default_timer())

        screen.blit(bkgrnd, (0,0))
        grfxs.update(clock.get_rawtime())
        grfxs.draw()
        pygame.display.flip()

    grfxs.list_assets()
    pygame.quit()
#-----------------------------------------------------------------------------------------------
if __name__ == '__main__':
    main()
