$(document).ready(function (){

    $(".modify_order").click(function(e){
        e.preventDefault();
        $.ajax({
            type: 'GET',
            url: $(this).prop("href"),
            cache: false,
            success: function(data) {
                window.open(data.data.redirect,"_self");
            },
            error: function(data) {
                for (const i in data.responseJSON.errors) {
                    alert(data.responseJSON.errors[i]);
                }
            }
        });

    });
    $(".delete").click(function(e){
        if(confirm("Do you really want to delete this record?")){
            e.preventDefault();
            $.ajax({
                type: 'GET',
                url: $(this).prop("href"),
                cache: false,
                success: function(data) {
                    alert(data.message);
                    window.location.reload();
                },
                error: function(data) {
                    for (const i in data.responseJSON.errors) {
                        alert(data.responseJSON.errors[i]);
                    }
                }
            });
        }
    });

    $(".payment_modal_link").click(function(e){
        e.preventDefault();
        $.ajax({
            type: 'GET',
            url: $(this).prop("href"),
            cache: false,
            success: function(data) {
                $(".resp_payment").html(data);
                $("#payment_modal").modal("show");
            },
            error: function(data) {
                for (const i in data.responseJSON.errors) {
                    alert(data.responseJSON.errors[i]);
                }
            }
        });
    });

    $("#btn_perfil").click(function(e){
        e.preventDefault();
        $.ajax({
            type: 'GET',
            url: $(this).prop("href"),
            cache: false,
            success: function(data) {
                $(".resp_profile").html(data);
                $("#profile_modal").modal("show");
            },
            error: function(data) {
                for (const i in data.responseJSON.errors) {
                    alert(data.responseJSON.errors[i]);
                }
            }
        });
    });


    $("body").on("submit", ".formGen", function(e) {
        e.preventDefault();
        var formdata = new FormData(this);
        var notificationError = $(this).find(".notification");
        $.ajax({
            type: 'POST',
            url: $(this).attr("action"),
            cache: false,
            processData: false,
            contentType: false,
            data: formdata,
            success: function(success) {
                alert(success.message)
                window.open(success.data.redirect,"_self");
            },
            error: function(data) {
                
                notificationError.html("<ul class='errors'></ul>");
                for (const i in data.responseJSON.errors) {
                    notificationError.find(".errors").append("<li>"+data.responseJSON.errors[i]+"</li>");
                }
                
                notificationError.removeClass("d-none");
            }
        });
    });
});
