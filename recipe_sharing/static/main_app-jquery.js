$(document).ready(function() {
    //alert("Hello from main_app jQuery")

    $("#ingredient_input").keyup(function () {    
        //alert( $(this).val());

        var query = $(this).val();
        $.get("",
             {"ingredient_input": query}, 
             function(data) { 
                $("#recipe_search_results").html($(data).filter("#recipe_search_results")); //.get("recipe_search_results")
                console.log($(data).filter("#recipe_search_results"));
             })
    });

    
});