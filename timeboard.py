class Timeboard(object):
    # initialize timeboard with current game ticks
        def __init__(self):
                self.seconds = 0
                
        def update(self):
                if (self.seconds < 360000): #max: 99:59:59
                        self.seconds += 1
                
        
                
        def print_time(self):
                hours = self.seconds / 3600
                minutes = (self.seconds % 3600) / 60
                seconds = self.seconds % 60
                print "%02d" % hours + ':' + "%02d" % minutes + ':' + "%02d" % seconds