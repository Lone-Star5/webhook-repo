setTimeout(() => {
    window.location.reload();
}, 15000);

let tm1 = document.getElementsByClassName('bi-chevron-double-right').item(0)
let symb = tm1.cloneNode(true);
symb.style.display='inline';

sym = document.createElement('div');
sym.style.width="10px";
sym.style['margin-left']="30px";
sym.classList.add('col-sm-1');
sym.appendChild(symb);

let ulPush = document.getElementById('PUSH');
let ulPull = document.getElementById('PULL');
let ulMerge = document.getElementById('MERGE');

fetch('/display',{
    method:'post',
    headers: {
        "Content-type": "application/x-www-form-urlencoded; charset=UTF-8"
    },
}).then((res)=>res.json()).then((data)=>{
    for(item in data){
        let {action,author,to_branch,from_branch,timestamp} = data[item]
        timestamp = new Date(timestamp.$date)
        if(action=="PUSH"){
            let div1 = document.createElement('div');
            div1.classList.add('row');
            let div2 = document.createElement('div');
            div2.classList.add('mt-0')
            div2.classList.add('li-element')
            div2.classList.add('col-sm')
            let text = `"${author}" pushed to "${to_branch}" on ${timestamp}`;
            div2.innerText = text
            div1.appendChild(sym.cloneNode(true));
            div1.appendChild(div2);
            ulPush.appendChild(div1)
        }
        else if(action=="PULL_REQUEST"){
            let div1 = document.createElement('div');
            div1.classList.add('row');
            let div2 = document.createElement('div');
            div2.classList.add('mt-0')
            div2.classList.add('li-element')
            div2.classList.add('col-sm')
            let text = `"${author}" submitted a pull request from "${from_branch}" to "${to_branch}" on ${timestamp}`;
            div2.innerText = text
            div1.appendChild(sym.cloneNode(true));
            div1.appendChild(div2);
            ulPull.appendChild(div1)
        }
        else if(action=="MERGE"){
            let div1 = document.createElement('div');
            div1.classList.add('row');
            let div2 = document.createElement('div');
            div2.classList.add('mt-0')
            div2.classList.add('li-element')
            div2.classList.add('col-sm')
            let text = `"${author}" merged branch "${from_branch}" to "${to_branch}" on ${timestamp}`;
            div2.innerText = text
            div1.appendChild(sym.cloneNode(true));
            div1.appendChild(div2);
            ulMerge.appendChild(div1)
        }
    }   
})