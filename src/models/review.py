class Review:
    def __init__(
        self,
        reviewId: int,
        rating: int,
        comment: str,
        reviewDate: str
    ):
        self.reviewId = reviewId
        self.rating = rating
        self.comment = comment
        self.reviewDate = reviewDate

    def addReview(self) -> None:
        print("Review added successfully.")

    def updateReview(self, rating: int, comment: str) -> None:
        if rating < 1 or rating > 5:
            print("Rating must be between 1 and 5.")
            return

        self.rating = rating
        self.comment = comment
        print("Review updated successfully.")

    def deleteReview(self) -> None:
        print("Review deleted successfully.")
