function new_plan() {
    var add_plan = $('#add_plan_div');
    add_plan.slideToggle();
}

function reset_new_plan() {
    var new_day = $('#day');
    var new_from_hour = $('#from_hour');
    var new_from_minute = $('#from_minute');
    var new_from_ampm = $('#from_ampm');
    var new_to_hour = $('#to_hour');
    var new_to_minute = $('#to_minute');
    var new_to_ampm = $('#to_ampm');
    var new_course_name = $('#coursename');
    new_day.prop('selectedIndex', 0);
    new_from_hour.prop('selectedIndex', 0);
    new_from_minute.prop('selectedIndex', 0);
    new_from_ampm.prop('selectedIndex', 0);
    new_to_hour.prop('selectedIndex', 0);
    new_to_minute.prop('selectedIndex', 0);
    new_to_ampm.prop('selectedIndex', 0);
    new_course_name.val("");
}

function clear_plan() {
    if (confirm('Create new plan will erase the current plan. Are you sure to create a new weekly plan?')) {
        $.get("/finalproject/clear_plan")
            .done(function () {
                $('#plan_main').load("/finalproject/plan_main").fadeIn();
            })
            .fail(function () {
                alert("Something wrong with the request. Please try again.");
            });
    }
}

function add_new_plan() {
    var new_day = $('#day');
    var new_from_hour = $('#from_hour');
    var new_from_minute = $('#from_minute');
    var new_from_ampm = $('#from_ampm');
    var new_to_hour = $('#to_hour');
    var new_to_minute = $('#to_minute');
    var new_to_ampm = $('#to_ampm');
    var new_course_name = $('#coursename');
    var plan_main = $('#plan_main');
    $.post("/finalproject/add_plan", {
        day: new_day.val(), from_hour: new_from_hour.val(),
        from_minute: new_from_minute.val(), from_ampm: new_from_ampm.val(), to_hour: new_to_hour.val(),
        to_minute: new_to_minute.val(), to_ampm: new_to_ampm.val(), course_name: new_course_name.val()
    }).done(function () {
        $('#plan_main').load("/finalproject/plan_main").fadeIn();
        reset_new_plan();
    }).fail(function () {
        alert("Illegal parameters");
        $(document).reload();
    });
}

$(document)
    .ready(function () {

        $('#plan_main').load("/finalproject/plan_main").fadeIn();
        $('#clear_plan').click(clear_plan);
        $('#new_plan').click(new_plan);
        $('#cancel_new_plan').click(reset_new_plan);
        $('#add_new_plan').click(add_new_plan);

        function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie != '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i]);
                    if (cookie.substring(0, name.length + 1) == (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }

        var csrftoken = getCookie('csrftoken');
        $.ajaxSetup({
            beforeSend: function (xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        });
    });