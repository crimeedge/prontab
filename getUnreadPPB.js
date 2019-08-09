
let urls = [];
	let posts;
	posts = document.querySelectorAll(".unread ");

	posts.forEach(function(node){
		let href = node.getAttribute("href");
		let url = location.origin + href.slice(1);
		var req = $.ajax( {method: "POST", url:url,async: false});
		req.done(function(data) {
			let topic = $.parseHTML(data);
			let content;
			content = $(".content",topic);


			$("a",content).each(function(){
				let link = $(this).attr( "href" );
				if (link !== undefined) {
					if (link.indexOf("http") == 0) {
						urls.push(link);
					}
				}
			});
		});
	});
// noinspection JSAnnotator
return urls;
