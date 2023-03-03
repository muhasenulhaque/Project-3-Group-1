
    ################################################################################    
    #   Project-3-Group-1
    #   *****************
    ################################################################################
    #
    #
    #   Group Membere:  Xu (Flora) Zhao
    #                   Md Muhasenul Haque
    #                   Samuel Nayacakalou
    #
    #   Date:           March 2023
    #
    #   Original Code:  https://github.com/tomw1808/distributed_exchange_truffle_class_3
    #

    ################################################################################
    # Below is a list of contract Helper functions gleaned from the bootstrap javascript file
    # that were used in this our web3 frontend (streamlit) file to connect the Web3 frontend to the 
    # Solidity smart contract backend.
    # 
    # 
    # getBalance
    # getEthBalanceInWei
    # depositEther
    # withdrawEther
    # depositToken
    # withdrawToken
    # getSellOrderBook
    # getBuyOrderBook
    # sellToken
    # buyToken
    # balanceOf
    # transfer
    # approve


import os
import json
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st


#   SET STREAMLIT PAGE LAYOUT TO "WIDE"
st.set_page_config(layout="wide")

load_dotenv()

# Define and connect a new Web3 provider
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))

################################################################################
# Contract Helper function:
# 1. Loads the contract once using cache
# 2. Connects to the contract using the contract address and ABI
################################################################################


@st.cache(allow_output_mutation=True)
def load_contract(abi_file_path,env_keywords):
    # Load the contract ABI
    with open(Path(abi_file_path)) as f:
        contract_abi = json.load(f)
    # Set the contract address (this is the address of the deployed contract)
    contract_address = os.getenv(env_keywords)
    # Get the contract
    contract = w3.eth.contract(
        address=contract_address,
        abi=contract_abi
    )
    return contract


# Load the contract
ex_abi_file_path='./contracts/compiled/Exchange_abi.json'
token_abi_file_path='./contracts/compiled/FixedSupplyToken_abi.json'
exch_smart_contract_address='SMART_CONTRACT_ADDRESS'
token_smart_contract_address ='TOKEN_SMART_CONTRACT_ADDRESS'
ex_contract = load_contract(ex_abi_file_path,exch_smart_contract_address)  ##load Exchange smart contract
token_contract = load_contract(token_abi_file_path,token_smart_contract_address)   ##load FixedSupplyToken smart contract

# Save Ganache Workspace as "SUBSTANTIAL-PLAY", with the following wallet addresses
# This was done for persistance between coding sessions
token_wallet = w3.eth.accounts[0]           # 0xebb4134ef71F2af6a3B99e812Cf50B6Ef8228C6e
exchange_wallet = w3.eth.accounts[1]        # 0x095fadC32C6aAC49888C2282E249575c32882e20
user_wallet = w3.eth.accounts[2]            # 0x3cAd17eE3Bb982c130238f9265ce6B4D2A3A95a1

#   Display Title

st.title ("Welcome to MSF Decentralized Token Exchange")
st.subheader ("Project 3 - Group 1 (March 2023)")
# st.markdown('<div style="text-align: center;">### Welcome to Project 3 - Team 1!</div>', unsafe_allow_html=True)
# st.markdown('<div style="text-align: center;">### Decentralized Token Exchange</div>', unsafe_allow_html=True)

st.markdown("---")

#   LOAD ACCOUNTS

# st.write("Choose an account to get started")
# accounts = w3.eth.accounts
# address = st.selectbox("Select Account", options=accounts)
#st.markdown("---")

################################################################################
#   SETUP SIDEBAR

option = st.sidebar.selectbox("Which Option?", ('Home', 'Deposit/Withdrawal', 'FIXED Token Trading', 'Manage Token', 'About'), 4)
                

################################################################################
#   FUNCTION CALL TO EXCHANGE.SOL
#
# # Token getBalance  
# 
#     function getBalance(string memory symbolName) view public returns (uint) {
#              
#       getBalance = contract.functions.getBalance().transact(
#             {'from': user_wallet_address, 'value':wei_deposit_amount,'gas': 1000000}
#             )

st.sidebar.subheader("Token Balance:")
if st.sidebar.button("Token Balance"):
    #st.sidebar.write(f"{ex_contract.address}")
    balance_of_token  = ex_contract.functions.getBalance("FIXED").call()
    #balance_eth = w3.fromWei(balance_wei,"ether")
    st.sidebar.write(f"The balance of token held by the smart contract is {balance_of_token}")



st.sidebar.subheader("ETH Balance")


################################################################################
#   FUNCTION CALL TO EXCHANGE.SOL
#
# getEthBalanceInWei
# function getEthBalanceInWei() view public returns (uint){
if st.sidebar.button("Check Ether Balance"):
    balance_wei = ex_contract.functions.getEthBalanceInWei().call(
        {'from':user_wallet,'gas': 1000000}
    )
    balance_eth = w3.fromWei(balance_wei,"ether")
    st.sidebar.write(f"The balance of wei held by the smart contract is {balance_wei} wei")


################################################################################
#   DISPLAY SELECTED OPTION PAGE

if option == 'Home':
    st.subheader("Home")
    st.image("./images/iStock-1323542329.jpg")


################################################################################
#   DIPOSIT / WITHDRAWAL PAGE

if option == 'Deposit/Withdrawal':
    st.subheader ("Deposit/Withdrawal Option")
    

    st.write("Here you can trade the FIXED token we discuss during our course. The Solidity Contract is not limited to a single token and new tokens can be easily added.")
    
    st.markdown("---")

    st.subheader("Deposit")

    col1, col2 = st.columns(2)
    with col1:
        
        st.subheader("Deposit Token")
        deposit_symbol_name = st.text_input("Deposit Symbol Name eg.'FIXED'")
        deposit_amount_token = st.text_input("Deposit Number of token")
        
        ### SELECT ADDRESS TO USE        
        accounts = w3.eth.accounts
        user_wallet = st.selectbox("Select Account to Deposit to    ", options=accounts)
        st.write("token_wallet = accounts[0] 0xebb4134ef71F2af6a3B99e812Cf50B6Ef8228C6e")
        st.write("exchange_wallet = accounts[1] 0x095fadC32C6aAC49888C2282E249575c32882e20")
        st.write("user_wallet = accounts[2]  0x3cAd17eE3Bb982c130238f9265ce6B4D2A3A95a1")
        st.markdown("---")

        ################################################################################
        #   FUNCTION CALL TO EXCHANGE.SOL
        #
        if st.button("Deposit Token"):
            tx_hash = ex_contract.functions.depositToken(
                deposit_symbol_name,
                int(deposit_amount_token)
            ).transact(
#                {'from':user_wallet,'gas': 1000000} # Use user wallet address here
                {'from':user_wallet,'gas': 1000000}

                )
            receipt = w3.eth.waitForTransactionReceipt(tx_hash)
            st.write(receipt)
            st.markdown(f"{deposit_amount_token} Token deposited")  


    with col2:
        st.subheader("Deposit ETH")
        #deposit_amount_ETH = st.text_input("Deposit Number of ETH")

        ################################################################################
        #   FUNCTION CALL TO EXCHANGE.SOL
        #
        deposit_amount_ETH = st.number_input("How many ETH do you want to deposit?")

        accounts = w3.eth.accounts
        user_wallet = st.selectbox("Select Wallet", options=accounts)
        st.write("token_wallet = accounts[0] 0xebb4134ef71F2af6a3B99e812Cf50B6Ef8228C6e")
        st.write("exchange_wallet = accounts[1] 0x095fadC32C6aAC49888C2282E249575c32882e20")
        st.write("user_wallet = accounts[2]  0x3cAd17eE3Bb982c130238f9265ce6B4D2A3A95a1")
        st.markdown("---")        

        wei_deposit_amount = w3.toWei(deposit_amount_ETH, "ether")

        if st.button("Deposit"):
            tx_hash = ex_contract.functions.depositEther().transact(
                {'from':user_wallet,'value':wei_deposit_amount,'gas': 1000000}
                )
            receipt = w3.eth.waitForTransactionReceipt(tx_hash)
            st.write(receipt)
            st.markdown(f"{deposit_amount_ETH} ETH deposited")

        if st.button("Check Eth Balance"):
#            st.write(f"{ex_contract.address}")
#            balance_wei = ex_contract.functions.getEthBalanceInWei().call()
            balance_wei = ex_contract.functions.getEthBalanceInWei().transact(
                {'from':user_wallet,'gas': 1000000}
            )

            balance_eth = w3.fromWei(balance_wei,"ether")
            st.write(f"The balance of wei held by the smart contract is {balance_wei} wei")

    st.markdown("---")

    st.subheader("Withdraw")

    col2_1, col2_2 = st.columns(2)
    with col2_1:
        st.subheader("Withdraw Token")
        withdraw_symbol_name = st.text_input("Withdraw Symbol Name eg.'FIXED'")
        withdraw_amount_token = st.text_input("Withdraw Number of token")
        accounts = w3.eth.accounts
        user_wallet = st.selectbox("Select Account to Withdraw from", options=accounts)
        st.write("token_wallet = accounts[0] 0xebb4134ef71F2af6a3B99e812Cf50B6Ef8228C6e")
        st.write("exchange_wallet = accounts[1] 0x095fadC32C6aAC49888C2282E249575c32882e20")
        st.write("user_wallet = accounts[2]  0x3cAd17eE3Bb982c130238f9265ce6B4D2A3A95a1")
        st.markdown("---")

 ################################################################################
#   FUNCTION CALL TO EXCHANGE.SOL
#
        if st.button("Withdraw Token"):
            tx_hash = ex_contract.functions.withdrawToken(
                withdraw_symbol_name,
                int(withdraw_amount_token)
            ).transact(
#                {'from':user_wallet,'gas': 1000000} # Use user wallet address here
                {'from':user_wallet,'gas': 1000000}

                )
            receipt = w3.eth.waitForTransactionReceipt(tx_hash)
            st.write(receipt)
            st.markdown(f"{withdraw_amount_token} Token Withdrawn")  

    with col2_2:
        st.subheader("Withdraw ETH")
        #withdraw_eth = st.text_input("Withdraw ETH")
        withdraw_amount_eth = st.text_input("Withdraw Number of ETH")
                

################################################################################
#   FIXED TOKEN TRADING PAGE

if option == 'FIXED Token Trading':
    st.subheader ("FIXED Token Trading Option")
    st.write("Here you can trade the FIXED token we discuss during our course. The Solidity Contract is not limited to a single token and new tokens can be easily added.")
    
    # st.write("Choose an account to get started")
    # accounts = w3.eth.accounts
    # address = st.selectbox("Select Account", options=accounts)    

    st.markdown("---")

    st.subheader("New Order")

    col1, col2 = st.columns(2)
    with col1:
        # new_title = '<p style="font-family:sans-serif; color:Green; font-size: 42px;">New image</p>'
        # st.markdown(new_title, unsafe_allow_html=True)
        
        buy_title = '<p style="font-family:sans-serif; color:Green; font-size: 42px;">Buy Token</p>'
        st.markdown(buy_title, unsafe_allow_html=True)
        
        #st.subheader("Buy Token")
        buy_symbol_name = st.text_input("Buy Symbol Name eg.'FIXED'")
        
        buy_amount_token = st.text_input("Buy Number of token")
        #buy_amount_token = int(buy_amount_token)
        
        bid_price_wei = st.text_input("Bid Price in wei")
        #bid_price_wei = int(bid_price_wei)

        ################################################################################
        #   FUNCTION CALL TO EXCHANGE.SOL
        #
        #   function buyToken(string memory symbolName, uint priceInWei, uint amount) public {

        if st.button("Buy Token"):
            buytk_tx_hash = ex_contract.functions.buyToken(
                buy_symbol_name, 
                int(bid_price_wei), 
                int(buy_amount_token)).transact({'from': exchange_wallet, 'gas': 1000000})
            receipt = w3.eth.waitForTransactionReceipt(buytk_tx_hash)
            st.write(receipt)
            st.markdown(f"{buy_amount_token} Token bought")
        

    with col2:
        #st.subheader("Sell Token")
        
        sell_title = '<p style="font-family:sans-serif; color:Red; font-size: 42px;">Sell Token</p>'
        st.markdown(sell_title, unsafe_allow_html=True)
                
        sell_symbol_name = st.text_input("Sell Symbol Name eg.'FIXED'")
        
        sell_amount_token = st.text_input("Sell Number of token")
        #sell_amount_token = int(sell_amount_token)
        
        ask_price_wei = st.text_input("Ask Price in wei")
        #ask_price_wei = int(ask_price_wei)


        ################################################################################
        #   FUNCTION CALL TO EXCHANGE.SOL
        #
        #    function sellToken(string memory symbolName, uint priceInWei, uint amount) public {

        if st.button("Sell Token"):
            selltk_tx_hash = ex_contract.functions.sellToken(
                sell_symbol_name, 
                int(ask_price_wei), 
                int(sell_amount_token)).transact({'from': exchange_wallet, 'gas': 1000000})
            receipt = w3.eth.waitForTransactionReceipt(selltk_tx_hash)
            st.write(receipt)
            st.markdown(f"{sell_amount_token} Token sold")
    st.markdown("---")

    st.subheader("Order Book")


    col2_1, col2_2 = st.columns(2)

    ################################################################################
    #   FUNCTION CALL TO EXCHANGE.SOL
    #
    # function getBuyOrderBook(string memory symbolName) view public returns (uint[] memory, uint[] memory) {


    with col2_1:
        st.subheader("Bid")
        #st.write(dict0
        st.write(ex_contract.functions.getBuyOrderBook("FIXED"))
        
    ################################################################################
    #   FUNCTION CALL TO EXCHANGE.SOL
    #
    # function getSellOrderBook(string memory symbolName) view public returns (uint[] memory, uint[] memory) {
    #

    with col2_2:
        st.subheader("Ask")
        #st.write(dict(
        #st.write(ex_contract.functions.getSellOrderBook("FIXED"))
        


################################################################################
#   MANAGE TOKEN PAGE
if option == 'Manage Token':
    st.subheader ("Manage Token Option")
    st.write("This page is intended for the FIXED Token as sample only. You can send token and you can approve token. Additionally you can add a token to the exchange provided in this example.") 

    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Approve Token Allowance")
        approve_token_amount = st.number_input("Approve token amount") # should be the exchange smart contract address
        approve_token_amount = int(approve_token_amount)
        approve_address = st.text_input("To approved address")   # should be the exchange smart contract address
        #approve_address = token_contract.address   # should be the exchange smart contract address\
        st.write(approve_address)

        st.write("Approve the address to be allowed to send a token from your address to another address. This is important for the Exchange. When you fund the token in the exchange then it will deduct in your name the token from your address to the token address.")

        ################################################################################
        #   FUNCTION CALL TO FIXEDSUPPYTOKEN.SOL
        #   Allow _spender to withdraw from your account, multiple times, up to the _value amount.
        #   If this function is called again it overwrites the current allowance with _value.
        #   function approve(address _spender, uint256 _amount) public returns (bool success) {

        if st.button("Allow Token to be used"):
            tx_hash = token_contract.functions.approve(ex_contract.address, approve_token_amount).transact(
                {
                'from': token_wallet,
                'gas': 1000000
                }
            )
            receipt = w3.eth.waitForTransactionReceipt(tx_hash)
            st.write(receipt)
        

    with col2:
        st.subheader("Send Token")
        send_amount_token = st.number_input("Enter the amount of token")
        send_amount_token = int(send_amount_token)
        
        send_to_address = st.text_input("Address to send to")
        st.write("Sending to the EXchange smart contract address")  

        ################################################################################
        #   FUNCTION CALL TO FIXEDSUPPYTOKEN.SOL
        #
        #   Send _value amount of tokens to address _to
        #   function transfer(address _to, uint256 _amount) public returns (bool success) {

        if st.button("Send Token"):                
            sendToken_tx_hash = token_contract.functions.transfer(
                send_to_address,
                send_amount_token
            ).transact({'from': user_wallet, 'gas': 1000000})

            sendToken_tx_receipt = w3.eth.waitForTransactionReceipt(sendToken_tx_hash)

            st.write("Send Token hash:", sendToken_tx_hash)
            st.write("Send Token Receipt:", sendToken_tx_receipt)   

    st.markdown("---")

    st.subheader("Add Token")
    token_symbol = st.text_input("Token Symbol eg. FIXED")
    token_contract_address = st.text_input("Token address eg. 0x1362FE...")

    st.write("Using the smart contract address of the Token:", token_contract.address)
    balance = w3.eth.getBalance(token_wallet) #Ganache Acc[0] - Token Wallet
    st.write(balance)
    st.write("Token wallet:", token_wallet)
    st.write("Token contract:", token_contract.address)
    st.write("Exchange wallet:", exchange_wallet)
    st.write("Exchange contract:", ex_contract.address)

    if st.button("Add Token"):

        ################################################################################
        #   FUNCTION CALL TO EXCHANGE.SOL
        #   function addToken(string memory symbolName, address erc20TokenAddress) public onlyowner
        addToken_tx_hash = ex_contract.functions.addToken(
            token_symbol,
            token_contract_address
        ).transact({'from': exchange_wallet, 'gas': 100000}) #Ganache Acc[0] - Token Wallet
        addToken_tx_receipt = w3.eth.waitForTransactionReceipt(addToken_tx_hash)


        st.write("Add Token hash:", addToken_tx_hash)
        st.write("Add Token Receipt:", addToken_tx_receipt)
    

################################################################################
#   ABOUT PAGE
#

if option == 'About':
    st.subheader("About Section")
    st.write("This is the final capstone project for Group 1 of the Sydney University FinTech Bootcamp. The Boot Camp takes a multidisciplinary approach to finance, fundamental programming, data analysis, and modern tools in cryptocurrency and blockchain. This capstone project aims to pull together all the skills gained during the course.")
    st.write("This project leverages the code base developed in Udemy course 'Ethereum Master Class: Build Real World Projects' by Ravinder Deol and Thomas Weisner. The course develops a decentralisd exchange using an Ethereum testnet and Solidity. Team members took the code and rebuilt the web3 frontend (originally Bootstrap) using Streamlit. Before this could be done a deep understanding of the Solidity Smart Contract code base had to be achieved. In doing so the code base was updated to current Ethereum and Solidity standards, removing deprecated code. We also improved security by converting code to use the SafeMath library from OpenZeppelin")
    st.write('Original Code:  https://github.com/tomw1808/distributed_exchange_truffle_class_3')
    
    st.subheader("Team Members")
    
    # st.image("Xu_Flora_Zhao.png")
    # st.write("Xu Flora Zhao")
    
    # st.image("Md_Muhasenul_Haque.png")
    # st.write("Md Muhasenul Haque")
        
    # st.image("Samuel_Nayacakalou.png")
    # st.write("Samuel Nayacakalou")
    
    team_members = ['./images/Xu_Flora_Zhao.png', './images/Md_Muhasenul_Haque.png', './images/Samuel_Nayacakalou.png']
    team_members_names =['Xu Flora Zhao', 'Md Muhasenul Haque', 'Samuel Nayacakalou']
    
    st.image(team_members, caption = team_members_names)
    
    st.subheader("Instructors")
    
    st.image("./images/Adrian Rusli - Instructor.png")
    st.write("Adrian Rusli - Instructor")
    
    st.image("./images/Larry Huang - TA.png")
    st.write("Larry Huang - TA")    
    
    


