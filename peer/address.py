from dataclasses import dataclass

@dataclass
class Address:
    ip: str
    port: int

    def __str__(self):
        return f"{self.ip}:{self.port}"