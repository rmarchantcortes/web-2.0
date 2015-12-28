$(document).ready(function(){
    $('.slider').slider({full_width: true});
    $('.collapsible').collapsible();
    $('.modal-trigger').leanModal();
    
    $('#see-questions').click(function(){
        $('#form-question').hide();
        $('#questions').show()
    });
    $('#make-question').click(function(){
        $('#form-question').show();
        $('#questions').hide()
    });
    $('button[name=question]').click(function(e){
        e.preventDefault();
        if($('textarea[name=question]').val() != "" ){
            $.ajax({
                url: BASE_URL+'/pets/'+$('#name').attr('pet_id')+'/questions/',
                type: 'POST',
                data: $('form[name=question]').serialize(),
                success: function(data, textStatus, jqXHR){
                    if(jqXHR.status == 201){
                        $('#questions').prepend(formatQuestion(data.data[0]));
                        $('#form-question').hide();
                        Materialize.toast('La consulta ha sido enviada', 4000);
                    }
                }
            });
        }
    }); 
    $('button[name=respond]').click(function(e){
        e.preventDefault();
        if($($(this).parent().parent().parent().attr('id')+' textarea').val() != ""){
            $.ajax({
                url: BASE_URL+'/pets/'+$('#name').attr('pet_id')+'/questions/'+$(this).parent().parent().parent().attr('id')+'/',
                type: 'PUT',
                data: $('#'+$(this).parent().parent().parent().attr('id')+' form').serialize(),
                success: function(data, textStatus, jqXHR){
                    if(jqXHR.status == 200){
                        $('#'+$(this).parent().parent().parent().attr('id')+' textarea').html(data.data[0].que_answer);
                        Materialize.toast('Respuesta enviada', 4000);
                    }
                }
            });
        }        
    });
        
    $('#send-message').click(function(){
        if($('textarea[name=message]').val() != ""){
            $.ajax({
                url: BASE_URL+'/users/me/messages/',
                type: 'POST',
                data: $('form[name=message]').serialize(),
                success: function(data, textStatus, jqXHR){
                    if(jqXHR.status == 201){
                        $('#message-modal').closeModal();
                        Materialize.toast('Su mensaje ha sido enviado', 4000);
                    }
                }
            })
        }
    });
    
    var formatQuestion = function(value){
        return "<li id='"+value.que_id+"'><div class='collapsible-header'>"+value.que_question+"<a><i class='material-icons right reply'>expand_more</i></a><div><div class='collapsible-body'><p></p></div></li>";
         
     }
            
});