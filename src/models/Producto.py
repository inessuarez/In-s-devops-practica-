import uuid

class Producto:
    def __init__(self, nombre: str, precio: float, stock: int):
        if precio < 0:
            raise ValueError("El precio no puede ser negativo.")
        if stock < 0:
            raise ValueError("El stock no puede ser negativo.")
        self.id: str = str(uuid.uuid4())
        self.nombre: str = nombre
        self.precio: float = float(precio)
        self.stock: int = int(stock)

    def hay_stock(self, cantidad: int) -> bool:
        """Devuelve True si hay al menos 'cantidad' en stock."""
        return cantidad > 0 and self.stock >= cantidad

    def actualizar_stock(self, cantidad: int) -> None:
        """Modifica el stock en 'cantidad' (puede ser positivo o negativo)."""
        nuevo_stock = self.stock + cantidad
        if nuevo_stock < 0:
            raise ValueError("Stock insuficiente.")
        self.stock = nuevo_stock

    def __str__(self) -> str:
        return f"Producto(id={self.id}, nombre={self.nombre}, precio={self.precio:.2f}€, stock={self.stock})"


class ProductoElectronico(Producto):
    def __init__(self, nombre: str, precio: float, stock: int, garantia_meses: int = 24):
        super().__init__(nombre, precio, stock)
        if garantia_meses <= 0:
            raise ValueError("Garantía inválida.")
        self.garantia_meses: int = garantia_meses

    def __str__(self) -> str:
        return (f"ProductoElectronico(id={self.id}, nombre={self.nombre}, "
                f"precio={self.precio:.2f}€, stock={self.stock}, "
                f"garantía={self.garantia_meses} meses)")


class ProductoRopa(Producto):
    def __init__(self, nombre: str, precio: float, stock: int, talla: str, color: str):
        super().__init__(nombre, precio, stock)
        if not talla or not color:
            raise ValueError("Talla y color obligatorios.")
        self.talla: str = talla
        self.color: str = color

    def __str__(self) -> str:
        return (f"ProductoRopa(id={self.id}, nombre={self.nombre}, "
                f"precio={self.precio:.2f}€, stock={self.stock}, "
                f"talla={self.talla}, color={self.color})")

