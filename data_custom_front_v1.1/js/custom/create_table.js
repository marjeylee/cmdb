function create_table_operate_function() {
    function cancel_display_div() {
        window.parent.parent.layer.closeAll()
    }

    function add_row_to_table() {
        let new_row = "<tr>\n" +
            "                <th class=\"create_column_checkbox_th\"><input type=\"checkbox\" style=\"margin-top: 0\"\n" +
            "                                                             class=\"create_column_checkbox\"/></th>\n" +
            "                <td><input style=\"width: 100%\" type=\"text\" name=\"column_content\"/></td>\n" +
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

    function save_table_info() {
        let table_name = $('#table_name_input').val()
        let table_comment = $('#table_comment').val()
        if (table_name.length === 0 || table_name.length > 63) {
            alert('表名为空')
            return false
        }
        let columns = []
        let trs = $('#create_column_tbody').find('tr')
        let tmp_tr;
        for (let i = 0; i < trs.length; i++) {
            tmp_tr = trs[i]
            let inputs = $(tmp_tr).find('input')
            let type = $($(tmp_tr).find('select')[0]).val()
            let column_name = $(inputs[1]).val()
            let description = $(inputs[2]).val()
            if (column_name.length === 0 || column_name.length > 63) {
                alert('列名为空')
                return false
            }
            let column = {'column_name': column_name, 'description': description, 'type': type}
            columns.push(column)
        }
        post_create_table(columns, table_name, table_comment)
        window.parent.init_table_function()
        cancel_display_div()
    }


    function event_binding() {
        $('#create_new_column_btn').click(add_row_to_table)
        $('#delete_column_btn').click(delete_row_in_display)
        $('#save_table_btn').click(save_table_info)
        $('#cancel_btn').click(cancel_display_div)
    }

    function process_function() {
        event_binding()
    }

    process_function()

}

$(document).ready(
    function () {
        create_table_operate_function()
    }
)