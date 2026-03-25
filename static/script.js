const modal = document.getElementById('modal-cadastro')
const btnCadastro = document.getElementById('btn-cadastro')
const btnFechar = document.getElementById('btn-fechar')
const btnSalvar = document.getElementById('btn-salvar')
const nome = document.getElementById('input-nome')
const classe = document.getElementById('select-classe')
const embalagem = document.getElementById('select-embalagem')

btnCadastro.addEventListener('click', function() {
    modal.style.display = 'flex'
})

btnFechar.addEventListener('click', function(){
    modal.style.display = 'none'
})

btnSalvar.addEventListener('click', function(){
    if(nome.value == '' || classe.value == '' || embalagem.value == '' ){
        console.log('Preencha os todos os campo')
    } else {
        fetch('/cadastrar-produto', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        nome: nome.value,
        classe: classe.value,
        embalagem: embalagem.value
    })
}).then(function(){
    modal.style.display = 'none'
    alert('Produto cadastrado com sucesso!')
    nome.value = ''
    classe.value = ''
    embalagem.value = ''
})
    }
})

const modalNovaContagem = document.getElementById('modal-nova-contagem')
const btnNovaContagem = document.getElementById('btn-nova-contagem')
const btnFecharNovaContagem = document.getElementById('btn-fechar-nova-contagem')
const btnIniciarContagem = document.getElementById('btn-iniciar-contagem')
const inputNomeContagem = document.getElementById('input-nome-contagem')

btnNovaContagem.addEventListener('click', function() {
    modalNovaContagem.style.display = 'flex'
})

btnFecharNovaContagem.addEventListener('click', function() {
    modalNovaContagem.style.display = 'none'
})

btnIniciarContagem.addEventListener('click', function() {
    if(inputNomeContagem.value == '') {
        alert('Digite um nome para a contagem!')
    } else {
        fetch('/nova-contagem', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                nome: inputNomeContagem.value
            })
        }).then(function(response) {
            return response.json()
        }).then(function(data) {
            window.location.href = '/contagem/' + data.contagem_id
        })
    }
})