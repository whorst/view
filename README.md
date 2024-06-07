# Demo Engineering interview homework

The homework here is representative of problems, technologies, and issues
you'll encounter on the Demo Engineering team.

Use this exercise as a way for you to show how you would write a working program while implementing software engineering best practices.

## Homework Guidance

### Time commitment

We've scoped this project to take about 4 hours to complete over a one week timeframe, but we can be flexible if you require more time. It's not a rush, however, completing it moves the interview process forward. We understand that everyone's work can pace differently and you're welcome to spend as much time on it as you are comfortable with. If you do spend extra time on it, please include your total time spent in the README.

### Grading

We'll be looking at the following criteria:
* Logical and maintainable project and code structure
* Sufficient documentation to allow another developer to successfully run the project
* Comments and unit tests
* A readable, reasonably concise, working program
* Insights into potential improvements to your solution if the coding effort is too large.

### Submission

Create a branch for your solution and submit it in the form of a Pull Request.

Any and all content of the Pull Request will also be evaluated as part of documentation / comments!

## Assignment

### Setup / Prerequisite

Please setup `docker` and `docker-compose` for your system.

Recommendations:
* On Linux, use `apt` to install `docker` and follow the [Github instructions](https://github.com/docker/compose#linux) to install `docker-compose`.
* On macOS, [install `colima`](https://github.com/abiosoft/colima) for docker compatibility and use [homebrew](https://brew.sh/) to install `docker-compose`.
* On Windows, use WSL2 and install the programs similarly on Linux.

While those are the recommendations, any method to get `docker-compose` working for you can be used.

### Part 1: Running existing services

While the `ascii-server` code base exists, it was written long ago without documentation.

The first task is to run two instances of the `ascii-server` using `docker-compose up` from the project root directory.

    $ pwd
    /demo-engineering-interview-homework
    $ docker-compose up

Notice that `letters-server` runs and can be reached at http://localhost:8081 .
The other instance, `numbers-server`, is running on port 8082, but notice that it is returning letters.

The first task is to update the `docker-compose.yaml` file to make `numbers-server` return numbers.

#### Constraints and clarifications

* Do not change the files inside the `ascii-server` directory.
* If you encounter too many `docker` related errors, feel free to skip this section find an alternative way to complete Part 2.

### Part 2: Creating a new service

Now that `numbers-server` returns the right data, write a containerized process that does the following:
1. Requests a number from the `numbers-server` instance.
2. Sum up the digits from the request and calls `letters-server` for that many strings.
   For example, if `21` is returned, get `2+1`=`3` strings from `letter-server`.
3. Count the number of occurrences of each character from all the strings and print them in the following format. For example, if the strings returned were "demo", "engineering", and "team":
   ```
   Strings: 3
   Character counts:
   1     1 5   2   2       2 3 1     1   1
   a b c d e f g h i j k l m n o p q r s t u v w x y z

   ```
   Notice that there is a new line after line with the alphabet, in order to separate from the next output.

4. This process should run indefinitely, with the following timings:
   * When the ISO week number of the year is odd, the process should run every 5 seconds.
   * When the ISO week number of the year is even, the process should run every 10 seconds.
   * For example, on August 2, 2023 UTC time, the week number is 31, so the process will run every 5 seconds.
5. This should all run from the project root directory with a single command,
   * The ideal solution will only require a `docker-compose up` command.
   * You can and are encouraged to provide scripts and instructions
     * To compile any code outside of the containerization process if necessary.
     * To run the setup if there are too many `docker` issues.

## Additional guidelines and clarifications

* Use a programming language (or multiple) of your choice, keeping in mind your audience.
  * On the Demo Engineering team, we write and maintain projects in Python, Ruby, Nodejs, Java, .Net, go-lang, bash (in no particular order).
  * There's some PHP, and other datadog teams use Rust, C, C++ as well.
* You are free to use any online tools or resources.
