function display_update_table_page(table_name) {
	console.log(table_name)
	window.parent.layer.open({
		type: 2,
		title: '修改表单',
		shade: 0.5,
		skin: 'layui-layer-rim',
		area: ['95%', '92%'],
		shadeClose: true,
		content: './html/update_table.html',
		yes: function() {
			alert(table_name)
		}
	});
}

function turn_to_data_operate_page(table_name) {
	window.parent.turn_to_data_tab(table_name)
}

function turn_to_data_page() {
	let tags = $('.table_name_class')
	if (tags.length > 0) {
		for (let i = 0; i < tags.length; i++) {
			let tag = $(tags[i])
			if (!tag.hasClass('binding_click')) {
				tag.click(function() {
					let table_name = $($(this)[0]).attr('name')
					turn_to_data_operate_page(table_name)
				})
				tag.addClass('binding_click')
			}

		}
	}
}

function delete_table(table_name) {
	let alert_str = '确定要删除【' + table_name + '】吗？（同时删除表中数据！）'
	if (confirm(alert_str) === true) {
		delete_table_post(table_name)
		query_table_data()
	}
}

function click_delete_event() {
	let tags = $('.delete_table_a_tag')
	if (tags.length > 0) {
		for (let i = 0; i < tags.length; i++) {
			let tag = $(tags[i])
			if (!tag.hasClass('binding_click')) {
				tag.click(function() {
					let table_name = $($(this)[0]).attr('name')
					delete_table(table_name)
				})
				tag.addClass('binding_click')
			}

		}
	}
}

function check_cookies() {
	var url = window.parent.document.URL
	cookie = url.split('?')[1]
	if (typeof cookie === 'undefined' || cookie.length < 4) {
		window.parent.location.href = "../index.html"
	}
	var data = {
		'cookie': cookie
	}
	if (!check_cookies_valid(data)) {
		window.parent.location.href = "../index.html"
	}
}

function query_table_data() {
	check_cookies()
	let table_name = $('#table_name_input').val()
	$("#table").bootstrapTable('destroy');
	$('#table').bootstrapTable({
		method: "post",
		striped: true,
		singleSelect: false,
		url: "http://" + SERVER_IP + '/search_table_info',
		dataType: "json",
		pagination: true, //分页
		pageSize: 10,
		pageNumber: 1,
		search: false, //显示搜索框
		contentType: "application/x-www-form-urlencoded",
		queryParams: {
			'table_name': table_name
		},
		columns: [{
				title: "表名",
				field: 'TABLE_NAME',
				align: 'center',
				formatter: function(table_name, row) {
					return '<a    class="table_name_class" name="' + table_name + '">' + table_name + '</a> '
				}
			}, {
				title: "表注释",
				field: 'TABLE_COMMENT',
				align: 'center',
				valign: 'middle'
			},
			{
				title: '操作',
				field: 'TABLE_NAME',
				align: 'center',
				formatter: function(table_name, row) {
					return '<a   name="' + table_name + '" class="update_table_a_tag" >修改表单</a> ' // +
					// '<a   name="' + table_name + '" class="delete_table_a_tag">删除表单</a> '
				}
			}
		],
	});

}

function click_update_table_name_event() {
	let tags = $('.update_table_a_tag')
	if (tags.length > 0) {
		for (let i = 0; i < tags.length; i++) {
			let tag = $(tags[i])
			if (!tag.hasClass('binding_click')) {
				tag.click(function() {
					let table_name = $($(this)[0]).attr('name')
					window.parent.table_name = table_name
					display_update_table_page(table_name)
				})
				tag.addClass('binding_click')
			}

		}
	}
}

function interval_function() {
	turn_to_data_page()
	click_delete_event()
	click_update_table_name_event()
}

setInterval(interval_function, 1000)

function table_operate_function() {
	function display_create_table_page() {
		window.parent.layer.open({
			type: 2,
			title: '创建表单',
			shade: 0.5,
			skin: 'layui-layer-rim',
			area: ['95%', '92%'],
			shadeClose: true,
			content: './html/create_table.html'
		});
	}


	function event_binding() {
		$('#create_table_a_tag').click(display_create_table_page)
		$('#search_table_btn').click(query_table_data)
		$('#reset_search_btn').click(function() {
			$('#table_name_input').val('')
		})

	}


	function process_function() {
		event_binding()
		query_table_data()
	}

	process_function()

}

$(function() {
	table_operate_function()
})
