from datetime import datetime


class DateRange:
    def __init__(self, start_date: str, end_date: str):
        self.start = datetime.strptime(start_date, '%Y-%m-%d')
        self.end = datetime.strptime(end_date, '%Y-%m-%d')

    def is_valid(self) -> bool:
        return self.start <= self.end
