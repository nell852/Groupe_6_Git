let currentInput = "";
let resultDisplayed = false;

function handleButton(action) {
    if (action === "clear") {
        currentInput = "";
        display.textContent = "0";
    } else if (action === "delete") {
        currentInput = currentInput.slice(0, -1);
        display.textContent = currentInput || "0";
    } else if (action === "=") {
        try {
            const result = eval(currentInput);
            display.textContent = result;
            addToHistory(currentInput + " = " + result);
            currentInput = result.toString();
            resultDisplayed = true;
        } catch {
            display.textContent = "Erreur";
        }
    } else {
        if (resultDisplayed) {
            currentInput = "";
            resultDisplayed = false;
        }
        currentInput += action;
        display.textContent = currentInput;
    }
}

document.getElementById("theme-toggle").addEventListener("click", () => {
    document.body.classList.toggle("dark");
});