// =============================================
// CONFIGURAÇÕES GLOBAIS
// =============================================
const debug = true; // Ativar logs detalhados
const VALOR_DIARIA = 35.00; // Valor fixo da diária

// =============================================
// ESTADO DA APLICAÇÃO
// =============================================
const appState = {
    viagemId: null,
    gastos: [],
    // Não precisamos mais carregar cidades via API
};

// =============================================
// FUNÇÕES PRINCIPAIS
// =============================================

/**
 * Calcula dias e valor da diária automaticamente
 */
function calcularDiasEDiaria() {
    const dataSaida = document.getElementById('dataSaida');
    const dataRetorno = document.getElementById('dataRetorno');
    const quantidadeDias = document.getElementById('quantidadeDias');
    const valorDiaria = document.getElementById('valorDiaria');

    if (dataSaida.value && dataRetorno.value) {
        const inicio = new Date(dataSaida.value);
        const fim = new Date(dataRetorno.value);
        
        if (fim < inicio) {
            alert('Data de retorno deve ser posterior à data de saída');
            dataRetorno.value = '';
            quantidadeDias.value = '';
            valorDiaria.value = '';
            return;
        }

        const diffTime = Math.abs(fim - inicio);
        const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24)) + 1;
        
        quantidadeDias.value = diffDays;
        valorDiaria.value = (diffDays * VALOR_DIARIA).toFixed(2);
    }
}

/**
 * Salva os dados principais da viagem
 */
async function salvarDadosPrincipais(event) {
    event.preventDefault();
    
    try {
        const formData = {
            cidadeDestino: document.getElementById('cidadeDestino').value,
            dataSaida: document.getElementById('dataSaida').value,
            dataRetorno: document.getElementById('dataRetorno').value,
            codigoRelatorio: document.getElementById('codigoRelatorio').value,
            tipoViagem: document.getElementById('tipoViagem').value,
            descricao: document.getElementById('descricao').value
        };

        // Simulação de envio - substitua por chamada real ao backend
        if (debug) console.log('Dados a serem enviados:', formData);
        
        const response = await fetch('/api/viagens', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        })

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(`Erro: ${errorData.message}`);    
        }

        const data = await response.json();
        if (debug) console.log('Resposta do servidor:', data);
        appState.viagemId = data.viagemId || null; // Armazenar ID da viagem
        appState.gastos = data.gastos || [];
        // Habilitar outras abas
        document.getElementById('financeiro-tab').removeAttribute('disabled');
        document.getElementById('outros-tab').removeAttribute('disabled');
        document.getElementById('bnt-salvar-principal').setAttribute('disabled', 'disabled'); // Desabilitar botão de salvar dados principais
        document.getElementById('bnt-salvar-principal').setAttribute('style', 'display:none'); // Desabilitar botão de salvar dados principais
        document.getElementById('financeiro-tab').click(); // Mudar para a aba financeira

        showToast('Dados principais salvos com sucesso!', 'success');

        

        
    } catch (error) {
        showToast('Erro ao salvar dados','Erro ao salvar dados');
        if (debug) console.error('Detalhes do erro:', error);
    }
}

/**
 * Salva um novo gasto associado à viagem
 */
async function salvarGasto(event) {
    event.preventDefault();
    
    try {
        if (!appState.viagemId) {
            throw new Error('Salve os dados principais primeiro');
        }

        const formData = new FormData(event.target);
        const gastoData = {
            viagemId: appState.viagemId,
            tipoGasto: formData.get('tipoGasto'),
            descricao: formData.get('descricaoGasto'),
            valor: formData.get('valorGasto'),
            dataHora: formData.get('dataHoraGasto'),
            estorno: formData.get('estorno') === 'on',
            tipoDocumento: formData.get('tipoDocumento')
        };

        // Simulação de envio - substitua por chamada real ao backend
        
        console.log('Gasto a ser enviado:', gastoData);
        const response = await fetch('/api/gastos',{
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(gastoData)
        })
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(`Erro: ${errorData.message}`);
        }
        const data = await response.json();
        if (debug) console.log('Resposta do servidor:', data);
        appState.gastos.push(data.gasto); // Adiciona o gasto à lista de gastos
        // Atualiza a tabela de gastos
        const tabelaGastos = document.getElementById('tabelaGastos');
        const novaLinha = tabelaGastos.insertRow();
        novaLinha.innerHTML = `
            <td>${data.gasto.tipoGasto}</td>
            <td>${data.gasto.descricao}</td>
            <td>${data.gasto.valor}</td>
            <td>${data.gasto.dataHora}</td>
            <td>${data.gasto.estorno ? 'Sim' : 'Não'}</td>
            <td>${data.gasto.tipoDocumento}</td>
        `;
        tabelaGastos.appendChild(novaLinha);
        // Atualiza o total de gastos
        const totalGastos = document.getElementById('totalGastos');
        const valorTotal = appState.gastos.reduce((acc, gasto) => acc + parseFloat(gasto.valor), 0);
        totalGastos.textContent = `Total: R$ ${valorTotal.toFixed(2)}`;
        // Limpa o formulário
        event.target.reset();
        // Atualiza o estado da aplicação
        appState.gastos.push(gastoData);
        


        // Simulação de resposta
        showToast('Gasto salvo com sucesso!', 'success');
        event.target.reset();
        
    } catch (error) {
        handleError('Erro ao salvar gasto', error);
    }
}

/**
 * Salva informações adicionais da viagem
 */
async function salvarOutros(event) {
    event.preventDefault();
    
    try {
        if (!appState.viagemId) {
            throw new Error('Salve os dados principais primeiro');
        }

        const outrosData = {
            viagemId: appState.viagemId,
            veiculo: document.getElementById('veiculo').value,
            placa: document.getElementById('placa').value,
            kmInicial: document.getElementById('kmInicial').value,
            kmFinal: document.getElementById('kmFinal').value
        };

        // Simulação de envio
        console.log('Dados adicionais:', outrosData);
        showToast('Informações salvas!', 'success');
        
    } catch (error) {
        handleError('Erro ao salvar informações', error);
    }
}

// =============================================
// FUNÇÕES AUXILIARES
// =============================================

// function showToast(message, type = 'info') {
//     // Implementação simples de toast
//     const toast = document.createElement('div');
//     toast.className = `toast ${type}`;
//     toast.textContent = message;
//     document.body.appendChild(toast);
    
//     setTimeout(() => toast.remove(), 3000);
// }
function createToastContainer() {
    const container = document.createElement('div');
    container.id = 'toastContainer';
    container.className = 'position-fixed bottom-0 end-0 p-3';
    container.style.zIndex = '11';
    document.body.appendChild(container);
    return container;
}

function showToast(message, type = 'info') {
    // Implementação simples de toast (pode ser substituída por uma biblioteca)
    const toastContainer = document.getElementById('toastContainer') || createToastContainer();
    const toast = document.createElement('div');
    
    toast.className = `toast show align-items-center text-white bg-${type} border-0`;
    toast.setAttribute('role', 'alert');
    toast.setAttribute('aria-live', 'assertive');
    toast.setAttribute('aria-atomic', 'true');
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">${message}</div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
        </div>
    `;
    
    toastContainer.appendChild(toast);
    
    // Remover toast após alguns segundos
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => toast.remove(), 300);
    }, 5000);
}

function handleError(message, error) {
    showToast(message, 'error');
    if (debug) console.error('Detalhes do erro:', error.message);
}

// =============================================
// INICIALIZAÇÃO
// =============================================

function setupEventListeners() {
    // Dados Principais
    document.getElementById('formDadosPrincipais').addEventListener('submit', salvarDadosPrincipais);
    document.getElementById('dataSaida').addEventListener('change', calcularDiasEDiaria);
    document.getElementById('dataRetorno').addEventListener('change', calcularDiasEDiaria);
    
    // Financeiro
    document.getElementById('formGasto').addEventListener('submit', salvarGasto);
    
    // Outros
    document.getElementById('formOutros').addEventListener('submit', salvarOutros);
    
    // Desabilitar abas secundárias inicialmente
    document.getElementById('financeiro-tab').setAttribute('disabled', 'disabled');
    document.getElementById('outros-tab').setAttribute('disabled', 'disabled');
}

// Inicia a aplicação quando o DOM estiver pronto
document.addEventListener('DOMContentLoaded', () => {
    setupEventListeners();
    if (debug) console.log('Aplicação iniciada');
});