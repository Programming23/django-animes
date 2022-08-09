var inp = vr('#inputEpisode')

inp.onkeyup =  function (){

        var inp = vr('#inputEpisode'),
        eps = vt('.num-es');
        

        for (i=0; i < eps.length;i++){
            var t = eps[i].innerHTML;

            if (t.indexOf(`${inp.value}`) != 0) {
                eps[i].parentElement.parentElement.style.display = 'none'; 
            }  
            
            else{
                eps[i].parentElement.parentElement.style.display = 'block';
            }
    
        }

}
