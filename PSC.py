import tkinter as tk
from tkinter import ttk
from zxcvbn import zxcvbn
import re 

def interpret_score(score): #Interprets the password strength score.
    if score == 0:
        return "within a few minutes"
    elif score == 1:
        return "within a hour"
    elif score == 2:
        return "within a few hours"
    elif score == 3:
        return "within days"
    else:
        return "within centuries (very strong password)"
    
common_passwords = set()

def load_common_passwords(): #Loads SecLists 10k-most-common.txt from the working directory.  Source -> https://github.com/danielmiessler/SecLists/blob/master/Passwords/Common-Credentials/10k-most-common.txt
    global common_passwords
    with open('10k-most-common.txt', 'r') as f:
        common_passwords = set(f.read().splitlines())

def validate_password(password): #Validates the password and returns a boolean and message.
    if not password:
        return False, "Please enter a password before pressing Enter."
    return True, ""

def get_custom_feedback(password): #Adds custom warnings and suggestions based on password provided.
    warnings = []
    suggestions = []
    if password in common_passwords: #Check if the password is in 10k-most-common.txt
        warnings.append("This password is too common and easily guessable.")
        suggestions.append("Choose a more unique password.")
        
    seasons_pattern = r"(Spring|Summer|Fall|Autumn|Winter)"
    
    if re.search(seasons_pattern, password, re.IGNORECASE): #Check if the passwords contains a season
        warnings.append("Avoid using seasons in your password.")
        suggestions.append("Avoid easily guessable patterns like seasons.")
    
    years_pattern = r"(19|20)\d{2}"

    if re.search(years_pattern, password): #Check if the password contains a year
        warnings.append("Avoid using years in your password.")
        suggestions.append("Years, especially recent ones or birth years, are easily guessable.")    

    if len(password) < 15: #Checks password length
        warnings.append("Your password is shorter than 15 characters.")
        suggestions.append("Consider using a longer password for better security.  The easiest way to make your passwords more resistant to cracking is increasing the length.")
        
    if password.isdigit() or password.isalpha(): #Checks for password diversity 
        warnings.append("Your password lacks diversity.")
        suggestions.append("Mix different types of characters (letters, numbers, symbols).")
        
    return warnings, suggestions


def estimated_crack_time_cli(password): #CLI version to estimate password crack time.
    is_valid, message = validate_password(password)
    if not is_valid:
        print("\033[91m{}\033[0m".format(message))  # Error handling
        return
    results = zxcvbn(password)
    score = results['score']
    custom_warnings, custom_suggestions = get_custom_feedback(password)
    print(f"Password: {password}\n")
    print(f"Estimated time to crack: {interpret_score(score)}\n")
    if custom_warnings:
        print("Warnings:")
        for warning in custom_warnings:
            print(f"- {warning}")
        print()
    if custom_suggestions:
        print("Suggestions:")
        for suggestion in custom_suggestions:
            print(f"- {suggestion}")
        print()

def prompt_for_password_cli(): #CLI input validation/error handling.
    while True:
        password = input("Enter a password to check: ")
        is_valid, message = validate_password(password)
        if is_valid:
            return password
        else:
            print("\033[91m{}\033[0m".format(message))

def launch_gui():
    def estimated_crack_time_gui(event=None): #GUI version to estimate password crack time.
        password = password_entry.get()
        is_valid, message = validate_password(password)
        if not is_valid:
            result_label.config(state="normal")
            result_label.delete(1.0, tk.END)
            result_label.insert(tk.END, message + "\n", 'error')  #Display error in GUI for no password provided.
            result_label.config(state="disabled")
            return
        else: 
            results = zxcvbn(password)
            score = results['score']
            custom_warnings, custom_suggestions = get_custom_feedback(password)
            feedback_text = f"Password: {password}\n\nEstimated time to crack: {interpret_score(score)}\n\n"
        if custom_warnings:
            feedback_text += "Warnings:\n" + "\n".join(f"- {w}" for w in custom_warnings) + "\n\n"
        if custom_suggestions:
            feedback_text += "Suggestions:\n" + "\n".join(f"- {s}" for s in custom_suggestions) + "\n"
        result_label.config(state="normal")
        result_label.delete(1.0, tk.END)
        result_label.insert(tk.END, feedback_text)
        result_label.config(state="disabled")
    
    #GUI Formatting/Content
    root = tk.Tk()
    root.resizable(width=False, height=False)
    root.title("Password Strength Checker")
    root.columnconfigure(0, weight=1)
    root.rowconfigure(1, weight=1)
    password_label = ttk.Label(root, text="Enter Password:")
    password_label.pack(pady=(10, 0), padx=20)
    password_entry = ttk.Entry(root, show="*")
    password_entry.pack(pady=10, padx=20)
    password_entry.bind("<Return>", estimated_crack_time_gui)
    check_button = ttk.Button(root, text="Check Strength", command=estimated_crack_time_gui)
    check_button.pack(pady=10, padx=20)
    result_label = tk.Text(root, height=20, width=100)
    result_label.pack(pady=10, padx=20)
    result_label.tag_config('error', foreground='red')
    result_label.config(state="disabled")
    root.mainloop()

if __name__ == "__main__":
    load_common_passwords()
    ascii_art = """
     ________   ________   ________        ________   ___    ___ 
    |\\   __  \\ |\\   ____\\ |\\   ____\\      |\\   __  \\ |\\  \\  /  /|
    \\ \\  \\|\\  \\\\ \\  \\___|_\\ \\  \\___|      \\ \\  \\|\\  \\\\ \\  \\/  / /
     \\ \\   ____\\\\ \\_____  \\\\ \\  \\          \\ \\   ____\\\\ \\    / / 
      \\ \\  \\___| \\|____|\\  \\\\ \\  \\____   ___\\ \\  \\___| \\/  /  /  
       \\ \\__\\      ____\\_\\  \\\\ \\_______\\|\\__\\\\ \\__\\  __/  / /    
        \\|__|     |\\_________\\\\|_______|\\|__| \\|__| |\\___/ /     
                  \\|_________|                      \\|___|/      
    """
    print(ascii_art)
    mode = input("Press 1, then Enter to launch the GUI - or press Enter to continue in CLI mode: ")
    if mode == "1":
        launch_gui()
    else:
        password = prompt_for_password_cli()
        estimated_crack_time_cli(password)