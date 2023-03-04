    #   Project-3-Group-1
    #   *****************

    #   Group Membere:  Xu (Flora) Zhao
    #                   Md Muhasenul Haque
    #                   Samuel Nayacakalou

    #   Date:           March 2023

    #   Original Code:  https://github.com/tomw1808/distributed_exchange_truffle_class_3



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

@st.cache_resource()
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


# Set parramatters for the laod_contract() function
ex_abi_file_path='./contracts/compiled/Exchange_abi.json'
token_abi_file_path='./contracts/compiled/FixedSupplyToken_abi.json'
ex_env_keywords='SMART_CONTRACT_ADDRESS'
token_env_keywords='TOKEN_SMART_CONTRACT_ADDRESS'

# Load Exchange smart contract
contract = load_contract(ex_abi_file_path,ex_env_keywords)  

# Load FixedSupplyToken smart contract
token_contract = load_contract(token_abi_file_path,token_env_keywords)   

####################################################################################################################
#   Display Title
st.markdown(""" <style> .font {
font-size:50px ; font-family: 'Cooper Black'; color: #FF9633;} 
</style> """, unsafe_allow_html=True)
st.markdown('<p class="font">Welcome to MSF Decentralized Token Exchange</p>', unsafe_allow_html=True)


st.markdown("---")

#   SETUP SIDEBAR

option = st.sidebar.selectbox("Which Option?", ('Manage Token','Fund Management', 'Token Trading' ),2)

# Test info saved for testing purpose only
# st.sidebar.write(f"The Exchange Smart Contract Address is : {contract.address}")
# st.sidebar.write(f"The Token Smart Contract Address is : {token_contract.address}")
# st.sidebar.write(f"The User Wallet Address Selected is : {user_wallet_address}")

###########################################################################################################################################

                                            #OPTION "Fund Management" SELECTED

###########################################################################################################################################

if option == 'Fund Management':
    st.subheader("Choose an account to get started")
    accounts = w3.eth.accounts
    user_wallet_address = st.selectbox("Select Token/Ether Owner's Wallet Address to manage the funds", options=accounts)
    
    st.header ("Fund Management")

    col1, col2, col3 = st.columns(3)
    with col1:        
        st.subheader("Deposit Token")
        deposit_symbol_name = st.text_input("Deposit Symbol Name eg.'FIXED'")
        deposit_amount_token = st.number_input("Deposit Number of token")
        deposit_amount_token=int(deposit_amount_token)

        if st.button("Deposit Token"):
            tx_hash = contract.functions.depositToken(deposit_symbol_name,deposit_amount_token).transact(
                {'from': user_wallet_address, 'gas':1000000}
                )

            receipt = w3.eth.waitForTransactionReceipt(tx_hash)
            st.sidebar.write(receipt)
            st.markdown(f"{deposit_amount_token}  {deposit_symbol_name}  token deposited!")

    with col2:
        st.subheader("Withdraw Token")
        withdraw_symbol_name = st.text_input("Withdraw Symbol Name eg.'FIXED'")
        withdraw_amount_token = st.number_input("Withdraw Number of token")
        withdraw_amount_token=int(withdraw_amount_token)

        if st.button("Withdraw Token"):
            tx_hash = contract.functions.withdrawToken(withdraw_symbol_name,withdraw_amount_token).transact(
                {'from': user_wallet_address, 'gas':1000000 , 'to':contract.address}
            )
            receipt = w3.eth.waitForTransactionReceipt(tx_hash)
            st.sidebar.write(receipt)
            st.markdown(f"{withdraw_amount_token} {withdraw_symbol_name} Token withdrawn!")
    
    with col3:
        st.subheader("Check Token Balance")
        symbol_name=st.text_input("Please input the symbol name to check balance")
        if st.button("Check Token Balance"):
            balance_token = contract.functions.getBalance(symbol_name).call({'from':user_wallet_address,'gas':1000000})
            st.write(f"The balance of {symbol_name}  is {balance_token} ")

    st.markdown("---")

    col2_1, col2_2, col3_3 = st.columns(3)
    with col2_1:       
        st.subheader("Deposit ETH")
        eth_deposit_amount = st.number_input("How many ETH do you want to deposit?")
        wei_deposit_amount = w3.toWei(eth_deposit_amount, "ether")

        if st.button("Deposit"):
            tx_hash = contract.functions.depositEther().transact(
                {'from': user_wallet_address, 'value':wei_deposit_amount,'gas': 1000000}
                )
            receipt = w3.eth.waitForTransactionReceipt(tx_hash)
            st.sidebar.write(receipt)
            st.markdown(f"{eth_deposit_amount} ETH deposited")   

    with col2_2:
        st.subheader("Withdraw ETH")
        eth_withdraw_amount = st.number_input("How many ETH do you want to withdraw?")
        wei_withdraw_amount = w3.toWei(eth_withdraw_amount, "ether")

        if st.button("Withdraw"):
            tx_hash = contract.functions.withdrawEther(wei_withdraw_amount).transact(
                {
                # the transaction is initiated from the wallet address to the smart contract address
                'from': user_wallet_address, 
                'gas': 1000000,
                'to':contract.address
                }
            )
            receipt = w3.eth.waitForTransactionReceipt(tx_hash)
            st.sidebar.write(receipt)
            st.markdown(f"{eth_withdraw_amount} ETH withdrawn!")

    with col3_3:           
        # Check Ether Balance
        st.subheader("Check Ether Balance")
        if st.button("Check Ether Balance"):
            balance_wei = contract.functions.getEthBalanceInWei().call({'from':user_wallet_address,'gas':1000000})
            balance_eth = w3.fromWei(balance_wei,"ether")
            st.write(f"The balance of Ether held by the smart contract is {balance_eth:.2f} ETH")


###########################################################################################################################################

                                            #OPTION "Token Trading" SELECTED

###########################################################################################################################################

if option == 'Token Trading':
    st.subheader("Choose an account to get started")
    accounts = w3.eth.accounts
    user_wallet_address = st.selectbox("Select Token Owner Wallet Address", options=accounts)
    st.markdown("---")

    st.header ("Token Trading Options")

    col1, col2 = st.columns(2)
    with col1:
        # new_title = '<p style="font-family:sans-serif; color:Green; font-size: 42px;">New image</p>'
        # st.markdown(new_title, unsafe_allow_html=True)
        
        buy_title = '<p style="font-family:sans-serif; color:Green; font-size: 42px;">Buy Token</p>'
        st.markdown(buy_title, unsafe_allow_html=True)
        
        #st.subheader("Buy Token")
        buy_symbol_name = st.text_input("Buy Symbol Name eg.'FIXED'")
        buy_amount_token = st.number_input("Buy Number of token")
        buy_amount_token=int(buy_amount_token)
        bid_price_wei = st.number_input("Bid Price in wei")
        bid_price_wei=int(bid_price_wei)

        if st.button("Buy Token"):
                    
            tx_hash = contract.functions.buyToken(buy_symbol_name, bid_price_wei,buy_amount_token).transact(
                {
                # the transaction is initiated from the wallet address to the smart contract address
                'from': user_wallet_address, 
                # 'value':wei_withdraw_amount,
                'gas': 2100000
                #'to':approve_address
                }
            )
            receipt = w3.eth.waitForTransactionReceipt(tx_hash)
            st.sidebar.write(receipt)

    with col2:
        #st.subheader("Sell Token")
        
        sell_title = '<p style="font-family:sans-serif; color:Red; font-size: 42px;">Sell Token</p>'
        st.markdown(sell_title, unsafe_allow_html=True)
                
        sell_symbol_name = st.text_input("Sell Symbol Name eg.'FIXED'")
        sell_amount_token = st.number_input("Sell Number of token")
        ask_price_wei = st.number_input("Ask Price in wei")
        sell_amount_token=int(sell_amount_token)
        ask_price_wei=int(ask_price_wei)

        if st.button("Sell Token"):
                    
            tx_hash = contract.functions.sellToken(sell_symbol_name, ask_price_wei,sell_amount_token).transact(
                {
                # the transaction is initiated from the wallet address to the smart contract address
                'from': user_wallet_address, 
                'gas': 2100000
                }
            )
            receipt = w3.eth.waitForTransactionReceipt(tx_hash)
            st.sidebar.write(receipt)

    st.markdown("---")

    st.header("Order Book")
    orderbook_symbol_name = st.text_input("Order Book Symbol Name eg.'FIXED'")
    col2_1, col2_2 = st.columns(2)
    with col2_1:
        st.subheader("Bid")
        arrPricesBuy, arrVolumesBuy=contract.functions.getBuyOrderBook(orderbook_symbol_name).call()
        st.write("Price to Buy\t\tVolumne to Buy")
        for price, volumne in zip(arrPricesBuy, arrVolumesBuy):
            st.write(f"{price:.2f}\t\t{volumne}")

    with col2_2:
        st.subheader("Ask")
        arrPricesSell,arrVolumesSell=contract.functions.getSellOrderBook(orderbook_symbol_name).call()
        st.write("Price to Sell\t\tVolumne to Sell")
        for price, volumne in zip(arrPricesSell, arrVolumesSell):
            st.write(f"{price:.2f}\t\t{volumne}")

###########################################################################################################################################

                                            #OPTION "Manage Token" SELECTED

###########################################################################################################################################
        
if option == 'Manage Token':
    # Only the exchange owner can add token, please choose the wallet address to deploy the exchange smart contract
    st.subheader("Choose an account to get started")
    accounts = w3.eth.accounts
    token_owner_wallet_address = st.selectbox("Select Exchange owner's Wallet Address", options=accounts)

    st.markdown("---")
    st.header ("Manage Token Option")

    col1, col2 = st.columns(2)
    with col1:

        st.subheader("Add Token")
        token_symbol = st.text_input("Token Symbol eg. FIXED")
        token_address = token_contract.address
        

        if st.button("Add Token"):
            addToken_tx_hash = contract.functions.addToken(
                token_symbol,
                token_address
            ).transact({'from': token_owner_wallet_address, 'gas': 1000000})
            # st.sidebar.write("Add Token hash:", addToken_tx_hash)
            st.write(f"{token_symbol} Token added!")

    st.markdown("---")
    with col2:
        st.subheader("Approve Token Allowance") 
        user_wallet_address_to_approve = st.selectbox("Select Token Onwer's Wallet Address to Approve the Token Allowance", options=accounts)
        approve_token_amount = st.number_input("Approve token amount") 
        approve_token_amount = int(approve_token_amount)

        if st.button("Allow Token to be used"):
            
            tx_hash = token_contract.functions.approve(contract.address, approve_token_amount).transact(
                {
                # the transaction is initiated from the wallet address to the smart contract address
                'from': user_wallet_address_to_approve, 
                'gas': 1000000,
                }
            )
            receipt = w3.eth.waitForTransactionReceipt(tx_hash)
            st.sidebar.write(receipt)

        st.write("Approve the address to be allowed to send a token from your address to another address. This is important for the Exchange. When you fund the token in the exchange then it will deduct in your name the token from your address to the exchange address.")



