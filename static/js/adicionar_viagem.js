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
    usuario: document.getElementById('usuario').value || null, // ID do usuário logado
    valor: 0,
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
    const quantidadeDiarias = document.getElementById('quantidadeDiarias');
    const valorDiaria = document.getElementById('valorDiaria');

    if (dataSaida.value && dataRetorno.value) {
        const inicio = new Date(dataSaida.value);
        const fim = new Date(dataRetorno.value);
        
        // Verifica se a data de retorno é anterior à de saída
        if (fim < inicio) {
            alert('Data de retorno deve ser posterior à data de saída');
            dataRetorno.value = '';
            quantidadeDiarias.value = '';
            valorDiaria.value = '';
            return;
        }

        // Calcula a diferença em dias completos (desconsiderando horários)
        const diffDays = Math.floor((fim - inicio) / (1000 * 60 * 60 * 24));
        
        // Verifica horários de saída e retorno
        const horaSaida = inicio.getHours() + inicio.getMinutes() / 60;
        const horaRetorno = fim.getHours() + fim.getMinutes() / 60;
        
        // Define os limites de horário (7:30 e 17:30 em formato decimal)
        const LIMITE_MANHA = 7.5;   // 7:30
        const LIMITE_TARDE = 17.5;  // 17:30
        
        // Calcula diárias considerando as regras
        let diarias = 0;
        
        // Se for no mesmo dia
        if (diffDays === 0) {
            // Verifica se saiu antes das 7:30
            if (horaSaida < LIMITE_MANHA) {
                diarias = 1;
            }
            // Verifica se retornou depois das 17:30
            else if (horaRetorno > LIMITE_TARDE) {
                diarias = 1;
            }
            // Se saiu depois das 7:30 e retornou antes das 17:30
            else {
                diarias = 0;
            }
        } 
        // Se for em dias diferentes
        else {
            // Diária do dia de saída (se saiu antes das 7:30)
            diarias += horaSaida < LIMITE_MANHA ? 1 : 0;
            
            // Diária do dia de retorno (se retornou depois das 17:30)
            diarias += horaRetorno > LIMITE_TARDE ? 1 : 0;
            
            // Dias completos entre saída e retorno (cada dia conta como 1 diária)
            diarias += diffDays ;
        }

        // // Garante no mínimo 1 diária se houver qualquer período
        // if (diarias === 0 && (inicio.getTime() !== fim.getTime())) {
        //     diarias = 1;
        // }
        console.log('Diárias calculadas:', diarias);
        console.log('Diferença de dias',diffDays)

        quantidadeDiarias.value = diarias;
        valorDiaria.value = (diarias * VALOR_DIARIA).toFixed(2);
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
            numeroDiarias: document.getElementById('quantidadeDiarias').value,
            valorDiaria: document.getElementById('valorDiaria').value,
            codigoRelatorio: document.getElementById('codigoRelatorio').value,
            tipoViagem: document.getElementById('tipoViagem').value,
            descricao: document.getElementById('descricao').value,
            usuario: appState.usuario,
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
        if (debug) console.log('Resposta do servidor Viagem:', data);
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
        const documentoUpload = document.getElementById('documentoUpload') ? await salvarGastoComDocumento() : null; // ID do documento, se houver
        const documentoUploadId = documentoUpload ? documentoUpload.documentoId : null;
        if (debug) console.log('Documento a ser enviado:', documentoUpload);
        const gastoData = {
            viagemId: appState.viagemId,
            tipoGasto: formData.get('tipoGasto'),
            descricao: formData.get('descricaoGasto'),
            valor: formData.get('valorGasto'),
            dataHora: formData.get('dataHoraGasto'),
            estorno: formData.get('estorno') === 'on',
            tipoDocumento: formData.get('tipoDocumento'), 
            arquivo: documentoUploadId || null // ID do documento, se houver
        };


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
        if (debug) console.log('Resposta do servidor Gasto:', data);

        // Limpa o formulário
        event.target.reset();
        // Atualiza a tabela de gastos
        await atualizarTabelaGastos(formData, data.gastoId, documentoUpload);
         // Atualiza o total de gastos
        await atulizarTotalGasto();
        appState.gastos.push(data.gasto); // Adiciona o gasto à lista de gastos
        
        appState.gastos.push(gastoData);

        // Simulação de resposta
        showToast('Gasto salvo com sucesso!', 'success');
        event.target.reset();
        
    } catch (error) {
        handleError('Erro ao salvar gasto', error);
    }
}

async function salvarGastoComDocumento() {
    try {
        const fileInput = document.getElementById('documentoUpload');
        
        // 1. Faz upload do documento e obtém o ID
        const documentoResponse = await uploadDocumento(appState.viagemId, fileInput);
        
        if (!documentoResponse) {
            throw new Error('Erro ao fazer upload do documento');
        }
        console.log('ID do documento salvo:', documentoResponse);
        return documentoResponse;
       
        
    } catch (error) {
        showToast(`Erro: ${error.message}`, 'error');
        console.error('Erro completo:', error);
    }
}

async function atualizarTabelaGastos(frmdata, idGasto, uploadDocumento) {
    // Atualiza a tabela de gastos
    const tabelaGastos = document.getElementById('tabelaGastos');
    const novaLinha = tabelaGastos.insertRow();
    if (tabelaGastos.querySelector('tr td[colspan="5"]')) {
        tabelaGastos.innerHTML = '';
    };
    
    const vlrGasto = frmdata.get('valorGasto');
    novaLinha.innerHTML = `
        <td>${idGasto}</td>
        <td>${await formatarData(frmdata.get('dataHoraGasto'))}</td>
        <td>${frmdata.get('tipoGasto')}</td>
        <td>R$ ${Number(vlrGasto).toFixed(2)}</td>
        <td>
            <button class="btn btn-sm btn-primary btn-action visualizar-gasto" title="Visualizar">
                <i class="bi bi-eye"></i>
            </button>
            <button class="btn btn-sm btn-warning btn-action editar-gasto" title="Editar">
                <i class="bi bi-pencil"></i>
            </button>
            <button class="btn btn-sm btn-danger btn-action excluir-gasto" title="Excluir">
                <i class="bi bi-trash"></i>
            </button>
            ${uploadDocumento ? `
            <button class="btn btn-sm btn-info btn-action ver-documento" title="Ver Documento">
                <i class="bi bi-file-earmark"></i>
            </button>
            ` : ''}
        </td>
    `;
    tabelaGastos.appendChild(novaLinha);

    // Adicionar event listeners aos botões
    novaLinha.querySelector('.visualizar-gasto').addEventListener('click', () => visualizarGasto(idGasto));
    novaLinha.querySelector('.editar-gasto').addEventListener('click', () => editarGasto(idGasto));
    novaLinha.querySelector('.excluir-gasto').addEventListener('click', () => excluirGasto(idGasto));
    if (novaLinha.querySelector('.ver-documento')) {
        novaLinha.querySelector('.ver-documento').addEventListener('click', () => verDocumento(uploadDocumento.documentoId));
    }

}
// Elementos do DOM - garantindo que existam
function getElementOrThrow(id) {
    const element = document.getElementById(id);
    if (!element) {
        throw new Error(`Elemento com ID '${id}' não encontrado`);
    }
    return element;
}

async function verDocumento(documentoID) {
    try {
        if (debug) console.log(`Solicitando documento ID: ${documentoID}`);
        
        // Obter referências aos elementos com tratamento de erro
        const documentoModal = new bootstrap.Modal(getElementOrThrow('documentoModal'));
        const documentoViewer = getElementOrThrow('documentoViewer');
        const imagemViewer = getElementOrThrow('imagemViewer');
        const downloadDocumento = getElementOrThrow('downloadDocumento');
        const modalTitle = getElementOrThrow('documentoModalLabel');

        // Mostrar modal imediatamente com spinner
        documentoViewer.style.display = 'none';
        imagemViewer.style.display = 'none';
        modalTitle.textContent = 'Carregando documento...';
        documentoModal.show();

        // 1. Obter informações do documento
        const response = await fetch(`/api/documentos/info/${documentoID}`);
        if (!response.ok) {
            throw new Error(await response.text() || 'Documento não encontrado');
        }
        
        const documentoInfo = await response.json();
        const documentoUrl = `/api/documentos/${documentoID}`;
        const extensao = documentoInfo.arquivo.split('.').pop().toLowerCase();
        
        // 2. Configurar visualizador conforme o tipo
        modalTitle.textContent = `Documento #${documentoID}`;
        
        if (extensao === 'pdf') {
            documentoViewer.src = documentoUrl;
            documentoViewer.style.display = 'block';
            imagemViewer.style.display = 'none';
        } else if (['jpg', 'jpeg', 'png'].includes(extensao)) {
            imagemViewer.src = documentoUrl;
            imagemViewer.style.display = 'block';
            documentoViewer.style.display = 'none';
        } else {
            throw new Error('Tipo de arquivo não suportado para visualização');
        }
        
        // 3. Configurar download
        downloadDocumento.href = documentoUrl;
        downloadDocumento.download = `documento_${documentoID}.${extensao}`;
        
    } catch (error) {
        console.error('Erro ao visualizar documento:', error);
        
        // Mostrar mensagem de erro no modal
        const modalBody = document.querySelector('#documentoModal .modal-body');
        modalBody.innerHTML = `
            <div class="alert alert-danger">
                Não foi possível carregar o documento:<br>
                ${error.message}
            </div>
        `;
        
        // Garantir que o modal ainda seja mostrado mesmo com erro
        if (documentoModal) documentoModal.show();
    }
}

// Atualizar totalizar tabela de gasto.
async function atulizarTotalGasto(){
    // Atualiza o total de gastos
    const totalGastos = document.getElementById('totalGastos');
    const totalGastosEstorno = document.getElementById('totalGastosEstorno');
    const valorTotalRespose = await calcularTotalGastos();
    const valorTotal= await valorTotalRespose.total;
    const valorTotalEstorno = await valorTotalRespose.estorno;
    totalGastos.textContent = `Total: R$ ${valorTotal.toFixed(2)}`;
    totalGastosEstorno.textContent = `Total: R$ ${valorTotalEstorno.toFixed(2)}`;
    // const dataTotal = await valorTotal.json();

}

/**Salvar Documento */
async function uploadDocumento(viagemId, fileInput) {
    try {
        // Verifica se há arquivo selecionado
        if (!fileInput.files || fileInput.files.length === 0) {
            throw new Error('Nenhum arquivo selecionado');
        }

        const arquivo = fileInput.files[0];
        
        // Valida o tipo do arquivo (opcional)
        const tiposPermitidos = ['application/pdf', 'image/jpeg', 'image/png', 'image/jpg'];
        if (!tiposPermitidos.includes(arquivo.type)) {
            throw new Error('Tipo de arquivo não permitido. Use PDF, JPEG ou PNG');
        }

        // Cria FormData para envio
        const formData = new FormData();
        formData.append('arquivo', arquivo);
        formData.append('viagemId', viagemId);
        formData.append('tipoDocumento', document.getElementById('tipoDocumento').value);

        // Envia para o backend
        const response = await fetch('/api/upload', {
            method: 'POST',
            body: formData
            // Não definir Content-Type - o browser faz automaticamente
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.message || 'Erro no upload');
        }

        const data = await response.json();
        return data; // Retorna o ID do documento salvo e caminho

    } catch (error) {
        console.error('Erro no upload:', error);
        throw error; // Propaga o erro para ser tratado pelo chamador
    }
}



// Formatar Data 
async function formatarData(dataISO) {
    try {
        const data = new Date(dataISO);
        
        if (isNaN(data.getTime())) {
            throw new Error('Data inválida');
        }
        
        const formato = new Intl.DateTimeFormat('pt-BR', {
            day: '2-digit',
            month: '2-digit',
            year: 'numeric',
            hour: '2-digit',
            minute: '2-digit',
            hour12: false
        });
        
        return formato.format(data).replace(',', '');
    } catch (error) {
        console.error('Erro ao formatar data:', error);
        return 'Data inválida';
    }
}

async function calcularTotalGastos() {
    try {
        const response = await fetch(`/api/gastos/total/${appState.viagemId}`, {
            method: 'GET',  // Alterado para GET
            headers: {
                'Accept': 'application/json'
            }
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(`Erro: ${errorData.message}`);
        }

        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Erro ao calcular total:', error);
        throw error;
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