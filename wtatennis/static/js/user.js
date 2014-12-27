$(function(){
    $("#register").click(function(){
        $.post("/account/signup", {"username": $("#username").val(), "password": $("#password").val(), "email": $("#email").val()}, function(data){
            if(data['status'] == 1){
                window.location.href = '/';
            }
            else{
                if(data['status'] == 0){
                    $('.alert-error').css('display', 'block');
                    $('.alert-error').html(data['message']);
                }
                else{
                    for(var i=0; i<3; i++){
                        if(data['message'][i]['status'] == -1){
                            $('.alert-error').css('display', 'block');
                            $('.alert-error').html(data['message'][i]['message']);
                            return;
                        }
                    }
                }
            }
        });
    });

    $("#login").click(function(){
        var remember = 'n';
        if($("#permanent").prop('checked')){
            remember = 'y';
        }
        $.post('/account/signin', {'email': $("#email").val(), 'password': $("#password").val(), 'remember': remember}, function(data){
            if(data['status'] == 1){
                window.location.href = '/';
            }
            else{
                $('.alert-error').css('display', 'block');
                $('.alert-error').html(data['message']);
            }
        });
    });

    $("#prov-select").change(function(){
        var province_name = $(this).find("option:selected").text();
        var city = $("#city-select");
        $.post('/account/setting', {'province_name': province_name}, function(data){
            city.empty();
            $.each(data, function (i, name){
                $("<option>" + name + "</option>").appendTo(city);
            })
        })
    })

    $('#fileupload').fileupload({
        acceptFileTypes: /(\.|\/)(jpe?g|png)$/i,
        maxFileSize: 5000000,
        }).on('fileuploaddone', function (e, data) {
            if(data.result == 'None'){
                alert('格式不符合要求');
                return;
            }
            $('.img-circle').attr('src', data.result);
        }).on('fileuploadfail', function(e, data){
            alert('上传失败，请重新上传...');
        })

    $('#update').click(function(){
        var city_name = $('#city-select').find("option:selected").text();
        $.post('/account/setting', {'city_name': city_name, 'photo_url': $('.img-circle').attr('src'), 'introduce': $('#description').val()},
            function(data){
                $('.alert-success').css('display', 'block');
                $('.alert-success').html('更新成功');
        })
    })
})