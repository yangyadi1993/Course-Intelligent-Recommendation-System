$(document).ready(function () {  // Runs when the document is ready

    // using jQuery
    // https://docs.djangoproject.com/en/1.10/ref/csrf/

    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    var csrftoken = getCookie('csrftoken');

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    $("#create-comment-form").on('submit', function (event) {
        event.preventDefault();
        var commentForm = $("#create-comment-form").serialize();
        var course_id = $("#create-comment-form").attr("class");
        var comment_area = $("#commentRow");
        $.post("/finalproject/addcoursecomment/" + course_id, commentForm, function (response) {
            console.log(response["message"]);
//            if(response["message"]!="error") {
            firstname = response["firstname"];
            console.log("hh");
            lastname = response["lastname"];
            profileid = response["profileid"];
            timestamp = response["time"];
            text = response["commentText"];
            userid = response["userid"];
            console.log(firstname);
            console.log(lastname);
            console.log(profileid);
            console.log(text);
            console.log(timestamp);
            $("#commentlist").append("<div> <div class=\"col-md-5\"> <a href='/finalproject/other_user_profile/" + userid + "'> <p>" + firstname + " " + lastname + "</p> </a></div>" +
                " <div class=\"col-md-7\"><span float=\"right\">" + timestamp + "</small> </div> <div class=\"col-md-12\"><p>" + text + "</p></div></div><hr>");
            var course_Area = $('#commentArea');
            course_Area.val("");

//        }
        });
    });

}); // End of $(document).ready
