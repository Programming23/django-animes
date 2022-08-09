

function remove_activate(){
	var li = document.querySelectorAll("#dropdown-list-add li")
	for(i=0; i < li.length;i++ ){
		li[i].style.cssText = ''
	}
	
}

var want = $("#want")
var done = $("#done")
var now = $("#watching")
var later = $("#later")
var dont = $("#dropped")
var dl = $("#delete-from-list")
var fav = $("#btn-fav")

want.click(function(){
	remove_activate()
	document.querySelector("#delete-from-list").style.cssText = ''
	$.ajax({
		'url': want.attr("url"),
		'type': 'get',
		success: function(response){
			want.attr("style", 'background: #ffcece;')
			
		}
	})
})

done.click(function(){
	remove_activate()
	$("#delete-from-list").attr("style", "")
	$.ajax({
		'url': done.attr("url"),
		'type': 'get',
		success: function(response){
			done.attr("style", 'background: #ffcece;')
		}
	})
})


now.click(function(){
	remove_activate()
	$("#delete-from-list").attr("style", "")
	$.ajax({
		'url': now.attr("url"),
		'type': 'get',
		success: function(response){
			now.attr("style", 'background: #ffcece;')
		}
	})
})

later.click(function(){
	remove_activate()
	$("#delete-from-list").attr("style", "")
	$.ajax({
		'url': later.attr("url"),
		'type': 'get',
		success: function(response){
			later.attr("style", 'background: #ffcece;')
		}
	})
})

dont.click(function(){
	remove_activate()
	$("#delete-from-list").attr("style", "")
	$.ajax({
		'url': dont.attr("url"),
		'type': 'get',
		success: function(response){
			dont.attr("style", 'background: #ffcece;')
		}
	})
})


dl.click(function(){
	remove_activate()
	
	$.ajax({
		'url': dl.attr("url"),
		'type': 'get',
		success: function(response){
			dl.attr("style", "display: none;")
		}
	})
})


fav.click(function(){
	$.ajax({
		'url': fav.attr("url"),
		'type': 'get',
		success: function(response){
			if (response.res == true){
				fav.attr("style", 'background: #ffcece')
				document.querySelector("#btn-fav").innerHTML = "تمت الإضافة لأنمياتي المفضلة"
			}
			else{
				fav.attr("style", '')
				document.querySelector("#btn-fav").innerHTML = '<i class="fa fa-plus"></i>\nإضافة لأنمياتي المفضلة'
			}
		}
	})
})