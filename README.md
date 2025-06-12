<title>Documentación - Vuelos para Mascotas</title>
Documentación del Proyecto

  <div class="mb-5">
    <h2>Autores</h2>
    <ul>
      <li>Jesús Vilardi</li>
      <li>Juan Esteban</li>
    </ul>
  </div>

  <div class="mb-5">
    <h2>Descripción</h2>
    <p>
      Sistema web para la gestión de usuarios y vuelos para mascotas, desarrollado como parte del proyecto <strong>"sigmotoaflights"</strong> en asociación con una aerolínea internacional.
      Los usuarios pueden reservar y comprar vuelos donde las mascotas son lo principal, gestionar la información de sus mascotas y consultar la disponibilidad de vuelos en tiempo real.
    </p>
  </div>

  <div class="mb-5">
    <h2>Funcionalidades Principales</h2>
    <ul>
      <li>Registro de usuarios y de mascotas (ambos en el mismo formulario)</li>
      <li>Consulta de vuelos disponibles por origen, destino y fecha</li>
      <li>Reserva de vuelos con validación de disponibilidad</li>
      <li>Compra de vuelos asociados a una reserva</li>
      <li>Consulta de la cantidad de mascotas con boleto en cada vuelo</li>
      <li>Gestión completa de usuarios y mascotas (buscar, actualizar, crear, eliminar)</li>
      <li>Interfaz web responsiva y funcional</li>
    </ul>
  </div>

  <div class="mb-5">
    <h2>Modelos de Datos</h2>
    <h5>Usuario</h5>
    <ul>
      <li><strong>id:</strong> int</li>
      <li><strong>nombre:</strong> str</li>
      <li><strong>edadUsuario:</strong> int</li>
      <li><strong>CC:</strong> str</li>
      <li><strong>nombreMascota:</strong> str</li>
      <li><strong>edadMascota:</strong> int</li>
      <li><strong>idMascota:</strong> int</li>
    </ul>
    <h5 class="mt-4">Vuelo</h5>
    <ul>
      <li><strong>id:</strong> int</li>
      <li><strong>origen:</strong> str</li>
      <li><strong>destino:</strong> str</li>
      <li><strong>fecha:</strong> str (YYYY-MM-DD)</li>
      <li><strong>sillasReservadas:</strong> int</li>
      <li><strong>sillasVendidas:</strong> int</li>
    </ul>
  </div>

  <div class="mb-5">
    <h2>Endpoints Principales</h2>
    <ul>
      <li><code>/usuarios</code> (GET, POST): Listar y crear usuarios</li>
      <li><code>/usuarios/{id}</code> (GET, PUT, DELETE): Obtener, actualizar y eliminar usuario</li>
      <li><code>/vuelos</code> (GET, POST): Listar y crear vuelos, permite filtrar por origen, destino y fecha</li>
      <li><code>/vuelos/{id}</code> (GET, PUT, DELETE): Obtener, actualizar y eliminar vuelo</li>
    </ul>
  </div>

  <div class="mb-5">
    <h2>Estructura del Proyecto</h2>
    <pre>

parcialfinal/
├── main.py
├── models/
│ ├── usuario.py
│ └── vuelo.py
├── routers/
│ ├── usuarios.py
│ └── vuelos.py
├── templates/
│ ├── index.html
│ ├── usuarios/...
│ └── vuelos/...
├── static/
│ └── (assets y estilos)
├── requirements.txt
└── README.md

  <div class="mb-5">
    <h2>Diagramas</h2>
    <h5>Casos de Uso</h5>
    <img src="/static/diagramas/casos_uso.png" alt="Diagrama de casos de uso" class="img-fluid mb-3">
    <h5>Clases</h5>
    <img src="/static/diagramas/clases.png" alt="Diagrama de clases" class="img-fluid">
  </div>

  <div class="mb-5">
    <h2>Instrucciones de Uso</h2>
    <ol>
      <li>Instala dependencias: <code>pip install -r requirements.txt</code></li>
      <li>Ejecuta el servidor: <code>uvicorn main:app --reload</code></li>
      <li>Accede al sistema en <a href="http://localhost:8000">http://localhost:8000</a></li>
    </ol>
  </div>

  <div class="mb-5">
    <h2>Autores</h2>
    <ul>
      <li>Jesús Vilardi</li>
      <li>Juan Esteban</li>
    </ul>
  </div>

</div>

<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
