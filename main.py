import sys


def main():
    print("Welcome to the Library System")
    print("1. Run CLI")
    print("2. Run GUI (not implemented)")
    choice = input("Choose interface: ")
    if choice == "1":
        from cli import menu

        menu()
    else:
        print("GUI not implemented. Exiting.")


if __name__ == "__main__":
    main()
