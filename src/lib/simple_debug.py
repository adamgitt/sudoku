import optparse
import defaults

parser = optparse.OptionParser(
    version=defaults.VERSION,
    option_list=[
    optparse.make_option("-v",const=True,action="store_const",
                         dest="debug",help="Print debug information",
                         default=False),
    #optparse.make_option("-w",const=True,action="store_const",
    #                     dest="walk",help="Step through program",
    #                     default=False),
    ]
    )

options,args = parser.parse_args()

    
# Make a lovely wrapper 
if options.debug:
    def simple_debug (f):
        def _ (self, *args,**kwargs):
            print self.__class__,f.__name__,args,kwargs
            return f(self,*args,**kwargs)
        return _

else:
    def simple_debug (f): return f
