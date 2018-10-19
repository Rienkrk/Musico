// Gets an input, makes an ajax call which returns a list of phones and displays those in the view.
function myFunction(value) {

    // Trim the given value.
      value = value.trim();
  
      // Empty the html view list.
    //   $(".search-drop").empty();
    //   $(".results").empty();
  
    // Make a ajax call with json, whom return a list of related phones.
      $.ajax({
        url: '/search/' + value,
        dataType: "json",
  
        // When succesfull run the respone function.
        success: function(response) {

          $( "#results" ).empty();

          // console.log(response)

          for(x in response){
            console.log(response[x])
            
            var html = "<li>"+response[x]['name']+"</li>"
            $("#results").prepend(html);
          }
            
            
  
        },
        error: function(error) {
          
          $( "#results" ).empty();
          console.log(error)

        }
  
    });
  
  };