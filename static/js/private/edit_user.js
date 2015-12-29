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
    $('#btn_edit_user').click(function(e){
        e.preventDefault();
        var shaObjac = new jsSHA("SHA-512", "TEXT");
        shaObjac.update($('input[name=last_passwd]').val());
        var hashac = shaObjac.getHash("HEX");

        var shaObjnew = new jsSHA("SHA-512", "TEXT");
        shaObjnew.update($('input[name=new_passwd]').val());
        var hashnew = shaObjnew.getHash("HEX");

        var shaObjrenew = new jsSHA("SHA-512", "TEXT");
        shaObjrenew.update($('input[name=re_new_passwd]').val());
        var hashrenew = shaObjrenew.getHash("HEX");
        console.log("asi");
        $.ajax({
            url: BASE_URL+'/users/me/profile',
            type: 'PUT',
            data: {
                name: $('input[name=name]').val(),
                email: $('input[name=email]').val(),
                u_country: $('select[name=u_country]').val(),
                u_state: $('select[name=u_state]').val(),
                phone: $('input[name=phone]').val(),
                last_passwd: hashac,
                new_passwd: hashnew,
                re_new_passwd: hashrenew
            },
            success: function(data){
                if (jqXHR.status == 200){
                    //window.location.href = BASE_URL+'/pets/'+data.data.pet_id+'/edit/';
                    Materialize.toast('El usuario ha sido actualizada', 4000);
                }
            }
        })
    });
});


