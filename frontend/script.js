document.getElementById("strategyForm").addEventListener("submit", function(event) {
  event.preventDefault(); // Prevent page reload

  // Collect strategy input values
  const strategyData = {
      tp1: parseFloat(document.getElementById("tp1").value),
      tp2: parseFloat(document.getElementById("tp2").value),
      be: parseFloat(document.getElementById("be").value),
      tp: parseFloat(document.getElementById("tp").value),
      tp1_percent: parseFloat(document.getElementById("tp1_percent").value),
      tp2_percent: parseFloat(document.getElementById("tp2_percent").value)
  };

  // Collect past trades input values
  const pastTradesData = {
      tp: parseFloat(document.getElementById("past_tp").value),
      sl: parseFloat(document.getElementById("past_sl").value),
      be: parseFloat(document.getElementById("past_be").value),
      direction: document.getElementById("direction").value // Long or Short
  };

  // Combine both datasets into one object
  const requestData = {
      strategy: strategyData,
      past_trades: pastTradesData
  };

  console.log("Collected Data:", requestData); // Debugging output

  // Send data to backend
  fetch("http://127.0.0.1:8000/calculate-strategy", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(requestData)
  })
  .then(response => response.json())
  .then(data => console.log("Backend Response:", data))
  .catch(error => console.error("Error:", error));
});
