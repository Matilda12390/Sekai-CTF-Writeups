from sympy import *
import socket
import time

# Creates and connects to the socket that is hosting the challenge
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("34.148.151.228", 9000))
# Receive the data from the socket and then convert it to a string
data = s.recv(1024)
stringSocket = data.decode('utf-8') 
# Print out the data received from the socket so you can see what is happening
print(stringSocket)
# Skip to position 331 in the string since that was the fixed length at the beginning without an equation
stringIndex = 162

# Set an arbitrary high number to loop through
for i in range(100):
    # Initate a boolean for the while loop and a string to store the equation before the equal sign
    randomVal = true
    stringEquation = ''
    while randomVal:
        # Takes the character at the stringIndex and sees if it is an equals sign or a new line, if it isn't adds it to the string
        tempChar = stringSocket[stringIndex]
        stringIndex = stringIndex + 1
        if tempChar == '=':
            randomVal = false
        elif tempChar == '\n':
            randomVal = false
        else: 
            stringEquation = stringEquation + tempChar
    
    # Use sympy to parse the strings before and after the equal signs into equations that sympy can use
    print("hi" + stringEquation)
    eq1 = eval(stringEquation)
    print(eq1)
    # Convert the int to the string for easier printing and encoding
    numString = str(eq1) + "\n"
    # Sends the correct answer encoded back to the server
    s.send(str.encode(numString))
    # Prints the value sent to the server so you can see what is happening
    print(numString)
    # Grab the new data and convert it into a string
    newData = s.recv(1024)
    stringSocket = newData.decode('utf-8') 
    # Print the string so you know what is going on
    print(stringSocket)
    # Sets the stringIndex back to one as the new data is only the new equation
    stringIndex = 8
