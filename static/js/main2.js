function vr(text){
    return document.querySelector(text)
}

function vt(text){
    return document.querySelectorAll(text)
}


function cral(text){
    return document.createElement(text);
}


function crtx(text){
    return document.createTextNode(text);
}


var btn_nvb = vr("#navbar-seach-control")
var nvb_ser = vr("div#navbar-container-search")
var drk = vr("#navbar-lbl-dark")
var body = vr("body")

function SearchNavbar(){
    nvb_ser.classList.toggle('ds-none') 
}

lck = localStorage.getItem('theme')

if (lck != 'dark' && lck != 'light' ){
	localStorage.setItem('theme', 'dark')
	lck = localStorage.getItem('theme')
}
body.classList = lck

drk.onclick = function (){
    if (body.classList.contains("dark")){
        body.classList = 'light'
		localStorage.setItem('theme', 'light')
    }
    else if(body.classList.contains("light")){
        body.classList = 'dark'
		localStorage.setItem('theme', 'dark')
    }
}

function gear(){
    var dr = vr("#dropdown-gear")
    var bt = vr("#navbar-lbl-gear")
    if (dr.classList.contains("ds-none")){
        dr.classList.remove("ds-none")
        if (bt.attributes[1].name != 'ch'){
			bt.style.cssText = 'background: #424040;'
		}
    }
    else{
        dr.classList.add("ds-none")
        if (body.classList == 'dark' && bt.attributes[1].name != 'ch'  ){
            bt.style.cssText = ''
        }
    }
}

function list(id){
	var d = vr(id)
	d.classList.toggle('ds-none')
}


body.onclick = function(e){
    var dr = vr("#dropdown-gear")
	var d =  vr("#dropdown-list")

    if ( dr.classList == 'dropdown-menu' && e.target.id != 'navbar-lbl-gear' && e.target.id != 'navbar-i-gear'  ){
        gear()
    }
	if (d != null && !d.classList.contains("ds-none") == true && e.target.id != 'btn-dropdown-list'){
		d.classList.add('ds-none')
	}
}




function EpisodesSearch(){
    var inp = vr("#inputEpisodeProfile")
    eps = vt('.nmb');
    

    for (i=0; i < eps.length;i++){
        var t = eps[i].innerHTML;

        if (t.indexOf(`${inp.value}`) != 0) {
            eps[i].parentElement.style.display = 'none'; 
        }  
        
        else{
            eps[i].parentElement.style.display = 'flex';
        }

    }

}