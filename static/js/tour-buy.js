$('#saveBuy').click(function(){
    $.ajax('/buy-tour', {
        'type': 'POST',
        'async': true,
        'dataType': 'json',
        'data': {
            'user_id': $('#user_id').val(),
            'tour_id': $('#tour_id').val(),
            'start_at': $('#start_at').val(),
            'end_at': $('#end_at').val()
                },
        'success': function(response){
            $('#user_id').val('');
            $('#tour_id').val('');
            $('#start_at').val('');
            $('#end_at').val('');
        }
    });
});
