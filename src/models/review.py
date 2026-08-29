class Review:
    def __init__(self, customer_id: int, product_id: int, rating: float, comment: str = ""):
        self.customer_id = customer_id
        self.product_id = product_id
        self.rating = rating
        self.comment = comment
