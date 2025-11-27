from typing import Dict, List, Tuple
from models.Producto import Producto
from models.Usuario import Usuario, Cliente, Administrador
from models.Pedido import Pedido, PedidoItem


class TiendaService:
    def __init__(self):
        # Índices en memoria
        self.usuarios: Dict[str, Usuario] = {}
        self.productos: Dict[str, Producto] = {}
        self.pedidos: Dict[str, Pedido] = {}
        self.email_index: Dict[str, str] = {}  # email -> usuario_id

    # ---------- Usuarios ----------
    def registrar_usuario(self, tipo: str, nombre: str, email: str, **kwargs) -> Usuario:
        """
        Crea y registra un usuario (cliente o administrador), asegurando email único.
        kwargs:
            - cliente: direccion_postal=str
        """
        if email in self.email_index:
            raise ValueError("El email ya existe en el sistema.")

        if tipo == "cliente":
            direccion = kwargs.get("direccion_postal", "").strip()
            usuario = Cliente(nombre, email, direccion)
        elif tipo == "administrador":
            usuario = Administrador(nombre, email)
        else:
            raise ValueError("Tipo de usuario inválido. Use 'cliente' o 'administrador'.")

        self.usuarios[usuario.id] = usuario
        self.email_index[email] = usuario.id
        return usuario

    def listar_usuarios(self) -> List[Usuario]:
        return list(self.usuarios.values())

    def obtener_usuario_por_email(self, email: str) -> Usuario:
        uid = self.email_index.get(email)
        if not uid:
            raise KeyError("No existe un usuario con ese email.")
        return self.usuarios[uid]

    # ---------- Productos ----------
    def agregar_producto(self, producto: Producto) -> Producto:
        if producto.id in self.productos:
            raise ValueError("Ya existe un producto con ese id.")
        self.productos[producto.id] = producto
        return producto

    def eliminar_producto(self, producto_id: str) -> None:
        if producto_id not in self.productos:
            raise KeyError("Producto no encontrado.")
        del self.productos[producto_id]

    def listar_productos(self) -> List[Producto]:
        return list(self.productos.values())

    def obtener_producto(self, producto_id: str) -> Producto:
        prod = self.productos.get(producto_id)
        if not prod:
            raise KeyError("Producto no encontrado.")
        return prod

    # ---------- Pedidos ----------
    def realizar_pedido(self, cliente_id: str, items: List[Tuple[str, int]]) -> Pedido:
        """
        Crea un pedido para el cliente con id `cliente_id`.
        `items` es una lista de tuplas (producto_id, cantidad).
        """
        # Validaciones básicas
        cliente = self.usuarios.get(cliente_id)
        if not cliente:
            raise ValueError("El cliente no existe.")
        if not isinstance(cliente, Cliente):
            raise ValueError("Solo los clientes pueden realizar pedidos.")
        if not items:
            raise ValueError("El pedido debe tener al menos un producto.")

        # 1) Verificar stock y construir líneas de pedido
        lineas: List[PedidoItem] = []
        for pid, cantidad in items:
            producto = self.obtener_producto(pid)
            if not producto.hay_stock(cantidad):
                raise ValueError(f"Stock insuficiente para '{producto.nombre}'.")
            linea = PedidoItem(
                producto_id=pid,
                nombre=producto.nombre,
                precio_unitario=producto.precio,
                cantidad=cantidad
            )
            lineas.append(linea)

        # 2) Descontar stock (si todo lo anterior fue válido)
        for pid, cantidad in items:
            self.productos[pid].actualizar_stock(-cantidad)

        # 3) Crear y guardar el pedido
        pedido = Pedido(cliente_id=cliente_id, items=lineas, cliente_nombre=cliente.nombre)
        self.pedidos[pedido.id] = pedido
        return pedido

    def listar_pedidos_usuario(self, cliente_id: str) -> List[Pedido]:
        """Devuelve los pedidos de un cliente ordenados por fecha (ascendente)."""
        pedidos_cliente = [p for p in self.pedidos.values() if p.cliente_id == cliente_id]
        return sorted(pedidos_cliente, key=lambda p: p.fecha)

    def obtener_pedido(self, pedido_id: str) -> Pedido:
        ped = self.pedidos.get(pedido_id)
        if not ped:
            raise KeyError("Pedido no encontrado.")
        return ped

