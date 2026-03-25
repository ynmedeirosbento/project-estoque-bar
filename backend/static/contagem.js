const btnFinalizar = document.getElementById('btn-finalizar')
const modalResumo = document.getElementById('modal-resumo')
const tabelaResumo = document.getElementById('tabela-resumo')
const btnFecharResumo = document.getElementById('btn-fechar-resumo')

btnFinalizar.addEventListener('click', function() {
    tabelaResumo.querySelectorAll('tr:not(:first-child)').forEach(e => e.remove())
    
    let total = 0
    document.querySelectorAll('input[type=number]').forEach(function(input) {
        const linha = input.closest('tr')
        const produto = linha.querySelector('td').innerText
        const quantidade = parseInt(input.value)
        total += quantidade

        const novaLinha = tabelaResumo.insertRow()
        novaLinha.insertCell().innerText = produto
        novaLinha.insertCell().innerText = quantidade
    })

    document.getElementById('total-geral').innerText = total
    modalResumo.style.display = 'flex'
})

btnFecharResumo.addEventListener('click', function() {
    modalResumo.style.display = 'none'
})

document.querySelectorAll('input[type=number]').forEach(function(input) {
    input.addEventListener('change', function() {
        const itemId = this.dataset.id
        const quantidade = this.value

        fetch('/atualizar-quantidade', {
            method: 'POST',
            headers:{'Content-Type': 'application/json'},
            body: JSON.stringify({
                item_id: itemId,
                quantidade: quantidade

            })
        })
    })


})

document.querySelectorAll('.btn-excluir-item').forEach(function(btn) {
    btn.addEventListener('click', function() {
        const id = this.dataset.id
        
        if(confirm('Tem certeza que deseja excluir este item?')) {
            fetch('/excluir-item', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ id: id })
            }).then(function() {
                window.location.reload()
            })
        }
    })
})

const btnWhatsapp = document.getElementById('btn-whatsapp')

btnWhatsapp.addEventListener('click', function() {
    const nome = document.body.dataset.nome
    const data = document.body.dataset.data
    
    let mensagem = `Contagem - ${nome}\nData: ${data}\n\n`
    
    document.querySelectorAll('#tabela-resumo tr:not(:first-child)').forEach(function(linha) {
        const produto = linha.cells[0].innerText
        const quantidade = linha.cells[1].innerText
        mensagem += `${produto}: ${quantidade} un\n`
    })
    
    const url = `https://wa.me/?text=${encodeURIComponent(mensagem)}`
    window.open(url, '_blank')
})