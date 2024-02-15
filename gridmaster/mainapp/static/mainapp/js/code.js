let squareCount = 21;
let horizontal = document.querySelector('.editor__horizontal');
let vertical = document.querySelector('.editor__vertical');
let gapGrid = (800 - 3 * squareCount) / 32 / squareCount;
let gapGridRem = `${gapGrid}rem`
let ant = document.querySelector('.ant')
ant.style.height = `${gapGrid - 0.225}rem`
ant.style.width = `${gapGrid - 0.225}rem`
ant.style.top = `${25.06 - gapGrid}rem`
ant.style.left = `${0.19}rem`
// ant.style.top = `${(gapGrid * squareCount - gapGrid) / 2 + (squareCount + 1) / 20}rem`
// ant.style.right = `${(gapGrid * squareCount - gapGrid) / 2 + (3 * squareCount + 3) / 64 - gapGrid / 4}rem`
horizontal.style.gap = gapGridRem
vertical.style.gap = gapGridRem
horizontal.style.paddingTop = gapGridRem;
vertical.style.paddingLeft = gapGridRem


for (let i = 0; i < squareCount; i++) {
    line = document.createElement('div');
    line.classList.add('line');
    horizontal.append(line);
    line = document.createElement('div');
    line.classList.add('line');
    vertical.append(line);
}

let valueTextArea;
let countRows;

function editTextarea(textarea) {
    valueTextArea = textarea.value;
    let rows = valueTextArea.split('\n')

    countRows = valueTextArea.split('\n').length;

    let maxLenRow = 0;
    for (let i = 0; i < countRows; i++) {
        if (rows[i].length > maxLenRow) {
            maxLenRow = rows[i].length;
        }
    }



    numRows = document.querySelector('.editor__code-numrows');
    numRows.style.height = `${1.5 * countRows}rem`;

    textarea.style.height = `${1.5 * countRows}rem`;
    textarea.style.width = `${0.5 * maxLenRow}rem`;
    // document.querySelector('.editor__code-area').style.width = `${0.5 * maxLenRow}rem`;
    if (countRows > numRows.children.length) {
        numRows.innerHTML = '';
        for (let i = 1; i <= countRows; i++) {

            let div = document.createElement('div');
            div.textContent = i
            numRows.append(div)
        }
    }
}

function saveTextareaAsTxt(){
    let textarea = document.querySelector('#code-area');
    let file = new Blob([textarea.value],{type: 'text/plain'})

    url = URL.createObjectURL(file);

    let a = document.querySelector('.saveTextArea')
    a.href = url
    a.click()
    
    URL.revokeObjectURL(url);  
}

function toggleExitAndSave(){
    let menu = document.querySelector('.exit-menu')

    menu.classList.toggle('show')
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
  }



let stop = []
trueStop = false
async function startAnimationAnt(name){
    let elem = document.getElementsByName('start')[0]
    elem.onclick = ""
    stop.push('')
    startTabs = true
    textTabs()
    let title = document.querySelector('.main-title__name').textContent;
    let csrf = getCookie('csrftoken');

    let result = await postCode("start")


    await fetch(`/mainapp/get_rendered_code/`, {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrf,
    })
    .then( responce => responce.json())
    .then(coords => {
        coords = JSON.parse(coords)
        let logs = document.querySelector('.log__data')
        logs.innerHTML = ""
        stop.pop()
        if (coords.Error){
            let span = document.createElement('span')
            span.textContent = coords.Error
            span.classList.add('error');
            logs.append(span)
            elem.onclick = startAnimationAnt
            throw new Error
        }

        let ant = document.querySelector('.ant');
        ant.style.transition = "none"
        ant.style.top = `${25.06 - gapGrid}rem`
        ant.style.left = `${0.19}rem`
        ant.style.transform = "rotate(0deg)"

        setTimeout( () => {

        ant.style.transition = "0.6s all ease"
        
        let topp = 25.06 - gapGrid
        let leftt = 0.19;

        tops = []
        lefts = []
        rotates = []
        corStep = []
        let len = Object.values(coords).length
        let current = [0,0]

        for(let i = 1; i < len; i++){
            now = coords[i]
            corStep.push(coords[i])
            delta = [now[0] - current[0], now[1] - current[1]]

            console.log('delta', delta)
            current = now;
            vector = delta.map( (n) =>{
                return n > 0 ? 1: n < 0 ? -1 : 0
            })
            console.log('vector', vector)
            if(vector.toString() == [0,1]){
                rotates.push("0deg")
            } else if( vector.toString() == [1,0] ){
                rotates.push("90deg")
            } else if( vector.toString() == [-1,0] ){
                rotates.push("-90deg")
            } else{
                rotates.push("180deg")
            }
            topp = topp - (delta[1] * gapGrid + delta[1] * 0.09375)
            tops.push(topp)
            leftt = leftt + (delta[0] * gapGrid + delta[0] * 0.09375)
            lefts.push(leftt)
           
        
        }

        function f() {
            if(i >= tops.length || stop.length > 0 || trueStop){ 
                stop.pop()
                if(trueStop){
                    trueStop = false;
                    let span = document.createElement('span')
                    span.textContent = "---Stop---"
                    logs.append(span)
           
                }
                return
            };

            ant.style.transform = `rotate(${rotates[i]})`
            setTimeout( () =>{

          
            ant.style.top = `${tops[i]}rem`
            ant.style.left = `${lefts[i]}rem`;
            
            let span = document.createElement('span')
            span.textContent = `x, y | ${corStep[i][0]} ${corStep[i][1]}`
            logs.append(span)
            ++i;
            setTimeout(f, 1000);
        }, 600)
          }
          var i = 0;
          f();
          elem.onclick = startAnimationAnt
    }, 1000)
    })
    



}

async function saveExit(name){
    
    let result = await postCode(name)

    document.location = "/mainapp/project_manager/"
}

async function postCode(name){

      let csrf = getCookie('csrftoken');

      let textarea = document.querySelector('#code-area').value
      let title = document.querySelector('.main-title__name').textContent;
      
      let obj = {
        "title": title,
        "code": textarea,
        "parent": name,
      }

      let response = await fetch(`/mainapp/code_editor/${title}/`.replaceAll(' ', ''), {
        method: 'POST',
        headers: {
          'X-CSRFToken': csrf,
          'Content-Type': 'application/json',
        },
        // mode: "same-origin", 
        body: JSON.stringify(obj)
    })

    return response;
}


window.onload = () =>{
    editTextarea(document.querySelector('#code-area'))
    console.log('x')
}



// табуляция

lastkey = ""
startTabs = false
document.addEventListener('keydown', textTabs)

function textTabs(){

    if(lastkey == "Alt" && event.key == "t" || startTabs){
        startTabs = false;
        let textarea = document.querySelector('#code-area')
        let code = textarea.value

        code = code.split('\n')
        codeTabs = []
        tcount = 0
        stack = []

        for (let i = 0; i<code.length; i++){
            row = code[i]
            row = row.split(' ')

            row[0] = row[0].replaceAll("\t", "")

            rowTabs = row.join(" ")
            
            let firstWord = row[0]

            if (row.indexOf("endrepeat") != -1 || firstWord == "endproc" || firstWord == "endif" || firstWord == "else"){
                tcount-=1
    
            }

            for (let j = 0; j < tcount; j++){
                rowTabs = '\t' + rowTabs
            }
            
            codeTabs.push(rowTabs)
            console.log
            if(row.indexOf("repeat") != -1 || row.indexOf("procedure") != -1 || row.indexOf("ifblock") != -1 ||  row.indexOf("else") != -1){
                tcount+=1
                console.log(tcount)
                if(tcount > 3){
                    tcount = 0;
                    let logs = document.querySelector('.log__data');
                    logs.innerHTML = ""
                    let span = document.createElement('span')
                    span.classList.add('error')
                    span.textContent = "Error - The number of nested structures has been exceeded"
                    logs.append(span)
                    throw new Error
                }
                if(firstWord!="else") stack.push(firstWord)
            }

            if(firstWord == "endrepeat" && stack[stack.length - 1] == "repeat") stack.pop()
            else if(firstWord == "endproc" && stack[stack.length - 1] == "procedure") stack.pop()
            else if(firstWord == "endif" && stack[stack.length - 1] == "ifblock") stack.pop()
        }
        
        if(stack.length == 0){
            textarea.value = codeTabs.join('\n')
        }
        
    }

    lastkey = event.key
}