$(document).ready(function() {
  countrylist = $.get('https://restcountries.eu/rest/v2/all', function() {
    for(var i in countrylist.responseJSON) {
     if(countrylist.responseJSON[i]['name'] != "United States of America" && countrylist.responseJSON[i]['name'] != "Russian Federation"){
      $('#dropdown').append("<option name= '"+countrylist.responseJSON[i]['name']+"' value= '"+countrylist.responseJSON[i]['name']+"' >"+countrylist.responseJSON[i]['name']+"</option>");
    }
  }
  }, "json");
});
