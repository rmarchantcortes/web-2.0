$(document).ready(function(){
    $('#login').click(function(e){
        e.preventDefault();
        var shaObj = new jsSHA("SHA-512", "TEXT");
        shaObj.update($('input[name=password]').val());
        var hash = shaObj.getHash("HEX");
        $.ajax({
            url: BASE_URL+'/users/login/',
            type: 'POST',
            data: {
                email: $('input[name=email]').val(),
                password: hash
            },
            success: function(data, textStatus, jqXHR){
                if (jqXHR.status == 200) location.reload();
            }
        })
    });
});