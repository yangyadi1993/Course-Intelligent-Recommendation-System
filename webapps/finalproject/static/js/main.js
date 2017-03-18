$("#add-list-form").on('submit', function (event) {
    event.preventDefault(); // Prevent form from being submitted
    var courseId = $("#courseid").attr("class");
    var postForm = $("#add-list-form").serialize();
    $.post("/finalproject/addcollection/" + courseId, postForm, function (response) {
        alert(courseId);
        alert("");

    });

});