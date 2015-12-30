$(document).ready(function(){
    $.ajax({
        url: BASE_URL+'/pets/types/', 
        type: 'GET',
        headers: {          
            Accept : "application/json"
        },
        success: function(data, textStatus, jqXHR){
            if (jqXHR.status == 200){
                $.each(data.data, function(index, value){
                    var option = "<option value='"+value.pty_id+"'>"+value.pty_detail+"</option>";
                    $('select[name=type]').append(option);
                });
                $('select').material_select();
            }
        }
    });
    $('#new-pet').click(function(e){
        e.preventDefault();
        $.ajax({
            url: BASE_URL+'/pets/',
            type: 'POST',
            data: $('form').serialize(),
            success: function(data, textStatus, jqXHR){
                if (jqXHR.status == 201){
                    window.location.href = BASE_URL+'/pets/'+data.data.pet_id+'/edit/';
                }
            }
        });
    });
});