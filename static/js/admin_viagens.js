
// const dashboardTotalGasto30Dias = document.getElementById("dashboard-total-gasto-30-dias");
const dashboardTotalGasto30DiasValue = document.getElementById("total-gasto-dashboard-line-value");
const dashboardTotalGasto30DiasPercent = document.getElementById("total-gasto-dashboard-line-percent");



async function getDashboardTotalGasto30Dias() {
    const response = await fetch("/api/dashboard/gastos");
    const data = await response.json();

    if (response.ok) {
        dashboardTotalGasto30DiasValue.innerText = `R$ ${data.gastos_ultimos_30_dias}`;
        dashboardTotalGasto30DiasPercent.innerText = `${0} %`;
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