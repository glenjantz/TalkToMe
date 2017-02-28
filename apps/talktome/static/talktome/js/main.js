
$(document).ready(function(){
    var DIV = $('#thisdiv').get(0);
    DIV.scrollTop = DIV.scrollHeight;
    setInterval(function(){
        $('#thisdiv').load('/chatroom #thisdiv');
        console.log('hi');
    }, 1500);

});
