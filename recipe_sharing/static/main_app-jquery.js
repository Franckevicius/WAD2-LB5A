$(document).ready(function() {
    alert("Hello from main_app jQuery")

    $("#ingredient_input").keyup(function () {    
        alert( $("#ingredient_input").val() );
    });
});