document.getElementById("strategyForm").addEventListener("submit", async function(event) {
    event.preventDefault();

    const getFloat = (id) => {
        const value = parseFloat(document.getElementById(id).value);
        return isNaN(value) ? 0 : value;
    };

    // Ensure TP percentages sum to 100
    let tp1Percent = getFloat("tp1_percent");
    let tp2Percent = getFloat("tp2_percent");
    if (tp1Percent + tp2Percent !== 100) {
        alert("TP1% and TP2% must add up to 100!");
        return;
    }

    // Collect past trades data, ignoring empty rows
    let pastTrades = [];
    document.querySelectorAll("#pastTradesTable tbody tr").forEach(row => {
        let past_tp = parseFloat(row.querySelector(".past_tp").value) || 0;
        let past_sl = parseFloat(row.querySelector(".past_sl").value) || 0;
        let past_be = parseFloat(row.querySelector(".past_be").value) || 0;

        if (past_tp !== 0 || past_sl !== 0 || past_be !== 0) {
            pastTrades.push({ past_tp, past_sl, past_be });
        }
    });

    const data = {
        tp1: getFloat("tp1"),
        tp2: getFloat("tp2"),
        be: getFloat("be"),
        sl: getFloat("sl"),
        tp1_percent: tp1Percent,
        tp2_percent: tp2Percent,
        past_trades: pastTrades
    };

    try {
        const response = await fetch("http://127.0.0.1:8002/calculate-strategy", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        });

        const result = await response.json();
        if (response.ok) {
            console.log("Strategy received:", result);
            document.getElementById("display_hit_sl").innerText = result.hit_sl;
            document.getElementById("display_hit_be_no_profit").innerText = result.hit_be_without_profit;
            document.getElementById("display_hit_tp1_then_be").innerText = result.hit_tp1_then_be;
            document.getElementById("display_hit_tp2").innerText = result.hit_tp2;
            document.getElementById("display_outcome").innerText = result.outcome;
        } else {
            console.error("Error:", result);
        }
    } catch (error) {
        console.error("Request failed:", error);
    }
});

// Ensure TP1% + TP2% = 100 dynamically
document.getElementById("tp1_percent").addEventListener("input", function () {
    let tp1 = parseFloat(this.value) || 0;
    document.getElementById("tp2_percent").value = Math.max(0, 100 - tp1);
});

document.getElementById("tp2_percent").addEventListener("input", function () {
    let tp2 = parseFloat(this.value) || 0;
    document.getElementById("tp1_percent").value = Math.max(0, 100 - tp2);
});

// Manage dynamic table rows
const tableBody = document.querySelector("#pastTradesTable tbody");
const rowCountDisplay = document.getElementById("rowCountDisplay");

function updateRowCount() {
    rowCountDisplay.innerText = tableBody.rows.length;
}

// Function to add a row
document.getElementById("addRow").addEventListener("click", function(event) {
    event.preventDefault();
    if (tableBody.rows.length >= 30) return;

    const newRow = document.createElement("tr");
    newRow.innerHTML = `
        <td><input type="number" class="past_tp"></td>
        <td><input type="number" class="past_sl"></td>
        <td><input type="number" class="past_be"></td>
    `;
    tableBody.appendChild(newRow);
    updateRowCount();
});

// Function to remove a row
document.getElementById("removeRow").addEventListener("click", function(event) {
    event.preventDefault();
    if (tableBody.rows.length > 1) {
        tableBody.removeChild(tableBody.lastChild);
        updateRowCount();
    }
});

// Ensure at least 1 row exists by default
if (tableBody.rows.length === 0) {
    document.getElementById("addRow").click();
}
