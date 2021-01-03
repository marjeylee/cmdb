function check_login_is_success() {
	var username = $('#username').val()
	var password = $('#password').val()
	// var input_check_code = $('#check_code').val()
	// var code = $('#code').val()
	if (username.length === 0 || password.length === 0) {
		alert('请输入账号、密码')
		return
	}
	// if (code !== input_check_code) {
	// 	alert('验证码错误')
	// 	return
	// }
	var data = {
		'username': username,
		'password': password
	}
	var login_cookie = query_login_info(data)
	return login_cookie
}

function ready_function() {
	$('#login_btn').click(function() {
		var login_cookie = check_login_is_success()
		if (login_cookie.length < 3) {
			alert('账号密码校验失败')
			return
		}
		window.location.href = "main.html?" + login_cookie
	})

}
$(document).ready(function() {
	ready_function()
})
