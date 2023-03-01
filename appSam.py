

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


@st.cache(allow_output_mutation=True)

# def load_contract():

#     # Load the contract ABI
#     with open(Path('./contracts/compiled/exchange_abi.json')) as f:
#         contract_abi = json.load(f)

#     # Set the contract address (this is the address of the deployed contract)
#     contract_address = os.getenv("SMART_CONTRACT_ADDRESS")

#     # Get the contract
#     contract = w3.eth.contract(
#         address=contract_address,
#         abi=contract_abi
#     )

#     return contract


# # Load the contract
# contract = load_contract()


####################################################################################################################
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
ex_env_keywords='SMART_CONTRACT_ADDRESS'
token_env_keywords='TOKEN_SMART_CONTRACT_ADDRESS'

contract = load_contract(ex_abi_file_path,ex_env_keywords)  ##load Exchange smart contract
token_contract = load_contract(token_abi_file_path,token_env_keywords)   ##load FixedSupplyToken smart contract



####################################################################################################################


#   Display Title

st.title ("Welcome to MSF Decentralized Token Exchange")
st.subheader ("Project 3 - Team 1 (March 2023)")
# st.markdown('<div style="text-align: center;">### Welcome to Project 3 - Team 1!</div>', unsafe_allow_html=True)
# st.markdown('<div style="text-align: center;">### Decentralized Token Exchange</div>', unsafe_allow_html=True)

st.markdown("---")

#   LOAD ACCOUNTS

# st.write("Choose an account to get started")
# accounts = w3.eth.accounts
# address = st.selectbox("Select Account", options=accounts)
#st.markdown("---")


#   SETUP SIDEBAR

option = st.sidebar.selectbox("Which Option?", ('Exchange Overview', 'FIXED Token Trading', 'Manage Token'), 2)

st.sidebar.write("Token Balance", )
#st.sidebar.write("ETH Balance")

###############################################################################################
# For User of the DEX

# Check Ether Balance
###############################################################################################

# if st.sidebar.button("Check Ether Balance"):
#     balance_wei = contract.functions.getEthBalanceInWei().call()
#     balance_eth = w3.fromWei(balance_wei,"ether")
#     # tx_hash = contract.functions.getEthBalanceInWei().transact({'from': contract.address, 'gas': 1000000})
#     # receipt = w3.eth.waitForTransactionReceipt(tx_hash)
#     # st.write("Transaction receipt mined:")
#     # st.write(dict(receipt))
#     st.sidebar.write(f"The balance of Ether held by the smart contract is {balance_eth:.2f} ETH")
# st.markdown("---")



if st.sidebar.button("Check Ether Balance"):
    balance_wei = contract.functions.getEthBalanceInWei().call()
    balance_eth = w3.fromWei(balance_wei,"ether")
    st.sidebar.write(f"The balance of Ether held by the smart contract is {balance_eth:.2f} ETH")
st.markdown("---")



#   DISPLAY SELECTED OPTION PAGE

#st.header(option)

# if option == 'DTE':
#     st.write ("DTE Option")

if option == 'Exchange Overview':
    st.write ("Exchange Overview Option")
    
    #st.subheader ("FIXED Token Trading Option")
    st.write("Here you can trade the FIXED token we discuss during our course. The Solidity Contract is not limited to a single token and new tokens can be easily added.")
    
    # st.write("Choose an account to get started")
    # accounts = w3.eth.accounts
    # address = st.selectbox("Select Account", options=accounts)    

    st.markdown("---")

    st.subheader("Deposit")

    user_wallet_address = st.text_input("Enter the wallet address from where you wannt to transfer the ETH or token")

    col1, col2 = st.columns(2)
    with col1:
        
        st.subheader("Deposit Token")
        deposit_symbol_name = st.text_input("Deposit Symbol Name eg.'FIXED'")
        deposit_amount_token = st.number_input("Deposit Number of token")
        deposit_amount_token=int(deposit_amount_token)
        # wallet_add=st.text_input("Enter the wallet address from where you wannt to transfer the ETH")
        st.markdown(f"{deposit_amount_token}  {deposit_symbol_name}  token is going to be deposited")

        st.markdown(f"ex smart contract address: {contract.address} ")
####################################################################################################################

        if st.button("Deposit Token"):
            tx_hash = contract.functions.depositToken(deposit_symbol_name,deposit_amount_token).transact(
                {'from': user_wallet_address, 'gas':1000000 , 'to':contract.address}
            )
            receipt = w3.eth.waitForTransactionReceipt(tx_hash)
            st.write(receipt)
            # st.markdown(f"{deposit_amount_token}  {deposit_symbol_name}token deposited")




    with col2:
        #st.subheader("Sell Token")
        
        st.subheader("Deposit ETH")
        #deposit_amount_ETH = st.text_input("Deposit Number of ETH")

###############################################################################

        # user_wallet_address = st.text_input("Enter the wallet address from where you wannt to transfer the ETH")
        eth_deposit_amount = st.number_input("How many ETH do you want to deposit?")

        #eth_deposit_amount=int(eth_deposit_amount)

        wei_deposit_amount = w3.toWei(eth_deposit_amount, "ether")

        if st.button("Deposit"):
            tx_hash = contract.functions.depositEther().transact(
                {'from': user_wallet_address, 'value':wei_deposit_amount,'gas': 1000000}
                )
            receipt = w3.eth.waitForTransactionReceipt(tx_hash)
            st.write(receipt)
            st.markdown(f"{eth_deposit_amount} ETH deposited")


###############################################################################

    st.markdown("---")

    st.subheader("Withdraw")

    col2_1, col2_2 = st.columns(2)
    with col2_1:
        st.subheader("Withdraw Token")
        withdraw_symbol_name = st.text_input("Withdraw Symbol Name eg.'FIXED'")
        withdraw_amount_token = st.number_input("Withdraw Number of token")
        withdraw_amount_token=int(withdraw_amount_token)
        st.write(f"{contract.address}")
###########################################################################################################

        if st.button("Withdraw Token"):
            tx_hash = contract.functions.withdrawToken(withdraw_symbol_name,withdraw_amount_token).transact(
                {'from': user_wallet_address, 'gas':1000000 , 'to':contract.address}
            )
            receipt = w3.eth.waitForTransactionReceipt(tx_hash)
            st.write(receipt)
            # st.markdown(f"{deposit_amount_token}  {deposit_symbol_name}token deposited")







###########################################################################################################

    with col2_2:
        st.subheader("Withdraw ETH")
        #withdraw_eth = st.text_input("Withdraw ETH")
        #withdraw_amount_eth = st.text_input("Withdraw Number of ETH")
                
####################################################################################
        receiver_wallet_address = st.text_input("Enter the wallet address to where you want to withdraw the ETH to")
        eth_withdraw_amount = st.number_input("How many ETH do you want to withdraw?")



        wei_withdraw_amount = w3.toWei(eth_withdraw_amount, "ether")

        
        if st.button("Withdraw"):
            st.write(f"sender address/exchange contract address: {contract.address}") 
            st.write(f"receiver wallet address: {receiver_wallet_address}") 
            st.write("######################################")
            tx_hash = contract.functions.withdrawEther(wei_withdraw_amount).transact(
                {
                # the transaction is initiated from the wallet address to the smart contract address
                'from': receiver_wallet_address, 
                'value':wei_withdraw_amount,
                'gas': 1000000,
                'to':contract.address
                }
            )
            receipt = w3.eth.waitForTransactionReceipt(tx_hash)
            st.write(receipt)
            st.markdown(f"{eth_withdraw_amount} ETH withdrawn")






####################################################################################
if option == 'FIXED Token Trading':
    st.subheader ("FIXED Token Trading Option")
    st.write("Here you can trade the FIXED token we discuss during our course. The Solidity Contract is not limited to a single token and new tokens can be easily added.")
    
    # st.write("Choose an account to get started")
    # accounts = w3.eth.accounts
    # address = st.selectbox("Select Account", options=accounts)    

    st.markdown("---")

    st.subheader("New Order")
    user_wallet_address = st.text_input("Enter the wallet address from where you wannt to transfer the ETH or token")

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
        st.write(user_wallet_address)
        st.write(contract.address)

        if st.button("Buy Token"):
                    
            tx_hash = contract.functions.buyToken(buy_symbol_name, bid_price_wei,buy_amount_token).transact(
                {
                # the transaction is initiated from the wallet address to the smart contract address
                'from': user_wallet_address, 
                # 'value':wei_withdraw_amount,
                'gas': 1000000
                #'to':approve_address
                }
            )
            receipt = w3.eth.waitForTransactionReceipt(tx_hash)
            st.write(receipt)







        # Allow _spender to withdraw from your account, multiple times, up to the _value amount.
        # If this function is called again it overwrites the current allowance with _value.
        # function approve(address _spender, uint256 _amount) public returns (bool success) {
        # approveToken_return = contract.functions.approve(
        #     approve_address,
        #     aprove_token_amount
        # ).transact({'from': address, 'gas': 1000000})
        

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
                # 'value':wei_withdraw_amount,
                'gas': 1000000
                #'to':approve_address
                }
            )
            receipt = w3.eth.waitForTransactionReceipt(tx_hash)
            st.write(receipt)
















    st.markdown("---")

    st.subheader("Order Book")
    orderbook_symbol_name = st.text_input("Order Book Symbol Name eg.'FIXED'")
    col2_1, col2_2 = st.columns(2)
    with col2_1:
        st.subheader("Bid")

        # buy_amount_token = st.text_input("Buy Number of token")
        # bid_price_wei = st.text_input("Bid Price in wei")
        if st.button("Buy Order Book"):
                    
            tx_hash = contract.functions.getBuyOrderBook(orderbook_symbol_name).transact(
                {
                # the transaction is initiated from the wallet address to the smart contract address
                'from': user_wallet_address, 
                # 'value':wei_withdraw_amount,
                'gas': 1000000
                #'to':approve_address
                }
            )
            receipt = w3.eth.waitForTransactionReceipt(tx_hash)
            st.write(receipt)
        






        # Allow _spender to withdraw from your account, multiple times, up to the _value amount.
        # If this function is called again it overwrites the current allowance with _value.
        # function approve(address _spender, uint256 _amount) public returns (bool success) {
        # approveToken_return = contract.functions.approve(
        #     approve_address,
        #     aprove_token_amount
        # ).transact({'from': address, 'gas': 1000000})
        

    with col2_2:
        st.subheader("Ask")
        # sell_symbol_name = st.text_input("Sell Symbol Name eg.'FIXED'")
        # sell_amount_token = st.text_input("Sell Number of token")
        # ask_price_wei = st.text_input("Ask Price in wei")
        if st.button("Sell Order Book"):
                    
            tx_hash = contract.functions.getSellOrderBook(orderbook_symbol_name).transact(
                {
                # the transaction is initiated from the wallet address to the smart contract address
                'from': user_wallet_address, 
                # 'value':wei_withdraw_amount,
                'gas': 1000000
                #'to':approve_address
                }
            )
            receipt = w3.eth.waitForTransactionReceipt(tx_hash)
            st.write(receipt)




        
if option == 'Manage Token':
    st.subheader ("Manage Token Option")
    st.write("This page is intended for the FIXED Token as sample only. You can send token and you can approve token. Additionally you can add a token to the exchange provided in this example.")
    
    st.write("Choose an account to get started")
    accounts = w3.eth.accounts
    address = st.selectbox("Select Account", options=accounts)    

    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Approve Token Allowance")
        #st.image("https://static.streamlit.io/examples/dog.jpg")
        #############################################################################################################


        #############################################################################################################

        approve_token_amount = st.number_input("Approve token amount") 
        approve_token_amount = int(approve_token_amount)
        approve_address = st.text_input("Approved address")   # should be the exchange smart contract address

        st.write(f"wallet address:{address}")
        if st.button("Allow Token to be used"):
            
            tx_hash = token_contract.functions.approve(approve_address, approve_token_amount).transact(
                {
                # the transaction is initiated from the wallet address to the smart contract address
                'from': address, 
                # 'value':wei_withdraw_amount,
                'gas': 1000000,
                #'to':approve_address
                }
            )
            receipt = w3.eth.waitForTransactionReceipt(tx_hash)
            st.write(receipt)













        st.write("Approve the address to be allowed to send a token from your address to another address. This is important for the Exchange. When you fund the token in the exchange then it will deduct in your name the token from your address to the token address.")

        # Allow _spender to withdraw from your account, multiple times, up to the _value amount.
        # If this function is called again it overwrites the current allowance with _value.
        # function approve(address _spender, uint256 _amount) public returns (bool success) {
        # approveToken_return = contract.functions.approve(
        #     approve_address,
        #     aprove_token_amount
        # ).transact({'from': address, 'gas': 1000000})
        





####################################################################################################################
    # with col2:
    #     st.subheader("Send Token")
    #     #st.image("https://static.streamlit.io/examples/cat.jpg")

    #     send_amount_token = st.text_input("Enter the name of token")
    #     send_to_address = st.text_input("Enter the 'to' address")  
    #     st.write("Directly send a token from your address to another address.")
###################################################################################################################









        # Send _value amount of tokens to address _to
        # function transfer(address _to, uint256 _value) public returns (bool success);
        # sendToken_tx_hash = contract.functions.transfer(
        #     send_to_address,
        #     send_amount_token
        # ).transact({'from': address, 'gas': 1000000})

        # if st.button("Send Token"):
        # tx_hash = contract.functions.registerArtwork(
        #     to_address,
        #     artwork_name,
        #     artist_name,
        #     int(initial_appraisal_value),
        #     artwork_uri
        # ).transact({'from': address, 'gas': 1000000})
    
        # receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        # st.write("Transaction receipt mined:")
        # st.write(dict(receipt))
        # st.markdown("---")
    st.markdown("---")

    st.subheader("Add Token")
    token_symbol = st.text_input("Token Symbol eg. FIXED")
    token_address = st.text_input("Token address eg. 0x1362FE...")
    

    if st.button("Add Token"):

    #exchange.sol:Smart Contract function call
    #function addToken(string memory symbolName, address erc20TokenAddress) public onlyowner
        addToken_tx_hash = contract.functions.addToken(
            token_symbol,
            token_address
        ).transact({'from': address, 'gas': 1000000})

        st.write("Add Token hash:", addToken_tx_hash)






