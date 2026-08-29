class OrderItem:
    def __init__(self,quantity : int,unitPrice : float,subtotal : float=0.0):
        
        self.quantity=quantity
        self.unitPrice=unitPrice
        self.subtotal=subtotal
        
    def calculateSubtotal(self):
        self.subtotal= self.quantity* self.unitPrice
        
        return self.subtotal
    
    
item = OrderItem(3, 500)

print(item.calculateSubtotal())