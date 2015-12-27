$(document).ready(function(){
    $('select').material_select();
    $.get(BASE_URL+'/countries/'+$('select[name=u_country]').val()+'/states/', function(data, textStatus, jqXHR){
        if(jqXHR.status == 200){
            $.each(data.data, function(key, value){
                var option = "<option value='"+value.sta_id+"'>"+value.sta_name+"</option>";
                $('select[name=u_state]').append(option);
            });
            $('select').material_select();
        }
    });
});