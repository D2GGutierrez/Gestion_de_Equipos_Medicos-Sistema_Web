// Datos del panel administrativo (Laboratorio 11, Parte 2): entidad principal = EquipoInstalado.
// Escritos a mano con la forma de la respuesta de la API de la Semana 8 (GET /api/equipos/) y con
// registros reales de db.sqlite3. Se reemplazarán por fetch en la Semana 12.
export const equiposIniciales = [
  { id: 3, numero_serie: 'ECO-0001', fecha_instalacion: '2026-10-04', fin_garantia: '2028-10-04', estado: 'OPERATIVO', producto: 1, producto_nombre: 'Ecógrafo Doppler Color', cliente: 1, cliente_razon_social: 'Clínica San Gabriel S.A.' },
  { id: 4, numero_serie: 'ECO-0002', fecha_instalacion: '2026-10-04', fin_garantia: '2028-10-04', estado: 'OPERATIVO', producto: 1, producto_nombre: 'Ecógrafo Doppler Color', cliente: 1, cliente_razon_social: 'Clínica San Gabriel S.A.' },
  { id: 5, numero_serie: 'MON-0101', fecha_instalacion: '2024-03-12', fin_garantia: '2026-03-12', estado: 'OPERATIVO', producto: 3, producto_nombre: 'Monitor Multiparámetro', cliente: 1, cliente_razon_social: 'Clínica San Gabriel S.A.' },
  { id: 6, numero_serie: 'MON-0102', fecha_instalacion: '2024-03-12', fin_garantia: '2026-03-12', estado: 'OPERATIVO', producto: 3, producto_nombre: 'Monitor Multiparámetro', cliente: 1, cliente_razon_social: 'Clínica San Gabriel S.A.' },
  { id: 7, numero_serie: 'MON-0103', fecha_instalacion: '2025-06-20', fin_garantia: '2027-06-20', estado: 'MANTENIMIENTO', producto: 3, producto_nombre: 'Monitor Multiparámetro', cliente: 2, cliente_razon_social: 'Hospital Regional de Arequipa' },
  { id: 8, numero_serie: 'MON-0104', fecha_instalacion: '2023-01-18', fin_garantia: '2025-01-18', estado: 'INACTIVO', producto: 3, producto_nombre: 'Monitor Multiparámetro', cliente: 3, cliente_razon_social: 'Centro Médico Santa Rosa E.I.R.L.' },
  { id: 9, numero_serie: 'VEN-0201', fecha_instalacion: '2025-02-05', fin_garantia: '2028-02-05', estado: 'OPERATIVO', producto: 5, producto_nombre: 'Ventilador Mecánico', cliente: 2, cliente_razon_social: 'Hospital Regional de Arequipa' },
  { id: 10, numero_serie: 'VEN-0202', fecha_instalacion: '2025-02-05', fin_garantia: '2028-02-05', estado: 'MANTENIMIENTO', producto: 5, producto_nombre: 'Ventilador Mecánico', cliente: 2, cliente_razon_social: 'Hospital Regional de Arequipa' },
  { id: 11, numero_serie: 'DES-0301', fecha_instalacion: '2024-11-03', fin_garantia: '2026-11-03', estado: 'OPERATIVO', producto: 6, producto_nombre: 'Desfibrilador Bifásico', cliente: 3, cliente_razon_social: 'Centro Médico Santa Rosa E.I.R.L.' },
  { id: 12, numero_serie: 'DES-0302', fecha_instalacion: '2023-08-27', fin_garantia: '2025-08-27', estado: 'MANTENIMIENTO', producto: 6, producto_nombre: 'Desfibrilador Bifásico', cliente: 1, cliente_razon_social: 'Clínica San Gabriel S.A.' },
  { id: 13, numero_serie: 'OXI-0401', fecha_instalacion: '2022-05-09', fin_garantia: '2023-05-09', estado: 'INACTIVO', producto: 4, producto_nombre: 'Pulsioxímetro de Mesa', cliente: 3, cliente_razon_social: 'Centro Médico Santa Rosa E.I.R.L.' },
  { id: 14, numero_serie: 'RX-0501', fecha_instalacion: '2025-09-15', fin_garantia: '2028-09-15', estado: 'OPERATIVO', producto: 2, producto_nombre: 'Rayos X Portátil', cliente: 2, cliente_razon_social: 'Hospital Regional de Arequipa' },
  { id: 15, numero_serie: 'MON-0201', fecha_instalacion: '2026-10-05', fin_garantia: '2028-10-05', estado: 'OPERATIVO', producto: 3, producto_nombre: 'Monitor Multiparámetro', cliente: 2, cliente_razon_social: 'Hospital Regional de Arequipa' },
  { id: 16, numero_serie: 'MON-0202', fecha_instalacion: '2026-10-05', fin_garantia: '2028-10-05', estado: 'OPERATIVO', producto: 3, producto_nombre: 'Monitor Multiparámetro', cliente: 2, cliente_razon_social: 'Hospital Regional de Arequipa' },
]
