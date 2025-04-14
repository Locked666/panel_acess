// Seleciona o botão de "Adicionar Viagem" e o modal
const addTripButton = document.getElementById('bnt-add-viagem');
const tripModal = document.getElementById('addViagemModal');
const closeModalButton = document.getElementById('closeModalButton');

// Função para abrir o modal
function openModal() {
    tripModal.style.display = 'block';
}

// Função para fechar o modal
function closeModal() {
    tripModal.style.display = 'none';
}

// Adiciona o evento de clique ao botão "Adicionar Viagem"
addTripButton.addEventListener('click', openModal);

// Adiciona o evento de clique ao botão de fechar o modal
closeModalButton.addEventListener('click', closeModal);

// Fecha o modal ao clicar fora dele
window.addEventListener('click', (event) => {
    if (event.target === tripModal) {
        closeModal();
    }
});