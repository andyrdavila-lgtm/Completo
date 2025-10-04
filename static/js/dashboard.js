// static/js/dashboard.js

// Función para cargar los datos del dashboard
async function loadDashboardData() {
    try {
        // Simular datos mientras se implementan las APIs reales
        const dashboardData = await fetchDashboardData();
        
        // Actualizar la interfaz con los datos
        updateUI(dashboardData);
    } catch (error) {
        console.error('Error cargando datos del dashboard:', error);
        showError('Error al cargar los datos del dashboard');
    }
}

// Función para simular la obtención de datos (reemplazar con APIs reales)
async function fetchDashboardData() {
    // En una implementación real, estas serían llamadas a APIs
    return {
        user: {
            name: "Juan Pérez",
            company: "A&D Empresa"
        },
        stats: {
            totalClients: 156,
            activeProjects: 24,
            monthlyRevenue: 24580
        },
        topClients: [
            { name: "Cliente A", sales: 12500, status: "Activo" },
            { name: "Cliente B", sales: 9800, status: "Activo" },
            { name: "Cliente C", sales: 7600, status: "Inactivo" },
            { name: "Cliente D", sales: 5400, status: "Activo" },
            { name: "Cliente E", sales: 3200, status: "Pendiente" }
        ],
        categories: [
            { name: "Categoría 1", value: 35 },
            { name: "Categoría 2", value: 25 },
            { name: "Categoría 3", value: 20 },
            { name: "Categoría 4", value: 15 },
            { name: "Categoría 5", value: 5 }
        ],
        status: {
            active: 42,
            pending: 18,
            completed: 89,
            cancelled: 7
        },
        alerts: [
            { type: "error", title: "Error de conexión", description: "No se puede conectar con el servidor de base de datos" },
            { type: "warning", title: "Espacio en disco", description: "Queda menos del 10% de espacio en disco" },
            { type: "info", title: "Actualización disponible", description: "Nueva versión del sistema disponible" }
        ]
    };
}

// Función para actualizar la interfaz con los datos
function updateUI(data) {
    // Actualizar información del usuario
    document.getElementById('user-name').textContent = data.user.name;
    
    // Actualizar estadísticas del sidebar
    document.getElementById('total-clients').textContent = data.stats.totalClients;
    document.getElementById('active-projects').textContent = data.stats.activeProjects;
    document.getElementById('monthly-revenue').textContent = `$${data.stats.monthlyRevenue.toLocaleString()}`;
    
    // Actualizar tabla de top clientes
    const clientsTable = document.getElementById('top-clients-table');
    clientsTable.innerHTML = data.topClients.map(client => `
        <tr>
            <td>${client.name}</td>
            <td>$${client.sales.toLocaleString()}</td>
            <td><span class="status-badge ${client.status.toLowerCase()}">${client.status}</span></td>
        </tr>
    `).join('');
    
    // Actualizar resumen de estados
    document.getElementById('status-active').textContent = data.status.active;
    document.getElementById('status-pending').textContent = data.status.pending;
    document.getElementById('status-completed').textContent = data.status.completed;
    document.getElementById('status-cancelled').textContent = data.status.cancelled;
    
    // Actualizar alertas del sistema
    const alertsContainer = document.getElementById('system-alerts');
    alertsContainer.innerHTML = data.alerts.map(alert => `
        <div class="alert-item ${alert.type}">
            <div class="alert-icon">
                ${alert.type === 'error' ? '⚠️' : alert.type === 'warning' ? '🔔' : 'ℹ️'}
            </div>
            <div class="alert-content">
                <div class="alert-title">${alert.title}</div>
                <div class="alert-description">${alert.description}</div>
            </div>
        </div>
    `).join('');
    
    // Aquí también se actualizarían los gráficos cuando se implementen
}

// Función para actualizar el dashboard con filtros de fecha
function updateDashboard() {
    const startDate = document.getElementById('start-date').value;
    const endDate = document.getElementById('end-date').value;
    
    if (startDate && endDate && startDate > endDate) {
        showError('La fecha de inicio no puede ser mayor que la fecha de fin');
        return;
    }
    
    // Mostrar indicador de carga
    showLoading(true);
    
    // Simular actualización de datos con filtros
    setTimeout(() => {
        loadDashboardData();
        showLoading(false);
        showSuccess('Dashboard actualizado correctamente');
    }, 1000);
}

// Función para cerrar sesión
function logout() {
    if (confirm('¿Está seguro de que desea cerrar sesión?')) {
        // Redirigir al logout (en Flask sería url_for('logout'))
        window.location.href = '/logout';
    }
}

// Funciones de utilidad
function showLoading(show) {
    // Implementar lógica para mostrar/ocultar indicador de carga
    console.log(show ? 'Mostrando carga...' : 'Ocultando carga...');
}

function showError(message) {
    // Implementar lógica para mostrar mensaje de error
    alert(`Error: ${message}`);
}

function showSuccess(message) {
    // Implementar lógica para mostrar mensaje de éxito
    console.log(`Éxito: ${message}`);
}

// Inicializar el dashboard cuando se carga la página
document.addEventListener('DOMContentLoaded', function() {
    // Establecer fechas por defecto (últimos 30 días)
    const endDate = new Date();
    const startDate = new Date();
    startDate.setDate(startDate.getDate() - 30);
    
    document.getElementById('start-date').valueAsDate = startDate;
    document.getElementById('end-date').valueAsDate = endDate;
    
    // Cargar datos iniciales
    loadDashboardData();
    
    // Configurar event listeners para las pestañas
    document.querySelectorAll('.tab').forEach(tab => {
        tab.addEventListener('click', function() {
            document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            this.classList.add('active');
            // Aquí se cargaría el contenido de la pestaña seleccionada
        });
    });
});