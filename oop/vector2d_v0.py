from array import array
import math

class Vector2d:
    typecode = 'd' # class attribute used to converted `Vector2d` instances to/from bytes
    
    def __init__(self, x, y):
        self.x = float(x) # catches error early incase Vector2d called with unsuitable arguments.
        self.y = float(y)
        
    def __iter__(self): # makes Vector2d iterable - this is what makes unpacking work
        return (i for i in (self.x, self.y))
     
    def __repr__(self): # interpolating the components with {!r} to get their repr
        class_name = type(self).__name__ # because Vector2d is iterable
        return '{}({!r},{!r})'.format(class_name, *self) # *self feeds the x and y component to format
    
    def __str__(self):
        return str(tuple(self))
    
    def __bytes__(self):
        return (bytes([ord(self.typecode)]) + # convert typecode to bytes and concatenates
               bytes(array(self.typecode, self)))
    
    def __eq__(self, other):
        return tuple(self) == tuple(other)
    
    def __abs__(self):
        return math.hypot(self.x, self.y)
    
    def __bool__(self):
        return bool(abs(self))
