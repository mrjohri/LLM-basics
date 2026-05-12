async function searchTopic() {
    const topic = document.getElementById("topic").value;
    const response = await fetch("/search", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ topic })
    });
    const data = await response.json();
    document.getElementById("output").innerHTML = data.result;
}
