$(document).ready( function(){
/*
* Delete staff users
* */
    $("tbody").on("click", "a", function () {
        if($(this).attr('data_delete')){
            $('#is_deleted_staff').modal();
            $('#delete_type').attr('data_id_type', $(this).attr('href'));
            return false;
         }
         return true;
    });

    $('#cancel_type').click(function () {
        $('#is_deleted_staff').modal('hide');
        $('#delete_type').attr('data_id_type', '');
        return false;
    });


    $('#delete_type').click(function () {
        $('#is_deleted_staff').modal('hide');
        var url = $(this).attr('data_id_type');
        $(location).attr('href',url);
    });
});