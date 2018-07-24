import pprint 
import inspect
import copy 
import operator


class Variable(object):

    default = -99

    def __init__(self, function=None, vtype=float, storageType="default", default=None):
        self.function = function
        self.vtype = vtype
        self.storageType = storageType
        self.default = default if default else self.__class__.default 
    
    def __call__(self, *args, **kwargs):
        return self.function(*args,**kwargs)

    def __repr__(self):
        return inspect.getsource(self.function).rstrip(',\n')

def to_leg(name, variables, leg, data_source):
    specific = dict()
    for vname, variable in variables.iteritems():
        specific['_'.join([leg,vname])] = variable
    return Block(name, data_source, **specific)

class Block(object):
    
    def __init__(self, name, data_source, **kwargs):
        self.name = name
        self.data_source = data_source
        self.vars = dict(**kwargs)

    def __getattr__(self, attr):
        return getattr(self.vars, attr)

    def __getitem__(self, item):
        return self.vars(item)

    def __setitem__(self,item, value):
        self.vars[item] = value

    def __repr__(self):
        header = 'Block {}'.format(self.name)
        return '\n'.join([header,
                          pprint.pformat(self.vars)])

class EventContent(list):

    def __init__(self, blocks):
        super(EventContent, self).__init__(blocks)

    def __str__(self):
        strblocks = []
        for block in sorted(self, key=operator.attrgetter('name')):
            strblocks.append(str(block))
        return '\n\n'.join(strblocks)

v = Variable
