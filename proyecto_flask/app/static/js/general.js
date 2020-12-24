$(document).ready(function (){
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