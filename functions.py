import sys, os
import pygame
from pygame.locals import *
from pygame.compat import geterror
import constants as const


#-----------------------------------------------------------------------------------------------
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
    
    aa=True

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
                    print ">>> The word {} is too long to fit in the rect passed.".format(word)
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

    #surface = pygame.Surface(rect.size, pygame.SRCALPHA)

    surface = pygame.Surface(rect.size).convert()
    surface.set_alpha(0)
    surface.fill(background_color)
    if transparent:
        surface.set_colorkey(background_color)
     
    accumulated_height = 0 
    for line in final_lines: 
        if accumulated_height + font.size(line)[1] >= rect.height:
            #raise TextRectException, "Once word-wrapped, the text string was too tall to fit in the rect."
            print "*** Once word-wrapped, the text string was too tall to fit in the rect."
        if line != "":
            tempsurface = font.render(line, aa, text_color)
            #tempsurface.set_alpha(0)
            if justification == 0:
                surface.blit(tempsurface, (0, accumulated_height))
            elif justification == 1:
                surface.blit(tempsurface, ((rect.width - tempsurface.get_width()) / 2, accumulated_height))
            elif justification == 2:
                surface.blit(tempsurface, (rect.width - tempsurface.get_width(), accumulated_height))
            else:
                print "Invalid justification argument: {}".format(justification)
        accumulated_height += font.size(line)[1]

    return surface

#-----------------------------------------------------------------------------------------------
def get_line(start, end, step=1):
    """Bresenham's Line Algorithm
    Produces a list of tuples from start and end
 
    >>> points1 = get_line((0, 0), (3, 4))
    >>> points2 = get_line((3, 4), (0, 0))
    >>> assert(set(points1) == set(points2))
    >>> print points1
    [(0, 0), (1, 1), (1, 2), (2, 3), (3, 4)]
    >>> print points2
    [(3, 4), (2, 3), (1, 2), (1, 1), (0, 0)]
    """
    # Setup initial conditions
    q=0
    x1, y1 = start
    x2, y2 = end
    dx = x2 - x1
    dy = y2 - y1
 
    # Determine how steep the line is
    is_steep = abs(dy) > abs(dx)
 
    # Rotate line
    if is_steep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2
 
    # Swap start and end points if necessary and store swap state
    swapped = False
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
        swapped = True
 
    # Recalculate differentials
    dx = x2 - x1
    dy = y2 - y1
 
    # Calculate error
    error = int(dx / 2.0)
    ystep = 1 if y1 < y2 else -1
 
    # Iterate over bounding box generating points between start and end
    y = y1
    points = []
    for x in range(x1, x2 + 1):
        coord = (y, x) if is_steep else (x, y)
        q+=1
        if q==step:
            points.append(coord)
            q=0
        error -= abs(dy)
        if error < 0:
            y += ystep
            error += dx
 
    # Reverse the list if the coordinates were swapped
    if swapped:
        points.reverse()
    return points

#-----------------------------------------------------------------------------------------------
def load_image(name, colorkey=None):
    #fullname = os.path.join(const.data_dir, name)
    try:
        image = pygame.image.load(name)
        image.convert_alpha()
    except pygame.error:
        print 'Cannot load image: {}'.format(name)
        image=pygame.Surface((29,29)).convert()
        image.fill((192,192,192,255))

    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
            print 'getting colorkeyfrom image'
        image.set_colorkey(colorkey, RLEACCEL)
    return image