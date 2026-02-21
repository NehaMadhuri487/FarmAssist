async function submitQuery() {
    let query = document.getElementById("query").value;
    let language = document.getElementById("language").value;
    //alert("Selected language is: " + language); 
    let formData = new FormData();
    formData.append("query", query);
    formData.append("language", language);
    document.getElementById("responseBox").innerHTML = "Loading...";

    const response = await fetch("/ask", {
        method: "POST",
        body: formData
    });

    const data = await response.json();

    // Only show answer, no confidence here
    document.getElementById("responseBox").innerHTML = `
        <div style="text-align:left;">
            <p><strong>🌾 Answer:</strong></p>
            <p>${data.answer}</p>
        </div>
    `;
}

