
// function toggleAtivo(entidadeId) {
//     fetch(`/toggle/${entidadeId}`, { method: 'POST' })
//         .then(response => response.json())
//         .then(data => {
//             if (data.status === 'success') {
//                 const card = document.getElementById('card-dinamico');
//                 document.getElementById('titulo-entidade').innerText = data.nome;
//                 document.getElementById('tipo-acesso').innerText = data.tipo_acesso;
//                 document.getElementById('nome-usuario').innerText = data.usuario;
//                 document.getElementById('horario-acesso').innerText = data.horario;

//                 card.style.display = 'block';
//                 location.reload();  // Recarrega para refletir o estado atualizado
//             }
//         })
//         .catch(error => console.error('Erro:', error));
// }


// function toggleAtivo(entidadeId, ativo) {
//     // Verifica se a entidade está ativa antes de pegar o valor do select
//     var selectElement = ativo ? document.getElementById(`tool-${entidadeId}`) : null;
//     var selectedTool = selectElement ? selectElement.value : null;

//     // Envia o ID da entidade e, se ativa, o valor do select para o backend via AJAX
//     $.ajax({
//         url: `/toggle/${entidadeId}`,
//         type: 'POST',
//         data: {
//             tool: selectedTool,  // Passa o valor apenas se ativo, caso contrário, será null
//             ativo: ativo
//         },
//         success: function(response) {
//             showToast('Status atualizado com sucesso:', response);
//         },
//         error: function(error) {
//             showToast('Erro ao atualizar o status:', error);
//         }
//     });
// }

function open_app(entidadeId) {
    fetch(`/open_app/${entidadeId}`, { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                showToast('Aplicativo aberto com sucesso!');
            }
        })
        .catch(error => console.error('Erro:', error));
}

function fecharCard() {
    document.getElementById('card-dinamico').style.display = 'none';
}

function fecharCard() {
    document.getElementById('card-dinamico').style.display = 'none';
}

// Filtro de tabela
function filterTable() {
    const filter = document.getElementById('search-filter').value.toLowerCase();
    const rows = document.querySelectorAll('#table-body tr');
    rows.forEach(row => {
        const text = row.textContent.toLowerCase();
        row.style.display = text.includes(filter) ? '' : 'none';
    });
}

// Autocomplete para o campo "entidade"
$(document).ready(function () {
    $("#entidade").autocomplete({
        source: function (request, response) {
            // Faz uma requisição para o backend Flask
            $.ajax({
                url: "/api/entidades",
                data: { q: request.term }, // O texto digitado pelo usuário
                success: function (data) {
                    // Formata os resultados para o autocomplete
                    response(data.map(item => ({
                        label: item.nome, // Nome exibido
                        value: item.nome, // Valor no campo
                        id: item.id      // ID para usar no formulário
                    })));
                },
                error: function () {
                    console.error("Erro ao buscar entidades.");
                }
            });
        },
        select: function (event, ui) {
            // Atualiza o campo oculto com o ID da entidade selecionada
            $("#entidade-id").val(ui.item.id);
        }
    });
});

// Submissão do formulário
document.getElementById("form-acesso").addEventListener("submit", async function (e) {
    e.preventDefault();

    const formData = new FormData(this);
    const data = Object.fromEntries(formData.entries());

    try {
        const response = await fetch("/cadastro_acesso", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (response.ok) {
            showToast(`Acesso adicionado com sucesso! ID: ${result.id}, Entidade: ${result.entidade}`);
        } else {
            showToast(`Erro: ${result.message}`, "error");
        }
    } catch (error) {
        showToast(`Erro: ${error.message}`, "error");
    }
});

// Exibir mensagens com toast
function showToast(message, type = "success") {
    const toast = document.getElementById("toast");
    const toastBody = toast.querySelector(".toast-body");

    // Ajusta a classe do toast conforme o tipo
    toast.classList.remove("text-bg-success", "text-bg-danger");
    toast.classList.add(type === "success" ? "text-bg-success" : "text-bg-danger");

    // Define a mensagem
    toastBody.textContent = message;

    // Exibe o toast
    const bsToast = new bootstrap.Toast(toast);
    bsToast.show();
}


