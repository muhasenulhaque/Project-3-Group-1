    refreshBalanceExchange: function () {
        //refresh your balance

            return exchangeInstance.getBalance("FIXED", {from: account});
        }).then(function (value) {
            var balance_element = document.getElementById("balanceTokenInExchange");
            balance_element.innerHTML = value.toNumber();
            return exchangeInstance.getEthBalanceInWei({from: account});

            return exchangeInstance.depositEther({value: web3.toWei(amountEther, "Ether"), from: account});

            return exchangeInstance.withdrawEther(web3.toWei(amountEther, "Ether"), {from: account});

            return exchangeInstance.depositToken(nameToken, amountToken, {from: account, gas: 4500000});

            return exchangeInstance.withdrawToken(nameToken, amountTokens, {from: account});

    updateOrderBooks: function () {
        //update the order books function

            return exchangeInstance.getSellOrderBook("FIXED");

            return exchangeInstance.getBuyOrderBook("FIXED");

//listen to trading events
        var exchangeInstance;

            exchangeInstance.LimitSellOrderCreated({}, {

            exchangeInstance.LimitBuyOrderCreated({}, {

            exchangeInstance.SellOrderFulfilled({}, {fromBlock: 0, toBlock: 'latest'}).watch(function (error, result) {

            exchangeInstance.BuyOrderFulfilled({}, {fromBlock: 0, toBlock: 'latest'}).watch(function (error, result) {

            return exchangeInstance.sellToken(tokenName, price, amount, {from: account, gas: 4000000});

            return exchangeInstance.buyToken(tokenName, price, amount, {from: account, gas: 4000000});

