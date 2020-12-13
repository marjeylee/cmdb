// window.table_name = '2020年10月22日大苏打ddd'
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

function load_save_info() {
    let inputs = $('.input_value')
    let input_res = {}
    for (let input of inputs) {
        input = $(input)
        let key = input.attr('name')
        input_res[key] = input.val()
    }
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

function save_data_info() {
    let save_info = load_save_info()
    let is_valid = validate_input_info()
    if (!is_valid) {
        return false
    }
    add_data({'table_name': table_name, 'data': save_info})
    window.parent.refresh_data_function(table_name)
    cancel_display_div()
}

function cancel_display_div() {
    window.parent.parent.layer.closeAll()
}

function event_binding() {
    $('#save_data_btn').click(save_data_info)
    $('#cancel_btn').click(cancel_display_div)
}

function put_old_info_to_page() {
    $('#table_name_label').text(table_name)
    put_old_column_info_to_page()
}

function ready_function() {
    if (typeof table_name === typeof undefined) {
        window.table_name = window.parent.data_operate_table_name
        console.log(table_name)
        // alert(table_name)
    }
    window.table_info = get_column_info(table_name)
    put_column_info_to_page()
    event_binding()
}

$(document).ready(function () {
    ready_function()
})