registry = set() # Adding and removing functions is faster

def register(active=True):
    def decorate(func): # This is the actual decorator - it takes a function as an argument
        print('Running register(active=%s) -> decorate(%s)'
             % (active, func))
        if active:
            registry.add(func)
        else:
            registry.discard(func)
            
        return func
    return decorate

# Now register must be invoked as a function with desired parameters
@register(active=False)
def f1():
    print('running f1()')
    
# Even if no parameters, still need to be a function
@register()
def f2():
    print('running f2()')
    
def f3():
    print('running f3()')
