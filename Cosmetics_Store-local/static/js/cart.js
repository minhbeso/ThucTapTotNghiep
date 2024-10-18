class Cart {
  constructor() {
    // Initialize the cart from localStorage or create a new one if it doesn't exist
    this.cart = JSON.parse(localStorage.getItem("cart")) || [];
  }

  // Save the current state of the cart to localStorage
  saveCart() {
    localStorage.setItem("cart", JSON.stringify(this.cart));
  }

  // Add a product to the cart
  addProduct(product) {
    const existingProduct = this.cart.find((item) => item.id === product.id);

    if (existingProduct) {
      existingProduct.quantity += product.quantity;
    } else {
      this.cart.push(product);
    }

    this.saveCart();
  }

  // Remove a product from the cart
  removeProduct(productId) {
    this.cart = this.cart.filter((item) => item.id !== productId);
    this.saveCart();
  }

  // Update product quantity in the cart
  updateProductQuantity(productId, newQuantity) {
    const product = this.cart.find((item) => item.id === productId);

    if (product) {
      if (newQuantity <= 0) {
        this.removeProduct(productId);
      } else {
        product.quantity = newQuantity;
      }
      this.saveCart();
    }
  }

  // Clear the cart
  clearCart() {
    this.cart = [];
    this.saveCart();
  }

  // Get the total price of all products in the cart
  getTotalPrice() {
    return this.cart.reduce(
      (total, product) => total + product.price * product.quantity,
      0
    );
  }

  // Get the total quantity of items in the cart
  getTotalQuantity() {
    return this.cart.reduce((total, product) => total + product.quantity, 0);
  }

  // Get all products in the cart
  getProducts() {
    return this.cart;
  }
}

// Example usage:
const cart = new Cart();

// Add a product to the cart
cart.addProduct({ id: 1, name: "Product 1", price: 100, quantity: 1 });

// Update quantity of a product
cart.updateProductQuantity(1, 2);

// Remove a product from the cart
// cart.removeProduct(1);

// Get the total price of the products in the cart
console.log("Total Price: ", cart.getTotalPrice());

// Get the total quantity of items in the cart
console.log("Total Quantity: ", cart.getTotalQuantity());

// Clear the cart
// cart.clearCart();
