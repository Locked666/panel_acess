const tabelaUsuarios = document.getElementById("tabela-usuarios");

const filtroUsuariosNome = document.getElementById("filtroNome");
const filtroUsuariosCodigo = document.getElementById("filtroCodigo");
const filtroUsuariosEmail = document.getElementById("filtroEmail");
const filtroUsuariosTipo = document.getElementById("filtroTipo");
const filtroUsuariosStatus = document.getElementById("filtroStatus");
const filtroUsuariosSetor = document.getElementById("filtroSetor");

async function buscarUsuarios() {
    const url = "/api/auth/consultaUsuarios";
    const bodyPayLoad = {};
    if (filtroUsuariosNome.value) bodyPayLoad.nome = filtroUsuariosNome.value;
    if (filtroUsuariosCodigo.value) bodyPayLoad.codigo = filtroUsuariosCodigo.value;
    if (filtroUsuariosEmail.value) bodyPayLoad.email = filtroUsuariosEmail.value;
    // if (filtroUsuariosTipo.value) bodyPayLoad.tipo = filtroUsuariosTipo.value;
    // if (filtroUsuariosStatus.value) bodyPayLoad.status = filtroUsuariosStatus.value;
    // if (filtroUsuariosSetor.value) bodyPayLoad.setor = filtroUsuariosSetor.value;

    const response = await fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: Object.keys(bodyPayLoad).length ? JSON.stringify(payload) : null
    });
    const data = await response.json();
    if (response.ok) {
        console.log("Dados filtrados:", data);
        const data_table = data.map(item => ({
            id: item.id,
            nome: item.usuario,
            email: item.email,
            tipo: item.admin,
            status: item.ativo,
            setor: item.setor
        }));
        console.log("data_table", data_table);
        atualizarTabelaUsuarios(data_table);
    } else {
        console.error("Erro ao buscar dados:", data);
        if (data.message === "No data found") {
            exibirToast(
                {
                    title: "Erro ao buscar dados",
                    message: data.message,
                    type: "error"
                }
            )
        };
    }

}

async function atualizarTabelaUsuarios(data) {
    console.log("atualizarTabelaUsuarios", data);
    tabelaUsuarios.innerHTML = "";
    if (data.length === 0) {
        tabelaUsuarios.innerHTML = "<tr><td colspan='6'>Nenhum usuário encontrado</td></tr>";
        return;
    }
    data.forEach(item => {
        const row = document.createElement("tr");
        row.innerHTML = `
        <td>
            <div class="d-flex px-2 py-1">
                <div>
                    <img src="/static/assets/img/icon_user.svg" class="avatar avatar-sm me-3 border-radius-lg" alt="user1">
                </div>
                <div class="d-flex flex-column justify-content-center">
                    <h6 class="mb-0 text-sm">${item.nome}</h6>
                    <p class="text-xs text-secondary mb-0">${item.email}</p>
                </div>
            </div>
        </td>

        <td>
            <p class="text-xs font-weight-bold mb-0">${item.tipo ? 'Administrador' : 'Usuário'}</p>
            <p class="text-xs text-secondary mb-0">${item.setor}</p>
        </td>

        <td class="align-middle text-center text-sm">
            <span class="badge badge-sm bg-gradient-${item.status ? 'success' : 'secondary'}">${item.status ? 'Ativo' : 'Inativo'}</span>
        </td>
        <td class="align-middle text-center">
            <a href="javascript:;" class="text-secondary font-weight-bold text-xs" data-toggle="tooltip" data-original-title="Edit user">
            Edit
            </a>
        </td>

        `;
        tabelaUsuarios.appendChild(row);
    });
}

async function gravarUsuario() {
    const url = "/api/auth/criar";
    const bodyPayLoad = {
        usuario: document.getElementById("nomeUsuario").value,
        email: document.getElementById("emailUsuario").value,
        senha: document.getElementById("senhaUsuario").value,
        admin: document.getElementById("usuarioAdmin").value,
        ativo: document.getElementById("usuarioAtivo").value,
        setor: document.getElementById("setorUsuario").value,
        diaria: document.getElementById("usuarioDiaria").value,
    };

    console.log("bodyPayLoad", bodyPayLoad);
    const response = await fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(bodyPayLoad)
    });
    const data = await response.json();
    if (response.ok) {
        console.log("Dados gravados:", data);
        exibirToast({
            tipo: "success",
            mensagem: "Usuário gravado com sucesso!",
            position: 'top',
            tempo: 5000
        });
        buscarUsuarios();
    } else {
        console.error("Erro ao gravar dados:", data);
        exibirToast({
            tipo: "danger",
            mensagem: data.message || "Erro ao gravar usuário.",
            tempo: 5000,
            position: 'top'
        });
    }
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

async function atribuirEventosButtons() {
    const btnGravar = document.getElementById("bnt-salvar-modal");
    // const btnLimpar = document.getElementById("btn-limpar-esse");

    btnGravar.addEventListener("click", async () => {
        await gravarUsuario();
    });

    
}

async function init(){
    await buscarUsuarios();
    await atribuirEventosButtons();
    filtroUsuariosNome.addEventListener("change", buscarUsuarios);
    filtroUsuariosCodigo.addEventListener("change", buscarUsuarios);
    filtroUsuariosEmail.addEventListener("change", buscarUsuarios);
    // filtroUsuariosSetor.addEventListener("change", buscarUsuarios);
}
init();