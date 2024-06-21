# AASCII Requester By Will Horst

Hello! This project consumes from the two ASCII Servers (Letters and Numbers Server) as defined in the homework. It's 
built using Python 3.12. It will send a curl request to the numbers server, sum up the input from it into number x, and then use the total sum to 
request x amount of strings from the letter server. It will then count the occurrences of every alphabetic character that exists in the received strings
and give the output as defined in the provided `readme.md` file, which will look like:
```
Strings: 37
Character Counts:
15 14 21 12 20 17 14 19 16 26 26 18 14 21 15 14 16 17 12 19 13 15 16 24 19 20
a  b  c  d  e  f  g  h  i  j  k  l  m  n  o  p  q  r  s  t  u  v  w  x  y  z
```


# Project Description

At a high level, this program (which is called ascii-requester) will request input from the letters and numbers server (as defined 
previously by DataDog) via some curl requests and transform it to match the output defined by DataDog. It's built and 
run in a Docker container running Python. One can check the included `docker-compose.yaml` file to see some of the important 
information for the ascii-requester to run. More details on that later! After starting the program, it will print the necessary
output to the command line every 5 seconds if the ISO week is odd, and 10 if the ISO week is even.

 It includes a full suite of unit tests (99% coverage according to my PyCharm coverage checker), and was built to be as
 robust and fail-safe as possible, even if that means exiting the program gracefully.                                 

## Table of Contents
1. [Project Structure](#project-structure)
2. [Installation](#installation)
2. [Usage](#usage)
5. [Testing](#testing)
6. [Notes](#notes)
7. [Authors](#authors)


## Project Structure

At the root level of the project, there are a few important files
* `docker-compose.yaml` - This defines the different services that will be running on three separate docker containers,
as well as some of the different information needed to run those services. The service that this program pertains to is under 
`ascii-requester`. A `depends_on` tag was added as for the ascii-requester to work, the numbers-server and letters-server
have to be running. Furthermore, I added four environment variables:
  * `LETTERS_ADDRESS`: Specifies the address of the letters server container.
  * `LETTERS_PORT`: Specifies the port on which the letters server is running.
  * `NUMBERS_ADDRESS`: Specifies the address of the numbers server container.
  * `NUMBERS_PORT`: Specifies the port on which the numbers server is running.
                                            
   
  These were added so they didn't have to be hard-coded in the Python code itself, instead they'll be retrieved as 
  environment variables. This makes those four values a little more configurable for the future. The environment variables are 
  all used to build  and curl the addresses of the relevant servers.
                   
* `asciirequester/` - This contains the main files required to run the ascii-requester. Namely, `main.py` is where the control flow of the program begins,
and is run with the Dockerfile that was created for this project.
  * `Dockerfile` - This is the docker file that helps define and run the ascii-requester. It runs the `main.py` script.

  
  * `server_utils/` - This directory is mainly responsible for handling communication the ascii-requester's communication with 
the numbers and letters servers, as well as logging potential errors. Server operations include:  
    1. Sanitizing/verifying that the container names and port numbers are valid 
    2. Building the server urls based off of the container names and port numbers
    3. Sending a curl request to both of these servers
    4. And returning the responses
            

 * `parsers/` - This is where the logic for receiving, calculating, storing, and logging the two server responses go. 
  There are three files within this directory
   * `number_parser.py` - The number parser will receive the response from the number server and sum the numbers 
   it receives, to create a total. This total will be used to grab x amount of strings from the letters server, where 
   x is the value returned from the letter parser.
   * `letter_parser.py` - The letter parser is responsible for taking in the letters from the letter server and 
   combining them to match the output defined in the requirements.
   * `parser_manager.py` - The parser manager will take in the data needed to run the number and letter parser, and 
   then execute the flow to build and log the output

 * `server/` - This is a wrapper class responsible for making server calls given a valid server address and port
   * `server.py` - Uses the container class to return responses from the given addresses
                     

 * `scheduler.py` - This class is responsible for running the code described above ever 5 or 10 seconds, depending on 
whether or not the ISO week number is odd or even.
      
* `tests/` - This is where the project's unit tests exist. They include happy and sad path tests and are mainly 
behavioral driven, with some implementation driven in test_parser_manager.py

## Installation
This code is made to be run within a container using docker-compose. If you want the installation instructions for those:

* On Linux, use `apt` to install `docker` and follow the [Github instructions](https://github.com/docker/compose#linux) to install `docker-compose`.
* On macOS, [install `colima`](https://github.com/abiosoft/colima) for docker compatibility and use [homebrew](https://brew.sh/) to install `docker-compose`.
* On Windows, use WSL2 and install the programs similarly on Linux.

If you'd like to run any of the code written for this project locally, you'll need to install Python 3.12. Assuming you already have Homebrew on your system, run 
 
```brew install python@3.12```

and make sure that it's executable from your shell/terminal by running 

`python --version`

As long as you can see successful output from that, you are good.

## Usage

Now that you have Homebrew, docker, docker-compose, and Python (for local testing) installed, how do you run this? Make 
sure your terminal is navigated to the directory `demo-engineering-interview-homework` (top level) and run the following 
two commands

```
docker-compose build
docker-compose up
```

And from there you should see output that looks like: 

```
ascii-requester  | Strings: 18
ascii-requester  | Character Counts:
ascii-requester  | 6 5 11 10 7 8 8 6 4 7 11 8 14 3 9 12 2 6 9 5 16 8 8 4 6 5
ascii-requester  | a b c  d  e f g h i j k  l m  n o p  q r s t u  v w x y z
```

If you'd like to run the code in `main.py` (that is, the ascii-requester)
locally (without the ascii-requester being containerized), one can set the four environment variables necessary for the ascii-requester 
to run (locally). You can figure out how to do that on your system by reading [This article](https://chlee.co/how-to-setup-environment-variables-for-windows-mac-and-linux/).
The default values for the four individual environment variables would be
```
NUMBERS_ADDRESS=localhost
LETTERS_ADDRESS=localhost
NUMBERS_PORT=8082
LETTERS_PORT=8081  
```

Next, open up a new terminal instance and make sure the ascii-requester service is commented out from the docker-compose file, 
then run the following two commands in the ner terminal instances: 
```
docker-compose build
docker-compose up
```
then, in the terminal instance where the environment variables were set, run the two following commands

```
cd asciirequester
python main.py
```

## Testing
                                           
There are currently 44 unit tests available in this project. To run them, navigate to the tests folder and run the tests command like so:

```
cd tests
python run_tests.py
```
If the tests pass, one should see the following output
```
Ran 44 tests in 0.004s
```

## Troubleshooting
Errors are most likely to happen when either the numbers or letters servers are down, or when something wasn't configured 
in the environment variables properly. To fix this, try running the two commands under the `Usage` section or check the 
environment variables in the docker-compose.yaml that were defined under ascii-requester and make sure that they line 
up with the information related to the numbers and letters servers

                           
## Notes                                                                                                                                                
I wasn't extremely sure on what the best formatting would be fore chars that include double, triple, or quadruple digit                                 
counts, so I simply lined up the beginning of the char values and number values to line up from teh first character in each,                            
demonstrated below with a b   

```
ascii-requester  | Strings: 18                                                          
ascii-requester  | Character Counts:                                                    
ascii-requester  | 6 5000 11 10 7 8 8 6 4 7 11 8 14 3 9 12 2 6 9 5 16 8 8 4 6 5            
ascii-requester  | a b    c  d  e f g h i j k  l m  n o p  q r s t u  v w x y z            
```                                                                                     

## Authors
https://www.linkedin.com/in/wjhorst/

                                                                                                                                          
