import uuid

class Usuario:
    def __init__(self, nombre: str, email: str):
        if not nombre:
            raise ValueError("El nombre no puede estar vacío.")
        if "@" not in email:
            raise ValueError("El email no es válido.")
        self.id: str = str(uuid.uuid4())
        self.nombre: str = nombre
        self.email: str = email

    def is_admin(self) -> bool:
        """Por defecto, un usuario no es administrador."""
        return False

    def __str__(self) -> str:
        return f"Usuario(id={self.id}, nombre={self.nombre}, email={self.email})"


class Cliente(Usuario):
    def __init__(self, nombre: str, email: str, direccion_postal: str):
        super().__init__(nombre, email)
        if not direccion_postal:
            raise ValueError("La dirección postal no puede estar vacía.")
        self.direccion_postal: str = direccion_postal

    def __str__(self) -> str:
        return (f"Cliente(id={self.id}, nombre={self.nombre}, "
                f"email={self.email}, direccion={self.direccion_postal})")


class Administrador(Usuario):
    def __init__(self, nombre: str, email: str):
        super().__init__(nombre, email)

    def is_admin(self) -> bool:
        """Un administrador siempre devuelve True."""
        return True

    def __str__(self) -> str:
        return f"Administrador(id={self.id}, nombre={self.nombre}, email={self.email})"

