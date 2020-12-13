SERVER_IP = '127.0.0.1:3344'
// SERVER_IP = '188.8.6.11:3344'
jQuery.support.cors = true;

function post_create_table(columns, table_name, table_comment) {
    let data = {'table_name': table_name, 'columns': columns, 'table_comment': table_comment}
    jQuery.support.cors = true;
    $.ajax({
        type: "POST",
        contentType: "application/json;charset=UTF-8",
        url: "http://" + SERVER_IP + '/create_table',
        data: JSON.stringify(data),
        async: false,
        success: function (result) {
            result = JSON.parse(result)
            alert(result["msg"])
            if (result["is_success"]) {
                return true
            }
        },
        error: function (e) {
            console.log(e)
            return false
        }
    });
}

function search_table_info(table_name) {
    let data = {'table_name': table_name}
    let msg = ''
    $.ajax({
        type: "POST",
        contentType: "application/json;charset=UTF-8",
        url: "http://" + SERVER_IP + '/search_table_info',
        data: JSON.stringify(data),
        async: false,
        success: function (result) {
            result = JSON.parse(result)
            msg = result["msg"]
        },
        error: function (e) {
            console.log(e)
            return false
        }
    });
    return msg
}

function alter_table_name(old_name, new_name) {
    let data = {'old_name': old_name, 'new_name': new_name}
    $.ajax({
        type: "POST",
        contentType: "application/json;charset=UTF-8",
        url: "http://" + SERVER_IP + '/alter_table_name',
        data: JSON.stringify(data),
        async: false,
        success: function (result) {
            result = JSON.parse(result)
            alert(result["msg"])
        },
        error: function (e) {
            console.log(e)
            return false
        }
    });
}

function get_column_info(table_name) {
    let data = {'table_name': table_name}
    let msg = ''
    $.ajax({
        type: "POST",
        contentType: "application/json;charset=UTF-8",
        url: "http://" + SERVER_IP + '/get_column_info',
        data: JSON.stringify(data),
        async: false,
        success: function (result) {
            result = JSON.parse(result)
            msg = result["msg"]
        },
        error: function (e) {
            console.log(e)
            return false
        }
    });
    return msg
}

function get_table_comment() {
    let data = {'table_name': table_name}
    let msg = ''
    $.ajax({
        type: "POST",
        contentType: "application/json;charset=UTF-8",
        url: "http://" + SERVER_IP + '/get_table_comment',
        data: JSON.stringify(data),
        async: false,
        success: function (result) {
            result = JSON.parse(result)
            msg = result["data"]
        },
        error: function (e) {
            console.log(e)
            return false
        }
    });
    return msg
}

function alter_column_name(table_name, columns_info, values) {
    let data = {'table_name': table_name, 'columns_info': columns_info, "values": values}
    $.ajax({
        type: "POST",
        contentType: "application/json;charset=UTF-8",
        url: "http://" + SERVER_IP + '/alter_column_name',
        data: JSON.stringify(data),
        async: false,
        success: function (result) {
            result = JSON.parse(result)
            alert(result["msg"])
        },
        error: function (e) {
            console.log(e)
            return false
        }
    });
}

function alter_table_info(change_info) {
    $.ajax({
        type: "POST",
        contentType: "application/json;charset=UTF-8",
        url: "http://" + SERVER_IP + '/alter_table_info',
        data: JSON.stringify(change_info),
        async: false,
        success: function (result) {
            result = JSON.parse(result)
            alert(result["msg"])
        },
        error: function (e) {
            console.log(e)
            return false
        }
    });
}


function add_column_name(data) {
    $.ajax({
        type: "POST",
        contentType: "application/json;charset=UTF-8",
        url: "http://" + SERVER_IP + '/add_column_name',
        data: JSON.stringify(data),
        async: false,
        success: function (result) {
            result = JSON.parse(result)
            alert(result["msg"])
        },
        error: function (e) {
            console.log(e)
            return false
        }
    });
}

function delete_column(table_name, column_name) {
    let data = {'table_name': table_name, 'column_name': column_name}
    $.ajax({
        type: "POST",
        contentType: "application/json;charset=UTF-8",
        url: "http://" + SERVER_IP + '/delete_column',
        data: JSON.stringify(data),
        async: false,
        success: function (result) {
            result = JSON.parse(result)
            alert(result["msg"])
        },
        error: function (e) {
            console.log(e)
            return false
        }
    });
}

function delete_table_post(table_name) {
    let data = {'table_name': table_name}
    $.ajax({
        type: "POST",
        contentType: "application/json;charset=UTF-8",
        url: "http://" + SERVER_IP + '/delete_table',
        data: JSON.stringify(data),
        async: false,
        success: function (result) {
            result = JSON.parse(result)
            alert(result["msg"])
        },
        error: function (e) {
            console.log(e)
            return false
        }
    });
}

function add_data(data) {
    $.ajax({
        type: "POST",
        contentType: "application/json;charset=UTF-8",
        url: "http://" + SERVER_IP + '/add_data',
        data: JSON.stringify(data),
        async: false,
        success: function (result) {
            result = JSON.parse(result)
            alert(result["msg"])
        },
        error: function (e) {
            console.log(e)
            return false
        }
    });
}

function update_data(data) {
    $.ajax({
        type: "POST",
        contentType: "application/json;charset=UTF-8",
        url: "http://" + SERVER_IP + '/update_data',
        data: JSON.stringify(data),
        async: false,
        success: function (result) {
            result = JSON.parse(result)
            alert(result["msg"])
        },
        error: function (e) {
            console.log(e)
            return false
        }
    });
}

function query_data_from_db(data, current_page, page_size) {
    let ret_data = []
    data['current_page'] = current_page
    data['page_size'] = page_size
    $.ajax({
        type: "POST",
        contentType: "application/json;charset=UTF-8",
        url: "http://" + SERVER_IP + '/query_data_from_db',
        data: JSON.stringify(data),
        async: false,
        success: function (result) {
            result = JSON.parse(result)
            ret_data = result["msg"]
        },
        error: function (e) {
            console.log(e)
            return false
        }
    });
    return ret_data
}

function query_data_by_unique_id_from_db(data) {
    let ret_data = []
    $.ajax({
        type: "POST",
        contentType: "application/json;charset=UTF-8",
        url: "http://" + SERVER_IP + '/query_data_by_unique_id',
        data: JSON.stringify(data),
        async: false,
        success: function (result) {
            ret_data = JSON.parse(result)
        },
        error: function (e) {
            console.log(e)
            return false
        }
    });
    return ret_data
}

function delete_data_post(table_name, unique_id) {
    let data = {'table_name': table_name, 'unique_id': unique_id}
    $.ajax({
        type: "POST",
        contentType: "application/json;charset=UTF-8",
        url: "http://" + SERVER_IP + '/delete_data_post',
        data: JSON.stringify(data),
        async: false,
        success: function (result) {
            result = JSON.parse(result)
            alert(result["msg"])
        },
        error: function (e) {
            console.log(e)
            return false
        }
    });
}


function gen_excel_data_post(query_condition) {
    let file_name = ''
    $.ajax({
        type: "POST",
        contentType: "application/json;charset=UTF-8",
        url: "http://" + SERVER_IP + '/gen_excel_data_post',
        data: JSON.stringify(query_condition),
        async: false,
        success: function (result) {
            result = JSON.parse(result)
            file_name = result['msg']
        },
        error: function (e) {
            console.log(e)
            return false
        }
    });
    return file_name
}