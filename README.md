Usage
=====
To start the web server, simply run the *start_server.sh* script from the
root project directory. The web API can then be accessed using a get request
of the from,

    localhost:5000/api&input="<input>"

where *<input>* is something a user might put in the main text box. Some
example inputs and outputs might be

    INPUT:
    localhost:5000/api&input="100m"

    OUTPUT:
    [
       [1, "Football Field"],
       [9, "Credit Card"],
       [10, "Toothpick"]
    ]

or,

    INPUT:
    localhost:5000/api&input="200 mi"

    OUTPUT:
    [
       [388, "Burj Khalifa"],
       [1, "Empire State Building"],
       [1, "Football Field"],
       [6, "Bus"],
       [3, "Credit Card"],
       [10, "Toothpick"]
    ]
