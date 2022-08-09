var inp = vr('#inputEpisodeProfile')

inp.onkeyup =  function (){
        
        eps = vt('.num-es');
        

        for (i=0; i < eps.length;i++){
            var t = eps[i].innerHTML;

            if (t.indexOf(`${inp.value}`) != 0) {
                eps[i].parentElement.parentElement.parentElement.parentElement.parentElement.style.display = 'none'; 
            }  
            
            else{
                eps[i].parentElement.parentElement.parentElement.parentElement.parentElement.style.display = 'block';
            }
    
        }

}