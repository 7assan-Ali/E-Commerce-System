class Address:
    def __init__(
        self,
        addressId: int,
        street: str,
        city: str,
        governorate: str,
        postalCode: str
    ):
        self.addressId = addressId
        self.street = street
        self.city = city
        self.governorate = governorate
        self.postalCode = postalCode

    def displayAddress(self) -> None:
        print("\nAddress Information")
        print("-------------------")
        print(f"Address ID: {self.addressId}")
        print(f"Street: {self.street}")
        print(f"City: {self.city}")
        print(f"Governorate: {self.governorate}")
        print(f"Postal Code: {self.postalCode}")

    def updateAddress(
        self,
        street: str,
        city: str,
        governorate: str,
        postalCode: str
    ) -> None:
        self.street = street
        self.city = city
        self.governorate = governorate
        self.postalCode = postalCode

        print("Address updated successfully.")
        
        
        
