$(document).ready(function(){
    $('.modal-trigger').leanModal();
    $('#cancel').click(function(){
        $.ajax({
            url: BASE_URL+'/pets/'+$('#name').attr('pet_id')+'/adopt/',
            type: 'DELETE',
            success: function(data, textStatus, jqXHR){
                if (jqXHR.status == 200){
                    window.location.href = BASE_URL + '/';
                }
            }
        });
    });
    $('#finish').click(function(){
        $.ajax({
            url: BASE_URL+'/pets/'+$('#name').attr('pet_id')+'/adopt/',
            type: 'PUT',
            success: function(data, textStatus, jqXHR){
                if (jqXHR.status == 200){
                    window.location.href = BASE_URL + '/users/me/pets/';
                }
            }
        });
    });
});