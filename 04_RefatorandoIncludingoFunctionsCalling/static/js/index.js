let chat = document.querySelector('#chat');
let input = document.querySelector('#input');
let botaoEnviar = document.querySelector('#botao-enviar');
let imagemSelecionada;
let botaoAnexo = document.querySelector('#mais_arquivo')
let miniaturaImagem;

async function pegarImagem() {
    let fileInput = document.createElement('input');
    fileInput.type = 'file';
    fileInput.accept = 'image/*';

    fileInput.onchange = async e => {
        if (miniaturaImagem) {
            miniaturaImagem.remove(); // apago a miniatura que está do lado do botão de +
        }
        imagemSelecionada = e.target.files[0]; // pego o arquivo que foi selecionado pelo usuário

        // crio o elemento do lado do botão de + que vai mostrar a miniatura da imagem
        miniaturaImagem = document.createElement('img');
        miniaturaImagem.src = URL.createObjectURL(imagemSelecionada);
        miniaturaImagem.style.maxWidth = '3rem';
        miniaturaImagem.style.maxHeight = '3rem';
        miniaturaImagem.style.margin = '0.5rem';
    
        // insiro a miniatura antes do container (onde o usuário digita)
        document.querySelector('.entrada__container').insertBefore(miniaturaImagem, input);
    
        // crio o form data e anexo a imagem nele
        let formData = new FormData();
        formData.append('imagem', imagemSelecionada);

        // faço um POST pro backend (python) da imagem pra rota /image_upload
        const response = await fetch('http://127.0.0.1:5000/image_upload', {
            method: 'POST',
            body: formData
        });

        // pego a resposta e printo no terminal
        const resposta = await response.text();
        console.log(resposta);
        console.log(imagemSelecionada);
    };

    fileInput.click(); // dou um click no fileInput pra garantir que ele feche
}

async function enviarMensagem() {
    if (input.value === "" || input.value == null) return;
    let mensagem = input.value;
    input.value = "";

    if (miniaturaImagem) {
        miniaturaImagem.remove();
    }

    let novaBolha = criaBolhaUsuario();
    novaBolha.innerHTML = mensagem;
    chat.appendChild(novaBolha);

    let novaBolhaBot = criaBolhaBot();
    chat.appendChild(novaBolhaBot);
    vaiParaFinalDoChat();
    novaBolhaBot.innerHTML = "Analisando ..."

    // Envia requisição com a mensagem para a API do ChatBot
    const resposta = await fetch("http://127.0.0.1:5000/chat", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({'msg': mensagem}),
    });
    const textoDaResposta = await resposta.text();
    console.log(textoDaResposta);
    novaBolhaBot.innerHTML = textoDaResposta.replace(/\n/g, '<br>');
    vaiParaFinalDoChat();
}

function criaBolhaUsuario() {
    let bolha = document.createElement('p');
    bolha.classList = 'chat__bolha chat__bolha--usuario';
    return bolha;
}

function criaBolhaBot() {
    let bolha = document.createElement('p');
    bolha.classList = 'chat__bolha chat__bolha--bot';
    return bolha;
}

function vaiParaFinalDoChat() {
    chat.scrollTop = chat.scrollHeight;
}

botaoEnviar.addEventListener('click', enviarMensagem);
botaoAnexo.addEventListener('click', pegarImagem)
input.addEventListener("keyup", function (event) {
    event.preventDefault();
    if (event.keyCode === 13) {
        botaoEnviar.click();
    }
});

