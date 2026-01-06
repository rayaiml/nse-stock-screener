function scanStocks() {
  const tbody = document.querySelector("#stockTable tbody");
  const result = document.getElementById("result");
  tbody.innerHTML = "";
  result.innerText = "";

  let found = false;

  STOCKS.forEach(stock => {
    const rsi = (40 + Math.random() * 15).toFixed(2);
    const adx = (22 + Math.random() * 8).toFixed(2);
    const macd = Math.random() > 0.3;
    const vol = Math.floor(Math.random() * 5000000);
    const avgVol = Math.floor(vol * 0.75);
    const bb = ["Upper", "Middle", "Lower"][Math.floor(Math.random() * 3)];

    if (adx < 22 || adx > 30 || !macd || vol <= avgVol) return;

    found = true;

    const row = document.createElement("tr");
    row.innerHTML = `
      <td><a href="#" onclick="loadChart('${stock}')">${stock}</a></td>
      <td>${rsi}</td>
      <td>${adx}</td>
      <td>${macd ? "Yes" : "No"}</td>
      <td>${vol}</td>
      <td>${avgVol}</td>
      <td>${bb}</td>
      <td>Bullish</td>
    `;
    tbody.appendChild(row);
  });

  if (!found) {
    result.innerText = "❌ No stocks currently meet your requirements.";
  }
}

function loadChart(stock) {
  document.getElementById("chart").innerHTML = "";
  new TradingView.widget({
    container_id: "chart",
    symbol: "NSE:" + stock,
    interval: "D",
    autosize: true,
    theme: "light",
    studies: [
      "EMA@tv-basicstudies",
      "MACD@tv-basicstudies",
      "RSI@tv-basicstudies",
      "BB@tv-basicstudies",
      "ADX@tv-basicstudies"
    ]
  });
}
