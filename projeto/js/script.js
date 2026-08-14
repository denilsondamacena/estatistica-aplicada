let soundEnabled = true;
let currentChart = null;

document.addEventListener("DOMContentLoaded", () => {
    setupCopyButtons();
    initInteractiveChart();
});

function playBeep(freq = 440, duration = 0.05) {
    if (!soundEnabled) return;
    try {
        const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.type = "square";
        osc.frequency.value = freq;
        gain.gain.value = 0.03;
        osc.connect(gain);
        gain.connect(audioCtx.destination);
        osc.start();
        osc.stop(audioCtx.currentTime + duration);
    } catch (e) {
    }
}

function toggleSound() {
    soundEnabled = !soundEnabled;
    const soundToggleEl = document.getElementById('sound-toggle');
    if (soundToggleEl) {
        soundToggleEl.innerText = soundEnabled ? "🔊 SOM [ON]" : "🔇 SOM [OFF]";
    }
}

function loadContent(e, sectionId) {
    playBeep(600, 0.04);

    const loader = document.getElementById('retro-loader');
    const sections = document.querySelectorAll('.content-section');
    const buttons = document.querySelectorAll('.menu-btn');

    sections.forEach(sec => sec.classList.remove('active'));
    buttons.forEach(btn => btn.classList.remove('active'));

    if (e && e.currentTarget) {
        e.currentTarget.classList.add('active');
    }

    if (loader) {
        loader.classList.add('active');
    }

    const contentArea = document.querySelector('.content-area');
    if (contentArea) {
        const targetTop = contentArea.getBoundingClientRect().top + window.pageYOffset - 15;
        window.scrollTo({
            top: targetTop,
            behavior: 'smooth'
        });
    }

    setTimeout(() => {
        if (loader) {
            loader.classList.remove('active');
        }

        const targetSection = document.getElementById(`content-${sectionId}`);
        if (targetSection) {
            targetSection.classList.add('active');

            if (window.MathJax && window.MathJax.typesetPromise) {
                window.MathJax.typesetPromise([targetSection]);
            }
        }
    }, 1000);
}

function runWinCalc() {
    playBeep(800, 0.08);
    const input = document.getElementById('calc-data').value;
    const output = document.getElementById('calc-output');

    const numbers = input.split(',').map(n => parseFloat(n.trim())).filter(n => !isNaN(n));

    if (numbers.length === 0) {
        output.innerHTML = "<span style='color:red;'>Erro: Insira números separados por vírgula!</span>";
        return;
    }

    const sum = numbers.reduce((a, b) => a + b, 0);
    const mean = sum / numbers.length;

    const sorted = [...numbers].sort((a, b) => a - b);
    const mid = Math.floor(sorted.length / 2);
    const median = sorted.length % 2 !== 0 ? sorted[mid] : (sorted[mid - 1] + sorted[mid]) / 2;

    const variance = numbers.reduce((a, b) => a + Math.pow(b - mean, 2), 0) / (numbers.length - 1 || 1);
    const stdev = Math.sqrt(variance);

    output.innerHTML = `
        <b>N:</b> ${numbers.length}<br>
        <b>Média:</b> ${mean.toFixed(2)}<br>
        <b>Mediana:</b> ${median.toFixed(2)}<br>
        <b>Desvio Padrão:</b> ${stdev.toFixed(2)}
    `;
}

function runDosTerminal() {
    playBeep(300, 0.1);
    const code = document.getElementById('dos-code').value;
    const output = document.getElementById('dos-result');

    try {
        const arr = JSON.parse(code);
        if (!Array.isArray(arr)) throw new Error();

        const sum = arr.reduce((a, b) => a + b, 0);
        const mean = sum / arr.length;
        const min = Math.min(...arr);
        const max = Math.max(...arr);

        output.innerHTML = `
            C:\\> PROCESSANDO ARRAY...<br>
            ---------------------------------<br>
            len(dados) = ${arr.length}<br>
            sum(dados) = ${sum}<br>
            min/max    = ${min} / ${max}<br>
            Média      = ${mean.toFixed(2)}<br>
            ---------------------------------<br>
            <span>STATUS: 200 OK - Executado com sucesso!</span>
        `;
    } catch (e) {
        output.innerHTML = `<span>C:\\> ERRO DE SINTAXE! Use formato de lista ex: [10, 20, 30]</span>`;
    }
}

function filterMenu() {
    const input = document.getElementById('search-input');
    const filter = input.value.toLowerCase();
    const menuItems = document.querySelectorAll('.sidebar-menu li');

    menuItems.forEach(item => {
        const text = item.textContent || item.innerText;
        item.style.display = text.toLowerCase().includes(filter) ? "" : "none";
    });
}

function setupCopyButtons() {
    document.querySelectorAll('.code-box').forEach((box) => {
        if (box.querySelector('.copy-btn')) return;

        const copyBtn = document.createElement('button');
        copyBtn.className = 'copy-btn';
        copyBtn.innerText = 'COPIAR 📋';

        copyBtn.addEventListener('click', () => {
            playBeep(1000, 0.05);
            const codeText = box.querySelector('code').innerText;
            navigator.clipboard.writeText(codeText).then(() => {
                copyBtn.innerText = 'COPIADO! ⚡';
                copyBtn.classList.add('copied');

                setTimeout(() => {
                    copyBtn.innerText = 'COPIAR 📋';
                    copyBtn.classList.remove('copied');
                }, 2000);
            }).catch(err => {
                console.error('Erro ao copiar código:', err);
            });
        });

        box.prepend(copyBtn);
    });
}

function initInteractiveChart() {
    const ctx = document.getElementById('matplotlibChart');
    if (!ctx) return;

    if (currentChart) {
        currentChart.destroy();
    }

    currentChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Nota 1', 'Nota 2', 'Nota 3', 'Nota 4', 'Nota 5', 'Nota 6'],
            datasets: [{
                label: 'Frequência de Alunos',
                data: [1, 2, 3, 2, 1, 1],
                backgroundColor: '#ff00ff',
                borderColor: '#000000',
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: { stepSize: 1, color: '#12002b', font: { family: 'Fira Code' } },
                    grid: { color: 'rgba(0, 0, 0, 0.1)' }
                },
                x: {
                    ticks: { color: '#12002b', font: { family: 'Fira Code' } },
                    grid: { color: 'rgba(0, 0, 0, 0.1)' }
                }
            },
            plugins: {
                legend: {
                    labels: { color: '#12002b', font: { family: 'VT323', size: 16 } }
                }
            }
        }
    });
}

function exportToColabNotebook() {
    playBeep(900, 0.08);

    const codeBoxes = document.querySelectorAll('.code-box code');
    const cells = [];

    cells.push({
        cell_type: "markdown",
        metadata: {},
        source: [
            "# 🐍 Estatística Aplicada com Python // Google Colab\n",
            "**Disciplina:** Estatística Aplicada - Análise e Desenvolvimento de Sistemas (ADS)\n",
            "*Gerado via Guia de Estudos 90s Web Edition*"
        ]
    });

    codeBoxes.forEach((box) => {
        const lines = box.innerText.split('\n').map(l => l + '\n');
        cells.push({
            cell_type: "code",
            execution_count: null,
            metadata: {},
            outputs: [],
            source: lines
        });
    });

    const notebookData = {
        cells: cells,
        metadata: {
            language_info: { name: "python" }
        },
        nbformat: 4,
        nbformat_minor: 2
    };

    const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(notebookData, null, 2));
    const downloadAnchor = document.createElement('a');
    downloadAnchor.setAttribute("href", dataStr);
    downloadAnchor.setAttribute("download", "Estatistica_Aplicada_Python_ADS.ipynb");
    document.body.appendChild(downloadAnchor);
    downloadAnchor.click();
    downloadAnchor.remove();
}

function updateChartData() {
    playBeep(800, 0.05);

    if (!currentChart) return;

    const f1 = parseInt(document.getElementById('freq-1').value) || 0;
    const f2 = parseInt(document.getElementById('freq-2').value) || 0;
    const f3 = parseInt(document.getElementById('freq-3').value) || 0;
    const f4 = parseInt(document.getElementById('freq-4').value) || 0;
    const f5 = parseInt(document.getElementById('freq-5').value) || 0;
    const f6 = parseInt(document.getElementById('freq-6').value) || 0;

    currentChart.data.datasets[0].data = [f1, f2, f3, f4, f5, f6];
    currentChart.update();
}
