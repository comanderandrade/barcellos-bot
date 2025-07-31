document.addEventListener('DOMContentLoaded', () => {
    const startBtn = document.getElementById('start-btn');
    const pauseBtn = document.getElementById('pause-btn');
    const resumeBtn = document.getElementById('resume-btn');

    const modal = document.getElementById('status-modal');
    const modalText = document.getElementById('modal-text');
    const productsTableBody = document.querySelector('#products-table tbody');
    const productDetailsPre = document.getElementById('product-details');

    let eventSource;

    function setControlsState(isProcessing) {
        startBtn.disabled = isProcessing;
        pauseBtn.disabled = !isProcessing;
        resumeBtn.disabled = true; // Sempre começa desabilitado
    }

    if (startBtn) {
        startBtn.addEventListener('click', () => {
            setControlsState(true);
            startBtn.textContent = 'Processando...';
            // ... (resto da lógica do startBtn)
            fetch('/start-processing')
                .then(response => {
                    if (response.ok) {
                        setupEventSource();
                    } else {
                        throw new Error('Falha ao iniciar o processamento.');
                    }
                })
                .catch(error => {
                    modalText.textContent = `Erro: ${error.message}`;
                    setControlsState(false);
                });
        });
    }

    if (pauseBtn) {
        pauseBtn.addEventListener('click', () => {
            fetch('/pause', { method: 'POST' });
            pauseBtn.disabled = true;
            resumeBtn.disabled = false;
        });
    }

    if (resumeBtn) {
        resumeBtn.addEventListener('click', () => {
            fetch('/resume', { method: 'POST' });
            resumeBtn.disabled = true;
            pauseBtn.disabled = false;
        });
    }


    function setupEventSource() {
        // ... (lógica do setupEventSource como antes) ...
        eventSource = new EventSource('/stream');

        eventSource.onmessage = (event) => {
            const data = JSON.parse(event.data);
            
            modalText.textContent = `[${data.product_name || 'Sistema'}]: ${data.message}`;
            
            if (data.product_id) {
                updateTable(data);
            }
            
            if (data.full_data) {
                productDetailsPre.textContent = JSON.stringify(data.full_data, null, 2);
            }

            if (data.status === 'finished') {
                modalText.textContent = 'Processo finalizado!';
                setControlsState(false);
                startBtn.textContent = 'Iniciar Novo Processamento';
                setTimeout(() => modal.classList.add('modal-hidden'), 5000);
                eventSource.close();
            }
        };
        // ... (resto da lógica do onopen e onerror) ...
    }

    function updateTable(data) {
        // ... (lógica do updateTable como antes) ...
        const { product_id, product_name, message, color } = data;
        let row = document.getElementById(`product-${product_id}`);

        if (!row) {
            row = document.createElement('tr');
            row.id = `product-${product_id}`;
            row.innerHTML = `<td>${product_name}</td><td class="status-cell"></td>`;
            productsTableBody.appendChild(row);
        }

        const statusCell = row.querySelector('.status-cell');
        statusCell.textContent = message;
        statusCell.className = `status-cell ${color}`;
    }
});