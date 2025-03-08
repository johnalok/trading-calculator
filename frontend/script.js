document.getElementById("strategyForm").addEventListener("submit", async function(event) {
    event.preventDefault();

    const getFloat = (id) => {
        const value = parseFloat(document.getElementById(id).value);
        return isNaN(value) ? 0 : value;  // Prevent sending "NaN"
    };

    const data = {
        tp1: getFloat("tp1"),
        tp2: getFloat("tp2"),
        be: getFloat("be"),
        sl: getFloat("sl"),
        tp1_percent: getFloat("tp1_percent"),
        tp2_percent: getFloat("tp2_percent"),
        past_tp: getFloat("past_tp"),
        past_sl: getFloat("past_sl"),
        past_be: getFloat("past_be"),
        past_direction: document.getElementById("past_direction").value.trim() || "long" // Default to "long"
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

            document.getElementById("hit_sl").value = result.hit_sl;
            document.getElementById("hit_be_no_profit").value = result.hit_be_no_profit;
            document.getElementById("hit_tp1_then_be").value = result.hit_tp1_then_be;
            document.getElementById("hit_tp2").value = result.hit_tp2;
            document.getElementById("outcome").value = result.outcome;

            document.getElementById("display_hit_sl").innerText = result.hit_sl;
            document.getElementById("display_hit_be_no_profit").innerText = result.hit_be_no_profit;
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
