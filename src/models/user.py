class User:
    def __init__(
        self,
        userID: int,
        name: str,
        email: str,
        password: str,
        phone: str
    ):
        self.userID = userID
        self.name = name
        self.email = email
        self.password = password
        self.phone = phone
        self.is_logged_in = False

    def login(self) -> bool:
        self.is_logged_in = True
        return True

    def logout(self) -> None:
        self.is_logged_in = False

    def updateProfile(self) -> None:
        print("\nCurrent Profile Data:")
        print(f"Name: {self.name}")
        print(f"Email: {self.email}")
        print(f"Phone Number: {self.phone}")

        print("\nWhat do you want to update?")
        print("1. Name")
        print("2. Email")
        print("3. Phone")
        print("4. All")
        print("5. Cancel")

        choice = input("Enter your choice: ")

        if choice == "1":
            self.name = input("Enter new name: ")
            print("Name updated successfully.")

        elif choice == "2":
            self.email = input("Enter new email: ")
            print("Email updated successfully.")

        elif choice == "3":
            self.phone = input("Enter new phone: ")
            print("Phone updated successfully.")

        elif choice == "4":
            self.name = input("Enter new name: ")
            self.email = input("Enter new email: ")
            self.phone = input("Enter new phone: ")
            print("Profile updated successfully.")

        elif choice == "5":
            print("Update cancelled.")

        else:
            print("Invalid choice.")