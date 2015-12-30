$(document).ready(function(){
    $('.modal-trigger').leanModal();
    $('#add').click(function(){
        $.ajax({
            url: BASE_URL + '/pets/types/',
            type: 'POST',
            data: { specie: $('input[name=specie-name]').val()
                  },
            success: function(data, textStatus, jqXHR){
                if (jqXHR.status == 201){
                    var item = "<li class='collection-item' id='"+data.data[0].pty_id+"'>"+data.data[0].pty_detail+"</li>";
                    $('.collection').append(item);
                    $('#new-specie-modal').closeModal();
                }
            }
        });
    });
    
});