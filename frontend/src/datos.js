// Datos escritos a mano (todavía no se consume la API: eso se hace en la Semana 12).
// Se mueven aquí desde App.jsx para que App.jsx quede solo con la interfaz.
// Misma forma que la respuesta de la API de la Semana 8 (GET /api/productos/):
// los decimales llegan como TEXTO ("4500.00"), no como número.
export const productos = [
  { id: 1, codigo_sku: 'ECO-100', nombre: 'Ecógrafo Doppler Color', marca: 'GE', modelo: 'Logiq P9', precio_base: '18500.00', meses_garantia: 24, stock: 3, categoria: { id: 1, nombre: 'Diagnóstico por Imagen' } },
  { id: 2, codigo_sku: 'MON-200', nombre: 'Monitor de Signos Vitales', marca: 'Philips', modelo: 'IntelliVue MX450', precio_base: '4500.5', meses_garantia: 12, stock: 8, categoria: { id: 2, nombre: 'Monitoreo de Pacientes' } },
  { id: 3, codigo_sku: 'VEN-300', nombre: 'Ventilador Mecánico', marca: 'Dräger', modelo: 'Evita V300', precio_base: '32000.00', meses_garantia: 24, stock: 2, categoria: { id: 3, nombre: 'Soporte Vital' } },
  { id: 4, codigo_sku: 'DES-400', nombre: 'Desfibrilador Bifásico', marca: 'Zoll', modelo: 'R Series', precio_base: '9800.75', meses_garantia: 18, stock: 0, categoria: { id: 3, nombre: 'Soporte Vital' } },
  { id: 5, codigo_sku: 'OXI-500', nombre: 'Oxímetro de Pulso', marca: 'Masimo', modelo: 'Rad-97', precio_base: '6.5', meses_garantia: 6, stock: 25, categoria: { id: 2, nombre: 'Monitoreo de Pacientes' } },
]

// Relación 1:N (Cliente -> equipos instalados), con la forma de GET /api/clientes-equipos/.
// Cada cliente trae un arreglo "equipos" dentro; los decimales llegan como texto.
export const clientes = [
  {
    id: 1, razon_social: 'Clínica San Gabriel S.A.',
    equipos: [
      { id: 11, numero_serie: 'ECO-0001', estado: 'OPERATIVO', producto_nombre: 'Ecógrafo Doppler Color', precio_base: '18500.00' },
      { id: 12, numero_serie: 'MON-0101', estado: 'OPERATIVO', producto_nombre: 'Monitor de Signos Vitales', precio_base: '4500.5' },
      { id: 13, numero_serie: 'DES-0302', estado: 'MANTENIMIENTO', producto_nombre: 'Desfibrilador Bifásico', precio_base: '9800.75' },
    ],
  },
  {
    id: 2, razon_social: 'Hospital Regional de Arequipa',
    equipos: [
      { id: 21, numero_serie: 'VEN-0201', estado: 'OPERATIVO', producto_nombre: 'Ventilador Mecánico', precio_base: '32000.00' },
      { id: 22, numero_serie: 'VEN-0202', estado: 'MANTENIMIENTO', producto_nombre: 'Ventilador Mecánico', precio_base: '32000.00' },
    ],
  },
  {
    id: 3, razon_social: 'Centro Médico Santa Rosa E.I.R.L.',
    equipos: [
      { id: 31, numero_serie: 'OXI-0401', estado: 'INACTIVO', producto_nombre: 'Oxímetro de Pulso', precio_base: '6.5' },
    ],
  },
]
