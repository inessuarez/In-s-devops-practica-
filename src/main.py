from models.Producto import ProductoElectronico, ProductoRopa
from services.Tienda_service import TiendaService

def main():
    tienda = TiendaService()

    # --- Usuarios ---
    admin = tienda.registrar_usuario("administrador", "Carlos Admin", "admin@tienda.com")
    cliente = tienda.registrar_usuario(
        "cliente",
        "Inés Cliente",
        "ines@correo.com",
        direccion_postal="Calle Falsa 123, Madrid"
    )

    # --- Productos ---
    movil = ProductoElectronico("Smartphone X", 499.99, 10, garantia_meses=24)
    camiseta = ProductoRopa("Camiseta básica", 19.99, 30, talla="M", color="Azul")

    tienda.agregar_producto(movil)
    tienda.agregar_producto(camiseta)

    print("== Catálogo inicial ==")
    for p in tienda.listar_productos():
        print(" ", p)

    # --- Pedido ---
    items = [
        (movil.id, 1),     # 1 smartphone
        (camiseta.id, 2),  # 2 camisetas
    ]
    pedido = tienda.realizar_pedido(cliente.id, items)
    print("\n== Pedido creado ==")
    print(pedido)

    print("\n== Catálogo tras pedido (stock actualizado) ==")
    for p in tienda.listar_productos():
        print(" ", p)

    print("\n== Pedidos del cliente ==")
    for p in tienda.listar_pedidos_usuario(cliente.id):
        print(" ", p.id, "->", p.total(), "€")

if __name__ == "__main__":
    main()

