import re
import reprlib

RE_WORD = re.compile('\w+')


class Sentence:
    
    def __init__(self, text):
        self.text = text # No need to have a words list
        
    def __repr__(self):
        return 'Sentence(%s)' % reprlib.repr(self.text)
    
    def __iter__(self):
        for match in RE_WORD.finditer(self.text): # finditer builds an iterator over the matches
                                                  # of RE_WORD on self.text
                                                  # yielding MatchObject instances
            yield match.group() # match.group() extracts the actual matched text from the MatchObject
                                # instance.
