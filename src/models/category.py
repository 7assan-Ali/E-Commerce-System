

class Category:
    def __init__(
        self,
        categoryId: int,
        name: str,
        description: str
    ):
        self.categoryId=categoryId
        self.name=name
        self.description=description
        self.products=[]
        
        
    def addProduct(self,product)->None:
        if product not in self.products:
            self.products.append(product)
            print(f"Product '{product.name}' added to category '{self.name}'.")
        else:
            print("Product already exists in this category.")
            
            
    def removeProduct(self,product)->None:
        if product in self.products:
            self.products.remove(product)
            print(f"Product '{product.name}' removed from category '{self.name}'.")
        else:
            print("Product not found in this category.")
            
            
            
