class MeasureNotFoundError(Exception):
    def __init__(self, measure_id: int):
        self.measure_id = measure_id
        super().__init__(f"Measure with ID {measure_id} not found")


class CustomerNotFoundError(Exception):
    def __init__(self, customer_id: int):
        self.customer_id = customer_id
        super().__init__(f"Customer with ID {customer_id} not found")


class UserNotFoundError(Exception):
    def __init__(self, user_id: int):
        self.customer_id = user_id
        super().__init__(f"User with ID {user_id} not found")
