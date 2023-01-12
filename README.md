# Timeblock

A timeblocking application to manage tasks like a to-do list and schedule them like a calendar. Improve your productivity by scheduling blocks of time for tasks and tracking the amount of time it takes to complete them.

## Usage

Please note that Timeblock is currently a work-in-progress. However, if you would like to try it out and provide feedback, you can install and use it as follows:

1. Clone the repository: `git clone https://github.com/daustin391/timeblock.git`
2. Create and activate a virtual environment:
   - `python3 -m venv .venv`
   - `source .venv/bin/activate`
3. Install the dependencies: `pip install -r requirements.txt`
4. Run the application: `python -m timeblock`

## Prerequisites

Timeblock requires the following dependencies:

- Flask: a web framework for Python, used to build the web interface
- typing_extensions: a library for extending the type hinting functionality in Python, used to improve the code quality

Additionaly, runnng tests requires:

- pytest: a testing framework for Python
- selenium: for automating a web browser
- requests: a library for making HTTP requests

To install these dependencies, you will need to have Python 3 and pip installed on your system. If you do not already have these, you can install them by following the instructions at the following URL: https://packaging.python.org/tutorials/installing-packages/

Once you have Python 3 and pip installed, you can install the other dependencies by running `pip install -r requirements.txt`.

## Contributing

Timeblock is an open source project with an MIT license. We welcome contributions from the community! If you would like to contribute, please follow these guidelines:

- Fork the repository
- Create a new branch for your changes
- Make your changes and test them thoroughly
- Submit a pull request

## Tests

We use pytest to test Timeblock. To run the tests, use the following command: `pytest`
The tests cover approximately 99% of the code in Timeblock.

## Additional Resources

For more information, refer to the source repository on GitHub: https://github.com/daustin391/timeblock
