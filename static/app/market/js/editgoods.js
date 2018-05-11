
function addgood(good_id) {

    csrf = $('input[name="csrfmiddlewaretoken"]').val();

    $.ajax({
        url: '/axf/addgood/',
        type: 'post',
        datatype: 'json',
        data: {'good_id': good_id},
        headers: {'X-CSRFToken': csrf},
        success: function (msg) {
            $('#num'+good_id).html(msg['c_num'])
        },
        error: function () {
            alert('操作失败')
        }

    });
}

function subgood(good_id) {

    csrf = $('input[name="csrfmiddlewaretoken"]').val();

    $.ajax({
        url: '/axf/subgood/',
        type: 'post',
        datatype: 'json',
        data: {'good_id': good_id},
        headers: {'X-CSRFToken': csrf},
        success: function (msg) {
            $('#num'+good_id).html(msg['c_num'])
        },
        error: function () {
            alert('操作失败')
        }

    });
}


function goodselect(id) {
    csrf = $('input[name="csrfmiddlewaretoken"]').val();
    $.ajax({
        url: '/axf/goodselect/',
        data: {'id': id },
        datatype: 'json',
        headers: {'X-CSRFToken': csrf},
        type: 'post',
        success:function (msg) {
            if (msg.status){
                $('#num' + id).html('<span onclick="goodselect('+ id + ')">√</span>')
            }else{
                $('#num' + id).html('<span onclick="goodselect('+ id + ')">X</span>')
            }

        },
        error: function (msg) {
            alert('操作失败')
        }
    })
}

function all() {

    csrf = $('input[name="csrfmiddlewaretoken"]').val();

    $.ajax({
        url: '/axf/allselect/',
        headers: {'X-CSRFToken': csrf},
        type: 'post',
        success:function () {

            $('#all').html('<span onclick="all()">√</span>');

        },
        error: function (msg) {
            alert('操作失败')
        }
    })
}