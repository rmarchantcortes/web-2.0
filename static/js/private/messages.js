$(document).ready(function(){    
    $('.collection-item').click(function(){
        $('.collection-item').removeClass('active');
        $(this).addClass('active');
        $.get(BASE_URL+'/users/me/messages/user/'+this.id+'/', function(data, textStatus, jqXHR){
            if(jqXHR.status == 200){
                $('.box-message').empty();
                $.each(data.data, function(key, value){
                    if(value.mes_user_from == $('.box-message').attr('user')) align = "right-align";
                    else align = "left-align"
                    var message = "<div id='"+value.mes_id+"' class='row'>";
                    message += "<div class='name col s12 "+align+"'>"+value.user2+"</div>";
                    message += "<div class='date col s12 "+align+"'>"+value.mes_date+"</div>";
                    message += "<div class='message col s12 "+align+"'>"+value.mes_message+"</div>";
                    message += "</div>"
                    $('.box-message').append(message);
                });
            }            
        });
    });
    $($('.collection-item')[0]).trigger('click');
})