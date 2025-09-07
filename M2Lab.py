# Name: Harold Ligon
# File: M2Lab.py
# Description: Gets student names and GPAs and determines whether each student qualifies for the Dean's List (GPA >= 3.5)
# or the Honor Roll (GPA >= 3.25). Application stops when last name 'ZZZ' is entered.
import unicodedata as u

def checkStudentStatus():
  # Greeting
    print("Welcome to Module 2 Lab!\nBy Harold Ligon")
    # Get student info in a loop until 'ZZZ' is entered for last name
    while True:
        lastName = input("Enter student's last name (or 'ZZZ' to quit): ").strip()
        if lastName.upper() == 'ZZZ':
            print("\nHave a nice day. Goodbye!")
            break

        firstName = input("Enter student's first name: ").strip()

        # Read GPA as float; if invalid notify and continue to next record
        try:
            gpaInput = input("Enter student's GPA: ").strip()
            gpa = float(gpaInput)
        except ValueError:
            print("Invalid GPA. Please enter a numeric value.\n")
            continue

        print(f"\nResult for {firstName} {lastName}:")
        if gpa >= 3.5:
            print("Congratulations! You've made the Dean's List." + u"\U0001F973" + u"\U0001F9D0")
        elif gpa >= 3.25:
            print("Great job! You've made the Honor Roll." + u"\U0001F973" + u"\U0001F913")
        else:
            print("Keep working hard. You're on your way." + u"\U0001F973" + u"\U0001F60E")
        print("-" * 40)


if __name__ == "__main__":
    checkStudentStatus()
