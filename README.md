# Password Strength Checker

Python-based Password Strength Checker (PSC) offering CLI and GUI to analyze password strength with an estimated brute-force cracking time. Includes actionable feedback with common password and pattern checks.

# Table of Contents
Features: #features
Installation: 
Usage: 

## Features:

Evaluates password strength using the zxcvbn library.
Estimates the time it would take to crack the password.
Provides custom warnings and suggestions for improving password strength.
Checks for common passwords, password length, and diversity.

## Installation:

Install the required libraries:
Lorem Ipsum

## Usage:

### CLI:

- Run PSC.py from your terminal (zsh example): python3 PSC.py
- When asked whether you want GUI or CLI, press "Enter"
- Enter a password to check its strength. 

Example(zsh): 
![alt text](image-2.png)

### GUI:

- Run the script and press "1", then "Enter" at the prompt to launch the GUI.
- Enter a password in the entry field and click "Check Strength."
- The results will be displayed in the text box below.

Example(macOS): 
![alt text](image.png)

Example(Windows): 
![alt text](image-1.png)

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Additional Notes:
This script uses the zxcvbn library to estimate password strength and assign it a score. For more information on the zxcvbn library, see its documentation: https://zxcvbn-ts.github.io/zxcvbn/guide/getting-started/.

The script also loads a list of common passwords from a file.  The list of common passwords can be updated as wanted by modifying "load_common_passwords()". 