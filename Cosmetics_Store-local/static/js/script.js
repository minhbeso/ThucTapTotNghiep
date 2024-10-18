document.addEventListener("keydown", function (e) {
  if (e.ctrlKey && e.key === "k") {
    e.preventDefault();
    const searchModalToggle = document.querySelector(
      "label[for='search-modal']"
    );
    searchModalToggle.click();
  }
});

function quantityUpdate(
  value,
  cart_item_id = "",
  post_form = false,
  max = 999
) {
  const updateQuantity = (inputElement, value) => {
    let currentValue = parseInt(inputElement.value) || 0;
    let newValue = currentValue + value;

    if (newValue > 0 && newValue <= max) {
      inputElement.value = newValue;
      return true;
    } else return false;
  };

  if (cart_item_id) {
    const pqi = document.querySelector(
      `input#${CSS.escape(cart_item_id + "-quantity")}`
    );
    if (pqi) {
      const is_post = updateQuantity(pqi, value);

      if (post_form && is_post) {
        const quantity_form = document.querySelector(
          `form#${CSS.escape(cart_item_id + "-form")}`
        );
        if (quantity_form) quantity_form.submit();
      }
    }
  } else {
    document.querySelectorAll("[product-quantity-input]").forEach((element) => {
      updateQuantity(element, value);
    });
  }
}

function createOneOrder() {
  const createOrderForm = document.getElementById("create-order");
  createOrderForm.submit();
}

function updateTotalPaymentAndSelection(itemTotalPrice, itemChecked) {
  const selectedAllCheckbox = document.getElementById("selected-all-checkbox");
  const totalSelectedLabel = document.querySelector("[total-selected-label]");
  const totalPaymentLabel = document.getElementById("total-payment-label");
  const btnBaseOnSelecteds = document.querySelectorAll(
    "[btn-base-on-selected]"
  );

  const maxTotalSelected = document.querySelectorAll(
    "[cart-item-checkbox]"
  ).length;

  const totalPayment =
    parseFloat(totalPaymentLabel.getAttribute("data-total-payment")) || 0;
  const totalSelected = parseInt(totalSelectedLabel.textContent) || 0;

  // Update total payment and selected count
  const newTotalPayment =
    totalPayment + (itemChecked ? itemTotalPrice : -itemTotalPrice);
  const newTotalSelected = totalSelected + (itemChecked ? 1 : -1);

  selectedAllCheckbox.checked = newTotalSelected >= maxTotalSelected;
  btnBaseOnSelecteds.forEach((btn) => (btn.disabled = newTotalPayment === 0));

  // Update labels
  totalPaymentLabel.textContent = formatMoney(newTotalPayment);
  totalPaymentLabel.setAttribute("data-total-payment", newTotalPayment);
  totalSelectedLabel.textContent = newTotalSelected;
}

function handleCartItemSelection(element) {
  const itemID = element.id.split("-")[0];
  const itemChecked = element.checked;

  const itemTotalPrice = parseFloat(
    document
      .querySelector(`#${CSS.escape(itemID + "-total-price")}`)
      .getAttribute("data-total-price")
  );
  const itemOthers = document.querySelectorAll(
    `input[cart-item-other][value='${itemID}']`
  );

  itemOthers.forEach((element) => (element.disabled = !itemChecked));
  updateTotalPaymentAndSelection(itemTotalPrice, itemChecked);
}

function onCartItemSelected(e) {
  handleCartItemSelection(e.target);
}

function onSelectAllCartItem(e) {
  const allCartItems = document.querySelectorAll("[cart-item-checkbox]");
  const allChecked = e.target.checked;

  allCartItems.forEach((element) => {
    if (element.checked != allChecked) {
      element.checked = allChecked;
      handleCartItemSelection(element);
    }
  });
}

function formatMoney(value) {
  return (
    new Intl.NumberFormat("en-US", { maximumFractionDigits: 20 }).format(
      value
    ) || value
  );
}

function previewAvatar(e, imgID) {
  const file = e.target.files[0];
  if (file && file.type.startsWith("image/")) {
    const reader = new FileReader();
    reader.onload = function (event) {
      const imgElement = document.getElementById(imgID);
      imgElement.src = event.target.result;
    };
    reader.readAsDataURL(file);
  }
}

function onSearch(e) {
  const searchInput = document.getElementById("search-input");

  if (e.key === "Enter") {
    if (!searchInput.checkValidity()) {
      searchInput.reportValidity();
      return;
    }
    this.submit();
  }
}
