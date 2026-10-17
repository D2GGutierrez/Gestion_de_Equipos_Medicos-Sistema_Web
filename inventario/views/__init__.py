# Paquete de vistas de inventario, separado por dominio:
#   productos   -> Productos, Productos con Proveedores y Categorías
#   suministros -> CRUD del modelo intermedio Suministro (N:M Producto <-> Proveedor)
#   clientes    -> Clientes
#   usuarios    -> Usuarios del sistema
#   equipos     -> Equipos Instalados y registro de instalaciones (RF-04)
#   tickets     -> Tickets de Soporte (RF-05)
#   reportes    -> Reportes con aggregate() / annotate()
