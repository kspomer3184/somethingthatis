import re
import json

# A class to hold information about real things with dimentions
class Something:
    def __init__(self, name, measure, unit):
        self.name=name
        self.measure=measure
        self.unit=unit

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
        self.unitTable={}
        for unit in units:
            self.unitTable[unit.name] = unit

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
                if unitName not in self.unitTable:
                    continue

                # Do unit conversion
                unit = self.unitTable[unitName]
                SIMeasure = measure * unit.SIFactor

                self.things.append( Something(name, SIMeasure, self.SIUnitName) )

    def knowsUnit(self, unitName):
        return unitName in [unit.name for unit in self.unitTable.values()]

    def comprehend(self, measure, unitName=None):
        """
        Output is in the form of a list a tuples. For each tuple,
        the first element is the number and the second element is
        the thing
        """
        # Start by sorting our list of things
        self.__sort__()

        # Make sure the measure is in standard units
        if unitName:
            for unit in self.unitTable.values():
                if unit.name == unitName:
                    measure *= unit.SIFactor
                    break
            else:
                raise Exception('Unit not recognized: {}'.format(unitName))

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

# Comprehender specialized in masses/weights
class MassComprehender( Comprehender ):
    def __init__(self):
        units = [ Unit('kg',  1),
                  Unit('g', 1e-3),
                  Unit('mg', 1e-6),
                  Unit('ton', 907.185) ]

        super(LengthComprehender, self).__init__(units, 'm')

# A class to generate JSON responses to dirty user inputs. Will be primary
# back-end point of contact for web interface
class QuaryParser:
    def __init__(self, comprehenders=[]):
        self.comprehenders = comprehenders
        self.reProgram = re.compile(r'([\d\.]+)\s*([a-z]+)$')

    def process(self, quary):
        # Kill all padding whitespace and make sure everything is lowercase
        quary = quary.strip().lower()

        # If there are commas, ditch those
        quary = quary.replace(',', '')

        # Use regex to pull out the number and the unit
        result = self.reProgram.match(quary)
        numberStr, unitName = result.group(1,2)
        number = float(numberStr)

        # Find the comprehender that deals with these units
        result = None
        for comprehender in self.comprehenders:
            if comprehender.knowsUnit(unitName):
                result = comprehender.comprehend(measure=number, unitName=unitName)
                break


        # Get the result into a JSON friendly form
        response = []
        for number, thing in result:
            response.append( (number, thing.name) )

        # Convert to JSON and return
        return json.dumps( response )


def RunInteractive():
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

if __name__ == '__main__':
    # Boring testing stuff... move along
    lenComp=LengthComprehender()
    lenComp.load('data/lengths')
    parser = QuaryParser( [lenComp] )

    # Run forever!!!
    while True:
        # Get input
        inputStr = input('>').strip().lower()

        # Check for known commands
        if inputStr == 'exit':
            break

        response = parser.process(inputStr)
        print(response)
