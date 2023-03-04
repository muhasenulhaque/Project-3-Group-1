# __Bootcamp Project 3: Decentralized Trading Platform Token and Coin trading with Etherium__ 

<img src="./images/iStock-1323542329.jpg" width = "500"> <br>


## __Executive summary__: 
The decentralized exchange can create non-fangible token using the etherium block chain technology. Through this exchange we can deposit or withdraw etherium in wallet, add token in the wallet through smart contract, then approve the added token allowance and then deposit the token to the DEX, buy or sell the token on the DEX and check the order books. 


## __Origin of the Project Concept__ 
The idea of the project is to create a platform where people can trade coins and token within Etherium Technology. We thought of a decentralized trading platform for trading coins and tokens. After research, we found there was already a project created by Thomas Wiesner regarding this matter where the front end is developed with .js file. We thought of understanding the project and communicating with streamlit front end. 

## __Data Collection, Cleanup, and Exploration__
We have reseached on available git hub libraries and found an wonderful work done by "Thomas Wiesne" on decentralized excahgne. The project files are in the following link. 

https://github.com/tomw1808/distributed_exchange_truffle_class_3

We updated the code, compiled it with a newer version of pragma ^0.5.0 instead of ^0.4.21, then we developed a new front end with streamlit.

## __Demo__

### Successfull Deployment of Codes in Remix Development Environment
<img src="./images/Successful_Deployment_of_Exchange_sol.jpg"> <br>
<img src="./images/Successful_Deployment_of_FixedSupplyToken_sol.jpg"> <br>


### Home Page Options
#### There are three tabs: Manage Token, Fund Management and Token Trading

<img src="./images/homepage_options.png"> <br>

### Manage Token Page
- Two main functions: Add Token and Approve Token Allowance

<img src="./images/manage_token_page.png"> <br>

- Only the admin of the exchange can add token, so please choose the wallet address of the exchange
- You can only add new tokens that the exchange hasn't added before
- The token allowance should be approved by the token owner, so please choose the token owner's wallet address in the 'Approve Token Allowance' Section

#### Add Token Successfully
##### Add Token Front End
<img src="./images/add_token_successfully.png" > <br>
##### Successful Transaction of added token
<img src="./images/SuccessfullyAddedToken_MFS.jpg"> <br>

#### Approve Token Allowance Successfully
##### Approve Token Allowance Front End
<img src="./images/approve_token_allowance_successfully.png"> <br>
##### Sucessfully Approved Token Back End
<img src="./images/SuccessfullyApprovedToken_MFS.jpg" > <br>


### Fund Management
#### The layout and functions for fund management page is as below:
<img src="./images/fund_management_page.png" > <br>

### Deposit Token
#### Deposit Token Front End
<img src="./images/deposit_token_successfully.png" > <br>

#### Withdraw Token
<img src="./images/withdraw_token_successfully.png" > <br>

#### Check Token Balance

<img src="./images/check_token_balance.png"> <br>

#### Deposit ETH
##### Wallet ether balance in Ganache before depositing ether to the DEX

<img src="./images/before_deposit_eth_ganache.png" > <br>

#### Successfully Deposited Ether
<img src="./images/Successfully Deposited  of 50 Ether.jpg" > <br>

##### Deposit 10 ETH 

<img src="./images/deposit_eth_successfully.png" > <br>
<img src="./images/ether_balance_check_in_DEX.png" > <br>
<img src="./images/ether_balance_check_in_ganache.png" > <br>

#### Withdraw ETH

<img src="./images/withdraw_eth_successfully.png" > <br>
<img src="./images/ether_balance_check_after_withdraw_in_DEX.png" > <br>

#### Check Ether Balance

as shown in the above

### Token Trading Page
You can buy/sell tokens and you can check order books in this page.

<img src="./images/token_trading_page.png" > <br>

#### Buy Token/Sell Token/Order Book

<img src="./images/buy_token_1.png" > <br>

<img src="./images/buy_token_2.png" > <br>

<img src="./images/buy_token_3.png" > <br>
<img src="./images/sell_token_2.png" > <br>
<img src="./images/sell_token_3.png" > <br>
<img src="./images/price_meet_before.png" > <br>
<img src="./images/price_meet_after.png" > <br>
#### Successfully transferred Token
<img src="./images/SuccessfullyTransferred100Token_MFS.jpg" > <br>

## __Difficulties Faced__ 
- Understanding the different concepts of token address, user wallet address, exchange address etc. and call/choose the right address for the input of the front end.
- Understanding the working machinisam for the decentralised trading platform, how a user should operate and execute the different functions, what is the working process.
- Understanding the data structure of token, orderbook and offers.
- We faced a bit of the difficulty in deploying the project beacuse of differnet versions of solidity. We tried checked and upgraded with recent solidy version. 
- We faced a bit of difficulty in interacting the back end with the front end. We debugged the issues with breaking the code in steps. 

## __Future Scope of Work__

- __ADDING NEW FEATURES__
  - Add more than one tokens to the DEX
  - Cancel Order Function
  - Emits Events : display more info in the front end or enable the user to check convieniently
  - Display more info in the front end, e.g. Display the allowance for the owner
  - Going for Initial Coin Offerings for the new coins introduced in the exchange. 
- __UI OPTIMIZATION__
  - Sidebar fonts should be bigger 
  - Some input boxes can be deleted when the functions are optimized
- __OTHER FRONT END SUPPORTED__
  - Creating mobile app to interact with the clients for the front end. Truffle version development to support mobile apps

## __References__

<img src="./images/udemy_course.png" > <br>

- https://github.com/tomw1808/distributed_exchange_truffle_class_3

- Imported SafeMath from 
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/math/SafeMath.sol";

- Imported ERC20.sol
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC20/ERC20.sol";

## __Team__


### Team Memebers Flora Zhao, Samuel Apakuki Nayacakalou, Md Muhasenul Haque
<p float="left">
    <img src="./images/Xu_Flora_Zhao.png" width = "100"> 
    <img src="./images/Samuel_Nayacakalou.png" width = "100"> 
    <img src="./images/Md_Muhasenul_Haque.png" width = "100"> 
</p>

### Course Instructor 
### Adrian Rusli
<img src="./images/Adrian Rusli - Instructor.png" width = "150"> <br>

### and Larry Hang
<img src="./images/Larry Huang - TA.png" width = "150"> <br>

