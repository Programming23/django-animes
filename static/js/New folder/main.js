
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

document.body.addEventListener('click', bodyClick)

var def = null

function bodyClick(e){
    

    if (e.target.classList == 'btn btn-default dropdown-toggle'){

        btn = e.target
        if (def != null && btn != def){
            def.nextElementSibling.classList.remove('dropdown-menu-custom')
        }      

        btn.nextElementSibling.classList.toggle('dropdown-menu-custom')       
        
        def = btn
    }


    
}

vr('#label-search-navbar').onclick = function (){
    vr('#search-navbar').classList.toggle('ds-none-2')      
}
