
$(document).ready(function(){
  var DIV1 = $('#thisdiv').get(0);
  DIV1.scrollTop = DIV1.scrollHeight;
    setInterval(function(){
        // $('#thisdiv').html();
        // event.preventDefault();
        // $('#thisdiv').animate({
        $('#outerdiv').load('/chatroom #thisdiv', function(){
          var DIV2 = $('#thisdiv').get(0);
          DIV2.scrollTop = DIV2.scrollHeight;
        });
        //   background-color: white,
        // });
        // $('#thisdiv').load('/chatroom' +' #thisdiv');
        // $('#thisdiv').get('#thisdiv');
        // var DIV1 = document.getElementById('thisdiv');
        // DIV1.scrollTop = DIV1.scrollHeight
        // var DIV1 = $('#thisdiv').get(0);
        // DIV1.scrollTop = DIV1.scrollHeight - DIV1.clientheight;
        // $('#thisdiv').load('/chatroom');
        // var DIV = $('#thisdiv').get(0);
        // DIV.scrollTop = DIV.scrollHeight;
        console.log('hi');
    }, 1500);

});
