from datetime import date
from dataclasses import dataclass

@dataclass
class ServicePriceRow:
    pk: int
    service: int
    price: int
    start_date: date
    deleted: bool
    version: int
