$(function() {
  console.log( "ready!" );
  $('.entry').on('click', function(){
  	//$(this).remove();
  	var entry = this;
  	var post_id = $(this).find('h2').attr('id');
  	$.ajax({
  		type:'GET',
		  url: '/delete' + '/' + post_id,
  		context: entry,
  		success:function(result){
  			if(result['status'] === 1){
  				$(this).remove();
  				console.log(result);
  			}
        /*else{
  				$('.status').show();
          $('.flash').text('Post not deleted');
  			}*/
  		}
  	});
  });
});