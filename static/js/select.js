class multiSelect{

    makeElements(){
        this.selecteds = document.createElement('ul');
        this.selecteds.classList = 'selecteds';
        this.selecteds.innerHTML += `<input type="search" class="multi-select-search" placeholder="${this.title}">`
        this.search = this.selecteds.lastElementChild;

        this.listSelect = document.createElement('div') ;
        this.listSelect.classList = 'list-select ds-none';

        this.parent.appendChild(this.selecteds);
        this.parent.appendChild(this.listSelect)
    }

    actionSearch(){
        this.search.onkeyup = (e) => {
            this.value = this.search.value;
            var children = this.listSelect.children ;
            for(var i=0; i < children.length; i++){
                if (children[i].textContent.indexOf(this.value) == -1){
                    children[i].style.cssText = 'display: none;'
                }else{
                    children[i].style.cssText = 'display: block;'
                }
            }
        }
    }

    removeSelectedOption(option, key){
        option.selected = false;
        var itemSelect = document.querySelector(`#${this.parent.id} > .list-select > .item-select[key="${key}"]`);
        itemSelect.classList.remove('active-option')
        var selected = document.querySelector(`#${this.parent.id} > .selecteds > li[key="${key}"]`)
        selected.remove()
    }

    addSelectedOption(option, key){
        option.selected = true;
        var item = document.querySelector(`#${this.parent.id} > .list-select > .item-select[key="${key}"]`);
        item.classList.add('active-option')
        var selected = document.createElement('li');
        selected.innerHTML = `<span>${item.textContent}</span>`;
        selected.setAttribute('key', key);

        var times = document.createElement('i');
        times.classList = 'fas fa-times';
        times.onclick = (e) => {
            selected = e.target.parentElement
            selected.remove()
            var itemSelect = document.querySelector(`#${this.parent.id} > .list-select > .item-select[key="${selected.getAttribute('key')}"]`);
            itemSelect.classList.remove('active-option')

            option = document.querySelector(`#${this.parent.id} > select `).children[selected.getAttribute('key')];
            option.selected = false;
        }
        selected.appendChild(times)
        this.selecteds.appendChild(selected)
    }

    constructor (selector, title, auto_value=true){
        this.auto_value = auto_value;
        this.selector = selector;
        this.title = title;
        this.parent = document.getElementById(this.selector);
        this.select = document.querySelector(`#${this.selector} > select`)
        this.options = this.select.children ;
        
        this.makeElements()
        this.actionSearch()

        for (var i = 0; i < this.options.length; i++) {
            if (this.auto_value == true){
                this.options[i].value = this.options[i].textContent ;
            }
            var item = document.createElement('div')
            item.classList = 'item-select';
            item.setAttribute('key', i.toString())
            item.textContent = this.options[i].textContent;
            this.listSelect.appendChild(item)
            if (this.options[i].selected == true){
                this.addSelectedOption(this.options[i], i.toString())
            }

            item.onclick = (e) => {
                var key = e.target.getAttribute('key')
                var option = this.options[key]
                
                if (option.selected == true){
                    this.removeSelectedOption(option, key)
                }else{
                    this.addSelectedOption(option, key)
                }
                
            };

            
            // <span>${options[i].textContent}</span><i class="fas fa-times"></i>
        }

        
        this.parent.onclick = (e) => {
            this.listSelect.classList.toggle('ds-none')
        }
    }
    

    
}

class SelectSingle{

    initialElements(){
        this.selected.textContent = this.options[0].textContent ;
        
        for (var i=0; i < this.options.length; i++){
            if (this.auto_value == true){
                this.options[i].value = this.options[i].textContent;
            }

            if (this.options[i].selected == true){
                this.selected.textContent = this.options[i].textContent
            }

            var li = document.createElement('li')
            var item = document.createElement('span') ;
            if (i == 0){
                item.classList.add('active-option')
            }
            item.setAttribute('key', i)
            item.textContent = this.options[i].textContent

            item.onclick = (e) => {
                var option = document.querySelectorAll(`#${this.selector} .active-option`)
                if (option.length > 0){
                    option[0].classList.remove('active-option')
                }

                this.selected.textContent = e.target.textContent ;
                this.select.selectedIndex = e.target.getAttribute('key')
                e.target.classList.add('active-option')
            }
            li.appendChild(item)
            this.list.appendChild(li) ;
        }


    }

    constructor (selector, auto_value=true){
        this.auto_value = auto_value;
        this.selector = selector ;
        this.parent = document.getElementById(selector);
        this.select = document.querySelector(`#${selector} > select`)
        this.options = this.select.children ;
        this.selected = document.querySelector(`#${selector} > div.button-select`) ;
        this.list = document.querySelector(`#${selector} > ul.list-dropdown`)

        this.initialElements();
    }
}