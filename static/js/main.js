// Funcionalidades generales del sistema SISTEMACOM

document.addEventListener('DOMContentLoaded', function() {
    console.log('SISTEMACOM - Sistema de Gestión Inicializado');
    
    // Manejar alertas automáticas
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            alert.style.transition = 'opacity 0.5s ease';
            setTimeout(() => {
                if (alert.parentNode) {
                    alert.parentNode.removeChild(alert);
                }
            }, 500);
        }, 5000);
    });

    // Cargar datos del dashboard vía API
    if (window.location.pathname === '/dashboard' || window.location.pathname === '/') {
        loadDashboardStats();
        setupDashboardCharts();
    }

    // Mejorar la experiencia de formularios
    enhanceForms();
});

// Función para cargar estadísticas del dashboard
function loadDashboardStats() {
    fetch('/api/dashboard_stats')
        .then(response => {
            if (!response.ok) {
                throw new Error('Error en la respuesta del servidor');
            }
            return response.json();
        })
        .then(data => {
            console.log('Datos del dashboard cargados:', data);
            updateDashboardStats(data);
        })
        .catch(error => {
            console.error('Error al cargar estadísticas:', error);
        });
}

// Función para actualizar estadísticas en el dashboard
function updateDashboardStats(data) {
    // Aquí puedes actualizar elementos específicos del DOM con los datos
    const statsElements = {
        'user_count': document.querySelector('.stat-card:nth-child(1) .stat-number'),
        'report_count': document.querySelector('.stat-card:nth-child(2) .stat-number'),
        'client_count': document.querySelector('.stat-card:nth-child(3) .stat-number')
    };

    for (const [key, element] of Object.entries(statsElements)) {
        if (element && data[key] !== undefined) {
            element.textContent = data[key];
        }
    }
}

// Función para configurar gráficos (placeholder para futura implementación)
function setupDashboardCharts() {
    // Aquí puedes integrar bibliotecas como Chart.js
    console.log('Configurando gráficos del dashboard...');
}

// Función para mejorar formularios
function enhanceForms() {
    // Agregar validación básica a formularios
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const requiredFields = form.querySelectorAll('[required]');
            let valid = true;

            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    valid = false;
                    field.style.borderColor = 'var(--color-error)';
                } else {
                    field.style.borderColor = '';
                }
            });

            if (!valid) {
                e.preventDefault();
                alert('Por favor complete todos los campos requeridos');
            }
        });
    });

    // Mejorar experiencia de campos de fecha
    const dateInputs = document.querySelectorAll('input[type="date"]');
    dateInputs.forEach(input => {
        if (!input.value) {
            input.value = new Date().toISOString().split('T')[0];
        }
    });
}

// Función para confirmar acciones importantes
function confirmAction(message, callback) {
    if (confirm(message || '¿Estás seguro de que deseas realizar esta acción?')) {
        if (typeof callback === 'function') {
            callback();
        }
        return true;
    }
    return false;
}

// Función para mostrar loading en botones
function setButtonLoading(button, isLoading) {
    if (isLoading) {
        button.disabled = true;
        button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Procesando...';
    } else {
        button.disabled = false;
        button.innerHTML = button.getAttribute('data-original-text') || button.innerHTML;
    }
}

// Función para formatear fechas
function formatDate(dateString) {
    const options = { 
        year: 'numeric', 
        month: '2-digit', 
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
    };
    return new Date(dateString).toLocaleDateString('es-ES', options);
}

// Exportar funciones para uso global
window.SISTEMACOM = {
    confirmAction,
    setButtonLoading,
    formatDate
};