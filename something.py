# A class to hold information about real things with dimentions
class Something:
    def __init__(self, name, measure, units):
        self.name=name
        self.measure=measure
        self.units=units

    # How many of these things fit in here?
    def fitIn(measure):
        return int( measure/self.measure )

# A class for turning incomprehensible lengths into comprehensible ones
class lengthComprehender:
    def __init__(self):
        self.things = []

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
                if line=='': # If it blank, we're done
                    break

                # Cut off that pesky newline character
                if line[-1] == '\n':
                    line=line[:-1]
                    if line=='':# If that's all that was there, we're done
                        break

                # Make the thing
                name, measureStr = line.split(',')
                measure=float(measureStr)
                self.things.append( Something(name, measure, 'm') )

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


if __name__ == '__main__':
    # Boring testing stuff... move along

    # Setup comprehender
    lenComp=lengthComprehender()
    lenComp.load('data/lengths-m')

    # Let the user know what's up
    print('Input a length in meters to have it turned into something real!')

    # Run forever!!!
    while True:
        # Get input
        try:
            x = int(input('>'))
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
