// ================= SECTION SWITCHING =================
function showSection(sectionId, element) {

    const sections = document.querySelectorAll(".section");
    sections.forEach(section => {
        section.classList.remove("active");
    });

    const selectedSection = document.getElementById(sectionId);
    if (selectedSection) {
        selectedSection.classList.add("active");
    }

    const menuItems = document.querySelectorAll(".sidebar ul li");
    menuItems.forEach(item => item.classList.remove("active"));

    if (element) {
        element.classList.add("active");
    }

    const lastUpdate = document.getElementById("lastUpdated");
    const sectionTitle = document.getElementById("sectionTitle");

    // ✅ Sirf dashboard par title show hoga
    if (sectionId === "dashboard") {

        if(sectionTitle){
            sectionTitle.style.display = "inline";
            sectionTitle.innerText = "Dashboard";
        }

        if(lastUpdate){
            lastUpdate.style.display = "block";
        }

    } else {

        if(sectionTitle){
            sectionTitle.style.display = "none";
        }

        if(lastUpdate){
            lastUpdate.style.display = "none";
        }
    }
}

// ================= AUTO TIME =================
function updateTime() {
    const now = new Date();
    const timeString = now.toLocaleTimeString();
    const lastUpdate = document.getElementById("lastUpdated");
    if(lastUpdate){
        lastUpdate.innerText = "Last Updated: " + timeString;
    }
}
setInterval(updateTime, 1000);
updateTime();

// ================= ADD PRODUCT MODAL =================
document.addEventListener("DOMContentLoaded", function(){

    const modal = document.getElementById("productModal");
    const addBtn = document.querySelector(".add-product-btn");
    const closeBtn = document.querySelector(".close-modal");
    const saveBtn = document.getElementById("saveProductBtn");

    // OPEN MODAL
    if(addBtn){
        addBtn.addEventListener("click", function(){
            modal.style.display = "flex";
        });
    }

    // CLOSE MODAL
    if(closeBtn){
        closeBtn.addEventListener("click", function(){
            modal.style.display = "none";
        });
    }

    // SAVE PRODUCT
    if(saveBtn){
        saveBtn.addEventListener("click", function(){

            const name = document.getElementById("newProductName").value;
            const barcode = document.getElementById("newProductBarcode").value;
            const category = document.getElementById("newProductCategory").value;
            const quantity = document.getElementById("newProductQuantity").value;
            const price = document.getElementById("newProductPrice").value;

            if(name && barcode && category && quantity && price){

                const tbody = document.querySelector(".product-table tbody");

                const newRow = `
                <tr>
                    <td class="product-name">
                        <div class="p-name">${name}</div>
                        <div class="p-id">ID: ${tbody.children.length}</div>
                    </td>
                    <td>${barcode}</td>
                    <td>${category}</td>
                    <td>${quantity}</td>
                    <td style="font-weight:bold;">$${price}</td>
                    <td><span class="stock-box in-stock">In Stock</span></td>
                    <td><i class="fas fa-ellipsis-h action-dots"></i></td>
                </tr>
                `;

                tbody.insertAdjacentHTML("beforeend", newRow);

                modal.style.display = "none";

            }else{
                alert("Please fill all fields");
            }

        });
    }

});

// ================= PRODUCT SEARCH =================
document.addEventListener("DOMContentLoaded", function(){

    const productSearch = document.querySelector(".product-search");

    if(productSearch){
        productSearch.addEventListener("keyup", function(){

            let filter = this.value.toLowerCase();
            let rows = document.querySelectorAll(".product-table tbody tr");

            rows.forEach((row, index) => {

                if(index === 0) return; // skip table heading row

                let text = row.innerText.toLowerCase();

                if(text.includes(filter)){
                    row.style.display = "";
                }else{
                    row.style.display = "none";
                }

            });

        });
    }

});

// ================= SALES SEARCH =================
document.addEventListener("DOMContentLoaded", function(){

    const salesSearch = document.getElementById("salesSearch");

    if(salesSearch){
        salesSearch.addEventListener("keyup", function(){

            let value = this.value.toLowerCase();
            let rows = document.querySelectorAll(".sales-table tr");

            rows.forEach((row, index) => {

                if(index === 0) return; // skip header row

                let itemName = row.children[0].innerText.toLowerCase();

                if(itemName.includes(value)){
                    row.style.display = "";
                }else{
                    row.style.display = "none";
                }

            });

        });
    }

});

// ================= QUANTITY BUTTONS & DELETE ICON =================
document.querySelector(".sales-table").addEventListener("click", function(e){

    // DELETE ICON
    if(e.target.classList.contains("delete-icon")){
        e.target.closest("tr").remove();
        updateTotals();
    }

    // PLUS BUTTON
    if(e.target.classList.contains("plus")){
        let qtySpan = e.target.parentElement.querySelector(".qty");
        let qty = parseInt(qtySpan.innerText);
        qty++;
        qtySpan.innerText = qty;
        updateTotals();
    }

    // MINUS BUTTON
    if(e.target.classList.contains("minus")){
        let qtySpan = e.target.parentElement.querySelector(".qty");
        let qty = parseInt(qtySpan.innerText);
        if(qty > 1){
            qty--;
            qtySpan.innerText = qty;
            updateTotals();
        }
    }

});

// ================= ADD PRODUCT TO SALES =================
function addToSale(row){

    // Product data
    let name = row.querySelector(".p-name").innerText;
    let barcode = row.children[1].innerText;
    let price = row.children[4].innerText;

    let salesTable = document.querySelector(".sales-table");

    // Check if already added
    let existingRows = salesTable.querySelectorAll("tr");

    for(let i=1; i<existingRows.length; i++){
        let existingName = existingRows[i].children[0].innerText;
        if(existingName.includes(name)){
            alert("Product already added!");
            return;
        }
    }

    // Add new row
    let newRow = `
    <tr>
        <td>
            <div style="display:flex; flex-direction:column;">
                <span>${name}</span>
                <small style="color:gray;">${barcode}</small>
            </div>
        </td>

        <td>
            <div class="qty-box">
                <button class="minus">-</button>
                <span class="qty">1</span>
                <button class="plus">+</button>
            </div>
        </td>

        <td>${price}</td>

        <td>
            ${price}
            <i class="fa-solid fa-trash delete-icon"></i>
        </td>
    </tr>
    `;

    salesTable.insertAdjacentHTML("beforeend", newRow);

    // ✅ Update totals after adding new product
    updateTotals();

}

// ================= UPDATE TOTALS =================
function updateTotals(){

    let rows = document.querySelectorAll(".sales-table tr");
    let subtotal = 0;

    rows.forEach((row, index) => {
        if(index === 0) return; // skip header row

        let priceText = row.children[2].innerText.replace("$","");
        let qtyText = row.querySelector(".qty").innerText;

        let price = parseFloat(priceText);
        let qty = parseInt(qtyText);

        let total = price * qty;

        row.children[3].innerText = "$" + total.toFixed(2) + ' ';
        row.children[3].innerHTML += '<i class="fa-solid fa-trash delete-icon"></i>';

        subtotal += total;
    });

    let tax = subtotal * 0.08;
    let finalTotal = subtotal + tax;

    const subtotalEl = document.querySelector(".subtotal");
    const taxEl = document.querySelector(".tax");
    const finalEl = document.querySelector(".final-total");

    if(subtotalEl) subtotalEl.innerText = "$" + subtotal.toFixed(2);
    if(taxEl) taxEl.innerText = "$" + tax.toFixed(2);
    if(finalEl) finalEl.innerText = "$" + finalTotal.toFixed(2);

}