from digit import *
class Timeboard(object):
    # initialize timeboard with TOP LEFT (x,y) coordinates
        def __init__(self, x, y):
                self.seconds = 0
                self.x = x
                self.y = y
                self.hour0 = Digit(x,y,0)
                self.hour1 = Digit(x + DIGIT_WIDTH, y,0)
                self.minute0 = Digit(x + 2 * DIGIT_WIDTH + COLON_WIDTH,y ,0)
                self.minute1 = Digit(x + 3 * DIGIT_WIDTH + COLON_WIDTH,y,0)
                self.second0 = Digit(x + 4 * DIGIT_WIDTH + 2 * COLON_WIDTH,y,0)
                self.second1 = Digit(x + 5 * DIGIT_WIDTH + 2 * COLON_WIDTH,y,0)
                self.digit_group = pygame.sprite.RenderPlain()
                self.digit_group.add(self.hour0)
                self.digit_group.add(self.hour1)
                self.digit_group.add(self.minute0)
                self.digit_group.add(self.minute1)
                self.digit_group.add(self.second0)
                self.digit_group.add(self.second1)
                                   
                
                
        def update(self):
                if (self.seconds < 360000): #max: 99:59:59
                        self.seconds += 1
                        self.hour0.set_digit((self.seconds / 3600) / 10)
                        self.hour1.set_digit((self.seconds / 3600) % 10)
                        self.minute0.set_digit(((self.seconds % 3600) / 60) / 10)
                        self.minute1.set_digit(((self.seconds % 3600) / 60) % 10)                
                        self.second0.set_digit((self.seconds % 60) / 10)
                        self.second1.set_digit((self.seconds % 60) % 10)                
                                
                
        
                
        def print_time(self):
                hours = self.seconds / 3600
                minutes = (self.seconds % 3600) / 60
                seconds = self.seconds % 60
                print "%02d" % hours + ':' + "%02d" % minutes + ':' + "%02d" % seconds