const tabButtons = document.querySelectorAll('.tab-button');
const tabContents = document.querySelectorAll('.tab-content');

tabButtons.forEach(button => {
    button.addEventListener('click', () => {
        const tabId = button.dataset.tab;

        tabButtons.forEach(btn => btn.classList.remove('active'));
        tabContents.forEach(content => content.classList.remove('active'));

        button.classList.add('active');
        document.getElementById(tabId).classList.add('active');
    });
});

// Baixar Imagens
document.getElementById('baixar_button').addEventListener('click', () => {
    const urlAnuncio = document.getElementById('url_anuncio').value;
    const pastaBaixar = document.getElementById('pasta_baixar').value;

    fetch('/baixar_imagens', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            url_anuncio: urlAnuncio,
            pasta_destino: pastaBaixar,
        }),
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('baixar_mensagem').textContent = data.mensagem;
    })
    .catch(error => {
        document.getElementById('baixar_mensagem').textContent = 'Erro ao baixar imagens.';
        console.error('Erro:', error);
    });
});

// Renomear Arquivos
document.getElementById('renomear_button').addEventListener('click', () => {
    const pastaRenomear = document.getElementById('pasta_renomear').value;

    fetch('/renomear_arquivos', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            pasta_imagens: pastaRenomear,
        }),
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('renomear_mensagem').textContent = data.mensagem;
    })
    .catch(error => {
        document.getElementById('renomear_mensagem').textContent = 'Erro ao renomear arquivos.';
        console.error('Erro:', error);
    });
});