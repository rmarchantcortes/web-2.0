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
                    if ($('select[name=type]').attr('selection') == value.pty_id) var option = "<option value='"+value.pty_id+"' selected>"+value.pty_detail+"</option>";
                    else var option = "<option value='"+value.pty_id+"'>"+value.pty_detail+"</option>";
                    $('select[name=type]').append(option);
                });
                $('select').material_select();
            }
        }
    });
    
    $.get(BASE_URL+'/pets/'+$('#data').attr('pet_id')+'/images/', function(data, textStatus, jqXHR){
        $.each(data.data, function(key, value){
            appendImage(value);
        });
    });
    
    $('#publish-pet').click(function(e){
        e.preventDefault();
        $.ajax({
            url: BASE_URL+'/pets/'+$('#data').attr('pet_id')+'/',
            type: 'PUT',
            data: $('form[name=pet-details]').serialize(),
            success: function(data, textStatus, jqXHR){
                if (jqXHR.status == 200){
                    //window.location.href = BASE_URL+'/pets/'+data.data.pet_id+'/edit/';
                    Materialize.toast('La mascota ha sido actualizada', 4000);
                }
            }
        });
    });
    
    $('input[type=file]').change(function(){
        var data = new FormData($('form[name=pet-image]')[0]);
        $.each($('input[name=file]')[0].files, function(i, file) {
            data.append(i, file);
        });
        $.ajax({
            url: BASE_URL+'/pets/'+$('#data').attr('pet_id')+'/images/',
            data: data,
            cache: false,
            contentType: false,
            processData: false,
            type: 'POST',
            success: function(data, textStatus, jqXHR){
                if (jqXHR.status == 201){
                    appendImage(data.data[0])
                    Materialize.toast('La imagen ha sido agregada', 4000);
                }                
            }
        });
    });
    
    var appendImage = function(value){
        var image = "<div id='"+value.pim_id+"' class='image-item' style='background-image: url(\""+BASE_URL+"/static/images/"+value.pim_url+"\")'></div>";
        $('.image-container').append(image);
    }
});