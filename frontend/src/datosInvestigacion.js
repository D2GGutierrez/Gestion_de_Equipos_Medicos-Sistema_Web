// Datos de la investigación propia (Proveedor y su modelo intermedio Suministro, relación
// ManyToMany Producto <-> Proveedor). Escritos a mano con la forma de la API y con los valores
// reales de db.sqlite3; se reemplazarán por fetch en la Semana 12.
// Los decimales llegan como TEXTO (así los devuelve DRF) y cada proveedor trae sus suministros anidados.
export const proveedores = [
  {
    id: 1,
    nombre_empresa: 'MedTech Perú S.A.C.',
    ruc_nit: '20512345671',
    contacto: 'Carla Mendoza',
    telefono: '014567890',
    suministros: [
      { id: 1, producto_nombre: 'Ecógrafo Doppler Color', precio_compra: '152000.00', dias_entrega_promedio: 15, es_proveedor_principal: true },
      { id: 4, producto_nombre: 'Rayos X Portátil', precio_compra: '274900.00', dias_entrega_promedio: 60, es_proveedor_principal: false },
      { id: 11, producto_nombre: 'Desfibrilador Bifásico', precio_compra: '55200.00', dias_entrega_promedio: 12, es_proveedor_principal: true },
    ],
  },
  {
    id: 2,
    nombre_empresa: 'BioEquipos Andinos S.R.L.',
    ruc_nit: '20498765432',
    contacto: 'Luis Paredes',
    telefono: '012345678',
    suministros: [
      { id: 2, producto_nombre: 'Ecógrafo Doppler Color', precio_compra: '158500.00', dias_entrega_promedio: 30, es_proveedor_principal: false },
      { id: 5, producto_nombre: 'Monitor Multiparámetro', precio_compra: '34800.00', dias_entrega_promedio: 10, es_proveedor_principal: true },
      { id: 10, producto_nombre: 'Ventilador Mecánico', precio_compra: '236000.00', dias_entrega_promedio: 25, es_proveedor_principal: false },
    ],
  },
  {
    id: 3,
    nombre_empresa: 'Distribuidora Hospitalaria del Sur',
    ruc_nit: '20600112233',
    contacto: 'Rosa Quispe',
    telefono: '054223344',
    suministros: [
      { id: 6, producto_nombre: 'Monitor Multiparámetro', precio_compra: '36200.00', dias_entrega_promedio: 7, es_proveedor_principal: false },
      { id: 8, producto_nombre: 'Pulsioxímetro de Mesa', precio_compra: '2650.00', dias_entrega_promedio: 3, es_proveedor_principal: true },
      { id: 12, producto_nombre: 'Desfibrilador Bifásico', precio_compra: '57800.00', dias_entrega_promedio: 5, es_proveedor_principal: false },
    ],
  },
  {
    id: 4,
    nombre_empresa: 'Global Health Supply E.I.R.L.',
    ruc_nit: '20555667788',
    contacto: 'Martín Salazar',
    telefono: '017788990',
    suministros: [
      { id: 3, producto_nombre: 'Rayos X Portátil', precio_compra: '268000.00', dias_entrega_promedio: 45, es_proveedor_principal: true },
      { id: 7, producto_nombre: 'Monitor Multiparámetro', precio_compra: '35500.00', dias_entrega_promedio: 20, es_proveedor_principal: false },
      { id: 9, producto_nombre: 'Ventilador Mecánico', precio_compra: '229000.00', dias_entrega_promedio: 40, es_proveedor_principal: true },
    ],
  },
]
