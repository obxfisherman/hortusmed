import sys, os
import pygame
from pygame.locals import *
from pygame.compat import geterror

size = width, height = 600, 600

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, 'data')
X=0
Y=1


#-----------------------------------------------------------------------------------------------
#functions to create our resources
def load_image(name, colorkey=None):
    fullname = os.path.join(data_dir, name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error:
        print ('Cannot load image:', fullname)
        raise SystemExit(str(geterror()))
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()

#-----------------------------------------------------------------------------------------------
class TextRectException:
    def __init__(self, message = None):
        self.message = message
    def __str__(self):
        return self.message

def render_textrect(string, font, rect, text_color, background_color, justification=0, transparent=True):
    """Returns a surface containing the passed text string, reformatted
    to fit within the given rect, word-wrapping as necessary. The text
    will be anti-aliased.

    Takes the following arguments:

    string - the text you wish to render. \n begins a new line.
    font - a Font object
    rect - a rectstyle giving the size of the surface requested.
    text_color - a three-byte tuple of the rgb value of the
                 text color. ex (0, 0, 0) = BLACK
    background_color - a three-byte tuple of the rgb value of the surface.
    justification - 0 (default) left-justified
                    1 horizontally centered
                    2 right-justified

    Returns the following values:

    Success - a surface object with the text rendered onto it.
    Failure - raises a TextRectException if the text won't fit onto the surface.
    """

    #import pygame
    
    aa=False

    final_lines = []

    requested_lines = string.splitlines()

    # Create a series of lines that will fit on the provided
    # rectangle.

    for requested_line in requested_lines:
        if font.size(requested_line)[0] > rect.width:
            words = requested_line.split(' ')
            # if any of our words are too long to fit, return.
            for word in words:
                if font.size(word)[0] >= rect.width:
                    raise TextRectException, "The word " + word + " is too long to fit in the rect passed."
            # Start a new line
            accumulated_line = ""
            for word in words:
                test_line = accumulated_line + word + " "
                # Build the line while the words fit.    
                if font.size(test_line)[0] < rect.width:
                    accumulated_line = test_line 
                else: 
                    final_lines.append(accumulated_line) 
                    accumulated_line = word + " " 
            final_lines.append(accumulated_line)
        else: 
            final_lines.append(requested_line) 

    # Let's try to write the text out on the surface.

    surface = pygame.Surface(rect.size).convert()
    surface.fill(background_color)
    if transparent:
        surface.set_colorkey(background_color)
     

    accumulated_height = 0 
    for line in final_lines: 
        if accumulated_height + font.size(line)[1] >= rect.height:
            raise TextRectException, "Once word-wrapped, the text string was too tall to fit in the rect."
        if line != "":
            tempsurface = font.render(line, aa, text_color)
            if justification == 0:
                surface.blit(tempsurface, (0, accumulated_height))
            elif justification == 1:
                surface.blit(tempsurface, ((rect.width - tempsurface.get_width()) / 2, accumulated_height))
            elif justification == 2:
                surface.blit(tempsurface, (rect.width - tempsurface.get_width(), accumulated_height))
            else:
                raise TextRectException, "Invalid justification argument: " + str(justification)
        accumulated_height += font.size(line)[1]

    return surface

def setfade(asset_list, id, delta, offset, dir=0):
    for asset in asset_list:
        if asset.id==id:
            print 'found'
            asset.fadedelta=delta
            asset.offset=offset
            asset.fade=dir

#-----------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------
class GrfxAsset(pygame.sprite.Sprite):
    def __init__(self, image, id):
        pygame.sprite.Sprite.__init__(self) #call Sprite initializer
        self.image = image          #need to make a copy of the image?
        self.rect = self.image.get_rect()
        self.id=id
        self.offset=(0,0)
        self.final_pos=(0,0)
        self.fadedelta=0
        self.alpha=0
        self.fade=0         #0=fade in  1=fade out 3=hold
        
    def update(self):       
        if self.offset[X]<0: self.offset=(self.offset[X] + Fade_dir[self.fade][1], self.offset[Y])
        if self.offset[X]>0: self.offset=(self.offset[X] + Fade_dir[self.fade][1], self.offset[Y])
        if self.offset[Y]<0: self.offset=(self.offset[X], self.offset[Y] + Fade_dir[self.fade][0])
        if self.offset[Y]>0: self.offset=(self.offset[X], self.offset[Y] - Fade_dir[self.fade][1])
        #print 'offset: {}'.format(self.offset)
        self.alpha += self.fadedelta
        if self.alpha<0:
            self.alpha=0
            self.fadedelta=0
        if self.alpha>255:
            self.alpha=255
            self.fadedelta=0
        self.rect=(self.final_pos[X] + self.offset[X], self.final_pos[Y] + self.offset[Y])
        self.image.set_alpha(self.alpha)
        #print '{}:{}'.format(self.id,self.alpha)


#-----------------------------------------------------------------------------------------------
def main():
    pygame.init()
    screen = pygame.display.set_mode(size)

    bkgrnd=pygame.image.load('paper017.jpg')

    screen.blit(bkgrnd, (0,0))
    pygame.display.flip()

    font=pygame.font.Font('newbaskerville.ttf', 36)

    asset_list = pygame.sprite.Group()

    my_rect=pygame.Rect((0,0,550,300))
    my_string='Brother Jacob returned from a long journey feeling very sick. The doctor suspects that he has a case of scurvy. Pick one of these plants to help Brother Jacob recover.'
    rendered_text = render_textrect(my_string, font, my_rect, (48,0,0), (0, 0, 0), 0, True)
    #if rendered_text:
    #    screen.blit(rendered_text, (25,25))

    asset=GrfxAsset(rendered_text)
    asset.final_pos=(25,25)
    asset.offset=(-25,-25)
    asset.fadedelta=16
    asset_list.add(asset, 0)

    my_rect=pygame.Rect((0,0,200,100))
    my_string='bla bla bla\nfoo foo foo'
    rendered_text = render_textrect(my_string, font, my_rect, (0,0,128), (0, 0, 0), 0, True)

    asset=GrfxAsset(rendered_text)
    asset.final_pos=(125,450)
    asset.offset=(100,-25)
    asset.fadedelta=2
    asset_list.add(asset, 1)

    running=True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                running = False
            elif event.type == KEYDOWN and event.key == K_SPACE:
                setfade(asset_list, 0,-8, (0,10), 1)

        screen.blit(bkgrnd, (0,0))
        asset_list.update()
        asset_list.draw(screen)
        clock.tick(20)              #10 frames per sec
        pygame.display.flip()

    pygame.quit()

#-----------------------------------------------------------------------------------------------
if __name__ == '__main__':
    main()