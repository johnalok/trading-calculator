fetch("http://127.0.0.1:8000/calculate-strategy", {  // Update URL to match backend
  method: "POST",
  headers: {
    "Content-Type": "application/json"
  },
  body: JSON.stringify({
    tp1: document.getElementById("tp1").value,
    tp2: document.getElementById("tp2").value,
    be: document.getElementById("be").value,
    tp: document.getElementById("tp").value,
    tp1_percentage: document.getElementById("tp1_percentage").value,
    tp2_percentage: document.getElementById("tp2_percentage").value
  })
})
  .then(response => response.json())
  .then(data => console.log("Backend Response:", data))
  .catch(error => console.error("Error:", error));
