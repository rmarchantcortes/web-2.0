$(document).ready(function() {
    $('select').material_select();
    $.get(BASE_URL+'/countries/', function(data){
        $.each(data.data, function(index, value){
            var option = "<option value='"+value.cou_id+"'>"+value.cou_name+"</option>";
            $('select[name=country]').append(option);
            $('select').material_select();
        })
    });
    $('select[name=country]').on('change', function(){
        console.log("dasd");
        $.get(BASE_URL+'/countries/'+$('select[name=country]').val()+'/states/', function(data){
            $.each(data.data, function(index, value){
                var option = "<option value='"+value.sta_id+"'>"+value.sta_name+"</option>";
                $('select[name=state]').append(option);
                $('select').material_select();
            })
        })
    });
    $('#new-user').click(function(e){
        e.preventDefault();
        var shaObj = new jsSHA("SHA-512", "TEXT");
        shaObj.update($('input[name=password]').val());
        var hash = shaObj.getHash("HEX");
        $.ajax({
            url: BASE_URL+'/users/',
            type: 'POST',
            data:{
                name: $('input[name=name]').val(),
                phone: $('input[name=phone]').val(),
                state: $('select[name=state]').val(),
                address: $('input[name=address]').val(),
                email: $('input[name=email]').val(),
                password: hash
            },
            success: function(data){
                console.log(data)
            }
        });
    });
});