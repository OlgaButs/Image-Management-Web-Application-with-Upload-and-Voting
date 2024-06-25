const btnMenu = document.querySelector('.btn-menu svg');
const navHeader = document.querySelector('.nav-header');
const btnCloseMenu = document.querySelector('.btn-close-menu');


$(document).ready(function()
{
  $("#registo").click(function() {window.location.replace("registo")});
  $("#login_btn").click(function() {
    var username = $("#username").val();
    var password = $("#password").val();
    if (username === "" || password === "") {
      alert("Missing username and/or password!");
    } else {
      $.post("/api/login", { username: username, password: password }, function(response) {
        if (response === "Login successful.") {
          window.location.replace("index");
        } else {
          alert(response);
        }
      });
    }
  });


  $("#register_btn").click(function() {
    var username = $("#username").val();
    var password = $("#password").val();
    var flag = $("#flexSwitchCheckDefault").prop("checked");
    if (username === "" || password === "") {
      alert("Missing username and/or password!");
    } else {
      $.post("/api/register", { username: username, password: password , flag: flag}, function(response) {
        console.log(response)
        if (response === "Registration successful.")
        {
          window.location.replace("index");
          alert("Account created successfully. Welcome in!"); 
        }
        else if (response === "Password Changed!")
        {
          window.location.replace("index");
          alert("Password changed successfully. Welcome in!"); 
        }
        else
        {
          alert(response);
        }
      });
    }
  });

  $("#sobre").click(function() {window.location.replace("sobre")} );
  $("#ua").click(function() {window.location.replace("ua")} );
  $("#login").click(function() {window.location.replace("login")} );

});