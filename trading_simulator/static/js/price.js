function showEOSprice(){
    $.ajax({
    method: "GET",
    url: "https://api.coinmarketcap.com/v2/ticker/1765/",
})
.done(function( msg ) {
    console.log(msg.data.quotes.USD.price);
    $('#eosPrice').text(msg.data.quotes.USD.price.toFixed(2) + " USD");
});
};

function showBTCprice(){
    $.ajax({
        method: "GET",
        url: "https://api.coinmarketcap.com/v2/ticker/1/",
    })
    .done(function( msg ) {
        console.log(msg.data.quotes.USD.price);
        $('#btcPrice').text(msg.data.quotes.USD.price.toFixed(2) + " USD");
    });
};

function showETHprice(){
    $.ajax({
    method: "GET",
    url: "https://api.coinmarketcap.com/v2/ticker/1027/",
})
.done(function( msg ) {
    console.log(msg.data.quotes.USD.price);
    $('#ethPrice').text(msg.data.quotes.USD.price.toFixed(2) + " USD");
});
};
    
function getPrices(){
    showBTCprice();
    showETHprice();
    showEOSprice();
}

getPrices();
var t = setInterval(getPrices, 10000);