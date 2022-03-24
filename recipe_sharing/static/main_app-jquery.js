$(document).ready(function() {
    alert("Hello from main_app jQuery")

    $("#ingredient_input").keyup(function () {    
        alert( $("#ingredient_input").val() );

        var query = $(this).val();
        $.get("search/",
             {"ingredient_input": query}, 
             function(data) { 
                //  $("#recipe_search_results").html(data);
                alert(data);
             })
    });

    
});