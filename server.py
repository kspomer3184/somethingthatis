from something import *
from flask import Flask

# Setup Comprehender objects
lengthComp = LengthComprehender()
lengthComp.load('data/lengths')

# Make a QuaryParser using the comprehenders
quaryParser = QuaryParser( [lengthComp] )

app=Flask(__name__)

@app.route('/api&input="<inputString>"')
def api(inputString):
    return quaryParser.process( inputString )

if __name__ == '__main__':
    app.run()
