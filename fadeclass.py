import sys, os
import pygame
from pygame.locals import *
import constants as const
import functions as function
import time

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
        self.speed=250             #millisec, how often does it update?
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
        rendered_text = function.render_textrect(text, font, pygame.Rect(size), color, const.clr_background, justification, True)
        asset=GrfxAsset(rendered_text, self.next_id, position)
        if visible:
            asset.alpha=255
        else:
            asset.alpha=0
        self.asset_list.append(asset)
        self.next_id += 1
        return asset.id        

    def load_image(self,filename, position, visible=True,colorkey=None):
        img=function.load_image(filename, colorkey)
        asset=GrfxAsset(img, self.next_id, position)
        if visible:
            asset.alpha=255
        else:
            asset.alpha=0
        self.asset_list.append(asset)
        self.next_id += 1
        return asset.id 

    def update(self, tics):
        for asset in self.asset_list:
            if not asset.delay_on:
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
                    if len(asset.points)>0:         #see if there is a list of points
                        asset.rect=asset.points.pop()   #pop a new location off the list
            elif tics>asset.delay_on:
                asset.delay_on=0
                asset.next_update = tics + asset.speed

    def draw(self):
        for asset in self.asset_list:
            asset.image.set_alpha(asset.alpha)
            self.screen.blit(asset.image, asset.rect)

    def fade_in(self, idnum, fadespeed=50, fadechange=16):
        found=False
        for asset in self.asset_list:
            if asset.id==idnum:
                asset.alpha=0
                asset.fadedelta=fadechange
                asset.speed=fadespeed
                print 'fading in {}'.format(idnum)
                found=True
        if not found: print 'fade_in: {} not found'.format(idnum)

    def fade_out(self, idnum, fadespeed=50, fadechange=16):
        found=False
        for asset in self.asset_list:
            if asset.id==idnum:
                asset.fadedelta=-fadechange
                asset.speed=fadespeed
                print 'fading in {}'.format(idnum)
                found=True
        if not found: print 'fade_out: {} not found'.format(idnum)

    def remove(self, idnum):
        pass

    def turn_on(self, idnum):
        for asset in self.asset_list:
            if asset.id==idnum:
                asset.alpha=255

    def turn_off(self, idnum):
        for asset in self.asset_list:
            if asset.id==idnum:
                asset.alpha=0

    def move_to(self, idnum, offset, speed=50, step=1):
        for asset in self.asset_list:
            if asset.id==idnum:
                asset.speed=speed
                location=(asset.rect[X]+offset[X], asset.rect[Y]+offset[Y])
                asset.points=function.get_line(location, asset.rect, step)
                #print '{}: {} to {}, {} points'.format(idnum, location, asset.rect, len(asset.points))

    def list_assets(self):
        for asset in self.asset_list:
            print '{}: loc {}, a:{}'.format(asset.id, asset.rect, asset.alpha)

    def set_delay(self, idnum, delay=1000):
        for asset in self.asset_list:
            if asset.id==idnum:
                asset.delay_on=pygame.time.get_ticks() + delay


#-----------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------
def main():
    pygame.init()
    screen = pygame.display.set_mode(const.SCRN_SIZE)  # add pygame.FULLSCREEN for full screen
    font=pygame.font.Font('assets/ITC-NewBaskervilleITCPro-Roman.otf', 36)
    #bkgrnd=pygame.image.load('assets/paper017.jpg')

    elements={}
    grfxs=GrfxControl(screen)
    elements['background']=grfxs.load_image(os.path.join(const.asset_dir,'paper017.jpg'),(0,0),const.clr_BLACK)
    
    txt='This is a test!'
    elements['t1']=grfxs.add_text(txt, (35,50), (0,0,150,150), font, (96,0,0))
    grfxs.set_delay(elements['t1'],2000)
    grfxs.fade_in(elements['t1'])
    grfxs.move_to(elements['t1'], (-10,-25))
    txt='Brother Jacob returned from a long journey feeling very sick. The doctor suspects that he has a case of scurvy.'
    t2=grfxs.add_text(txt, (25,250), (0,0,500,350), font, (0,0,96),1)
    t3=grfxs.load_image(os.path.join(const.asset_dir,'face.png'),(400,50), -1)

    clock = pygame.time.Clock()
    running=True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                running = False
            elif event.type == KEYDOWN and event.key == K_SPACE:
                grfxs.fade_out(t2)
                grfxs.move_to(t2,(0,35),2)
            elif event.type == KEYDOWN and event.key == K_DELETE:
                print 'delete'
                grfxs.move_to(t3, (-10,25))
                grfxs.fade_out(t3)

        #screen.blit(bkgrnd, (0,0))
        grfxs.update(pygame.time.get_ticks())
        grfxs.draw()
        pygame.display.flip()

    grfxs.list_assets()
    pygame.quit()
#-----------------------------------------------------------------------------------------------
if __name__ == '__main__':
    main()
