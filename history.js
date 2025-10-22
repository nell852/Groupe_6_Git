const historyDiv = document.getElementById("history");

function addToHistory(entry) {
    if (!entry) return; // Empêche d'ajouter des lignes vides

    const line = document.createElement("div");
    line.classList.add("history-item");
    line.textContent = entry;

    // Ajoute l’entrée en haut avec une petite animation
    historyDiv.prepend(line);

    // Limite la taille de l’historique (par exemple à 10 entrées)
    const maxItems = 10;
    const items = historyDiv.querySelectorAll(".history-item");
    if (items.length > maxItems) {
        historyDiv.removeChild(items[items.length - 1]);
    }
}
