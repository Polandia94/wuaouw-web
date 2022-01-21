
const productContainers = [...document.querySelectorAll('.product-container')];
const nxtBtn = [...document.querySelectorAll('.nxt-btn')];
const preBtn = [...document.querySelectorAll('.pre-btn')];

productContainers.forEach((item, i) => {
    console.log("b")
    let containerDimenstions = item.getBoundingClientRect();
    let containerWidth = containerDimenstions.width;

    nxtBtn[i].addEventListener('click', () => {
        item.scrollLeft += containerWidth;
    })

    preBtn[i].addEventListener('click', () => {
        item.scrollLeft -= containerWidth;
    })
})

function calcularElementos(oldItems){
    botones = document.querySelectorAll('.card-btn-cancel')
    botones.forEach(element => {
        element.style.visibility = 'hidden'
    });
    numeros = document.querySelectorAll('.cantidad-comprada')
    numeros.forEach(element => {
        element.style.visibility = 'hidden'
    });

    elementosContados = {}
    oldItems.forEach(element => {
        if(element in elementosContados){
            elementosContados[element] = elementosContados[element] + 1
            nombre = "cantidad-comprada-"+element
            document.getElementById(nombre).innerHTML = elementosContados[element]
        }else{
            elementosContados[element] = 1
            nombre = "cantidad-comprada-"+element
            document.getElementById(nombre).innerHTML = elementosContados[element]
            console.log('btnEliminar'+element)
            var nombre = 'btnEliminar'+element
            document.getElementById(nombre).style.visibility = 'visible'
            nombre = "cantidad-comprada-"+element
            document.getElementById(nombre).style.visibility = 'visible'
        }
    
    });
    console.log(elementosContados)
    
    

}

$(document).on("click", "button[id^=btnComprar]", function (event) {
    var id_shop = $(this).data('id_shop');
    var oldItems = JSON.parse(localStorage.getItem('carrito')) || [];
    var newItem = id_shop
    oldItems.push(newItem);
    localStorage.setItem('carrito', JSON.stringify(oldItems));
    calcularCarrito()
    calcularElementos(oldItems)
})
$(document).on("click", "button[id^=btnEliminar]", function (event) {
    var id_shop = $(this).data('id_shop');
    var oldItems = JSON.parse(localStorage.getItem('carrito')) || [];
    var deleteItem = id_shop
    var aEliminar = true
    oldItems.forEach((element, i) => {
        if(deleteItem == element && aEliminar){
            oldItems.splice(i, 1);
            aEliminar = false;
        }
    });
    localStorage.setItem('carrito', JSON.stringify(oldItems));
    calcularCarrito()
    calcularElementos(oldItems)
})
var oldItems = JSON.parse(localStorage.getItem('carrito')) || [];
calcularElementos(oldItems)

$(document).on("click", "button[id^=btnSearch]", function (event) {
    var busqueda = document.getElementById("boxSearch").value
    location.href = "/search?busqueda="+busqueda
});