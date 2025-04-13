async function analyze() {
  const symbol = document.getElementById("symbol").value;
  const interval = document.getElementById("interval").value;

  const response = await fetch("/analyze", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ symbol, interval }),
  });

  const data = await response.json();
  document.getElementById("result").innerHTML = `
    <h3>Recommendation: ${data.recommendation}</h3>
    <p>BUY: ${data.BUY}, NEUTRAL: ${data.NEUTRAL}, SELL: ${data.SELL}</p>
  `;
}
