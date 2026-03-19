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