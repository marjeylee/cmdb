function init_table_function() {
    let iframes = $('.LRADMS_iframe')
    for (let iframe of iframes) {
        iframe = $(iframe)
        if ('./html/table_operate.html' === iframe.attr('data-id')) {
            iframe[0].contentWindow.query_table_data()
        }
    }
}

function refresh_data_function(table_name) {
    let child_window = $('#' + table_name + '_iframe')[0].contentWindow;
    child_window.search_data()
}

function get_all_tab_a_tags() {
    return $('#page_tabs_div').find('a')
}

function binding_tab_click_event() {
    let a_tags = get_all_tab_a_tags()
    for (let i = 0; i < a_tags.length; i++) {

    }
}

function create_data_iframe(table_name) {
    let str = '<iframe class="LRADMS_iframe" width="100%" height="100%"  src="./html/data_operate.html" frameborder="0"\n' +
        '                        data-id="' + table_name + '" id="' + table_name + '_iframe"></iframe>'
    $('#content-main').append(str)
    let tmp_frame = $('#' + table_name + '_iframe')
    tmp_frame.load(function () {
        tmp_frame[0].contentWindow.insert_table_name(table_name)
    })
}

function create_data_tab(table_name) {
    if ($('#' + table_name + '_tab_tag').length === 0) {
        let tag_a = '<a href="javascript:" class="menuTab  data_tab" id="' + table_name + '_tab_tag" title="' + table_name + '" data-id="' + table_name + '">' +
            table_name + ' <i class="fa fa-remove"></i></a>'
        $('#page_tabs_div').append(tag_a)
        create_data_iframe(table_name)
    }
}

function add_data_tab(table_name) {
    create_data_tab(table_name)
    $('#' + table_name + '_tab_tag').click()


}

function turn_to_data_tab(table_name) {
    add_data_tab(table_name)
}
