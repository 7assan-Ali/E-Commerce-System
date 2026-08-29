class CartItem:
    def __init__(self,quantity:int, unitPrice:float):
        self.quantity=quantity
        self.unitPrice=unitPrice
        
    def calculateSubtotal(self):
        return self.quantity * self.unitPrice
    
    def updateQuantity(self,quantity:int):
        if quantity<=0:
            print("Quantity must be greater than 0.")
            return
        
        self.quantity=quantity
        print("Quantity updated successfully.")