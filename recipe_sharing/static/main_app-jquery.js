$(document).ready(function() {
    alert("Hello from main_app jQuery")

    //could not figure out how to fix this to work via AJAX
    //currently search only work via URL, eg: "/search/?ingredient_input=p"
    $("#ingredient_input").keyup(function () {    
        alert( $(this).val());

        var query = $(this).val();
        $.get("search/",
             {"ingredient_input": query}, 
             function(data) { 
                //  $("#recipe_search_results").html(data);
                alert(data);
             })
    });

    
});