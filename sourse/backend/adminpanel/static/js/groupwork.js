$(document).ready( function(){
/*
* Add new group
* */
  $('#add_new_group').click(function () {

          var new_name = $('#new_name_group').val();

          if(new_name == ''){
              alert('Enter correct data for new type!!!');
              return false;
          }
          $.get(
              "/adminpanel/group/add/",
              {
                  name: new_name,

              },
              onAjaxSuccess
            );
            function onAjaxSuccess(data)
            {
              if (data.status){
                  if ($('#group_list tr:last-child td:first-child').text() == ''){
                      var num_n = 1;
                  }
                  else{
                      var num_n = +$('#group_list tr:last-child td:first-child').text() + 1;
                  }

                  var new_type = '<tr><td>'+num_n+'</td><td class="text-center">'+new_name+'</td>' +
                                    '<td class="text-center"><a type="button" data_delete="delete" id="'+data.id+'"'+
                                    'class="btn btn-sm btn-danger" href="/adminpanel/group/delete/'+data.id+'/">' +
                                    'Редактировать</a></td>';

                  $('#group_list').append(new_type);
                  $('#new_name_group').val('');
              }
            }

  });


/*
* Delete group
* */
    $("tbody").on("click", "a", function () {
        if($(this).attr('data_delete')){
            $('#is_deleted_group').modal();
            $('#delete_type').attr('data_id_type', $(this).attr('href'));
            return false;
         }
         return true;
    });

    $('#cancel_type').click(function () {
        $('#is_deleted_group').modal('hide');
        $('#delete_type').attr('data_id_type', '');
        return false;
    });


    $('#delete_type').click(function () {
        $('#is_deleted_group').modal('hide');
        var url = $(this).attr('data_id_type');
        $(location).attr('href',url);
    });
});