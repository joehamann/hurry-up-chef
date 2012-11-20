import os, pygame

class Image(object):
    @staticmethod
    def load_image(filename):
        return pygame.image.load(os.path.join('image', filename)).convert_alpha()
    
    @staticmethod
    def load_sliced_sprites(w, h, filename):
        '''
        Specs :
            Master can be any height.
            Sprites frames width must be the same width
            Master width must be len(frames)*frame.width
        Assuming you resources directory is named "image"
        '''
        images = []
        master_image = Image.load_image(filename)
        for i in xrange(int(master_image.get_width()/w)):
            images.append(master_image.subsurface((i*w,0,w,h)))
        return images