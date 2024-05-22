// updates.js

function updateQuantity(element) {
  let quantity = element.value;
  let productId = element.getAttribute("data-commerce-sku-id");

  fetch("/update-quantity", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      product_id: productId,
      quantity: quantity,
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      console.log("Success:", data);
      // Optionally update the UI based on the server's response
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}
