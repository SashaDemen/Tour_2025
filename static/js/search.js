$('#idSearch').click(function(){
    $.ajax('/search', {
        'type': 'POST',
        'async': true,
        'dataType': 'json',
        'data': {'search': $('#search').val()},
        'success':
        function(response){
            document.getElementById(`tours`).innerHTML = response.tours;
        }
    });
});