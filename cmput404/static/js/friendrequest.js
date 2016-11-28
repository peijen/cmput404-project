
$("#friend_form").submit(function(e){
    //debugger;
    document.getElementById("friendButton").disabled = true;
    e.preventDefault();
    var FriendForm = $(this);
    var csrftoken = Cookies.get('csrftoken');
    //sending data using post


    var data= {
               "author": request_user,  
               "user_id": user_id,
               "friend": friend,
               "friend_id": profile_id, 
              }   


    function csrfSafeMethod(method) {
      // these HTTP methods do not require CSRF protection
      return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
      beforeSend: function(xhr, settings) {
          if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
              xhr.setRequestHeader("X-CSRFToken", csrftoken);
          }
      }
    });
 
    $.ajax({
        cache: false,
        url : "/service/friendrequest",
        type: "POST",
        contentType:"application/json; charset=utf-8",
        data: JSON.stringify(data),
        dataType : "json",
        //data : data,
        success : function(callback){
            //Where $(this) => context == FORM

            //$(this).html("Received HTTP 200. Post should now be in database.");
            //window.location.href = "{% url 'website:home'%}"
            console.log("SUCCESSSSSSS");

        },
        error : function(xhr, thrownError){
            console.log(xhr.status);
            console.log(thrownError)
            $(this).html("Error!");
        }
    });
 
    //root user id: 6a431053-35bc-4c44-8250-06c65f577864
   

});





