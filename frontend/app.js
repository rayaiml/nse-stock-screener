fetch('../data/scan_result.json')
.then(r=>r.json())
.then(d=>{
const tb=document.getElementById('tbody');
if(!d.length){document.getElementById('result').innerText='No stocks meet criteria';return;}
d.forEach(s=>{
tb.innerHTML+=`<tr>
<td><a href='#' onclick="loadChart('${s.stock}')">${s.stock}</a></td>
<td>${s.rsi}</td><td>${s.adx}</td><td>${s.macd}</td>
<td>${s.volume}</td><td>${s.avg_volume}</td>
<td>${s.bb}</td><td>${s.trend}</td></tr>`;
});
});
function loadChart(sym){
document.getElementById('chart').innerHTML='';
new TradingView.widget({
container_id:'chart',symbol:'NSE:'+sym,interval:'D',
autosize:true,studies:['EMA@tv-basicstudies','MACD@tv-basicstudies','RSI@tv-basicstudies','BB@tv-basicstudies','ADX@tv-basicstudies']
});
}
