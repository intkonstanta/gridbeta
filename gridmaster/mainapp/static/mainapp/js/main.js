document.querySelectorAll('tr').forEach((elem) => {
    elem.addEventListener('click', (event) => {
        preopenFile(event.target.parentElement)
    })
})

lastActive = 0;
function preopenFile(tr) {
    let tds = tr.querySelectorAll('td')
    if(tds.length == 0){
        tr = tr.parentElement
        console.log(tr)
        // если 0, то нажали на span about
        tds = tr.querySelectorAll('td')
    }
    if (tds[0].textContent == '#' || tds[0].textContent == lastActive) return;

    document.querySelector(".files__table-wrapper").querySelectorAll('tr')[lastActive].classList.remove('active');

    tr.classList.add('active')

    // let title = document.querySelector('.preview__title');
    // let lastEdit = document.querySelector('.preview__date');
    // let about = document.querySelector('.preview__about');

    // let change = [title, lastEdit, about]
    // for (let elem of change) {
    //     elem.style.opacity = '0'
    // }

    // setTimeout(() => {
    //     about.textContent = tds[3].textContent;
    //     title.textContent = tds[1].textContent;
    //     lastEdit.textContent = tds[2].textContent;

    //     for (let elem of change) {
    //         elem.style.opacity = '1'
    //     }
    // }, 550)


    lastActive = tds[0].textContent
}



// диаграммма

let procent = Math.floor(100 - document.querySelector('.procent').textContent);
procent = isNaN(procent) ? 100 : procent
let divProcent = document.querySelector('.cloud__procent');
divProcent.textContent = `${procent}%`;

let data = {
    datasets: [{
        data: [procent, 100 - procent],
        backgroundColor: [
            '#6d6b6b',
            '#4D4D4D',
        ],
        borderWidth: 0
    }]
};

let chartOptions = {
    plugins: {
        tooltip: {
            enabled: false,
            mode: false,

        },
    },
    responsive: true,
    maintainAspectRatio: false,
    showScale: false,
    rotation: -Math.PI * 50,
    cutout: '70%',
    circumference: Math.PI * 100,

};
const config = {
    type: 'doughnut',
    data: data,
    options: chartOptions,
};
var canvas = document.getElementById("diagram");
const diagram = new Chart(canvas, config)

canvas.style.height = '5rem'
canvas.style.width = '5rem'

function toggleCreateFileMenu(){
    document.querySelector('.create-menu').classList.toggle('show')
}

async function labelFile(){
    let file = document.querySelector('#upload-file');
    let label = document.querySelector('.upload-label')
    fileName = await file.files[0].name;
    label.textContent = fileName;
}

async function openPreview(elem){


    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
      }
      
    let title = elem.children[1].textContent;
    let file = {
        'title': title,
    }
    let csrf = getCookie('csrftoken');
    let response = await fetch('/mainapp/code_preview/', {
        method: 'POST',
        headers: {
          'X-CSRFToken': csrf,
          'Content-Type': 'application/json',
        },
        mode: "same-origin",
        body: JSON.stringify(file)
      });
    

    await fetch('/mainapp/code_preview/', {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrf,
    })
    .then( response => response.json())
    .then(info => {
        x = info;
        document.querySelector('.preview__wrap').classList.add('show');
        document.querySelector('.prev-section').classList.remove('show')
        let title = document.querySelector('.preview__title');
        let lastEdit = document.querySelector('.preview__edit');
        let about = document.querySelector('.preview__about');
        let size = document.querySelector('.preview__size');

        let load = document.querySelector(".preview__load");
        console.log(info)
        load.addEventListener("click", () =>{
            event.preventDefault()
            url = x.download_url
            fetch( url, {
                method: 'get',  
                mode:'no-cors',
                referrerPolicy: 'no-referrer'
            })
            .then(res => res.blob())
            .then(res => {
                console.log(res)
                a = document.querySelector('.load-a')
                a.download = "file.txt"
                url = URL.createObjectURL(res)
                a.href = url
                // a.target = '_blank'
                a.click();
              
                window.URL.revokeObjectURL(url)
            })
        })

        console.log(info)
        title.textContent = info.title
        lastEdit.textContent = `Last edit: ${info['date']}` 
        about.textContent = info.description
        size.textContent = `Size: ${info.size} byte`

        code = info.code_preview
        code = code.split('\n')

        let numCols = document.querySelector('.preview__num-cols')
        numCols.innerHTML = ""

        let codeText = document.querySelector('.preview__code-text');
        codeText.innerHTML = ""
        for (let i = 1; i <= code.length; i++){

            let num = document.createElement('div');
            num.classList.add('preview__num');
            num.textContent = i;
            
            numCols.append(num)

            let codeRow = document.createElement('div');
            codeRow.classList.add('preview__code-row');
            row = code[i-1].replace('  ', '\t')
            codeRow.innerHTML = row
            codeRow.style.paddingLeft = `${0.4 * (row.split('\t').length -1) }rem`
            // console.log(code[i-1].replace('  ', '\t'))
            codeText.append(codeRow)
        }

        })
    

      
   
}