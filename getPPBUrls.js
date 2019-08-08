/* GetphpBB URLs Version 1.0 */
/* javascript:(function()%7Bfunction callback()%7BGetphpBBUrlsSetup()%7Dvar s%3Ddocument.createElement("script")%3Bs.src%3D"https%3A%2F%2Fhairvids.ng-bvg.de%2Fvideos%2Fscripts%2FgetPPBUrls.js"%3Bif(s.addEventListener)%7Bs.addEventListener("load"%2Ccallback%2Cfalse)%7Delse if(s.readyState)%7Bs.onreadystatechange%3Dcallback%7Ddocument.body.appendChild(s)%3B%7D)() */
/* javascript:(function()%7Bfunction callback()%7BGetphpBBUrlsSetup()%7Dvar s%3Ddocument.createElement("script")%3Bs.src%3D"https%3A%2F%2Fraw.githubusercontent.com%2Fcrimeedge%2Fprontab%2Fmaster%2FgetPPBUrls.js"%3Bif(s.addEventListener)%7Bs.addEventListener("load"%2Ccallback%2Cfalse)%7Delse if(s.readyState)%7Bs.onreadystatechange%3Dcallback%7Ddocument.body.appendChild(s)%3B%7D)() */

function GetphpBBUrlsSetup(){

	let elSpacer = document.createElement("li");
	elSpacer.innerHTML = "&nbsp;&nbsp;&nbsp;";

	let elgetphpBB = document.createElement("li");


	let elUnreadCB = document.createElement("input");
	elUnreadCB.setAttribute("type","checkbox");
	elUnreadCB.setAttribute("id","GetphpBBUrls-unread");

	let elUnreadCBlb = document.createElement("label");
	elUnreadCBlb.setAttribute("for","GetphpBBUrls-unread");
	elUnreadCBlb.innerText = " Only unread Posts?"


	let elFirstPostCB = document.createElement("input");
	elFirstPostCB.setAttribute("type","checkbox");
	elFirstPostCB.setAttribute("checked","checked");
	elFirstPostCB.setAttribute("id","GetphpBBUrls-firstContent");

	let elFirstPostCBlb = document.createElement("label");
	elFirstPostCBlb.setAttribute("for","GetphpBBUrls-firstContent");
	elFirstPostCBlb.innerText = " Only first Post in Thread"


	let elThanksCB = document.createElement("input");
	elThanksCB.setAttribute("type","checkbox");
	elThanksCB.setAttribute("id","GetphpBBUrls-thanks");

	let elThanksCBlb = document.createElement("label");
	elThanksCBlb.setAttribute("for","GetphpBBUrls-thanks");
	elThanksCBlb.innerText = " Thanking each Poster??!?!?!?!?!?"


	let elGetphpBBUrlsBtn = document.createElement("button");
	elGetphpBBUrlsBtn.setAttribute("type","button");
	elGetphpBBUrlsBtn.setAttribute("class","button");
	elGetphpBBUrlsBtn.innerText = "Get URLs from Posts";


	elgetphpBB.append(elUnreadCB);
	elgetphpBB.append(elUnreadCBlb);
	elgetphpBB.append(elFirstPostCB);
	elgetphpBB.append(elFirstPostCBlb);
	elgetphpBB.append(elThanksCB);
	elgetphpBB.append(elThanksCBlb);

	elgetphpBB.append(elGetphpBBUrlsBtn);


	document.getElementById("nav-breadcrumbs").append(elSpacer);
	document.getElementById("nav-breadcrumbs").append(elgetphpBB);

	if (elGetphpBBUrlsBtn.addEventListener) {
		elGetphpBBUrlsBtn.addEventListener("click", GetphpBBUrlsRun, false);
	} else if (elGetphpBBUrlsBtn.attachEvent) {
		elGetphpBBUrlsBtn.attachEvent('onclick', GetphpBBUrlsRun);
	}

};
function toggleDim(){
	if (document.getElementById("GetphpBBUrls-overlay")) {
		document.getElementById("GetphpBBUrls-overlay").remove();
		document.getElementById("loading-indicator").style.display = "none";
	} else {
		document.getElementById("loading-indicator").style.display = "inline";
		let elDimm = document.createElement("div");
		elDimm.setAttribute("id","GetphpBBUrls-overlay");
		elDimm.style["background-color"] = "rgba(0,0,0,0.5)";
		elDimm.style.position = "fixed";
		elDimm.style.left = "0";
		elDimm.style.top = "0";
		elDimm.style.width = "100%";
		elDimm.style.height = "100%";
		document.getElementsByTagName("body")[0].append(elDimm);
	}
}

function GetphpBBUrlsRun(){
	toggleDim();
	let urls = [];
	let posts;
	if (document.getElementById("GetphpBBUrls-unread").checked){
		posts = document.querySelectorAll(".unread ");
	} else {
		posts = document.querySelectorAll(".topictitle ");
	}

	const thanking = document.getElementById("GetphpBBUrls-thanks").checked;

	posts.forEach(function(node){
		let href = node.getAttribute("href");
		let url = location.origin + href.slice(1)
		var req = $.ajax( {method: "POST", url:url,async: false});
		req.done(function(data) {
			let topic = $.parseHTML(data);
			let content;
			if (document.getElementById("GetphpBBUrls-firstContent").checked){
				content = $(".content",topic)[0];
			} else {
				content = $(".content",topic);
			}

			$("a",content).each(function(){
				let link = $(this).attr( "href" );
				if (link !== undefined) {
					if (link.indexOf("http") == 0) {
						urls.push(link);
					}
				}
			});
			if (thanking) {
				let parent = content.parentElement;
				$("a",parent).each(function(){
					let id = $(this).attr( "id" );
					if (id !== undefined) {
						if (id.indexOf("lnk_thanks_") >= 0){
							let href = $(this).attr( "href" );
							let url = location.origin + href.slice(1)
							$.ajax( {method: "POST", url:url,async: false});
						}
					}
				});
			}
		});
	});
	let today = new Date();
	let date = today.getFullYear() + '-' + (today.getMonth() + 1) + '-' + today.getDate();
	let time = today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();
	let FileNameTime = today.getHours() + "-" + today.getMinutes() + "-" + today.getSeconds();
	let FileNamedateTime = date + "_" + FileNameTime;
	let dateTime = date + " " + time;
	header="##########################################\n# Urls in Posts of Page:\n# " + document.title + "\n# (" + document.baseURI + ")\n# Created at: " + dateTime + "\n# Links found: " + urls.length + "\n##########################################\n";
	toggleDim();
	GetphpBBUrlsDownload("urls from " + document.domain + " " + FileNamedateTime + ".txt",header + urls.join("\n"));
};


function GetphpBBUrlsDownload(filename, text) {
  var element = document.createElement('a');
  element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
  element.setAttribute('download', filename);

  element.style.display = 'none';
  document.body.appendChild(element);

  element.click();

  document.body.removeChild(element);
}
