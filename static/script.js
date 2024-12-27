
function toggleAtivo(entidadeId) {
    fetch(`/toggle/${entidadeId}`, { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                const card = document.getElementById('card-dinamico');
                document.getElementById('titulo-entidade').innerText = data.nome;
                document.getElementById('tipo-acesso').innerText = data.tipo_acesso;
                document.getElementById('nome-usuario').innerText = data.usuario;
                document.getElementById('horario-acesso').innerText = data.horario;

                card.style.display = 'block';
                location.reload();  // Recarrega para refletir o estado atualizado
            }
        })
        .catch(error => console.error('Erro:', error));
}

function fecharCard() {
    document.getElementById('card-dinamico').style.display = 'none';
}



