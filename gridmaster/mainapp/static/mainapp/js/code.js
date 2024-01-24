let squareCount = 21;
let horizontal = document.querySelector('.editor__horizontal');
let vertical = document.querySelector('.editor__vertical');
let gapGrid = (800 - 3 * squareCount) / 32 / squareCount;
let gapGridRem = `${gapGrid}rem`
let ant = document.querySelector('.ant')

ant.style.height = gapGridRem;
ant.style.width = gapGridRem;
ant.style.top = `${12.6 - gapGrid / 2}rem`
ant.style.left = `${12.65 - gapGrid / 2}rem`
// ant.style.top = `${(gapGrid * squareCount - gapGrid) / 2 + (squareCount + 1) / 20}rem`
// ant.style.right = `${(gapGrid * squareCount - gapGrid) / 2 + (3 * squareCount + 3) / 64 - gapGrid / 4}rem`
horizontal.style.gap = gapGridRem
vertical.style.gap = gapGridRem



for (let i = 0; i < squareCount; i++) {
    line = document.createElement('div');
    line.classList.add('line');
    horizontal.append(line);
    line = document.createElement('div');
    line.classList.add('line');
    vertical.append(line);
}

// let activeDiv;
// let activeNum;
// function toTextarea(div) {
//     document.querySelector('#code-area').focus()

//     activeDiv = div;
//     div.classList.add('active');

//     let codeArea = document.querySelector('.editor__code-area').children;
//     codeArea = Array.from(codeArea);
//     indexActive = codeArea.indexOf(activeDiv)

//     let numRows = document.querySelector('.editor__code-numrows').children;
//     activeNum = numRows[indexActive]
//     activeNum.classList.add('active')
// }

// function divChange() {
//     let value = document.querySelector('#code-area').value;
//     activeDiv.querySelector('.editor__row-text').textContent = value;

// }

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
    // textarea.style.width = `${0.5 * maxLenRow}rem`;
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

// function scrollWrap(edCode) {
//     let wrap = document.querySelector('.editor__wrapper');
//     if (edCode.scrollTop < 400 && countRows > 14) {
//         wrap.style.overflowY = 'scroll';
//         return;
//     }
//     wrap.style.overflowY = 'hidden'
// }
window.onload = () => {
    document.querySelector('#code-area').value = '';
}