let editingId = null;

/* --------------------------
   LOAD ALL WEBHOOKS
--------------------------- */
async function loadWebhooks() {
    const resp = await fetch("/api/webhooks");
    const data = await resp.json();

    const tbody = document.querySelector("#webhookTable tbody");
    tbody.innerHTML = "";

    data.forEach(w => {
        tbody.innerHTML += `
            <tr>
                <td>${w.url}</td>
                <td>${w.event}</td>
                <td>${w.active ? "Yes" : "No"}</td>
                <td>
                    <button onclick="editWebhook(${w.id})">Edit</button>
                    <button onclick="deleteWebhook(${w.id})">Delete</button>
                    <button onclick="testWebhook(${w.id})">Test</button>
                </td>
            </tr>
        `;
    });
}

/* --------------------------
   OPEN ADD MODAL
--------------------------- */
function openAdd() {
    editingId = null;
    document.getElementById("modalTitle").innerText = "Add Webhook";
    document.getElementById("modal").classList.remove("hidden");

    document.getElementById("modalUrl").value = "";
    document.getElementById("modalEvent").value = "";
    document.getElementById("modalActive").value = "true";
}

/* --------------------------
   OPEN EDIT MODAL
--------------------------- */
async function editWebhook(id) {
    editingId = id;

    const resp = await fetch("/api/webhooks");
    const data = await resp.json();
    const item = data.find(x => x.id === id);

    if (!item) {
        alert("Webhook not found!");
        return;
    }

    document.getElementById("modalTitle").innerText = "Edit Webhook";
    document.getElementById("modal").classList.remove("hidden");

    document.getElementById("modalUrl").value = item.url;
    document.getElementById("modalEvent").value = item.event;
    document.getElementById("modalActive").value = item.active ? "true" : "false";
}

/* --------------------------
   SAVE (CREATE / UPDATE)
--------------------------- */
document.getElementById("saveBtn").onclick = async () => {
    const payload = {
        url: document.getElementById("modalUrl").value,
        event: document.getElementById("modalEvent").value,
        active: document.getElementById("modalActive").value === "true"
    };

    if (editingId === null) {
        await fetch("/api/webhooks", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });
    } else {
        await fetch(`/api/webhooks/${editingId}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });
    }

    closeModal();
    loadWebhooks();
};

/* --------------------------
   CLOSE MODAL
--------------------------- */
function closeModal() {
    document.getElementById("modal").classList.add("hidden");
}

/* --------------------------
   DELETE WEBHOOK
--------------------------- */
async function deleteWebhook(id) {
    if (!confirm("Are you sure?")) return;

    await fetch(`/api/webhooks/${id}`, {
        method: "DELETE"
    });

    loadWebhooks();
}

/* --------------------------
   TEST WEBHOOK
--------------------------- */
async function testWebhook(id) {
    alert("Testing webhook...");

    const resp = await fetch(`/api/webhooks/${id}/test`, {
        method: "POST"
    });

    const result = await resp.json();

    alert(
        `Status: ${result.status}\n` +
        (result.http_status ? `HTTP Status: ${result.http_status}\n` : "") +
        (result.error ? `Error: ${result.error}\n` : "") +
        `Response Time: ${result.response_time_ms} ms`
    );
}

/* --------------------------
   INITIAL LOAD
--------------------------- */
loadWebhooks();
