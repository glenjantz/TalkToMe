
$(document).ready(function(){
    var DIV = $('#thisdiv').get(0);
    DIV.scrollTop = DIV.scrollHeight;
    setInterval(function(){
        $('#mydiv').load('templates/talktome/chat.html' + '#thisdiv');
        console.log('hi');
    }, 1500);

});
