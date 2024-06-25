if ( getCookie("login_status") == "false" )
{
	$("#account").hide()
	$("#login").show()
}
else
{
	$("#account").show()
	$("#login").hide()
};

$(document).ready(function() {
								$("#home").click(function() {window.location.replace("index")});
								$("#gallery").click(function() {window.location.replace("gallery")});
								$("#upload").click(function() {window.location.replace("upload")});
								$("#about").click(function() {window.location.replace("sobre")});
								$("#ua").click(function() {window.location.replace("ua")});
								$("#process").click(function() {window.location.replace("process")});
								$("#login").click(function() {window.location.replace("login")});
								//$("#changePassword").click(function() {window.location.replace("changePassword")});
								$("#logout").click(function() {$.post("/api/logout"); window.location.replace("login")});
							});

function getCookie(cname)
{
	let name = cname + "=";
	let decodedCookie = decodeURIComponent(document.cookie);
	let ca = decodedCookie.split(';');
	for(let i = 0; i <ca.length; i++)
	{
		let c = ca[i];
		while (c.charAt(0) == ' ')
		{
			c = c.substring(1);
		}
		if (c.indexOf(name) == 0)
		{
			return c.substring(name.length, c.length);
		}
	}
	return "";
}