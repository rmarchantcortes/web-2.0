$(document).ready(function(){
    $('.modal-trigger').leanModal();
    var pet;
    $('.delete-btn').click(function(){
        pet = $(this).parent().parent().attr('id');
    })
    $('#delete-pet').click(function(){
        $.ajax({
            url: BASE_URL + '/pets/'+pet+'/',
            type: 'DELETE',
            success: function(data, textStatus, jqXHR){
                if(jqXHR.status == 200){
                    window.location.href = BASE_URL + '/users/me/pets/';
                }
            }
        })
    });
});