from dataclasses import dataclass


@dataclass(repr=False)
class InventoryItem:
    name: str
    acquire_probability: float = 1
    description = ''

    'An object that can be acquired'
    
    def __init__(self, name, acquire_probability = 1, description = ''):
        self.name = name
        self.acquire_probability = acquire_probability
        self.description = description

    def __str__(self):
        return f'{self.name}, Acquire probability: {self.acquire_probability}'

    def __repr__(self) -> str:
        return self.__str__()
    
    # def desc(self):
    #     return (f'Item description: {self.desc}')
