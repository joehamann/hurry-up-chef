from digit import *
class Scoreboard(object):
    # initialize timeboard with TOP RIGHT (x,y) coordinates
        def __init__(self, x, y, score):
                self.x = x
                self.y = y
                self.score = 0
                self.digits = []
                self.digits.append(Digit(x -  DIGIT_WIDTH, y,self.score))
                self.digit_group = pygame.sprite.RenderPlain()
                self.digit_group.add(self.digits[0])
                self.set_score(score)
                                   
                
                
        def set_score(self, score):
                self.score = score
                print "score = " + str(self.score)
                ones = score % 10
                self.digits[0].set_digit(ones)
                divisor = 10
                place = 1
                while(score >= divisor):
                        score = score / divisor
                        digit = score % 10
                        if (len(self.digits) <= place):
                                self.digits.append(Digit(self.x - DIGIT_WIDTH * (place + 1), self.y, digit))
                                self.digit_group.add(self.digits[place])
                        else:
                                self.digits[place].set_digit(digit)
                        place += 1
                while (place < len(self.digits) ):
                        self.digit_group.remove(self.digits.pop())
                        
        
                
        