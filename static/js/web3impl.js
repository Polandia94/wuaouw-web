const provider = new ethers.providers.Web3Provider(window.ethereum)
//const providerJson = new ethers.providers.JsonRpcProvider();

// The MetaMask plugin also allows signing transactions to
// send ether and pay to change state within the blockchain.
// For this, you need the account signer...

async function iniciarSesion(){
    await provider.send("eth_requestAccounts", []);
    const signer = provider.getSigner();
    address = await signer.getAddress()
    login.innerHTML = address.substring(0,8) + "..."
    return await signer
}

async function realizarPago(direccion, monto){
    console.log(typeof signer)
    if(typeof signer == 'undefined'){
        signer = await iniciarSesion()
    }
    const tx = await signer.sendTransaction({
        to: direccion,
        value: monto
    });
    return tx
}

async function firmar(texto){
    if(typeof signer == 'undefined'){
        signer = await iniciarSesion()
    }
    signature = await signer.signMessage(texto);
    return await signer.getAddress()
}

async function cargarBilletera(){
    const signer = provider.getSigner();
    address = await signer.getAddress()
    login.innerHTML = address.substring(0,8) + "..."
    return await signer
}
signer = cargarBilletera()
//iniciarSesion();
$(document).on("click", "button[id^=login]", function (event) {
    signer = iniciarSesion()
    
});


