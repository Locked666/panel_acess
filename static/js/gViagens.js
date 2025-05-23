let usersDiaria = [];



const filtroUsuarios = document.getElementById("filterUsuario");
const filtroUsuariosModal = document.getElementById("modal-usuario");

const filtroDataInicio = document.getElementById("data_inicio");
const filtroDataFim = document.getElementById("data_fim");
const filtroEntidade = document.getElementById("entidade");
const filtroIdViagem= document.getElementById("id_viagem");
const filtroRelatorio = document.getElementById("relatorio");

const buttonFiltrar = document.getElementById("btn-filtrar");
const buttonLimpar = document.getElementById("btn-limpar");


async function getUsers() {
    const response = await fetch("/api/auth/consultaUsuarios");
    const data = await response.json();
    return data;
}

async function setUserDiaria() {
    const users = await getUsers();

    users.forEach(user => {
        if (user.diaria) {
            const option = document.createElement("option");
            option.value = user.id;
            option.textContent = user.usuario;
            usersDiaria.push(user);
            filtroUsuarios.appendChild(option);
            filtroUsuariosModal.appendChild(option.cloneNode(true));

        }
    });
}




async function autoPreencherData() {
    // adicionar data inicio o primeiro dia do mes
    const hoje = new Date();
    const dia = String(hoje.getDate()).padStart(2, '0');
    const mes = String(hoje.getMonth() + 1).padStart(2, '0'); // Janeiro é 0!
    const ano = hoje.getFullYear();

    const primeiroDia = new Date(hoje.getFullYear(), hoje.getMonth(), 1);
    const diaInicio = String(primeiroDia.getDate()).padStart(2, '0');
    const mesInicio = String(primeiroDia.getMonth() + 1).padStart(2, '0'); // Janeiro é 0!
    const anoInicio = primeiroDia.getFullYear();
    const dataInicioAtual = `${anoInicio}-${mesInicio}-${diaInicio}`;
    filtroDataInicio.value = dataInicioAtual;
    
    //adicionar ultimo dia do mes data fim 

    const ultimoDia = new Date(hoje.getFullYear(), hoje.getMonth() + 1, 0);
    const diaFim = String(ultimoDia.getDate()).padStart(2, '0');
    const dataFimAtual = `${ano}-${mes}-${diaFim}`;
    filtroDataFim.value = dataFimAtual;
}

async function filtrarDados(dataInicio = '', dataFim = '', entidade = '', idViagem = '', usuario = '', relatorio = '', tipo_viagem = '') {
    const url = "/api/viagens/consultaViagens";

    const payload = {};

    if (dataInicio && dataInicio !== '0') payload.data_inicio = dataInicio
    if (dataFim && dataFim !== '0') payload.data_fim = dataFim
    if (entidade && entidade !== '0') payload.entidade = entidade;
    if (idViagem && idViagem !== '0') payload.id = idViagem;
    if (usuario && usuario !== '0') payload.usuario = usuario;
    if (relatorio && relatorio !== '0') payload.n_intranet = relatorio;
    if (tipo_viagem) payload.tipo_viagem = tipo_viagem;
    // if (relatorio === true) payload.relatorio = relatorio;

    console.log("Payload:", payload);
    const response = await fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: Object.keys(payload).length ? JSON.stringify(payload) : null
    });
    
    const data = await response.json();

    if (response.ok) {
        console.log("Dados filtrados:", data);
        const data_table = data.map(item => ({
            id: item.id,
            usuario: item.usuario_nome,
            entidade: item.entidade,
            data_inicio: item.data_inicio,
            data_fim: item.data_fim,
            diarias: item.n_diarias,
            relatorio: item.n_intranet,
            valor: "R$ " + item.total_gasto.toFixed(2),
        }));
        preencherTabelaViagens(data_table);
    } else {
        console.error("Erro ao buscar dados:", data);
        if (data.message === "No data found") {
            exibirToast({
                tipo: "info",
                mensagem: "Nenhum dado encontrado para o Filtro selecionado.",
                position: 'top',
                tempo: 5000
            });
        }
        else if (data.message === "Invalid date format") {
            exibirToast({
                tipo: "danger",
                mensagem: "Formato de data inválido.",
                tempo: 5000
            });
        } else if (data.message === "Invalid user ID") {
            exibirToast({
                tipo: "danger",
                mensagem: "ID de usuário inválido.",
                tempo: 5000
            });
        } else if (data.message === "Invalid entity") {
            exibirToast({
                tipo: "danger",
                mensagem: "Entidade inválida.",
                tempo: 5000
            });
        }
        else{
            exibirToast({
                tipo: "danger",
                mensagem: "Ocorreu um erro ao buscar os dados." + data.message,
                tempo: 5000
            });

        }

    }
}

async function preencherTabelaViagens(dados) {
    const tabela = document.getElementById("tabela-viagens");
    tabela.innerHTML = ""; // Limpar tabela antes de preencher

    dados.forEach(dado => {
        const linha = document.createElement("tr");

        // Adicionar células à linha
        Object.values(dado).forEach(valor => {
            const celula = document.createElement("td");
            celula.textContent = valor;
            linha.appendChild(celula);
        });

        tabela.appendChild(linha);
    });
}

function exibirToast({ tipo = "info", mensagem = "Mensagem padrão",position = 'bottom' ,tempo = 4000 }) {
    const icones = {
        success: "check",
        info: "notifications",
        warning: "travel_explore",
        danger: "campaign"
    };

    const classes = {
        success: "bg-white text-success",
        info: "bg-gradient-info text-white",
        warning: "bg-white text-warning",
        danger: "bg-white text-danger"
    };

    const toastContainerId = "toast-container";
    let container = document.getElementById(toastContainerId);

    if (!container) {
        container = document.createElement("div");
        container.id = toastContainerId;
        container.className = `position-fixed ${position}-1 end-1 z-index-2`;
        document.body.appendChild(container);
    }

    const toast = document.createElement("div");
    toast.className = `toast fade show p-2 mt-2 ${classes[tipo] || "bg-white"}`;
    toast.setAttribute("role", "alert");
    toast.setAttribute("aria-live", "assertive");
    toast.setAttribute("aria-atomic", "true");

    toast.innerHTML = `
        <div class="toast-header ${tipo === 'info' ? 'bg-transparent' : 'border-0'}">
            <i class="material-icons me-2">${icones[tipo] || "notifications"}</i>
            <span class="me-auto font-weight-bold ${tipo === 'danger' ? 'text-danger' : ''}">Sistema</span>
            <small class="${tipo === 'info' ? 'text-white' : 'text-body'}">agora</small>
            <i class="fas fa-times text-md ms-3 cursor-pointer ${tipo === 'info' ? 'text-white' : ''}" data-bs-dismiss="toast" aria-label="Close"></i>
        </div>
        <hr class="horizontal ${tipo === 'info' ? 'light' : 'dark'} m-0">
        <div class="toast-body ${tipo === 'info' ? 'text-white' : ''}">
            ${mensagem}
        </div>
    `;

    container.appendChild(toast);

    const bsToast = new bootstrap.Toast(toast);
    bsToast.show();

    setTimeout(() => {
        bsToast.hide();
        toast.addEventListener('hidden.bs.toast', () => toast.remove());
    }, tempo);
}


async function setEventoButtons() {
    buttonFiltrar.addEventListener("click", async () => {
        const dataInicio = filtroDataInicio.value;
        const dataFim = filtroDataFim.value;
        const entidade = filtroEntidade.value;
        const idViagem = filtroIdViagem.value;
        const usuario = filtroUsuarios.value;
        const relatorio = filtroRelatorio.value;

        await filtrarDados(dataInicio, dataFim, entidade, idViagem, usuario,relatorio);

    });
    buttonLimpar.addEventListener("click", () => {
        // filtroDataInicio.value = "";
        // filtroDataFim.value = "";
        filtroEntidade.value = "";
        filtroIdViagem.value = "";
        filtroUsuarios.value = "";
        filtroRelatorio.value = "";
    });

}






async function init() {
    await autoPreencherData();
    await setUserDiaria();
    await setEventoButtons();
    await filtrarDados(filtroDataInicio.value,filtroDataFim.value);
    
}

init();