
const searchIcon = document.getElementById('seachIcon');

function showFormNavbar(e) {
    nav = document.getElementById('navbar-mes');
    nav.classList.toggle('show-form')
}

function ShowDropDown(id) {
    drop = document.getElementById(id)
    drop.classList.toggle('ds-none') 
}

function showNavbarList(e, submit=true) {
    this.onsubmit = (e) => e.preventDefault();

    const nav = document.getElementById('navbar-list');
    nav.classList.toggle('hide-list')
}

theme = localStorage.getItem('theme')
body = document.getElementById('body')

if (theme != 'dark' && theme != 'light') {
    localStorage.setItem('theme', 'dark')
    theme = localStorage.getItem('theme')
}
body.classList = theme

function changeTheme(e) {
    if (body.classList.contains("dark")) {
        body.classList = 'light'
        localStorage.setItem('theme', 'light')
    } else if (body.classList.contains("light")) {
        body.classList = 'dark'
        localStorage.setItem('theme', 'dark')
    }
}

function GoToLink(ele){
    link = document.createElement('a');
    link.href = ele.getAttribute('link')
    link.click()
}

function hideDropDown(id, target){
    dr = document.getElementById(id);
    if (dr == null){
        return 
    }

    button = dr.previousElementSibling;
    children = button.children;

    if (dr.classList == 'list-dropdown') {
        if (target == button){
            return 
        }
        for(i=0; i < children.length; i++){
            if (children[i] == target){
                return 
            }
        }
        ShowDropDown(id)
    }
}

function hideListSelects(e) {
    ls = document.getElementsByClassName('list-select') ;
    for(i=0; i<ls.length; i++){
        
        if (ls[i].classList == 'list-select' ){
            
            parent = ls[i].parentElement
            if (parent == e.target){
                return 
            }
            
            children = parent.children ;
            for(var ind=0; ind<children.length; ind++){
                if (children[ind] == e.target){
                    return 
                }
            }
            children = ls[i].previousElementSibling.children
            for(var ind=0; ind<children.length; ind++){
                if (children[ind] == e.target){
                    return 
                }
            }
            ls[i].classList.add('ds-none')
        }
        
    }
}

body.onclick = function(e) {
    lists = document.getElementsByClassName('list-dropdown');
    for(i=0;i<lists.length; i++){
        hideDropDown(lists[i].id, e.target)
    }
    
    hideListSelects(e)
       
}


function media(){
    width = window.innerWidth
    cards = document.querySelectorAll('.item-card')
    parent_imgs = document.querySelectorAll('.conatainer-img-card')
    
    

    if (width <= 600){
        width = (width/2)-25
        var height = width*1.3
        cards.forEach(element => {
            element.style.cssText = `width: ${width}px; `
        });
        for(i=0;i<parent_imgs.length;i++){
            parent_imgs[i].style.cssText = `height: ${height}px;`
        }
    }
    else{
       
        for(i=0;i<parent_imgs.length;i++){
            parent_imgs[i].style.cssText = ''
            cards[i].style.cssText = ''
        }
    }
}   

function clk_server(self) {
    var iframe = document.querySelector('.vd')
    data = self.getAttribute('data')
    if (!self.classList.contains('activate-server') && data != iframe.src) {
        document.querySelector('.activate-server').classList.remove('activate-server')
        self.classList.add('activate-server')
        iframe.src = data
    }
}

function wstory() {
    var story = document.querySelector("#story")
    var text = story.textContent
    story.innerHTML = text
}


function EpisodesSearch(){
    var inp = document.querySelector("#inputEpisodeProfile")
    eps = document.querySelectorAll('.nmb');
    

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