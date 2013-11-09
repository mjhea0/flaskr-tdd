$(function() {
  console.log( "ready!" );
  $('.entry').on('click', function(){
  	$(this).remove();
  });
});