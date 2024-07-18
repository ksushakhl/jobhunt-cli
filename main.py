import argparse
import os
import csv
from tempfile import NamedTemporaryFile
import shutil


def create_parser():
    parser = argparse.ArgumentParser(description="Command-line Job Applications Tracker")
    parser.add_argument("-a", "--add", metavar="", help="Add a new application")
    parser.add_argument("-l", "--list", action="store_true", help="List all applications")
    parser.add_argument("-u", "--update", nargs='+', metavar="", help="Update an application by name")
    return parser


def add_application(application):
    with open("jobs.csv", "a") as file:
        file.write(application + "," + "applied" + "," + "\n")


def list_applications():
    if os.path.exists("jobs.csv"):
        with open("jobs.csv", "r") as file:
            tasks = file.readlines()
        for index, task in enumerate(tasks, start=1):
            print(f"{index}. {task.strip()}")
    else:
        print("No applications found.")


def update_application(name, status):
    tempfile = NamedTemporaryFile(mode="w", delete=False)
    fields = ["Company", "Status"]
    if os.path.exists("applications.csv"):
        with open("applications.csv", "r", newline='') as file, tempfile:
            reader = csv.DictReader(file)
            writer = csv.DictWriter(tempfile, fieldnames=fields)
        for row in reader:
            if row["Company"] == str(name):
                print("updating row", row["Company"])
                row["Status"] = status
            row = {"Company": row["Company"], "Status": row["Status"]}
            writer.writerow(row)

        shutil.move(tempfile.name, "jobs.csv")
    else:
        print("No applications found.")


def main():
    parser = create_parser()
    args = parser.parse_args()

    if args.add:
        add_application(args.add)
    elif args.list:
        list_applications()
    elif args.update:
        update_application(str(args.company), str(args.status))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
