const btnComparar = document.getElementById('btn-comparar')

btnComparar.addEventListener('click', function() {
    const checkboxes = document.querySelectorAll('input[type=checkbox]:checked')
    
    if(checkboxes.length !== 2) {
        alert('Selecione exatamente 2 contagens para comparar!')
        return
    }
    
    const id1 = checkboxes[0].value
    const id2 = checkboxes[1].value
    
    window.location.href = '/comparar/' + id1 + '/' + id2
})

document.querySelectorAll('.btn-excluir-contagem').forEach(function(btn) {
    btn.addEventListener('click', function() {
        const id = this.dataset.id
        
        if(confirm('Tem certeza que deseja excluir esta contagem?')) {
            fetch('/excluir-contagem', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ id: id })
            }).then(function() {
                window.location.reload()
            })
        }
    })
})