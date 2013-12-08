


class Automaton(object):
    def __init__(self, pos=(0,0), **kwargs):
        self.pos = pos

        self._vel = kwargs.get('velocity', 0)       # 
        self._dir = kwargs.get('direction', 0)     # in radians
        
        # whether setting an attribute results in automatic .next() trigger.
        self.auto = kwargs.get('auto', False)
        
        
    @property
    def velocity(self):
        return self._vel
        
    @attr.setter
    def velocity(self, value):
        self._vel = value

    @property
    def direction(self):
        return self._dir
    
    @attr.setter
    def direction(self, value):
        self._dir = value
        
    def next(self):
        'using current object properties, move object to next position and return new pos.'
        
        
        

# # # # 
# Words
#
# 
#
    
    