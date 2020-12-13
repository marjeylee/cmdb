table_name = window.parent.parent.table_name

// window.table_name = '2020年10月22日大苏打ddd'

function put_old_column_info_to_page() {
    let columns = old_table_info
    for (const column of columns) {
        let column_name = column['COLUMN_NAME']
        let data_type = column['DATA_TYPE']
        let comment = column['COLUMN_COMMENT']
        if (column_name === 'unique_id') {
            continue
        }
        let new_row = "<tr>\n" +
            "                <th class=\"create_column_checkbox_th\"><input type=\"checkbox\" style=\"margin-top: 0\"\n" +
            "  class=\"create_column_checkbox\"/></th> <td><input style=\"width: 100%\" type=\"text\"" +
            " old_value ='" + column_name + "' value='" + column_name + "' name=\"column_content\"/></td>\n" +
            "   <td><label>" + data_type + "</label></td>\n" +
            "   <td><input style=\"width: 100%\" type=\"text\" old_value='" + comment + "' value='" + comment + "' name=\"column_comment\"/></td>\n" +
            "            </tr>"
        $('#create_column_tbody').append(new_row)
    }
}

function add_row_to_table() {
    let new_row = "<tr>\n" +
        "                <th class=\"create_column_checkbox_th\"><input type=\"checkbox\" style=\"margin-top: 0\"\n" +
        "                                                             class=\"create_column_checkbox\"/></th>\n" +
        "                <td><input style=\"width: 100%\" type=\"text\" name=\"column_content\" " +
        "placeholder='修改后字段名不可与其他字段名相同'/></td>\n" +
        "                <td><select class=\"form_input\" name=\"column_type\">\n" +
        "                    <option value='text'>文本</option>\n" +
        '  <option value="textarea">多行文本</option>' +
        "                    <option value='number'>数字</option>\n" +
        "                    <option value='date'>时间</option>\n" +
        "                </select></td>\n" +
        "                <td><input style=\"width: 100%\" type=\"text\" name=\"column_comment\"/></td>\n" +
        "            </tr>"
    $('#create_column_tbody').append(new_row)
}

function get_left_column_info() {
    let columns = []
    let trs = $('#create_column_tbody').find('tr')
    let tmp_tr;
    for (let i = 0; i < trs.length; i++) {
        tmp_tr = trs[i]
        let inputs = $(tmp_tr).find('input')
        let type = $($(tmp_tr).find('select')[0]).val()
        let column_name_input = $(inputs[1])
        let column_name = column_name_input.val()
        let description = $(inputs[2]).val()
        if (column_name.length === 0 || column_name.length > 63) {
            alert('列名为空')
            return false
        }
        let attr = column_name_input.attr('old_value')
        let column = {'new_column_name': column_name, 'description': description, 'type': type}
        if (typeof attr !== typeof undefined && attr !== false && attr.length > 0) {
            column['old_column_name'] = attr
        }
        columns.push(column)
    }
    return columns
}

function get_update_info(submit_column_info) {
    let update_column = []
    for (let new_column_info of submit_column_info) {
        if (new_column_info.hasOwnProperty('old_column_name') && new_column_info['old_column_name'].length > 0) {
            for (const old_info of old_table_info) {
                if (new_column_info['old_column_name'] === old_info['COLUMN_NAME'] && (
                    new_column_info['new_column_name'] !== old_info['COLUMN_NAME'] ||
                    new_column_info['description'] !== old_info['COLUMN_COMMENT'])) {
                    new_column_info['type'] = old_info['DATA_TYPE']
                    update_column.push(new_column_info)
                }
            }
        }
    }
    return update_column
}

function get_add_info(submit_column_info) {
    let add_column = []
    for (let new_column_info of submit_column_info) {
        let is_old = false
        if (new_column_info.hasOwnProperty('old_column_name')) {
            is_old = true
        } else {
            for (const old_info of old_table_info) {
                if (new_column_info['new_column_name'] === old_info['COLUMN_NAME']) {
                    is_old = true
                }
            }
        }
        if (!is_old) {
            add_column.push(new_column_info)
        }
    }
    return add_column
}

function get_delete_info(submit_column_info) {
    let delete_column = []
    for (let old of old_table_info) {
        if (old['COLUMN_NAME'] === 'unique_id') {
            continue
        }
        let is_delete = true
        for (const new_info of submit_column_info) {
            if (new_info.hasOwnProperty('old_column_name') && new_info['old_column_name'].length > 0) {
                if (new_info['old_column_name'] === old['COLUMN_NAME']) {
                    is_delete = false
                }
            }
        }
        if (is_delete) {
            delete_column.push(old)
        }
    }
    return delete_column
}

function get_change_info() {
    let change_info = {'table_name': {}, 'column_update_info': [], 'column_add_info': [], 'column_delete_info': []}
    change_info['table_name']['old_name'] = table_name
    change_info['table_name']['new_name'] = $('#table_name_input').val()
    change_info['table_comment'] = $('#table_comment').val()
    change_info['table_name']['is_change'] = table_name !== change_info['table_name']['new_name'];
    let left_column_info = get_left_column_info()
    change_info['column_update_info'] = get_update_info(left_column_info)
    change_info['column_add_info'] = get_add_info(left_column_info)
    change_info['column_delete_info'] = get_delete_info(left_column_info)
    return change_info

}

function update_table_info() {
    let change_info = get_change_info()
    let table_name = $('#table_name_input').val()
    let table_comment = $('#table_comment').val()
    if (table_name.length === 0 || table_name.length > 63) {
        alert('表名为空')
        return false
    }
    alter_table_info(change_info)
    window.parent.init_table_function()
    cancel_display_div()
}

function delete_row_in_display() {
    let checkbox = $('.create_column_checkbox')
    let is_checked;
    for (let input of checkbox) {
        input = $(input)
        is_checked = input.is(':checked');
        if (is_checked) {
            let parent = input.parent().parent()
            parent.remove()
        }
    }
}

function cancel_display_div() {
    window.parent.parent.layer.closeAll()
}

function event_binding() {
    $('#create_new_column_btn').click(add_row_to_table)
    $('#delete_column_btn').click(delete_row_in_display)
    $('#save_table_btn').click(update_table_info)
    $('#cancel_btn').click(cancel_display_div)
}

function put_old_info_to_page() {
    let table_name_input = $('#table_name_input')
    table_name_input.attr('old_value', table_name)
    table_name_input.val(table_name)
    put_old_column_info_to_page()
    let table_comment = get_table_comment(table_name)
    $('#table_comment').val(table_comment)
}

function ready_function() {
    window.old_table_info = get_column_info(table_name)

    put_old_info_to_page()
    event_binding()
}

$(document).ready(function () {
    ready_function()
})