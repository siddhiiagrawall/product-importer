document.getElementById("uploadForm").addEventListener("submit", async function(e) {
    e.preventDefault();

    const fileInput = document.getElementById("csvFile");
    if (!fileInput.files.length) {
        alert("Please select a CSV file.");
        return;
    }

    const formData = new FormData();
    formData.append("file", fileInput.files[0]);

    document.getElementById("status").innerText = "Uploading...";

    // Upload file
    const uploadResponse = await fetch("/api/upload", {
        method: "POST",
        body: formData
    });

    const result = await uploadResponse.json();
    const uploadId = result.upload_id;

    document.getElementById("status").innerText = "Upload started. Processing...";

    // Show progress bar
    document.getElementById("progress-container").style.display = "block";

    // Connect to SSE
    const eventSource = new EventSource(`/api/progress/${uploadId}/sse`);

    eventSource.onmessage = function(event) {
        if (!event.data.trim() || event.data === "ping") return;

        // ⭐ FIX HERE
        let jsonStr = event.data.trim();
        if (jsonStr.startsWith("data:")) {
            jsonStr = jsonStr.replace("data: ", "");
        }

        let data;
        try {
            data = JSON.parse(jsonStr);
        } catch (err) {
            console.log("Invalid JSON:", jsonStr);
            return;
        }

        const bar = document.getElementById("progress-bar");
        bar.style.width = data.percent + "%";

        if (data.percent >= 100 || data.status === "complete") {
            document.getElementById("status").innerText = "Import Complete!";
            eventSource.close();
        }
    };

    eventSource.onerror = () => {
        document.getElementById("status").innerText = "Error receiving progress.";
        eventSource.close();
    };
});
