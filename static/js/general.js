function calcularCarrito(){
    var oldItems = JSON.parse(localStorage.getItem('carrito')) || [];
    var cantidad = oldItems.length
    console.log(cantidad)
    cart.innerHTML = '<i class="fas fa-shopping-cart"></i> ' + cantidad
}
calcularCarrito()

$(document).on("click", "a[id^=cart]", function (event) {
    var oldItems = JSON.parse(localStorage.getItem('carrito')) || [];
    location.href = "/cart?carrito="+oldItems
});