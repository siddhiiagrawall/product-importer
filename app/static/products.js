let currentPage = 1;
let currentEditingId = null;

async function loadProducts(page = 1) {
    currentPage = page;

    const sku = document.getElementById("filterSku").value;
    const name = document.getElementById("filterName").value;
    const active = document.getElementById("filterActive").value;

    let url = `/api/products?page=${page}&limit=10`;
    if (sku) url += `&sku=${sku}`;
    if (name) url += `&name=${name}`;
    if (active !== "") url += `&active=${active}`;

    const resp = await fetch(url);
    const data = await resp.json();

    const tbody = document.querySelector("#productTable tbody");
    tbody.innerHTML = "";

    data.items.forEach(product => {
        const row = `
            <tr>
                <td>${product.sku}</td>
                <td>${product.name}</td>
                <td>${product.description ?? ""}</td>
                <td>${product.price}</td>
                <td>${product.active ? "Yes" : "No"}</td>
                <td>
                    <button onclick="openEdit(${product.id})">Edit</button>
                    <button onclick="deleteProduct(${product.id})">Delete</button>
                </td>
            </tr>
        `;
        tbody.innerHTML += row;
    });

    document.getElementById("pageInfo").innerText =
        `Page ${data.page}`;
}

document.getElementById("addBtn").onclick = () => openAdd();

function openAdd() {
    currentEditingId = null;
    document.getElementById("modalTitle").innerText = "Add Product";
    document.getElementById("modal").classList.remove("hidden");

    document.getElementById("modalSku").value = "";
    document.getElementById("modalName").value = "";
    document.getElementById("modalDesc").value = "";
    document.getElementById("modalPrice").value = "";
    document.getElementById("modalActive").value = "true";
}

async function openEdit(id) {
    currentEditingId = id;

    const resp = await fetch(`/api/products/${id}`);
    const item = await resp.json();

    document.getElementById("modalTitle").innerText = "Edit Product";
    document.getElementById("modal").classList.remove("hidden");

    document.getElementById("modalSku").value = item.sku;
    document.getElementById("modalName").value = item.name;
    document.getElementById("modalDesc").value = item.description;
    document.getElementById("modalPrice").value = item.price;
    document.getElementById("modalActive").value = item.active ? "true" : "false";
}

document.getElementById("saveBtn").onclick = async () => {
    const payload = {
        sku: document.getElementById("modalSku").value,
        name: document.getElementById("modalName").value,
        description: document.getElementById("modalDesc").value,
        price: parseFloat(document.getElementById("modalPrice").value),
        active: document.getElementById("modalActive").value === "true"
    };

    if (currentEditingId === null) {
        await fetch("/api/products", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(payload)
        });
    } else {
        await fetch(`/api/products/${currentEditingId}`, {
            method: "PUT",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(payload)
        });
    }

    closeModal();
    loadProducts(currentPage);
};

function closeModal() {
    document.getElementById("modal").classList.add("hidden");
}

async function deleteProduct(id) {
    if (!confirm("Are you sure? This cannot be undone.")) return;

    await fetch(`/api/products/${id}`, {
        method: "DELETE"
    });

    loadProducts(currentPage);
}

document.getElementById("prevPage").onclick = () => {
    if (currentPage > 1) loadProducts(currentPage - 1);
};

document.getElementById("nextPage").onclick = () => {
    loadProducts(currentPage + 1);
};

loadProducts(1);
