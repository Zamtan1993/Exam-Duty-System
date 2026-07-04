#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 21:33:02 2026

@author: mdtanimbinana
"""

import pandas as pd


# ==========================
# Read Excel File
# ==========================

def read_roster(filename):
    """Reads the Excel file and converts it into a nested dictionary."""

    df = pd.read_excel(filename)

    roster = {}

    for _, row in df.iterrows():

        teacher = str(row["Teacher"]).strip()
        schedule = {}

        for date in df.columns[1:]:
            schedule[date] = str(row[date]).strip()

        roster[teacher] = schedule

    return roster


# ==========================
# Display Teacher Schedule
# ==========================

def get_teacher_schedule(roster, teacher_name):

    teacher_name = teacher_name.strip()

    if teacher_name not in roster:
        print("\nTeacher not found.")
        return

    print(f"\n========== SCHEDULE OF {teacher_name} ==========\n")

    for date, duty in roster[teacher_name].items():
        print(f"{date:<15} {duty}")


# ==========================
# Show All Teachers
# ==========================

def show_all_teachers(roster):

    print("\n========== TEACHER LIST ==========\n")

    for teacher in roster:
        print(teacher)


# ==========================
# Search by Duty Type
# ==========================

def search_by_duty(roster, duty_name):

    duty_name = duty_name.strip().lower()

    found = False

    print(f"\n========== {duty_name.upper()} ==========\n")

    for teacher, schedule in roster.items():

        for date, duty in schedule.items():

            if duty.lower() == duty_name:

                print(f"{teacher:<35} {date}")
                found = True

    if not found:
        print("No records found.")


# ==========================
# Find Possible Swaps
# ==========================

def find_possible_swaps(roster, my_name):

    my_name = my_name.strip()

    if my_name not in roster:
        return []

    swaps = []

    my_schedule = roster[my_name]

    for date, my_duty in my_schedule.items():

        if my_duty.lower() == "reserve":

            for teacher, schedule in roster.items():

                if teacher == my_name:
                    continue

                duty = schedule[date]

                if duty.startswith("R-"):

                    swaps.append({
                        "Date": date,
                        "My Name": my_name,
                        "My Duty": "Reserve",
                        "Swap With": teacher,
                        "Their Duty": duty
                    })

    return swaps


# ==========================
# Display Swaps
# ==========================

def display_swaps(swaps):

    if not swaps:
        print("\nNo possible swaps found.")
        return

    print("\n========== POSSIBLE SWAPS ==========\n")

    for swap in swaps:

        print(f"Date       : {swap['Date']}")
        print(f"Swap With  : {swap['Swap With']}")
        print(f"Their Duty : {swap['Their Duty']}")
        print("-" * 40)


# ==========================
# Export Swaps
# ==========================

def export_swaps(swaps):

    if not swaps:
        print("Nothing to export.")
        return

    df = pd.DataFrame(swaps)

    output_file = "/Users/mdtanimbinana/Desktop/Possible_Duty_Swaps.xlsx"

    df.to_excel(output_file, index=False)

    print("\nExcel file created successfully!")
    print(f"Saved to: {output_file}")


# ==========================
# Main Program
# ==========================

def main():

    filename = "/Users/mdtanimbinana/Downloads/Exam_Duty_Roster_Example_Data.xlsx"

    try:

        roster = read_roster(filename)

    except FileNotFoundError:

        print("Excel file not found.")
        return

    while True:

        print("\n========== EXAM DUTY SYSTEM ==========")
        print("1. Show All Teachers")
        print("2. Show Teacher Schedule")
        print("3. Find Possible Swaps")
        print("4. Duty Search")
        print("5. Exit")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":

            show_all_teachers(roster)

        elif choice == "2":

            teacher = input("Enter teacher name: ").strip()

            get_teacher_schedule(roster, teacher)

        elif choice == "3":

            teacher = input("Enter teacher name: ").strip()

            swaps = find_possible_swaps(roster, teacher)

            display_swaps(swaps)

            export = input("\nExport to Excel? (y/n): ").strip().lower()

            if export == "y":
                export_swaps(swaps)

        elif choice == "4":

            print("\n========== DUTY SEARCH ==========")
            print("1. Reserve")
            print("2. On Duty")
            print("3. Quirat Duty")

            duty_choice = input("\nEnter your choice: ").strip()

            if duty_choice == "1":

                search_by_duty(roster, "Reserve")

            elif duty_choice == "2":

                search_by_duty(roster, "On Duty")

            elif duty_choice == "3":

                search_by_duty(roster, "Quirat Duty")

            else:

                print("Invalid choice.")

        elif choice == "5":

            print("\nThank you for using the Exam Duty System.")
            break

        else:

            print("\nInvalid choice. Please try again.")


# ==========================
# Start Program
# ==========================

if __name__ == "__main__":
    main()
