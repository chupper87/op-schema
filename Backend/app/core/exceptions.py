class MeasureNotFoundError(Exception):
    def __init__(self, measure_id: int):
        self.measure_id = measure_id
        super().__init__(f"Measure with ID {measure_id} not found")
