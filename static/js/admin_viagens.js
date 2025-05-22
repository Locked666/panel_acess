
// const dashboardTotalGasto30Dias = document.getElementById("dashboard-total-gasto-30-dias");
const dashboardTotalGasto30DiasValue = document.getElementById("total-gasto-dashboard-line-value");
const dashboardTotalGasto30DiasPercent = document.getElementById("total-gasto-dashboard-line-percent");

const dashboardTotalViagens30diasValue = document.getElementById("total-viagens-dashboard-line-value");
const dashboardTotalViagens30diasPercent = document.getElementById("total-viagens-dashboard-line-percent");

const dashboardTotalDiariasDias30diasValue = document.getElementById("total-diarias-dashboard-line-dias-value");
const dashboardTotalDiariasDias30diasPercent = document.getElementById("total-diarias-dashboard-line-dias-percent");

const dashboardTotalDiarias30diasValue = document.getElementById("total-diarias-dashboard-line-valor-value");


// Função para obter os dados do dashboard e atualizar os elementos HTML card
async function getDashboardTotalGasto30Dias() {
    const response = await fetch("/api/dashboard");
    const data = await response.json();
    
    // testar aguardar 10 segundos
    if (response.ok) {
        dashboardTotalGasto30DiasValue.innerText = `R$ ${data.gastos_ultimos_30_dias.toFixed(2)}`;
        dashboardTotalGasto30DiasPercent.innerText = `${10}% `;
        dashboardTotalViagens30diasValue.innerText = `${data.viagens_ultimos_30_dias} viagens`;
        dashboardTotalDiariasDias30diasValue.innerText = `${data.diarias_ultimos_30_dias} diárias`;
        dashboardTotalDiarias30diasValue.innerText = `R$ ${data.valor_diarias_ultimos_30_dias.toFixed(2)}`;


    } else {
        console.error("Error fetching data:", data);
    }
}

// Função para obter os dados do dashboard e atualizar os gráficos
async function getDashboardRows() {

    var ctx = document.getElementById("chart-bars").getContext("2d");

    // Primeiro Grafico 
    new Chart(ctx, {
      type: "bar",
      data: {
        labels: ["Jan.", "Fev", "Mar", "Abr", "Jun", "Jul", "Agos", "Set", "Out", "Nov", "Dez"],
        datasets: [{
          label: "Gasto",
          tension: 0.4,
          borderWidth: 0,
          borderRadius: 4,
          borderSkipped: false,
          backgroundColor: "rgba(255, 255, 255, .8)",
          data: [50, 20, 10, 22, 50, 10, 40, 20, 50, 30, 40],
          maxBarThickness: 6
        }, ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: false,
          }
        },
        interaction: {
          intersect: false,
          mode: 'index',
        },
        scales: {
          y: {
            grid: {
              drawBorder: false,
              display: true,
              drawOnChartArea: true,
              drawTicks: false,
              borderDash: [5, 5],
              color: 'rgba(255, 255, 255, .2)'
            },
            ticks: {
              suggestedMin: 0,
              suggestedMax: 500,
              beginAtZero: true,
              padding: 10,
              font: {
                size: 14,
                weight: 300,
                family: "Roboto",
                style: 'normal',
                lineHeight: 2
              },
              color: "#fff"
            },
          },
          x: {
            grid: {
              drawBorder: false,
              display: true,
              drawOnChartArea: true,
              drawTicks: false,
              borderDash: [5, 5],
              color: 'rgba(255, 255, 255, .2)'
            },
            ticks: {
              display: true,
              color: '#f8f9fa',
              padding: 10,
              font: {
                size: 14,
                weight: 300,
                family: "Roboto",
                style: 'normal',
                lineHeight: 2
              },
            }
          },
        },
      },
    });

    // Segundo Grafico
    var ctx2 = document.getElementById("chart-line").getContext("2d");

    new Chart(ctx2, {
      type: "line",
      data: {
        labels: ["Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
        datasets: [{
          label: "Mobile apps",
          tension: 0,
          borderWidth: 0,
          pointRadius: 5,
          pointBackgroundColor: "rgba(255, 255, 255, .8)",
          pointBorderColor: "transparent",
          borderColor: "rgba(255, 255, 255, .8)",
          borderColor: "rgba(255, 255, 255, .8)",
          borderWidth: 4,
          backgroundColor: "transparent",
          fill: true,
          data: [50, 40, 300, 320, 500, 350, 200, 230, 500],
          maxBarThickness: 6

        }],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: false,
          }
        },
        interaction: {
          intersect: false,
          mode: 'index',
        },
        scales: {
          y: {
            grid: {
              drawBorder: false,
              display: true,
              drawOnChartArea: true,
              drawTicks: false,
              borderDash: [5, 5],
              color: 'rgba(255, 255, 255, .2)'
            },
            ticks: {
              display: true,
              color: '#f8f9fa',
              padding: 10,
              font: {
                size: 14,
                weight: 300,
                family: "Roboto",
                style: 'normal',
                lineHeight: 2
              },
            }
          },
          x: {
            grid: {
              drawBorder: false,
              display: false,
              drawOnChartArea: false,
              drawTicks: false,
              borderDash: [5, 5]
            },
            ticks: {
              display: true,
              color: '#f8f9fa',
              padding: 10,
              font: {
                size: 14,
                weight: 300,
                family: "Roboto",
                style: 'normal',
                lineHeight: 2
              },
            }
          },
        },
      },
    });
    // Terceiro Grafico
    var ctx3 = document.getElementById("chart-line-tasks").getContext("2d");

    new Chart(ctx3, {
      type: "line",
      data: {
        labels: ["Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
        datasets: [{
          label: "Mobile apps",
          tension: 0,
          borderWidth: 0,
          pointRadius: 5,
          pointBackgroundColor: "rgba(255, 255, 255, .8)",
          pointBorderColor: "transparent",
          borderColor: "rgba(255, 255, 255, .8)",
          borderWidth: 4,
          backgroundColor: "transparent",
          fill: true,
          data: [50, 40, 300, 220, 500, 250, 400, 230, 500],
          maxBarThickness: 6

        }],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: false,
          }
        },
        interaction: {
          intersect: false,
          mode: 'index',
        },
        scales: {
          y: {
            grid: {
              drawBorder: false,
              display: true,
              drawOnChartArea: true,
              drawTicks: false,
              borderDash: [5, 5],
              color: 'rgba(255, 255, 255, .2)'
            },
            ticks: {
              display: true,
              padding: 10,
              color: '#f8f9fa',
              font: {
                size: 14,
                weight: 300,
                family: "Roboto",
                style: 'normal',
                lineHeight: 2
              },
            }
          },
          x: {
            grid: {
              drawBorder: false,
              display: false,
              drawOnChartArea: false,
              drawTicks: false,
              borderDash: [5, 5]
            },
            ticks: {
              display: true,
              color: '#f8f9fa',
              padding: 10,
              font: {
                size: 14,
                weight: 300,
                family: "Roboto",
                style: 'normal',
                lineHeight: 2
              },
            }
          },
        },
      },
    });

}


async function init() {
    await new Promise(resolve => setTimeout(resolve, 100));
    await getDashboardTotalGasto30Dias();
    await new Promise(resolve => setTimeout(resolve, 300));
    await getDashboardRows();
}

init();
// Função para formatar o valor em reais
function formatarValorEmReais(valor) {
    return valor.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });
}