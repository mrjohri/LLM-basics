// Store chat history per panel
let histories = [[], [], []];


// -----------------------------
// INIT (fix slider issue)
// -----------------------------
document.addEventListener("DOMContentLoaded", () => {
    initializeSliders();
});

function initializeSliders() {
    document.querySelectorAll(".panel").forEach(panel => {
        const temp = panel.querySelector(".temp");
        const tempVal = panel.querySelector(".temp-val");

        const topP = panel.querySelector(".top_p");
        const topPVal = panel.querySelector(".top_p-val");

        // Set initial values
        if (temp && tempVal) tempVal.innerText = temp.value;
        if (topP && topPVal) topPVal.innerText = topP.value;

        // Attach listeners
        if (temp) {
            temp.addEventListener("input", () => {
                tempVal.innerText = temp.value;
            });
        }

        if (topP) {
            topP.addEventListener("input", () => {
                topPVal.innerText = topP.value;
            });
        }
    });
}


// -----------------------------
// ADD MESSAGE (UI)
// -----------------------------
function addMessage(chatId, text, sender) {
    const chat = document.getElementById(chatId);

    const msg = document.createElement("div");
    msg.classList.add("message");
    msg.classList.add(sender === "You" ? "user" : "ai");

    msg.innerText = text;

    chat.appendChild(msg);
    chat.scrollTop = chat.scrollHeight;
}


// -----------------------------
// SEND MESSAGE
// -----------------------------
async function sendMessage() {
    const messageInput = document.getElementById("message");
    const message = messageInput.value.trim();

    if (!message) return;

    // Show user message in all panels
    for (let i = 0; i < 3; i++) {
        addMessage("chat" + i, message, "You");
    }

    let panels = [];

    for (let i = 0; i < 3; i++) {
        let panel = document.getElementById("panel" + i);

        let system = panel.querySelector(".system")?.value || "";
        let temp = parseFloat(panel.querySelector(".temp")?.value || 0.7);
        let tokens = parseInt(panel.querySelector(".tokens")?.value || 200);
        let top_p = parseFloat(panel.querySelector(".top_p")?.value || 1);

        let history = [];

        // Add system prompt if present
        if (system.trim() !== "") {
            history.push({ role: "system", content: system });
        }

        // Append previous history
        history = history.concat(histories[i]);

        panels.push({
            temperature: temp,
            max_tokens: tokens,
            top_p: top_p,
            history: history
        });
    }

    try {
        const res = await fetch("/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                message: message,
                panels: panels
            })
        });

        const data = await res.json();

        data.forEach((panel, i) => {
            addMessage("chat" + i, panel.response, "AI");
            histories[i] = panel.history;
        });

    } catch (error) {
        console.error("Error:", error);
    }

    messageInput.value = "";
}


// -----------------------------
// ENTER KEY SUPPORT
// -----------------------------
document.getElementById("message").addEventListener("keypress", function (e) {
    if (e.key === "Enter") {
        sendMessage();
    }
});