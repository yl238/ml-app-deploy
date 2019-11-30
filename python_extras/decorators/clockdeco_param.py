import time

DEFAULT_FMT = '[{elapsed:0.8f}s] {name}({args}) -> {result}'

def clock(fmt=DEFAULT_FMT): # decorator factory
    def decorate(func): # decoractor
        def clocked(*_args): # clocked wraps the decorated function
            t0 = time.time()
            _result = func(*_args) # _result is the actual result of the decorated function
            elapsed = time.time() - t0
            name = func.__name__
            args = ', '.join(repr(arg) for arg in _args) # _args holds the actual argument of clocked, 
                                                         # args is used for display
            result = repr(_result) # result is the `str` representation of `_result` for display.
            print(fmt.format(**locals())) # using **locals() allows any local variables of clocked
                                          # to be referenced in the fmt.
            return _result # clocked replaces the decorated function, so returns whatever the function
                           # returns
        return clocked   # decorate returns clocked.
    return decorate # clock returns decorate

if __name__ == '__main__':
    @clock()
    def snooze(seconds):
        time.sleep(seconds)

    for i in range(3):
        snooze(.123)
