class MenuItem:
    def __init__(self, name: str, price: float, description: str):
        self.name = name
        self.price = price
        self.description = description

    def __str__(self):
        return f"{self.name} (${self.price:.2f}): {self.description}"
