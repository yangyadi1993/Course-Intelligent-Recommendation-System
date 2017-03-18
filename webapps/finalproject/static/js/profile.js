function update_info_div() {
    var update_info_div = $('#update_info_div');
    update_info_div.slideToggle();
}


function add_education_div() {
    var add_education_div = $('#add_education_div');
    add_education_div.slideToggle();
}


function add_skill_div() {
    var add_skill_div = $('#add_skill_div');
    add_skill_div.slideToggle();
}

function add_work_experience_div() {
    var add_work_experience_div = $('#add_work_experience_div');
    add_work_experience_div.slideToggle();
}

function add_honor_div() {
    var add_honor_div = $('#add_honor_div');
    add_honor_div.slideToggle();
}


function add_project_div() {
    var add_project_div = $('#add_project_div');
    add_project_div.slideToggle();
}


function add_language_div() {
    var add_language_div = $('#add_language_div');
    add_language_div.slideToggle();
}

function upload_resume_div() {
    var upload_resume_div = $('#page_upload_resume');
    upload_resume_div.slideToggle();
}

function upload_resume() {
    $.post("/finalproject/page_upload_resume")
}


function reset_update_info() {
    var phone = $('#phone');
    var email = $('#email');
    var location = $('#location');
    var industry = $('#industry');
    var summary = $('#summary');
    phone.val("");
    email.val("");
    location.val("");
    industry.val("");
    summary.val("");
}

function update_info() {
    var new_phone = $('#phone').val();
    var new_email = $('#email').val();
    var new_location = $('#location').val();
    var new_industry = $('#industry').val();
    var new_summary = $('#summary').val();
    $.post("/finalproject/update_info", {
        phone: new_phone,
        email: new_email,
        location: new_location,
        industry: new_industry,
        summary: new_summary
    }).done(function () {
        $('#profile_info').load("/finalproject/profile_info").fadeIn();
        reset_update_info();
    }).fail(function () {
        alert("Illegal parameters");
        $(document).reload();
    });
}

function reset_education() {
    var school_name = $('#school_name');
    var start_date = $('#start_date');
    var degree = $('#degree');
    var graduate_date = $('#graduate_date');
    var major = $('#major');
    var minor = $('#minor');
    school_name.val("");
    start_date.val("");
    degree.val("");
    graduate_date.val("");
    major.val("");
    minor.val("");
}

function add_education() {
    var school_name = $('#school_name').val();
    var start_date = $('#start_date').val();
    var degree = $('#degree').val();
    var graduate_date = $('#graduate_date').val();
    var major = $('#major').val();
    var minor = $('#minor').val();

    var start_d = new Date(start_date);
    var graduate_d = new Date(graduate_date);

    if (graduate_d < start_d) {
        alert("Start date should be earlier than graduate date.");
        return;
    }

    $.post("/finalproject/add_education", {
        school_name: school_name,
        start_date: start_date,
        graduate_date: graduate_date,
        degree: degree,
        major: major,
        minor: minor
    }).done(function () {
        $('#education_div').load("/finalproject/education_load").fadeIn();
        reset_education();
    }).fail(function () {
        alert("Illegal parameters");
        $(document).reload();
    });
}

function reset_skill() {
    var skill = $('#skill');
    var proficiency = $('#proficiency');
    skill.prop('selectedIndex', 0);
    proficiency.prop('selectedIndex', 0);
}

function add_skill() {
    var skill_name = $('#skill').val();
    var proficiency = $('#proficiency').val();
    $.post("/finalproject/add_skill", {
        skill_name: skill_name,
        proficiency: proficiency
    }).done(function () {
        $('#skill_div').load("/finalproject/skill_load").fadeIn();
        reset_skill();
    }).fail(function () {
        alert("Illegal parameters");
        $(document).reload();
    });
}

function reset_work_experience() {
    var organization_name = $('#organization_name');
    var responsibility = $('#responsibility');
    var city = $('#city');
    var country = $('#country');
    var work_start_date = $('#work_start_date');
    var work_end_date = $('#work_end_date');
    var work_description = $('#work_description');
    organization_name.val("");
    responsibility.val("");
    city.val("");
    country.val("");
    work_start_date.val("");
    work_end_date.val("");
    work_description.val("");
}

function add_work_experience() {
    var employer_name = $('#organization_name').val();
    var responsibility = $('#responsibility').val();
    var location_city = $('#city').val();
    var location_country = $('#country').val();
    var start_date = $('#work_start_date').val();
    var end_date = $('#work_end_date').val();
    var description = $('#work_description').val();


    var start_d = new Date(start_date);
    var end_d = new Date(end_date);

    if (end_d < start_d) {
        alert("Start date should be earlier than end date.");
        return;
    }


    $.post("/finalproject/add_work_experience", {
        employer_name: employer_name,
        responsibility: responsibility,
        location_city: location_city,
        location_country: location_country,
        start_date: start_date,
        end_date: end_date,
        description: description
    }).done(function () {
        $('#work_experience_div').load("/finalproject/work_experience_load").fadeIn();
        reset_work_experience();
    }).fail(function () {
        alert("Illegal parameters");
        $(document).reload();
    });
}

function reset_honor() {
    var honor_title = $('#honor_title');
    var issued_date = $('#issued_date');
    var issued_organization = $('#issued_organization');
    honor_title.val("");
    issued_date.val("");
    issued_organization.val("");
}

function add_honor() {
    var title = $('#honor_title').val();
    var issued_date = $('#issued_date').val();
    var issued_organization = $('#issued_organization').val();
    $.post("/finalproject/add_honor", {
        title: title,
        issued_date: issued_date,
        issued_organization: issued_organization
    }).done(function () {
        $('#honor_div').load("/finalproject/honor_load").fadeIn();
        reset_honor();
        reset_skill();
    }).fail(function () {
        alert("Illegal parameters");
        $(document).reload();
    });
}

function reset_project() {
    var project_name = $('#project_name');
    var project_organization_name = $('#project_organization_name');
    var project_start_date = $('#project_start_date');
    var project_end_date = $('#project_end_date');
    var project_responsibility = $('#project_responsibility');
    var description = $('#description');
    project_name.val("");
    project_organization_name.val("");
    project_start_date.val("");
    project_end_date.val("");
    project_responsibility.val("");
    description.val("");
}


function add_project() {
    var project_name = $('#project_name').val();
    var organization_name = $('#project_organization_name').val();
    var start_date = $('#project_start_date').val();
    var end_date = $('#project_end_date').val();
    var responsibility = $('#project_responsibility').val();
    var description = $('#description').val();

    var start_d = new Date(start_date);
    var end_d = new Date(end_date);

    if (end_d < start_d) {
        alert("Start date should be earlier than end date.");
        return;
    }

    $.post("/finalproject/add_project", {
        project_name: project_name,
        organization_name: organization_name,
        start_date: start_date,
        end_date: end_date,
        responsibility: responsibility,
        description: description
    }).done(function () {
        $('#project_div').load("/finalproject/project_load").fadeIn();
        reset_project();
    }).fail(function () {
        alert("Illegal parameters");
        $(document).reload();
    });
}

function reset_language() {
    var language = $('#language');
    var language_proficiency = $('#language_proficiency');
    language.val("");
    language_proficiency.val("");
}

function add_language() {
    var language_name = $('#language').val();
    var proficiency = $('#language_proficiency').val();
    $.post("/finalproject/add_language", {
        language_name: language_name,
        proficiency: proficiency
    }).done(function () {
        $('#language_div').load("/finalproject/language_load").fadeIn();
        reset_language();
    }).fail(function () {
        alert("Illegal parameters");
        $(document).reload();
    });
}


$(document)
    .ready(function () {

        $('#update_info_btn').click(update_info_div);
        $("#update_info_cancel").click(update_info_div);

        $('#education_btn').click(add_education_div);
        $('#add_education_cancel').click(add_education_div);

        $('#skill_btn').click(add_skill_div);
        $('#add_skill_cancel').click(add_skill_div);

        $('#work_btn').click(add_work_experience_div);
        $('#add_work_cancel').click(add_work_experience_div);

        $('#honor_btn').click(add_honor_div);
        $('#add_honor_cancel').click(add_honor_div);

        $('#project_btn').click(add_project_div);
        $('#add_project_cancel').click(add_project_div);

        $('#language_btn').click(add_language_div);
        $('#add_language_cancel').click(add_language_div);

        $('#profile_info').load("/finalproject/profile_info").fadeIn();
        $('#education_div').load("/finalproject/education_load").fadeIn();
        $('#skill_div').load("/finalproject/skill_load").fadeIn();
        $('#work_experience_div').load("/finalproject/work_experience_load").fadeIn();
        $('#honor_div').load("/finalproject/honor_load").fadeIn();
        $('#project_div').load("/finalproject/project_load").fadeIn();
        $('#language_div').load("/finalproject/language_load").fadeIn();

        $('#update_info').click(update_info);
        $('#add_education').click(add_education);
        $('#add_skill').click(add_skill);
        $('#add_work_experience').click(add_work_experience);
        $('#add_honor').click(add_honor);
        $('#add_project').click(add_project);
        $('#add_language').click(add_language);


        $('#upload_resume').click(upload_resume_div);
        $('#upload_resume_cancel').click(upload_resume_div);
        $('#submit_resume').click(upload_resume);

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
