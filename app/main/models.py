import textwrap


class Room(object):
    '''A Room has a name and may contain stuff.
    '''
    def __init__(self, name, stuff=None):
        # stuff: A list of tuples: (item, price)
        self.name = name
        self.stuff = stuff
        self.padding = max([len(item) for (item, price) in stuff])

    def add_item(self, item, price=None):
        self.stuff.append((item, price))

    def __repr__(self):
        return f'<Room {self.name} stuff count: {len(self.stuff)}>'

    def __str__(self):
        '''
        EXAMPLE
        Living Room
            bookshelf        50                
            fridge           8                 
            thingamabob      4567452           
            TV               500               
            whatchamacallit  9
        '''
        PADDING = self.padding + 3
        strings = [self.name]
        for (item, price) in self.stuff:
            item = textwrap.indent(item, 2 * ' ').ljust(PADDING)

            price = str(price).ljust(PADDING)
            strings.append("{1: >{0}} {2: >{0}}".format(PADDING, item, price))
        return '\n'.join(strings)