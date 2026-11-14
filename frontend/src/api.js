// Instancia única de Axios para hablar con la API REST de Django (Semana 8).
// Los componentes importan "api" y solo escriben la parte final de la ruta: api.get('/clientes/').
// Si el servidor cambia (otro puerto, producción), se modifica SOLO esta línea.
import axios from 'axios'

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000/api', // dirección base de la API de Django
  timeout: 5000, // si el servidor no responde en 5 s, Axios cancela y lanza un error
  headers: { 'Content-Type': 'application/json' },
})

export default api
