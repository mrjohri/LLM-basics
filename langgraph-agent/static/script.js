async function sendQuery() {
    const query = document.getElementById("query").value;
    const loading = document.getElementById("loading");
    const output = document.getElementById("output");

    loading.style.display = "block";
    output.innerHTML = "";

    const response = await fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query })
    });

    const data = await response.json();
    loading.style.display = "none";
    output.innerHTML = marked.parse(data.response);
}
