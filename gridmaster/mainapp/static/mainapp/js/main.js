document.querySelectorAll('tr').forEach((elem) => {
    elem.addEventListener('click', (event) => {
        preopenFile(event.target.parentElement)
    })
})

lastActive = 0;
function preopenFile(tr) {
    let tds = tr.querySelectorAll('td')
    if (tds[0].textContent == '#' || tds[0].textContent == lastActive) return;

    document.querySelector(".files__table-wrapper").querySelectorAll('tr')[lastActive].classList.remove('active');

    tr.classList.add('active')

    let title = document.querySelector('.preview__title');
    let lastEdit = document.querySelector('.preview__date');
    let about = document.querySelector('.preview__about');

    let change = [title, lastEdit, about]
    for (let elem of change) {
        elem.style.opacity = '0'
    }

    setTimeout(() => {
        about.textContent = tds[3].textContent;
        title.textContent = tds[1].textContent;
        lastEdit.textContent = tds[2].textContent;

        for (let elem of change) {
            elem.style.opacity = '1'
        }
    }, 550)


    lastActive = tds[0].textContent
}



// диаграммма
let procent = 80;
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