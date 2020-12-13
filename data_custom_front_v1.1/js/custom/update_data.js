function change_data_type(old_type) {
    if (old_type === '文本') {
        return 'text'
    }
    if (old_type === '日期') {
        return 'datetime-local'
    }
    if (old_type === '数字') {
        return 'number'
    }
    if (old_type === '多行文本') {
        return 'textarea'
    }
}

function put_column_info_to_page() {
    for (const column of table_info) {
        let column_name = column['COLUMN_NAME']
        let data_type = change_data_type(column['DATA_TYPE'])
        if (column_name === 'unique_id') {
            continue
        }
        let new_row = ''
        if (data_type === 'textarea') {
            new_row = "<tr> <td><label name='" + column_name + "'>" +
                column_name + "</label></td><td><label>" + column['DATA_TYPE'] + "</label></td><td><textarea " +
                "class='input_value' style=\"width: 100%\" type='" + data_type + "'   name='" +
                column_name + "'></textarea></td> </tr>"
        } else {
            new_row = "<tr> <td><label name='" + column_name + "'>" +
                column_name + "</label></td><td><label>" + column['DATA_TYPE'] + "</label></td><td><input " +
                "class='input_value' style=\"width: 100%\" type='" + data_type + "'   name='" +
                column_name + "'/></td> </tr>"
        }
        $('#create_data_tbody').append(new_row)
    }
}

function init_data_type_mapping() {
    console.log(table_info)
    window.column_tpye_mapping = {}
    for (let info of table_info) {
        column_tpye_mapping[info['COLUMN_NAME']] = info['DATA_TYPE']
    }
}

function query_data_by_unique_id() {
    let query_data = {'unique_id': unique_id, 'table_name': table_name}
    let res = query_data_by_unique_id_from_db(query_data)
    console.log(res)

    let inputs = $('#create_data_tbody').find('input')
    for (let input of inputs) {
        input = $(input)
        let name = input.attr('name')
        let data_type = column_tpye_mapping[name]
        let value = res[name]
        if (data_type === '日期') {
            value = value.replace(' ', 'T')
        }
        input.val(value)
    }
    let text_areas = $('#create_data_tbody').find('textarea')
    for (let input of text_areas) {
        input = $(input)
        let name = input.attr('name')
        let data_type = column_tpye_mapping[name]
        let value = res[name]
        if (data_type === '日期') {
            value = value.replace(' ', 'T')
        }
        input.val(value)
    }
}


function load_save_info() {
    let inputs = $('.input_value')
    let input_res = {}
    for (let input of inputs) {
        input = $(input)
        let key = input.attr('name')
        input_res[key] = input.val()
    }
    input_res['unique_id'] = unique_id
    return input_res
}

function validate_input_info() {
    let inputs = $('#create_data_tbody').find('input')
    for (let input of inputs) {
        input = $(input)
        let data_type = input.attr('type')
        let name = input.attr('name')
        if (data_type === 'datetime-local' || data_type === 'number') {
            if (input.val().length === 0) {
                alert('【' + name + '】为必填项。（日期，数字类型均为必填项）')
                return false
            }
        }
    }
    return true
}

function save_update_data_info() {
    let save_info = load_save_info()
    let is_valid = validate_input_info()
    if (!is_valid) {
        return false
    }
    update_data({'table_name': table_name, 'data': save_info})
    window.parent.refresh_data_function(table_name)
    cancel_display_div()
}

function cancel_display_div() {
    window.parent.parent.layer.closeAll()
}

function event_binding() {
    $('#save_data_btn').click(save_update_data_info)
    $('#cancel_btn').click(cancel_display_div)
}

function put_old_info_to_page() {
    $('#table_name_label').text(table_name)
    put_old_column_info_to_page()

}

function ready_function() {
    window.table_info = get_column_info(table_name)
    init_data_type_mapping()
    put_column_info_to_page()
    query_data_by_unique_id()
    event_binding()
}

$(document).ready(function () {
    ready_function()
})