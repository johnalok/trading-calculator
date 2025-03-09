document.addEventListener("DOMContentLoaded", function () {
    const maxRows = 30;
    const minRows = 1;
    const tableBody = document.querySelector("#pastTradesTable tbody");
    const rowCountDisplay = document.getElementById("rowCountDisplay");

    function updateRowCount() {
        rowCountDisplay.innerText = tableBody.children.length;
    }

    function createRow() {
        const row = document.createElement("tr");
        row.classList.add("past-trade-row");

        row.innerHTML = `
            <td><input type="number" class="past_tp" placeholder="Past TP"></td>
            <td><input type="number" class="past_sl" placeholder="Past SL"></td>
            <td><input type="number" class="past_be" placeholder="Past BE"></td>
        `;

        return row;
    }

    // Add row button
    document.getElementById("addRow").addEventListener("click", function () {
        if (tableBody.children.length < maxRows) {
            tableBody.appendChild(createRow());
            updateRowCount();
        }
    });

    // Remove row button
    document.getElementById("removeRow").addEventListener("click", function () {
        if (tableBody.children.length > minRows) {
            tableBody.removeChild(tableBody.lastElementChild);
            updateRowCount();
        }
    });

    // Form submission
    document.getElementById("strategyForm").addEventListener("submit", async function (event) {
        event.preventDefault();

        const getFloat = (id) => {
            const value = parseFloat(document.getElementById(id).value);
            return isNaN(value) ? 0 : value; // Prevent NaN
        };

        // Collect past trades dynamically
        const pastTrades = [];
        document.querySelectorAll(".past-trade-row").forEach(row => {
            const past_tp = parseFloat(row.querySelector(".past_tp").value) || 0;
            const past_sl = parseFloat(row.querySelector(".past_sl").value) || 0;
            const past_be = parseFloat(row.querySelector(".past_be").value) || 0;
            
            pastTrades.push({ past_tp, past_sl, past_be });
        });

        // Prepare the data object
        const data = {
            tp1: getFloat("tp1"),
            tp2: getFloat("tp2"),
            be: getFloat("be"),
            sl: getFloat("sl"),
            tp1_percent: getFloat("tp1_percent"),
            tp2_percent: getFloat("tp2_percent"),
            past_trades: pastTrades,  // Send all past trades as a list
        };

        try {
            const response = await fetch("http://127.0.0.1:8002/calculate-strategy", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(data)
            });

            const result = await response.json();

            if (response.ok) {
                console.log("Strategy received:", result);

                // Update results in form
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

    // Initialize row count
    updateRowCount();
});
