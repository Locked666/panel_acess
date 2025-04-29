// Seleciona o botão de "Adicionar Viagem" e o modal
const addTripButton = document.getElementById('bnt-add-viagem');
const tripModal = document.getElementById('addViagemModal');
const closeModalButton = document.getElementById('closeModalButton');

// Adiciona um evento de clique ao botão de "Adicionar Viagem"
addTripButton.addEventListener('click', () => {
    const href = addTripButton.getAttribute('href');
    if (href) {
        window.location.href = href;
    }
});

// Limpar filtros
document.getElementById('btn-limpar-filtros').addEventListener('click', function() {
    document.getElementById('filtro-data-inicial').value = '';
    document.getElementById('filtro-data-final').value = '';
    document.getElementById('filtro-entidade').value = '';
    document.getElementById('filtro-relatorio').value = '';
});

// // Imprimir relatório
// document.getElementById('btn-imprimir').addEventListener('click', function() {
//     window.print(); // Ou implementar lógica específica de impressão
// });

// Inicialização do Accordion
document.addEventListener('DOMContentLoaded', function() {
    // Mantém o estado do accordion no localStorage
    const accordion = document.getElementById('filtrosAccordion');
    
    // Restaura estado salvo
    const savedState = localStorage.getItem('accordionState');
    if (savedState) {
        const activeItem = accordion.querySelector(savedState);
        if (activeItem) {
            const bsCollapse = new bootstrap.Collapse(activeItem, { toggle: true });
        }
    }

    // Salva estado quando muda
    accordion.addEventListener('shown.bs.collapse', function(event) {
        localStorage.setItem('accordionState', `#${event.target.id}`);
    });
});

// Limpar filtros
document.getElementById('btn-limpar-filtros').addEventListener('click', function() {
    document.querySelectorAll('#filtrosAccordion input, #filtrosAccordion select').forEach(el => {
        el.value = '';
    });
});

async function abrirRelatorioPDF(event) {
    event.preventDefault(); // Impede o link de recarregar a página

    const urlAtual = new URL(window.location.href);
    urlAtual.searchParams.set("imprimir", "true");

    window.open(urlAtual.toString(), "_blank");
}
//adicionar o evento de visualizar o modal o modal



document.addEventListener('DOMContentLoaded', function () {
    const botoesVisualizar = document.querySelectorAll('.visualizar-viagem');

    botoesVisualizar.forEach(function (botao) {
        botao.addEventListener('click', async function () {
            const viagemId = this.value;

            try {
                // Consulta a API com o ID da viagem
                const response = await fetch(`/api/viagens/consulta?viagemId=${viagemId}`);
                
                if (!response.ok) {
                    throw new Error("Erro ao buscar os dados da viagem.");
                }

                const dados = await response.json();

                // Preenche os campos do modal
                document.getElementById('detalhe-tecnico').innerText =  dados.tecnico  || '---';
                document.getElementById('detalhe-entidade').innerText = dados.entidade || '---';
                document.getElementById('detalhe-data-inicial').innerText = dados.data_inicio || '---';
                document.getElementById('detalhe-data-final').innerText = dados.data_fim || '---';
                document.getElementById('detalhe-tipo-viagem').innerText = dados.tipo_viagem || '---';
                document.getElementById('detalhe-total-gasto').innerText = 'R$' +' '+ dados.total_gasto || '---';
                document.getElementById('detalhe-descricao').innerText = dados.descricao || '---';

                // Abre o modal com Bootstrap
                const modal = new bootstrap.Modal(document.getElementById('modalVisualizarViagem'));
                modal.show();

            } catch (error) {
                console.error("Erro ao carregar dados da viagem:", error);
                alert("Não foi possível carregar os detalhes da viagem.");
            }
        });
    });
});


// Adicionar evento para editiar viagem
document.addEventListener('DOMContentLoaded', function () {
    // Seleciona todos os botões com a classe .editar-viagem
    const botoesEditar = document.querySelectorAll('.editar-viagem');

    // Adiciona o evento de clique em cada botão
    botoesEditar.forEach(function (botao) {
        botao.addEventListener('click', function () {
            const viagemId = this.value;
            // Redireciona para a rota com o parâmetro
            window.location.href = `/adicionar_viagem?viagemId=${viagemId}`;
        });
    });
});
