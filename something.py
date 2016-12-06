# A class to hold information about real things with dimentions
class Something:
    def __init__(self, name, measure, units):
        self.name=name
        self.measure=measure
        self.units=units

    # How many of these things fit in here?
    def fitIn(measure):
        return int( measure/self.measure )

class Unit:
    def __init__(self, name, SIFactor):
        self.name = name
        self.SIFactor = SIFactor

# A class for turning incomprehensible numbers into comprehensible ones
class Comprehender:
    def __init__(self, units, SIUnitName):
        # Things we know the measure of
        self.things = []

        # Put unit objects into dictionary for easier reference
        self.units={}
        for unit in units:
            self.units[unit.name] = unit

        # The name of the standard SI unit for the dimention we specialize in
        self.SIUnitName = SIUnitName

    def __sort__(self):
        self.things.sort(key=lambda x:x.measure)

    def load(self, filename):
        # Clear old things
        self.things=[]

        # Open the file
        with open(filename, 'r') as f:
            # Start reading lines
            while True:
                # Get a nicely formatted line
                line=f.readline()
                if line=='' or line=='\n': # If it blank, we're done
                    break

                # Try to make the thing
                splitLine = line.split(',')
                unitName = splitLine[2].strip().lower()
                measure = float(splitLine[1])
                name = splitLine[0].strip()

                # If it has units we don't recognize, skip it
                unitName = splitLine[2].strip().lower()
                if unitName not in self.units:
                    continue

                # Do unit conversion
                unit = self.units[unitName]
                SIMeasure = measure * unit.SIFactor

                self.things.append( Something(name, SIMeasure, self.SIUnitName) )

    def isKnownUnit(self, unitName):
        return unitName in self.units

    def comprehend(self, measure):
        """
        Output is in the form of a list a tuples. For each tuple,
        the first element is the number and the second element is
        the thing
        """
        # Start by sorting our list of things
        self.__sort__()

        # Now the meat
        remainder = measure
        output=[]
        while True:
            # Find the largest thing measuring smaller than remainder
            thingToUse=None
            for thing in self.things:
                if thing.measure < remainder:
                    thingToUse= thing
                else:
                    break
            # If nothing was found, we're done
            if thingToUse == None:
                break
            # Otherwise, add it to the list and update remainder
            else:
                number = int(remainder/thingToUse.measure)
                remainder %= thingToUse.measure
                output.append( (number, thingToUse) )

        return output

# Comprehender specialized in lengths
class LengthComprehender( Comprehender ):
    def __init__(self):
        units = [ Unit('m',  1),
                  Unit('mi', 1609.34),
                  Unit('ly', 9.461*10**15) ]

        super(LengthComprehender, self).__init__(units, 'm')


if __name__ == '__main__':
    # Boring testing stuff... move along

    # Setup comprehender
    lenComp=LengthComprehender()
    lenComp.load('data/lengths')

    # Let the user know what's up
    print('Input a length in meters to have it turned into something real!')

    # Run forever!!!
    while True:
        # Get input
        inputStr = input('>').strip().lower()

        # Check for known commands
        if inputStr == 'exit':
            break

        # Try to make a numeric value
        try:
            x = float( inputStr )
        except Exception:
            print('Invalid input.')
            continue

        # Compute result and display
        result=lenComp.comprehend(x)
        print('That is...')
        for number, thing in result:
            if number==1:
                print('1 '+thing.name)
            else:
                # Yes, we're very fancy
                plural='s'
                if thing.name[-1] == 's':
                    plural='ses'
                    if thing.name[-2] == 's':
                        plural='es'
                print( '{} {}{}'.format(number, thing.name, plural) )
