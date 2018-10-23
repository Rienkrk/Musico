// Gets an input, makes an ajax call which returns a list of phones and displays those in the view.
function myFunction(value) {

    $( "#results" ).empty();

    if(value != "") { 

      value = value.trim();
  
      // Make a ajax call with json, whom return a list of related phones.
        $.ajax({
          url: '/search/' + value,
          dataType: "json",
    
          // When succesfull run the respone function.
          success: function(response) {

            console.log(response)

            if (response.length > 0) {

              for(x in response){
                person = response[x]['name'].split('/').join('%2F');
                person = encodeURI(person);
                var html = "<li><a href=/"+response[x]['category']+"/" + person + ">"+response[x]['name']+"</a></li>"
                $("#results").prepend(html);
              }

            } else {
              var html = "<li>Geen resultaten gevonden</li>"
              $("#results").prepend(html);
            };
                
          },
          error: function(error) {

            var html = "<li>Er ging iets goed mis.</li>"
            $("#results").prepend(html);

          }
    
      });

    };
  
  };