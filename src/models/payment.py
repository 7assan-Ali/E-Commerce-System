class Payment:
    def __init__(
        self,
        paymentId: int,
        amount: float,
        paymentDate: str,
        status: str = "Pending",
        method: str = "Cash"
    ):

        self.paymentId=paymentId
        self.amount=amount
        self.paymentDate=paymentDate
        self.status=status
        self.method=method
        
        
    def processPayment(self):
        if self.status=="Paid":
            print("Payment has already been processed.")
            return
        self.status="Paid"
        print("Payment processed successfully.")
    
    def refund(self):
        if self.status != "Paid":
           print("Payment cannot be refunded.")
           return 
        
        self.status="Refunded"
        print("Payment refunded successfully")
        
        
    def checkStatus(self):
        return self.status
    
    
payment = Payment(
    1,
    25000.50,
    "2026-08-30",
    method="Credit Card"
)

print(payment.checkStatus())

payment.processPayment()

print(payment.checkStatus())

payment.refund()

print(payment.checkStatus())
        
        