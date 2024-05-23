function updateCartItemsInCart(inputElement) {
  const productId = inputElement.getAttribute("data-product-id");
  const cartId = inputElement.getAttribute("data-cart-id");
  const newQuantity = inputElement.value;

  console.log("productID : ", productId);
  console.log("cartID : ", cartId);
  console.log("newQuantity : ", newQuantity);

  // Ensure productId and cartId are not null or undefined
  if (!productId || !cartId) {
    console.error("Failed to retrieve productId or cartId.");
    return;
  }

  fetch("/update-cart-items-in-cart", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      product_id: productId,
      cart_id: cartId,
      quantity: newQuantity,
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        console.log("Cart updated successfully");

        // Update tổng số tiền cần trả trong giỏ hàng
        document.querySelector(
          ".w-commerce-commercecartordervalue"
        ).textContent = `$ ${newQuantity} USD`;

        // Update tổng số lượng hàng trong giỏ hàng
        document.querySelector("input[name='quantity']").value =
          newQuantity.toString();
      } else {
        console.error("Oh shit ! Failed to update cart");
      }
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}
