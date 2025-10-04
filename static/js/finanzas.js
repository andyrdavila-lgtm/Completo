function calcularCuota() {
            const monto = parseFloat(document.getElementById('prestamo-monto').value) || 0;
            const tasa = parseFloat(document.getElementById('prestamo-tasa').value) || 0;
            const plazo = parseInt(document.getElementById('prestamo-plazo').value) || 1;
            
            if (monto > 0 && tasa > 0 && plazo > 0) {
                const tasaMensual = tasa / 100;
                const cuota = (monto * tasaMensual) + (monto / plazo);
                const totalPagar = cuota * plazo;
                const interesTotal = totalPagar - monto;
                
                document.getElementById('cuota-mensual').textContent = cuota.toFixed(2);
                document.getElementById('total-pagar').textContent = totalPagar.toFixed(2);
                document.getElementById('interes-total').textContent = interesTotal.toFixed(2);
            } else {
                document.getElementById('cuota-mensual').textContent = '0.00';
                document.getElementById('total-pagar').textContent = '0.00';
                document.getElementById('interes-total').textContent = '0.00';
            }
        }