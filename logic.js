let currentInput = "";
let resultDisplayed = false;

// Initialisation sécurisée du display et de l'historique
const display = document.getElementById("display");
const historyContainer = document.getElementById("history");
const themeToggle = document.getElementById("theme-toggle");

// Fonction sécurisée pour évaluer les expressions
function safeEval(expression) {
    if (/^[0-9+\-*/(). ]+$/.test(expression)) {
        return Function('"use strict";return (' + expression + ')')();
    } else {
        throw new Error("Expression invalide");
    }
}

// Fonction pour ajouter une entrée dans l'historique
function addToHistory(entry) {
    if (!historyContainer) return;  // Vérifie existence
    const item = document.createElement("div");
    item.textContent = entry;
    historyContainer.appendChild(item);
}

// Fonction principale pour gérer les boutons
function handleButton(action) {
    if (!display return;  // Vérifie que display existe

    if (action === "clear") {
        currentInput = "";
        display.textContent = "0";
    } else if (action === "delete") {
        currentInput = currentInput.slice(0, -1);
        display.textContent = currentInput || "0";
    } else if (action === "=") {
        try {
            const result = safeEval(currentInput);
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

// Gestion du toggle thème avec vérification
if (themeToggle) {
    themeToggle.addEventListener("click", () => {
        document.body.classList.toggle("dark");
    });
}
