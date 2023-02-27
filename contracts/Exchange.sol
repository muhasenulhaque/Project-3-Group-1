pragma solidity ^0.5.0;
//
//      Project-3-Group-1
//      *****************
//
//      Group Membere:  Xu (Flora) Zhao
//                      Md Muhasenul Haque
//                      Samuel Nayacakalou
//
//      Date:           March 2023
//
//      Original Code:  https://github.com/tomw1808/distributed_exchange_truffle_class_3
//


// Adding SafeMath Library to improve security
// @NOTE: This only works in Remix. Alternatively, paste the contents of SafeMath.sol directly here above ArcadeToken. You should use version 2.5.

import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/math/SafeMath.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC20/ERC20.sol";

import "./owned.sol";
import "./FixedSupplyToken.sol";


contract Exchange is owned {

//      Project-3-Group-1
//      *****************
// Using SafeMath Library for improved security
    using SafeMath for uint;
 //   using SafeMath for uint;

/*
EXAMPLE CODE

    function transfer(address recipient, uint value) public {
        balances[msg.sender] = balances[msg.sender].sub(value);
        balances[recipient] = balances[recipient].add(value);
    }
*/

    ///////////////////////
    // GENERAL STRUCTURE //
    ///////////////////////
    struct Offer {

    uint amount;
    address who;
    }

    struct OrderBook {

    uint higherPrice;
    uint lowerPrice;

    mapping (uint => Offer) offers;

    uint offers_key;
    uint offers_length;
    }

    struct Token {

    address tokenContract;

    string symbolName;


    mapping (uint => OrderBook) buyBook;

    uint curBuyPrice;
    uint lowestBuyPrice;
    uint amountBuyPrices;


    mapping (uint => OrderBook) sellBook;
    uint curSellPrice;
    uint highestSellPrice;
    uint amountSellPrices;

    }


    //we support a max of 255 tokens...
    mapping (uint => Token) tokens;
    uint tokenIndex;

    //////////////
    // BALANCES //
    //////////////
    mapping (address => mapping (uint => uint)) tokenBalanceForAddress;

    mapping (address => uint) balanceEthForAddress;




    ////////////
    // EVENTS //
    ////////////

    //EVENTS for Deposit/withdrawal
    event DepositForTokenReceived(address indexed _from, uint indexed _symbolIndex, uint _amount, uint _timestamp);

    event WithdrawalToken(address indexed _to, uint indexed _symbolIndex, uint _amount, uint _timestamp);

    event DepositForEthReceived(address indexed _from, uint _amount, uint _timestamp);

    event WithdrawalEth(address indexed _to, uint _amount, uint _timestamp);

    //events for orders
    event LimitSellOrderCreated(uint indexed _symbolIndex, address indexed _who, uint _amountTokens, uint _priceInWei, uint _orderKey);

    event SellOrderFulfilled(uint indexed _symbolIndex, uint _amount, uint _priceInWei, uint _orderKey);

    event SellOrderCanceled(uint indexed _symbolIndex, uint _priceInWei, uint _orderKey);

    event LimitBuyOrderCreated(uint indexed _symbolIndex, address indexed _who, uint _amountTokens, uint _priceInWei, uint _orderKey);

    event BuyOrderFulfilled(uint indexed _symbolIndex, uint _amount, uint _priceInWei, uint _orderKey);

    event BuyOrderCanceled(uint indexed _symbolIndex, uint _priceInWei, uint _orderKey);

    //events for management
    event TokenAddedToSystem(uint _symbolIndex, string _token, uint _timestamp);



    //////////////////////////////////
    // DEPOSIT AND WITHDRAWAL ETHER //
    //////////////////////////////////
    
	function depositEther() public payable {


	//      Project-3-Group-1
    //      *****************
	//	Converted arithmetic operations to SafeMath equivalent	
	//
	//require(balanceEthForAddress[msg.sender] + msg.value >= balanceEthForAddress[msg.sender]);
	//balanceEthForAddress[msg.sender] += msg.value;	
        require(balanceEthForAddress[msg.sender].add(msg.value) >= balanceEthForAddress[msg.sender]);
        balanceEthForAddress[msg.sender] = balanceEthForAddress[msg.sender].add(msg.value);
        emit DepositForEthReceived(msg.sender, msg.value, now);
    }

    function withdrawEther(uint amountInWei) public {
	
	//      Project-3-Group-1
    //      *****************
	//	Converted arithmetic operations to SafeMath equivalent	
	//
    //    require(balanceEthForAddress[msg.sender] - amountInWei >= 0);
    //    require(balanceEthForAddress[msg.sender] - amountInWei <= balanceEthForAddress[msg.sender]);
    //    balanceEthForAddress[msg.sender] -= amountInWei;	
        require(balanceEthForAddress[msg.sender].sub(amountInWei) >= 0);
        require(balanceEthForAddress[msg.sender].sub(amountInWei) <= balanceEthForAddress[msg.sender]);
        balanceEthForAddress[msg.sender] = balanceEthForAddress[msg.sender].sub(amountInWei);
        msg.sender.transfer(amountInWei);
        emit WithdrawalEth(msg.sender, amountInWei, now);
    }

    function getEthBalanceInWei() view public returns (uint){
        return balanceEthForAddress[msg.sender];
    }


    //////////////////////
    // TOKEN MANAGEMENT //
    //////////////////////

    //      Project-3-Group-1
    //      *****************
    // FIXED - TypeError: Data location must be "memory" for parameter in function, but none was given.
    //Added 'memory' to function declaration
    function addToken(string memory symbolName, address erc20TokenAddress) public onlyowner {
        require(!hasToken(symbolName));
		
	//      Project-3-Group-1
    //      *****************
	//	Converted arithmetic operations to SafeMath equivalent	
	//
    //    require(tokenIndex + 1 > tokenIndex);
    //    tokenIndex++;
        require(tokenIndex.add(1) > tokenIndex);
        tokenIndex = tokenIndex.add(1);

        tokens[tokenIndex].symbolName = symbolName;
        tokens[tokenIndex].tokenContract = erc20TokenAddress;
        emit TokenAddedToSystem(tokenIndex, symbolName, now);
    }

    //      Project-3-Group-1
    //      *****************    
    // FIXED - TypeError: Data location must be "memory" for parameter in function, but none was given.
    //Added 'memory' to function declaration
    function hasToken(string memory symbolName) view public returns (bool) {
        uint index = getSymbolIndex(symbolName);
        if (index == 0) {
            return false;
        }
        return true;
    }

    //      Project-3-Group-1
    //      *****************
    // FIXED - TypeError: Data location must be "memory" for parameter in function, but none was given.
    //Added 'memory' to function declaration
    function getSymbolIndex(string memory symbolName) internal view returns (uint) {
        for (uint i = 1; i <= tokenIndex; i++) {
            if (stringsEqual(tokens[i].symbolName, symbolName)) {
                return i;
            }
        }
        return 0;
    }

    //      Project-3-Group-1
    //      *****************
    // FIXED - TypeError: Data location must be "memory" for parameter in function, but none was given.
    //Added 'memory' to function declaration
    function getSymbolIndexOrThrow(string memory symbolName) public view returns (uint) {
        uint index = getSymbolIndex(symbolName);
        require(index > 0);
        return index;
    }







    //////////////////////////////////
    // DEPOSIT AND WITHDRAWAL TOKEN //
    //////////////////////////////////

    //      Project-3-Group-1
    //      *****************
    // FIXED - TypeError: Data location must be "memory" for parameter in function, but none was given.
    //Added 'memory' to function declaration
    function depositToken(string memory symbolName, uint amount) public {
        uint symbolNameIndex = getSymbolIndexOrThrow(symbolName);
        require(tokens[symbolNameIndex].tokenContract != address(0));

        ERC20Interface token = ERC20Interface(tokens[symbolNameIndex].tokenContract);

        require(token.transferFrom(msg.sender, address(this), amount) == true);
        require(tokenBalanceForAddress[msg.sender][symbolNameIndex] + amount >= tokenBalanceForAddress[msg.sender][symbolNameIndex]);

	//      Project-3-Group-1
    //      *****************
	//	Converted arithmetic operations to SafeMath equivalent	
	//
    //    tokenBalanceForAddress[msg.sender][symbolNameIndex] += amount;
	
		tokenBalanceForAddress[msg.sender][symbolNameIndex] = tokenBalanceForAddress[msg.sender][symbolNameIndex].add(amount);

        emit DepositForTokenReceived(msg.sender, symbolNameIndex, amount, now);
    }

    //      Project-3-Group-1
    //      *****************
    // FIXED - TypeError: Data location must be "memory" for parameter in function, but none was given.
    //Added 'memory' to function declaration
    function withdrawToken(string memory symbolName, uint amount) public {
        uint symbolNameIndex = getSymbolIndexOrThrow(symbolName);
        require(tokens[symbolNameIndex].tokenContract != address(0));

        ERC20Interface token = ERC20Interface(tokens[symbolNameIndex].tokenContract);

        require(tokenBalanceForAddress[msg.sender][symbolNameIndex] - amount >= 0);
        require(tokenBalanceForAddress[msg.sender][symbolNameIndex] - amount <= tokenBalanceForAddress[msg.sender][symbolNameIndex]);
	//      Project-3-Group-1
    //      *****************
	//	Converted arithmetic operations to SafeMath equivalent	
	//
    //    tokenBalanceForAddress[msg.sender][symbolNameIndex] -= amount;

        tokenBalanceForAddress[msg.sender][symbolNameIndex] = tokenBalanceForAddress[msg.sender][symbolNameIndex].sub(amount);
        require(token.transfer(msg.sender, amount) == true);
        emit WithdrawalToken(msg.sender, symbolNameIndex, amount, now);
    }

    
    //      Project-3-Group-1
    //      *****************
    // FIXED - TypeError: Data location must be "memory" for parameter in function, but none was given.
    //Added 'memory' to function declaration
    function getBalance(string memory symbolName) view public returns (uint) {
        uint symbolNameIndex = getSymbolIndexOrThrow(symbolName);
        return tokenBalanceForAddress[msg.sender][symbolNameIndex];
    }



    /////////////////////////////
    // ORDER BOOK - BID ORDERS //
    /////////////////////////////

    //      Project-3-Group-1
    //      *****************
    // FIXED - TypeError: Data location must be "memory" for parameter in function, but none was given.
    //Added 'memory' to function declaration
    //Added 'memory to return datatype
    function getBuyOrderBook(string memory symbolName) view public returns (uint[] memory, uint[] memory) {
        uint tokenNameIndex = getSymbolIndexOrThrow(symbolName);
        uint[] memory arrPricesBuy = new uint[](tokens[tokenNameIndex].amountBuyPrices);
        uint[] memory arrVolumesBuy = new uint[](tokens[tokenNameIndex].amountBuyPrices);

        uint whilePrice = tokens[tokenNameIndex].lowestBuyPrice;
        uint counter = 0;
        if (tokens[tokenNameIndex].curBuyPrice > 0) {
            while (whilePrice <= tokens[tokenNameIndex].curBuyPrice) {
                arrPricesBuy[counter] = whilePrice;
                uint volumeAtPrice = 0;
                uint offers_key = 0;

                offers_key = tokens[tokenNameIndex].buyBook[whilePrice].offers_key;
                while (offers_key <= tokens[tokenNameIndex].buyBook[whilePrice].offers_length) {

	//      Project-3-Group-1
    //      *****************
	//	Converted arithmetic operations to SafeMath equivalent	
	//
    //                volumeAtPrice += tokens[tokenNameIndex].buyBook[whilePrice].offers[offers_key].amount;
    //                offers_key++;	
                    volumeAtPrice = volumeAtPrice.add(tokens[tokenNameIndex].buyBook[whilePrice].offers[offers_key].amount);
                    offers_key = offers_key.add(1);
                }

                arrVolumesBuy[counter] = volumeAtPrice;

                //next whilePrice
                if (whilePrice == tokens[tokenNameIndex].buyBook[whilePrice].higherPrice) {
                    break;
                }
                else {
                    whilePrice = tokens[tokenNameIndex].buyBook[whilePrice].higherPrice;
                }
				
	//      Project-3-Group-1
    //      *****************
	//	Converted arithmetic operations to SafeMath equivalent	
	//
    //            counter++;	
                counter = counter.add(1);

            }
        }

        return (arrPricesBuy, arrVolumesBuy);

    }


    /////////////////////////////
    // ORDER BOOK - ASK ORDERS //
    /////////////////////////////

    //      Project-3-Group-1
    //      *****************
    // FIXED - TypeError: Data location must be "memory" for parameter in function, but none was given.
    //Added 'memory' to function declaration
    //Added 'memory to return datatype
    function getSellOrderBook(string memory symbolName) view public returns (uint[] memory, uint[] memory) {
        uint tokenNameIndex = getSymbolIndexOrThrow(symbolName);
        uint[] memory arrPricesSell = new uint[](tokens[tokenNameIndex].amountSellPrices);
        uint[] memory arrVolumesSell = new uint[](tokens[tokenNameIndex].amountSellPrices);
        uint sellWhilePrice = tokens[tokenNameIndex].curSellPrice;
        uint sellCounter = 0;
        if (tokens[tokenNameIndex].curSellPrice > 0) {
            while (sellWhilePrice <= tokens[tokenNameIndex].highestSellPrice) {
                arrPricesSell[sellCounter] = sellWhilePrice;
                uint sellVolumeAtPrice = 0;
                uint sell_offers_key = 0;

                sell_offers_key = tokens[tokenNameIndex].sellBook[sellWhilePrice].offers_key;
                while (sell_offers_key <= tokens[tokenNameIndex].sellBook[sellWhilePrice].offers_length) {

	//      Project-3-Group-1
    //      *****************
	//	Converted arithmetic operations to SafeMath equivalent	
	//
    //                sellVolumeAtPrice += tokens[tokenNameIndex].sellBook[sellWhilePrice].offers[sell_offers_key].amount;
    //                sell_offers_key++;
	
                    sellVolumeAtPrice = sellVolumeAtPrice.add(tokens[tokenNameIndex].sellBook[sellWhilePrice].offers[sell_offers_key].amount);
                    sell_offers_key = sell_offers_key.add(1);
                }

                arrVolumesSell[sellCounter] = sellVolumeAtPrice;

                //next whilePrice
                if (tokens[tokenNameIndex].sellBook[sellWhilePrice].higherPrice == 0) {
                    break;
                }
                else {
                    sellWhilePrice = tokens[tokenNameIndex].sellBook[sellWhilePrice].higherPrice;
                }
	//      Project-3-Group-1
    //      *****************
	//	Converted arithmetic operations to SafeMath equivalent	
	//
    //            sellCounter++;
	
                sellCounter = sellCounter.add(1);

            }
        }

        //sell part
        return (arrPricesSell, arrVolumesSell);
    }





    ////////////////////////////
    // NEW ORDER - BID ORDER //
    ///////////////////////////

    //      Project-3-Group-1
    //      *****************
    // FIXED - TypeError: Data location must be "memory" for parameter in function, but none was given.
    //Added 'memory' to function declaration
    function buyToken(string memory symbolName, uint priceInWei, uint amount) public {
        uint tokenNameIndex = getSymbolIndexOrThrow(symbolName);
        uint total_amount_ether_necessary = 0;

        if (tokens[tokenNameIndex].amountSellPrices == 0 || tokens[tokenNameIndex].curSellPrice > priceInWei) {
            //if we have enough ether, we can buy that:
			
	//      Project-3-Group-1
    //      *****************
	//	Converted arithmetic operations to SafeMath equivalent	
	//
    //        total_amount_ether_necessary = amount * priceInWei;

            total_amount_ether_necessary = amount.mul(priceInWei);

            //overflow check
            require(total_amount_ether_necessary >= amount);
            require(total_amount_ether_necessary >= priceInWei);
            require(balanceEthForAddress[msg.sender] >= total_amount_ether_necessary);

	//      Project-3-Group-1
    //      *****************
	//	Converted arithmetic operations to SafeMath equivalent	
	//
    //        require(balanceEthForAddress[msg.sender] - total_amount_ether_necessary >= 0);
    //        require(balanceEthForAddress[msg.sender] - total_amount_ether_necessary <= balanceEthForAddress[msg.sender]);
	
            require(balanceEthForAddress[msg.sender].sub(total_amount_ether_necessary) >= 0);
            require(balanceEthForAddress[msg.sender].sub(total_amount_ether_necessary) <= balanceEthForAddress[msg.sender]);

            //first deduct the amount of ether from our balance
            //balanceEthForAddress[msg.sender] -= total_amount_ether_necessary;

            balanceEthForAddress[msg.sender] = balanceEthForAddress[msg.sender].sub(total_amount_ether_necessary);

            //limit order: we don't have enough offers to fulfill the amount

            //add the order to the orderBook
            addBuyOffer(tokenNameIndex, priceInWei, amount, msg.sender);
            //and emit the event.
            emit LimitBuyOrderCreated(tokenNameIndex, msg.sender, amount, priceInWei, tokens[tokenNameIndex].buyBook[priceInWei].offers_length);
        }
        else {
            //market order: current sell price is smaller or equal to buy price!

            //1st: find the "cheapest sell price" that is lower than the buy amount  [buy: 60@5000] [sell: 50@4500] [sell: 5@5000]
            //2: buy up the volume for 4500
            //3: buy up the volume for 5000
            //if still something remaining -> buyToken

            //2: buy up the volume
            //2.1 add ether to seller, add symbolName to buyer until offers_key <= offers_length

            uint total_amount_ether_available = 0;
            uint whilePrice = tokens[tokenNameIndex].curSellPrice;
            uint amountNecessary = amount;
            uint offers_key;
            while (whilePrice <= priceInWei && amountNecessary > 0) {//we start with the smallest sell price.
                offers_key = tokens[tokenNameIndex].sellBook[whilePrice].offers_key;
                while (offers_key <= tokens[tokenNameIndex].sellBook[whilePrice].offers_length && amountNecessary > 0) {//and the first order (FIFO)
                    uint volumeAtPriceFromAddress = tokens[tokenNameIndex].sellBook[whilePrice].offers[offers_key].amount;

                    //Two choices from here:
                    //1) one person offers not enough volume to fulfill the market order - we use it up completely and move on to the next person who offers the symbolName
                    //2) else: we make use of parts of what a person is offering - lower his amount, fulfill out order.
                    if (volumeAtPriceFromAddress <= amountNecessary) {
					
	//      Project-3-Group-1
    //      *****************
	//	Converted arithmetic operations to SafeMath equivalent	
	//
    //                    total_amount_ether_available = volumeAtPriceFromAddress * whilePrice;
	
                        total_amount_ether_available = volumeAtPriceFromAddress.mul(whilePrice);

                        require(balanceEthForAddress[msg.sender] >= total_amount_ether_available);
                        require(balanceEthForAddress[msg.sender] - total_amount_ether_available <= balanceEthForAddress[msg.sender]);
                        //first deduct the amount of ether from our balance
						
                        //balanceEthForAddress[msg.sender] -= total_amount_ether_available;
                        balanceEthForAddress[msg.sender] = balanceEthForAddress[msg.sender].sub(total_amount_ether_available);

                        require(tokenBalanceForAddress[msg.sender][tokenNameIndex] + volumeAtPriceFromAddress >= tokenBalanceForAddress[msg.sender][tokenNameIndex]);
                        require(balanceEthForAddress[tokens[tokenNameIndex].sellBook[whilePrice].offers[offers_key].who] + total_amount_ether_available >= balanceEthForAddress[tokens[tokenNameIndex].sellBook[whilePrice].offers[offers_key].who]);
                        //overflow check
                        //this guy offers less or equal the volume that we ask for, so we use it up completely.
						
                        //tokenBalanceForAddress[msg.sender][tokenNameIndex] += volumeAtPriceFromAddress;
                        tokenBalanceForAddress[msg.sender][tokenNameIndex] = tokenBalanceForAddress[msg.sender][tokenNameIndex].add(volumeAtPriceFromAddress);
                        tokens[tokenNameIndex].sellBook[whilePrice].offers[offers_key].amount = 0;

                        //balanceEthForAddress[tokens[tokenNameIndex].sellBook[whilePrice].offers[offers_key].who] += total_amount_ether_available;
                        //tokens[tokenNameIndex].sellBook[whilePrice].offers_key++;
                        balanceEthForAddress[tokens[tokenNameIndex].sellBook[whilePrice].offers[offers_key].who] = balanceEthForAddress[tokens[tokenNameIndex].sellBook[whilePrice].offers[offers_key].who].add(total_amount_ether_available);
                        tokens[tokenNameIndex].sellBook[whilePrice].offers_key = tokens[tokenNameIndex].sellBook[whilePrice].offers_key.add(1);

                        emit SellOrderFulfilled(tokenNameIndex, volumeAtPriceFromAddress, whilePrice, offers_key);

                        amountNecessary -= volumeAtPriceFromAddress;
                    }
                    else {
                        require(tokens[tokenNameIndex].sellBook[whilePrice].offers[offers_key].amount > amountNecessary);//sanity

	//      Project-3-Group-1
    //      *****************
	//	Converted arithmetic operations to SafeMath equivalent	
	//
                        //total_amount_ether_necessary = amountNecessary * whilePrice;
                        total_amount_ether_necessary = amountNecessary.mul(whilePrice);
                        require(balanceEthForAddress[msg.sender] - total_amount_ether_necessary <= balanceEthForAddress[msg.sender]);

                        //first deduct the amount of ether from our balance
                        //balanceEthForAddress[msg.sender] -= total_amount_ether_necessary;
                        balanceEthForAddress[msg.sender] = balanceEthForAddress[msg.sender].sub(total_amount_ether_necessary);

                        require(balanceEthForAddress[tokens[tokenNameIndex].sellBook[whilePrice].offers[offers_key].who] + total_amount_ether_necessary >= balanceEthForAddress[tokens[tokenNameIndex].sellBook[whilePrice].offers[offers_key].who]);
                        //overflow check
                        //this guy offers more than we ask for. We reduce his stack, add the tokens to us and the ether to him.

                        //tokens[tokenNameIndex].sellBook[whilePrice].offers[offers_key].amount -= amountNecessary;
                        //balanceEthForAddress[tokens[tokenNameIndex].sellBook[whilePrice].offers[offers_key].who] += total_amount_ether_necessary;
                        //tokenBalanceForAddress[msg.sender][tokenNameIndex] += amountNecessary;
                        tokens[tokenNameIndex].sellBook[whilePrice].offers[offers_key].amount = tokens[tokenNameIndex].sellBook[whilePrice].offers[offers_key].amount.sub(amountNecessary);
                        balanceEthForAddress[tokens[tokenNameIndex].sellBook[whilePrice].offers[offers_key].who] = balanceEthForAddress[tokens[tokenNameIndex].sellBook[whilePrice].offers[offers_key].who].add(total_amount_ether_necessary);
                        tokenBalanceForAddress[msg.sender][tokenNameIndex] = tokenBalanceForAddress[msg.sender][tokenNameIndex].add(amountNecessary);

                        amountNecessary = 0;
                        //we have fulfilled our order
                        emit SellOrderFulfilled(tokenNameIndex, amountNecessary, whilePrice, offers_key);
                    }

                    //if it was the last offer for that price, we have to set the curBuyPrice now lower. Additionally we have one offer less...
                    if (
                    offers_key == tokens[tokenNameIndex].sellBook[whilePrice].offers_length &&
                    tokens[tokenNameIndex].sellBook[whilePrice].offers[offers_key].amount == 0
                    ) {

                        tokens[tokenNameIndex].amountSellPrices--;
                        //we have one price offer less here...
                        //next whilePrice
                        if (whilePrice == tokens[tokenNameIndex].sellBook[whilePrice].higherPrice || tokens[tokenNameIndex].buyBook[whilePrice].higherPrice == 0) {
                            tokens[tokenNameIndex].curSellPrice = 0;
                            //we have reached the last price
                        }
                        else {
                            tokens[tokenNameIndex].curSellPrice = tokens[tokenNameIndex].sellBook[whilePrice].higherPrice;
                            tokens[tokenNameIndex].sellBook[tokens[tokenNameIndex].buyBook[whilePrice].higherPrice].lowerPrice = 0;
                        }
                    }
                    offers_key++;
                }

                //we set the curSellPrice again, since when the volume is used up for a lowest price the curSellPrice is set there...
                whilePrice = tokens[tokenNameIndex].curSellPrice;
            }

            if (amountNecessary > 0) {
                buyToken(symbolName, priceInWei, amountNecessary);
                //add a limit order!
            }
        }
    }


    ///////////////////////////
    // BID LIMIT ORDER LOGIC //
    ///////////////////////////
    function addBuyOffer(uint _tokenIndex, uint priceInWei, uint amount, address who) internal {
        tokens[_tokenIndex].buyBook[priceInWei].offers_length++;
        tokens[_tokenIndex].buyBook[priceInWei].offers[tokens[_tokenIndex].buyBook[priceInWei].offers_length] = Offer(amount, who);


        if (tokens[_tokenIndex].buyBook[priceInWei].offers_length == 1) {
            tokens[_tokenIndex].buyBook[priceInWei].offers_key = 1;
            //we have a new buy order - increase the counter, so we can set the getOrderBook array later

	//      Project-3-Group-1
    //      *****************
	//	Converted arithmetic operations to SafeMath equivalent	
	//
            //tokens[_tokenIndex].amountBuyPrices++;
            tokens[_tokenIndex].amountBuyPrices = tokens[_tokenIndex].amountBuyPrices.add(1);


            //lowerPrice and higherPrice have to be set
            uint curBuyPrice = tokens[_tokenIndex].curBuyPrice;

            uint lowestBuyPrice = tokens[_tokenIndex].lowestBuyPrice;
            if (lowestBuyPrice == 0 || lowestBuyPrice > priceInWei) {
                if (curBuyPrice == 0) {
                    //there is no buy order yet, we insert the first one...
                    tokens[_tokenIndex].curBuyPrice = priceInWei;
                    tokens[_tokenIndex].buyBook[priceInWei].higherPrice = priceInWei;
                    tokens[_tokenIndex].buyBook[priceInWei].lowerPrice = 0;
                }
                else {
                    //or the lowest one
                    tokens[_tokenIndex].buyBook[lowestBuyPrice].lowerPrice = priceInWei;
                    tokens[_tokenIndex].buyBook[priceInWei].higherPrice = lowestBuyPrice;
                    tokens[_tokenIndex].buyBook[priceInWei].lowerPrice = 0;
                }
                tokens[_tokenIndex].lowestBuyPrice = priceInWei;
            }
            else if (curBuyPrice < priceInWei) {
                //the offer to buy is the highest one, we don't need to find the right spot
                tokens[_tokenIndex].buyBook[curBuyPrice].higherPrice = priceInWei;
                tokens[_tokenIndex].buyBook[priceInWei].higherPrice = priceInWei;
                tokens[_tokenIndex].buyBook[priceInWei].lowerPrice = curBuyPrice;
                tokens[_tokenIndex].curBuyPrice = priceInWei;

            }
            else {
                //we are somewhere in the middle, we need to find the right spot first...

                uint buyPrice = tokens[_tokenIndex].curBuyPrice;
                bool weFoundIt = false;
                while (buyPrice > 0 && !weFoundIt) {
                    if (
                    buyPrice < priceInWei &&
                    tokens[_tokenIndex].buyBook[buyPrice].higherPrice > priceInWei
                    ) {
                        //set the new order-book entry higher/lowerPrice first right
                        tokens[_tokenIndex].buyBook[priceInWei].lowerPrice = buyPrice;
                        tokens[_tokenIndex].buyBook[priceInWei].higherPrice = tokens[_tokenIndex].buyBook[buyPrice].higherPrice;

                        //set the higherPrice'd order-book entries lowerPrice to the current Price
                        tokens[_tokenIndex].buyBook[tokens[_tokenIndex].buyBook[buyPrice].higherPrice].lowerPrice = priceInWei;
                        //set the lowerPrice'd order-book entries higherPrice to the current Price
                        tokens[_tokenIndex].buyBook[buyPrice].higherPrice = priceInWei;

                        //set we found it.
                        weFoundIt = true;
                    }
                    buyPrice = tokens[_tokenIndex].buyBook[buyPrice].lowerPrice;
                }
            }
        }
    }




    ////////////////////////////
    // NEW ORDER - ASK ORDER //
    ///////////////////////////

    //      Project-3-Group-1
    //      *****************
    // FIXED - TypeError: Data location must be "memory" for parameter in function, but none was given.
    //Added 'memory' to function declaration
    //Added 'memory to return datatype
    function sellToken(string memory symbolName, uint priceInWei, uint amount) public {
        uint tokenNameIndex = getSymbolIndexOrThrow(symbolName);
        uint total_amount_ether_necessary = 0;
        uint total_amount_ether_available = 0;


        if (tokens[tokenNameIndex].amountBuyPrices == 0 || tokens[tokenNameIndex].curBuyPrice < priceInWei) {

            //if we have enough ether, we can buy that:

	//      Project-3-Group-1
    //      *****************
	//	Converted arithmetic operations to SafeMath equivalent	
	//
            //total_amount_ether_necessary = amount * priceInWei;
            total_amount_ether_necessary = amount.mul(priceInWei);

            //overflow check
            require(total_amount_ether_necessary >= amount);
            require(total_amount_ether_necessary >= priceInWei);
            require(tokenBalanceForAddress[msg.sender][tokenNameIndex] >= amount);

            //require(tokenBalanceForAddress[msg.sender][tokenNameIndex] - amount >= 0);
            //require(balanceEthForAddress[msg.sender] + total_amount_ether_necessary >= balanceEthForAddress[msg.sender]);
            require(tokenBalanceForAddress[msg.sender][tokenNameIndex].sub(amount) >= 0);
            require(balanceEthForAddress[msg.sender].add(total_amount_ether_necessary) >= balanceEthForAddress[msg.sender]);

            //actually subtract the amount of tokens to change it then
            //tokenBalanceForAddress[msg.sender][tokenNameIndex] -= amount;
            tokenBalanceForAddress[msg.sender][tokenNameIndex] = tokenBalanceForAddress[msg.sender][tokenNameIndex].add(amount);

            //limit order: we don't have enough offers to fulfill the amount

            //add the order to the orderBook
            addSellOffer(tokenNameIndex, priceInWei, amount, msg.sender);
            //and emit the event.
            emit LimitSellOrderCreated(tokenNameIndex, msg.sender, amount, priceInWei, tokens[tokenNameIndex].sellBook[priceInWei].offers_length);

        }
        else {
            //market order: current buy price is bigger or equal to sell price!

            //1st: find the "highest buy price" that is higher than the sell amount  [buy: 60@5000] [buy: 50@4500] [sell: 500@4000]
            //2: sell up the volume for 5000
            //3: sell up the volume for 4500
            //if still something remaining -> sellToken limit order

            //2: sell up the volume
            //2.1 add ether to seller, add symbolName to buyer until offers_key <= offers_length


            uint whilePrice = tokens[tokenNameIndex].curBuyPrice;
            uint amountNecessary = amount;
            uint offers_key;
            while (whilePrice >= priceInWei && amountNecessary > 0) {//we start with the highest buy price.
                offers_key = tokens[tokenNameIndex].buyBook[whilePrice].offers_key;
                while (offers_key <= tokens[tokenNameIndex].buyBook[whilePrice].offers_length && amountNecessary > 0) {//and the first order (FIFO)
                    uint volumeAtPriceFromAddress = tokens[tokenNameIndex].buyBook[whilePrice].offers[offers_key].amount;


                    //Two choices from here:
                    //1) one person offers not enough volume to fulfill the market order - we use it up completely and move on to the next person who offers the symbolName
                    //2) else: we make use of parts of what a person is offering - lower his amount, fulfill out order.
                    if (volumeAtPriceFromAddress <= amountNecessary) {

	//      Project-3-Group-1
    //      *****************
	//	Converted arithmetic operations to SafeMath equivalent	
	//
                        //total_amount_ether_available = volumeAtPriceFromAddress * whilePrice;	
                        total_amount_ether_available = volumeAtPriceFromAddress.mul(whilePrice);


                        //overflow check
                        require(tokenBalanceForAddress[msg.sender][tokenNameIndex] >= volumeAtPriceFromAddress);
                        //actually subtract the amount of tokens to change it then

                        //tokenBalanceForAddress[msg.sender][tokenNameIndex] -= volumeAtPriceFromAddress;
                        tokenBalanceForAddress[msg.sender][tokenNameIndex] = tokenBalanceForAddress[msg.sender][tokenNameIndex].sub(volumeAtPriceFromAddress);

                        //overflow check
    
    //      Project-3-Group-1
    //      *****************
	//	Converted arithmetic operations to SafeMath equivalent	
	//
                        //require(tokenBalanceForAddress[msg.sender][tokenNameIndex] - volumeAtPriceFromAddress >= 0);
                        //require(tokenBalanceForAddress[tokens[tokenNameIndex].buyBook[whilePrice].offers[offers_key].who][tokenNameIndex] + volumeAtPriceFromAddress >= tokenBalanceForAddress[tokens[tokenNameIndex].buyBook[whilePrice].offers[offers_key].who][tokenNameIndex]);
                        //require(balanceEthForAddress[msg.sender] + total_amount_ether_available >= balanceEthForAddress[msg.sender]);
                        require(tokenBalanceForAddress[msg.sender][tokenNameIndex].sub(volumeAtPriceFromAddress) >= 0);
                        require(tokenBalanceForAddress[tokens[tokenNameIndex].buyBook[whilePrice].offers[offers_key].who][tokenNameIndex].add(volumeAtPriceFromAddress) >= tokenBalanceForAddress[tokens[tokenNameIndex].buyBook[whilePrice].offers[offers_key].who][tokenNameIndex]);
                        require(balanceEthForAddress[msg.sender].add(total_amount_ether_available) >= balanceEthForAddress[msg.sender]);

                        //this guy offers less or equal the volume that we ask for, so we use it up completely.
                        //tokenBalanceForAddress[tokens[tokenNameIndex].buyBook[whilePrice].offers[offers_key].who][tokenNameIndex] += volumeAtPriceFromAddress;
                        tokenBalanceForAddress[tokens[tokenNameIndex].buyBook[whilePrice].offers[offers_key].who][tokenNameIndex] = tokenBalanceForAddress[tokens[tokenNameIndex].buyBook[whilePrice].offers[offers_key].who][tokenNameIndex].add(volumeAtPriceFromAddress);
                        tokens[tokenNameIndex].buyBook[whilePrice].offers[offers_key].amount = 0;

                        //balanceEthForAddress[msg.sender] += total_amount_ether_available;
                        //tokens[tokenNameIndex].buyBook[whilePrice].offers_key++;
                        balanceEthForAddress[msg.sender] = balanceEthForAddress[msg.sender].add(total_amount_ether_available);
                        tokens[tokenNameIndex].buyBook[whilePrice].offers_key = tokens[tokenNameIndex].buyBook[whilePrice].offers_key.add(1);

                        emit SellOrderFulfilled(tokenNameIndex, volumeAtPriceFromAddress, whilePrice, offers_key);

                        //amountNecessary -= volumeAtPriceFromAddress;
                        amountNecessary = amountNecessary.sub(volumeAtPriceFromAddress);
                    }
                    else {
                        
						
	//      Project-3-Group-1
    //      *****************
	//	Converted arithmetic operations to SafeMath equivalent	
	//
                        //require(volumeAtPriceFromAddress - amountNecessary > 0);
						require(volumeAtPriceFromAddress.sub(amountNecessary) > 0);
                        
						//just for sanity
                        //total_amount_ether_necessary = amountNecessary * whilePrice;									
                        total_amount_ether_necessary = amountNecessary.mul(whilePrice);

                        //we take the rest of the outstanding amount

                        //overflow check
                        require(tokenBalanceForAddress[msg.sender][tokenNameIndex] >= amountNecessary);
                        
						//actually subtract the amount of tokens to change it then
                        //tokenBalanceForAddress[msg.sender][tokenNameIndex] -= amountNecessary;
                        tokenBalanceForAddress[msg.sender][tokenNameIndex] = tokenBalanceForAddress[msg.sender][tokenNameIndex].sub(amountNecessary);

                        //overflow check
                        require(tokenBalanceForAddress[msg.sender][tokenNameIndex] >= amountNecessary);
    
    //      Project-3-Group-1
    //      *****************
	//	Converted arithmetic operations to SafeMath equivalent	
	//
                        //require(balanceEthForAddress[msg.sender] + total_amount_ether_necessary >= balanceEthForAddress[msg.sender]);
                        //require(tokenBalanceForAddress[tokens[tokenNameIndex].buyBook[whilePrice].offers[offers_key].who][tokenNameIndex] + amountNecessary >= tokenBalanceForAddress[tokens[tokenNameIndex].buyBook[whilePrice].offers[offers_key].who][tokenNameIndex]);
                        require(balanceEthForAddress[msg.sender].add(total_amount_ether_necessary) >= balanceEthForAddress[msg.sender]);
                        require(tokenBalanceForAddress[tokens[tokenNameIndex].buyBook[whilePrice].offers[offers_key].who][tokenNameIndex].add(amountNecessary) >= tokenBalanceForAddress[tokens[tokenNameIndex].buyBook[whilePrice].offers[offers_key].who][tokenNameIndex]);

                        //this guy offers more than we ask for. We reduce his stack, add the eth to us and the symbolName to him.
                        
                        //tokens[tokenNameIndex].buyBook[whilePrice].offers[offers_key].amount -= amountNecessary;
                        //balanceEthForAddress[msg.sender] += total_amount_ether_necessary;
                        //tokenBalanceForAddress[tokens[tokenNameIndex].buyBook[whilePrice].offers[offers_key].who][tokenNameIndex] += amountNecessary;
                        tokens[tokenNameIndex].buyBook[whilePrice].offers[offers_key].amount = tokens[tokenNameIndex].buyBook[whilePrice].offers[offers_key].amount.sub(amountNecessary);
                        balanceEthForAddress[msg.sender] = balanceEthForAddress[msg.sender].add(total_amount_ether_necessary);
                        tokenBalanceForAddress[tokens[tokenNameIndex].buyBook[whilePrice].offers[offers_key].who][tokenNameIndex] = tokenBalanceForAddress[tokens[tokenNameIndex].buyBook[whilePrice].offers[offers_key].who][tokenNameIndex].add(amountNecessary);

                        emit SellOrderFulfilled(tokenNameIndex, amountNecessary, whilePrice, offers_key);

                        amountNecessary = 0;
                        //we have fulfilled our order
                    }

                    //if it was the last offer for that price, we have to set the curBuyPrice now lower. Additionally we have one offer less...
                    if (
                    offers_key == tokens[tokenNameIndex].buyBook[whilePrice].offers_length &&
                    tokens[tokenNameIndex].buyBook[whilePrice].offers[offers_key].amount == 0
                    ) {
	//      Project-3-Group-1
    //      *****************
	//	Converted arithmetic operations to SafeMath equivalent	
	//
						//tokens[tokenNameIndex].amountBuyPrices--;
                        tokens[tokenNameIndex].amountBuyPrices = tokens[tokenNameIndex].amountBuyPrices.sub(1);
                        //we have one price offer less here...
                        //next whilePrice
                        if (whilePrice == tokens[tokenNameIndex].buyBook[whilePrice].lowerPrice || tokens[tokenNameIndex].buyBook[whilePrice].lowerPrice == 0) {
                            tokens[tokenNameIndex].curBuyPrice = 0;
                            //we have reached the last price
                        }
                        else {
                            tokens[tokenNameIndex].curBuyPrice = tokens[tokenNameIndex].buyBook[whilePrice].lowerPrice;
                            tokens[tokenNameIndex].buyBook[tokens[tokenNameIndex].buyBook[whilePrice].lowerPrice].higherPrice = tokens[tokenNameIndex].curBuyPrice;
                        }
                    }
                    //offers_key++;
                    offers_key = offers_key.add(1);
                }

                //we set the curSellPrice again, since when the volume is used up for a lowest price the curSellPrice is set there...
                whilePrice = tokens[tokenNameIndex].curBuyPrice;
            }

            if (amountNecessary > 0) {
                sellToken(symbolName, priceInWei, amountNecessary);
                //add a limit order, we couldn't fulfill all the orders!
            }

        }
    }



    ///////////////////////////
    // ASK LIMIT ORDER LOGIC //
    ///////////////////////////
    function addSellOffer(uint _tokenIndex, uint priceInWei, uint amount, address who) internal {
        tokens[_tokenIndex].sellBook[priceInWei].offers_length++;
        tokens[_tokenIndex].sellBook[priceInWei].offers[tokens[_tokenIndex].sellBook[priceInWei].offers_length] = Offer(amount, who);


        if (tokens[_tokenIndex].sellBook[priceInWei].offers_length == 1) {
            tokens[_tokenIndex].sellBook[priceInWei].offers_key = 1;
            //we have a new sell order - increase the counter, so we can set the getOrderBook array later


	//      Project-3-Group-1
    //      *****************
	//	Converted arithmetic operations to SafeMath equivalent	
	//
            //tokens[_tokenIndex].amountSellPrices++;
			tokens[_tokenIndex].amountSellPrices = tokens[_tokenIndex].amountSellPrices.add(1);

            //lowerPrice and higherPrice have to be set
            uint curSellPrice = tokens[_tokenIndex].curSellPrice;

            uint highestSellPrice = tokens[_tokenIndex].highestSellPrice;
            if (highestSellPrice == 0 || highestSellPrice < priceInWei) {
                if (curSellPrice == 0) {
                    //there is no sell order yet, we insert the first one...
                    tokens[_tokenIndex].curSellPrice = priceInWei;
                    tokens[_tokenIndex].sellBook[priceInWei].higherPrice = 0;
                    tokens[_tokenIndex].sellBook[priceInWei].lowerPrice = 0;
                }
                else {

                    //this is the highest sell order
                    tokens[_tokenIndex].sellBook[highestSellPrice].higherPrice = priceInWei;
                    tokens[_tokenIndex].sellBook[priceInWei].lowerPrice = highestSellPrice;
                    tokens[_tokenIndex].sellBook[priceInWei].higherPrice = 0;
                }

                tokens[_tokenIndex].highestSellPrice = priceInWei;

            }
            else if (curSellPrice > priceInWei) {
                //the offer to sell is the lowest one, we don't need to find the right spot
                tokens[_tokenIndex].sellBook[curSellPrice].lowerPrice = priceInWei;
                tokens[_tokenIndex].sellBook[priceInWei].higherPrice = curSellPrice;
                tokens[_tokenIndex].sellBook[priceInWei].lowerPrice = 0;
                tokens[_tokenIndex].curSellPrice = priceInWei;

            }
            else {
                //we are somewhere in the middle, we need to find the right spot first...

                uint sellPrice = tokens[_tokenIndex].curSellPrice;
                bool weFoundIt = false;
                while (sellPrice > 0 && !weFoundIt) {
                    if (
                    sellPrice < priceInWei &&
                    tokens[_tokenIndex].sellBook[sellPrice].higherPrice > priceInWei
                    ) {
                        //set the new order-book entry higher/lowerPrice first right
                        tokens[_tokenIndex].sellBook[priceInWei].lowerPrice = sellPrice;
                        tokens[_tokenIndex].sellBook[priceInWei].higherPrice = tokens[_tokenIndex].sellBook[sellPrice].higherPrice;

                        //set the higherPrice'd order-book entries lowerPrice to the current Price
                        tokens[_tokenIndex].sellBook[tokens[_tokenIndex].sellBook[sellPrice].higherPrice].lowerPrice = priceInWei;
                        //set the lowerPrice'd order-book entries higherPrice to the current Price
                        tokens[_tokenIndex].sellBook[sellPrice].higherPrice = priceInWei;

                        //set we found it.
                        weFoundIt = true;
                    }
                    sellPrice = tokens[_tokenIndex].sellBook[sellPrice].higherPrice;
                }
            }
        }
    }

    //////////////////////////////
    // CANCEL LIMIT ORDER LOGIC //
    //////////////////////////////

    //      Project-3-Group-1
    //      *****************
    // FIXED - TypeError: Data location must be "memory" for parameter in function, but none was given.
    //Added 'memory' to function declaration
    //Added 'memory to return datatype
    function cancelOrder(string memory symbolName, bool isSellOrder, uint priceInWei, uint offerKey) public {
        uint symbolNameIndex = getSymbolIndexOrThrow(symbolName);
        if (isSellOrder) {
            require(tokens[symbolNameIndex].sellBook[priceInWei].offers[offerKey].who == msg.sender);

            uint tokensAmount = tokens[symbolNameIndex].sellBook[priceInWei].offers[offerKey].amount;

	//      Project-3-Group-1
    //      *****************
	//	Converted arithmetic operations to SafeMath equivalent	
	//
            //require(tokenBalanceForAddress[msg.sender][symbolNameIndex] + tokensAmount >= tokenBalanceForAddress[msg.sender][symbolNameIndex]);
            require(tokenBalanceForAddress[msg.sender][symbolNameIndex].add(tokensAmount) >= tokenBalanceForAddress[msg.sender][symbolNameIndex]);

            //tokenBalanceForAddress[msg.sender][symbolNameIndex] += tokensAmount;
            tokenBalanceForAddress[msg.sender][symbolNameIndex] = tokenBalanceForAddress[msg.sender][symbolNameIndex].add(tokensAmount);
            tokens[symbolNameIndex].sellBook[priceInWei].offers[offerKey].amount = 0;
            emit SellOrderCanceled(symbolNameIndex, priceInWei, offerKey);

        }
        else {
            require(tokens[symbolNameIndex].buyBook[priceInWei].offers[offerKey].who == msg.sender);
            uint etherToRefund = tokens[symbolNameIndex].buyBook[priceInWei].offers[offerKey].amount * priceInWei;

	//      Project-3-Group-1
    //      *****************
	//	Converted arithmetic operations to SafeMath equivalent	
	//
            //require(balanceEthForAddress[msg.sender] + etherToRefund >= balanceEthForAddress[msg.sender]);
			require(balanceEthForAddress[msg.sender].add(etherToRefund) >= balanceEthForAddress[msg.sender]);

            //balanceEthForAddress[msg.sender] += etherToRefund;
            balanceEthForAddress[msg.sender] = balanceEthForAddress[msg.sender].add(etherToRefund);
            tokens[symbolNameIndex].buyBook[priceInWei].offers[offerKey].amount = 0;
            emit BuyOrderCanceled(symbolNameIndex, priceInWei, offerKey);
        }
    }






    ////////////////////////////////
    // STRING COMPARISON FUNCTION //
    ////////////////////////////////

    //      Project-3-Group-1
    //      *****************
    /// FIXED: what does "Warning: This function only accepts a single "bytes" argument. Please use "abi.encodePacked(...)" mean
    //https://ethereum.stackexchange.com/questions/50592/what-does-warning-this-function-only-accepts-a-single-bytes-argument-please

    // FIXED - TypeError: Data location must be "memory" for parameter in function, but none was given.
    //Added 'memory' to function declaration
    //Added 'memory to return datatype

    function stringsEqual(string memory _a, string memory _b) internal pure returns (bool) {
        return keccak256(abi.encodePacked(_a)) == keccak256(abi.encodePacked(_b)); // FIXED line of code
    }


}