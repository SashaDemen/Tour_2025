TOUR_HTML = '''
<div class="col">
    <div class="card mx-3 mt-3">
        <img src="{tour_images}" alt="Card image cap" class="card-img-top" style="width:430px;height:250px;">
        <div class="card-body">
         <div class="card-title">
            </div>
            <div class="card-text" id="tourCard{tour_id}">
                <ul id="tour{tour_id}">
                            <h5>{tour_name}</h5>
                            <li>{tour_city}</li>
                            <li>{tour_days}</li>
                            <li>{tour_price}$</li>
                            <li>{tour_date}</li>
                </ul>
       <button type="button" class="btn btn-outline-success" data-bs-target="#buyModal" data-bs-toggle="modal">
            Buy Tour
       </button>
            </div>
        </div>
    </div>
</div>
            '''