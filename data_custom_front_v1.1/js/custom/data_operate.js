function build_search_data_div() {
    let data_search_div = $('#data_search_div')
    console.log(window.column_info)
    let text_lst = []
    let time_lst = []
    for (let i = 0; i < window.column_info.length; i++) {
        let current_info = window.column_info[i]
        let column_name = current_info['COLUMN_NAME']
        let data_type = current_info['DATA_TYPE']
        if (column_name === "unique_id" || data_type === '数字') {
            continue
        }
        if (data_type === '文本' || data_type === '多行文本') {
            let tmp_str = '<label class="find_labela" title="' + column_name + '">' + column_name + ' : </label>' +
                '<input type="text" class="find_input" name="' + column_name + '" />'
            text_lst.push(tmp_str)
        } else if (data_type === '日期') {
            let tmp_str = '<label class="find_labela" title="' + column_name + '">' + column_name + ' : </label>' +
                '<input type="datetime-local" class="datetime_select" name="' + column_name + '_start" /> 至 ' +
                '<input type="datetime-local" class="datetime_select" name="' + column_name + '_end" />'
            time_lst.push(tmp_str)
        }
    }
    let combine_str = ''
    for (let j = 1; j < text_lst.length + 1; j++) {
        let tmp_str = text_lst[j - 1]
        if (j % 4 === 0) {
            tmp_str = tmp_str + '<br/>'
        }
        combine_str = combine_str + tmp_str
    }
    combine_str = combine_str + '<br/>'
    for (let j = 1; j < time_lst.length + 1; j++) {
        let tmp_str = time_lst[j - 1] + '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'
        if (j % 2 === 0) {
            tmp_str = tmp_str + '<br/>'
        }
        combine_str = combine_str + tmp_str
    }
    combine_str = '<h4 style="color: #2c82c9;text-align: center;"><b>' + table_name + '</b></h4><br/>' + combine_str
    data_search_div.html(combine_str)
}

function get_query_data() {
    let inputs = $('#data_search_div').find('input')
    let query_content = {}
    for (const input of inputs) {
        let tmp_input = $(input)
        let value = tmp_input.val()
        let key = tmp_input.attr('name')
        query_content[key] = value
    }
    return {'query_content': query_content, 'column_info': column_info, 'table_name': table_name}
}

function get_column_info_json() {
    let columns = [{
        checkbox: "true",
        field: 'check',
        align: 'center',
        valign: 'middle',
    }]
    for (const column of column_info) {
        let column_name = column['COLUMN_NAME']
        let column_format = {
            title: column_name,
            field: column_name,
            align: 'center',
            formatter: function (value, row) {
                if (String(value).indexOf('\n') !== -1) {
                    return '<pre class="pre_class" style="border: 0" >' + value + '</pre>'
                }
                return value

            }
        }
        columns.push(column_format)
    }
    return columns
}


function query_data_data(query_condition) {
    $("#table").bootstrapTable('destroy');
    let tmp_column_info = get_column_info_json()
    $('#table').bootstrapTable({
        method: "post",
        striped: true,
        singleSelect: false,
        url: "http://" + SERVER_IP + '/query_data_from_db',
        dataType: "json",
        pagination: true,
        pageSize: 10,
        pageNumber: 1,
        search: false, //显示搜索框
        contentType: "application/x-www-form-urlencoded",
        queryParams: {'data': JSON.stringify(query_condition)},
        columns: tmp_column_info,
    });
}

function search_data() {
    let data = get_query_data()
    query_data_data(data)
}

function search_reset_btn() {
    let inputs = $('#data_search_div').find('input')
    for (const input of inputs) {
        $(input).val('')
    }
}

function create_data() {
    window.parent.data_operate_table_name = table_name
    window.parent.layer.open({
        type: 2,
        title: '新增数据',
        shade: 0.5,
        skin: 'layui-layer-rim',
        area: ['95%', '92%'],
        shadeClose: true,
        content: './html/create_data.html'
    });
}

function get_unique_id_index() {
    let ths = $('thead').find('th')
    for (let i = 0; i < ths.length; i++) {
        let th = $(ths[i])
        if ('unique_id' === th.attr('data-field')) {
            return i
        }
    }
}

function update_data_operate() {
    let unique_id_index = get_unique_id_index()
    let trs = $('tbody').find('tr')
    for (let tr of trs) {
        let current_tr = $(tr)
        let tds = current_tr.find('td')
        let unique_id = $(tds[unique_id_index]).text()
        current_tr.attr('unique_id', unique_id)
    }
    let checkboxes = $("input[name='btSelectItem']")
    let checked_boxes = []
    for (let checkbox of checkboxes) {
        if ($(checkbox).is(':checked')) {
            checked_boxes.push(checkbox)
        }
    }
    if (checked_boxes.length !== 1) {
        alert('选中一条记录')
        return false
    }
    let checked_box = $(checked_boxes[0])
    let unique_id = checked_box.parent().parent().attr('unique_id')
    window.parent.layer.open({
        type: 2,
        title: '修改数据',
        shade: 0.5,
        skin: 'layui-layer-rim',
        area: ['95%', '92%'],
        shadeClose: true,
        content: './html/update_data.html?' + unique_id + '|' + table_name
    });
}

function delete_data() {
    let unique_id_index = get_unique_id_index()
    let trs = $('tbody').find('tr')
    for (let tr of trs) {
        let current_tr = $(tr)
        let tds = current_tr.find('td')
        let unique_id = $(tds[unique_id_index]).text()
        current_tr.attr('unique_id', unique_id)
    }
    let checkboxes = $("input[name='btSelectItem']")
    let checked_boxes = []
    for (let checkbox of checkboxes) {
        if ($(checkbox).is(':checked')) {
            checked_boxes.push(checkbox)
        }
    }
    if (checked_boxes.length !== 1) {
        alert('选中一条记录')
        return false
    }
    let checked_box = $(checked_boxes[0])
    let unique_id = checked_box.parent().parent().attr('unique_id')
    let alert_str = '确定要删除该数据吗？'
    if (confirm(alert_str) === true) {
        delete_data_post(table_name, unique_id)
        $('#search_data_btn').click()
    }
}


function launch_gen_excel_request() {
    let data = get_query_data()
    return gen_excel_data_post(data)
}

function export_data() {
    let file_name = launch_gen_excel_request()
    window.location = "http://" + SERVER_IP + "/download_file?fileName=" + file_name
}

function pre_click_event_binding() {
    let pres = $('.pre_class')
    for (let pre of pres) {
        pre = $(pre)
        if (!pre.hasClass('binding_click')) {
            pre.click(function () {
                window.parent.pre_content = pre.html()
                console.log(window.parent.pre_content)
                window.parent.layer.open({
                    type: 2,
                    title: '显示内容',
                    shade: 0.5,
                    skin: 'layui-layer-rim',
                    area: ['85%', '85%'],
                    shadeClose: true,
                    content: './html/display_pre_content.html'
                });
            })
            pre.addClass('binding_click')
        }
    }
}

function interval_function() {
    pre_click_event_binding()
}

setInterval(interval_function, 1000)

function event_binding() {
    $('#search_reset_btn').click(search_reset_btn)
    $('#search_data_btn').click(search_data)
    $('#create_data_a_tag').click(create_data)
    $('#update_data__tag').click(update_data_operate)
    $('#delete_data_a_tag').click(delete_data)
    $('#export_data_tag').click(export_data)
}

function data_ready_function() {
    window.column_info = get_column_info(window.table_name)
    build_search_data_div()
    event_binding()
}

function insert_table_name(table_name) {
    window.table_name = table_name
    data_ready_function()
}