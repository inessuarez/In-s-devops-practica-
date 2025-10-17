import uuid
from datetime import datetime
from typing import List

class PedidoItem:
    def __init__(self, producto_id: str, nombre: str, precio_unitario: float, cantidad: int):
        if cantidad <= 0:
            raise ValueError("Cantidad inválida")
        if precio_unitario < 0:
            raise ValueError("Precio inválido")
        self.producto_id: str = producto_id
        self.nombre: str = nombre
        self.precio_unitario: float = float(precio_unitario)
        self.cantidad: int = int(cantidad)

    def subtotal(self) -> float:
        return round(self.precio_unitario * self.cantidad, 2)


class Pedido:
    def __init__(self, cliente_id: str, items: List[PedidoItem], cliente_nombre: str = None):
        if not items:
            raise ValueError("El pedido debe tener productos")
        self.id: str = str(uuid.uuid4())
        self.cliente_id: str = cliente_id
        self.cliente_nombre: str = cliente_nombre or f"Cliente({cliente_id})"
        self.items: List[PedidoItem] = items
        self.fecha = datetime.now()

    def total(self) -> float:
        return round(sum(i.subtotal() for i in self.items), 2)

    def __str__(self) -> str:
        lineas = "\n".join(
            f"  - {i.nombre} x{i.cantidad} @ {i.precio_unitario:.2f}€ = {i.subtotal():.2f}€"
            for i in self.items
        )
        return (
            f"Pedido(id={self.id}, fecha={self.fecha:%Y-%m-%d %H:%M}, cliente={self.cliente_nombre})\n"
            f"{lineas}\n"
            f"Total: {self.total():.2f}€"
        )

