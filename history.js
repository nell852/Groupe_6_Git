const historyDiv = document.getElementById("history");

function addToHistory(entry) {
    const line = document.createElement("div");
    line.textContent = entry;
    historyDiv.prepend(line);
}