$('#saveTour').click(function(){
    var data = new FormData()                            //поміщяємо всі змінні які хочемо відправити
    data.append('images', document.getElementById('images').files[0])
    data.append('name', $('#tourName').val())
    data.append('city', $('#tourCity').val())
    data.append('days', $('#tourDays').val())
    data.append('price', $('#tourPrice').val())
    data.append('date', $('#tourDate').val())
    $.ajax('/create-tour',{
        'type': 'POST',
        'async': true,
        'dataType': 'json',
        'data': data,
        'processData': false,
        'contentType': false,
        'success': function(response){
            document.getElementById(`tours`).innerHTML +=
                `
                <div class="card-body">
                    <div class="card-title">
                    </div>
                    <div class="card-text" id="tourCard${response.id}">
                        <ul id="tour${response.id}">
                            <h5>${$('#tourName').val()}</h5>
                            <li>${$('#tourCity').val()}</li>
                            <li>${$('#tourDays').val()}</li>
                            <li>${$('#tourPrice').val()}</li>
                            <li>${$('#tourDate').val()}</li>
                        </ul>
                    </div>
                </div>
                `;
            $('#tourName').val('');
            $('#tourCity').val('');
            $('#tourDays').val('');
            $('#tourPrice').val('');
            $('#tourDate').val('');
        }
    });
});

