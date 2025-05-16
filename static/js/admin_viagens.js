
// const dashboardTotalGasto30Dias = document.getElementById("dashboard-total-gasto-30-dias");
const dashboardTotalGasto30DiasValue = document.getElementById("total-gasto-dashboard-line-value");
const dashboardTotalGasto30DiasPercent = document.getElementById("total-gasto-dashboard-line-percent");

const dashboardTotalViagens30diasValue = document.getElementById("total-viagens-dashboard-line-value");
const dashboardTotalViagens30diasPercent = document.getElementById("total-viagens-dashboard-line-percent");

const dashboardTotalDiariasDias30diasValue = document.getElementById("total-diarias-dashboard-line-dias-value");
const dashboardTotalDiariasDias30diasPercent = document.getElementById("total-diarias-dashboard-line-dias-percent");

const dashboardTotalDiarias30diasValue = document.getElementById("total-diarias-dashboard-line-valor-value");



async function getDashboardTotalGasto30Dias() {
    const response = await fetch("/api/dashboard");
    const data = await response.json();

    if (response.ok) {
        dashboardTotalGasto30DiasValue.innerText = `R$ ${data.gastos_ultimos_30_dias.toFixed(2)}`;
        dashboardTotalGasto30DiasPercent.innerText = `${0} %`;
        dashboardTotalViagens30diasValue.innerText = `${data.viagens_ultimos_30_dias} viagens`;
        dashboardTotalDiariasDias30diasValue.innerText = `${data.diarias_ultimos_30_dias} diárias`;
        dashboardTotalDiarias30diasValue.innerText = `R$ ${data.valor_diarias_ultimos_30_dias.toFixed(2)}`;


    } else {
        console.error("Error fetching data:", data);
    }
}

async function init() {
    await getDashboardTotalGasto30Dias();
}

init();
// Função para formatar o valor em reais
function formatarValorEmReais(valor) {
    return valor.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });
}