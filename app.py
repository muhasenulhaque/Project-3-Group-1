
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
def load_contract():

    # Load the contract ABI
    with open(Path('./contracts/compiled/exchange_abi.json')) as f:
        contract_abi = json.load(f)

    # Set the contract address (this is the address of the deployed contract)
    contract_address = os.getenv("SMART_CONTRACT_ADDRESS")

    # Get the contract
    contract = w3.eth.contract(
        address=contract_address,
        abi=contract_abi
    )

    return contract


# Load the contract
contract = load_contract()



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
                

# Token getBalance               
# getBalance = contract.functions.getBalance().transact(
#             {'from': user_wallet_address, 'value':wei_deposit_amount,'gas': 1000000}
#             )

#token_balance = contract.functions.getBalance().tranact()

#st.sidebar.subheader(f"Token Balance:", {token_balance})
st.sidebar.subheader("Token Balance:")

# getEthBalanceInWei
# function getEthBalanceInWei() view public returns (uint){

# getEthBalanceInWei = contract.functions.getEthBalanceInWei().transact(
#             {'from': user_wallet_address, 'value':wei_deposit_amount,'gas': 1000000}
#             )

#st.sidebar.subheader(f"ETH Balance", {contract.functions.getEthBalanceInWei()})
st.sidebar.subheader("ETH Balance")

################################################################################
#   DISPLAY SELECTED OPTION PAGE

if option == 'Home':
    st.subheader("Home")
    st.image("./images/iStock-1323542329.jpg")

if option == 'Deposit/Withdrawal':
    st.subheader ("Deposit/Withdrawal Option")
    
    #st.subheader ("FIXED Token Trading Option")
    st.write("Here you can trade the FIXED token we discuss during our course. The Solidity Contract is not limited to a single token and new tokens can be easily added.")
    
    # st.write("Choose an account to get started")
    # accounts = w3.eth.accounts
    # address = st.selectbox("Select Account", options=accounts)    

    st.markdown("---")

    st.subheader("Deposit")

    col1, col2 = st.columns(2)
    with col1:
        
        st.subheader("Deposit Token")
        deposit_symbol_name = st.text_input("Deposit Symbol Name eg.'FIXED'")
        deposit_amount_token = st.text_input("Deposit Number of token")


        # Allow _spender to withdraw from your account, multiple times, up to the _value amount.
        # If this function is called again it overwrites the current allowance with _value.
        # function approve(address _spender, uint256 _amount) public returns (bool success) {
        # approveToken_return = contract.functions.approve(
        #     approve_address,
        #     aprove_token_amount
        # ).transact({'from': address, 'gas': 1000000})
        

    with col2:
        #st.subheader("Sell Token")
        
        st.subheader("Deposit ETH")
        deposit_amount_ETH = st.text_input("Deposit Number of ETH")

    st.markdown("---")

    st.subheader("Withdraw")

    col2_1, col2_2 = st.columns(2)
    with col2_1:
        st.subheader("Withdraw Token")
        withdraw_symbol_name = st.text_input("Withdraw Symbol Name eg.'FIXED'")
        withdraw_amount_token = st.text_input("Withdraw Number of token")
        

    with col2_2:
        st.subheader("Withdraw ETH")
        #withdraw_eth = st.text_input("Withdraw ETH")
        withdraw_amount_eth = st.text_input("Withdraw Number of ETH")
                
    

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
        bid_price_wei = st.text_input("Bid Price in wei")

        # if st.button("Buy Token"):
        #     buytk_tx_hash = contract.functions.depositEther().transact(
        #         {'from': user_wallet_address, 'value':wei_deposit_amount,'gas': 1000000}
        #         )
        #     receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        #     st.write(receipt)
        #     st.markdown(f"{eth_deposit_amount} ETH deposited")
        

    with col2:
        #st.subheader("Sell Token")
        
        sell_title = '<p style="font-family:sans-serif; color:Red; font-size: 42px;">Sell Token</p>'
        st.markdown(sell_title, unsafe_allow_html=True)
                
        sell_symbol_name = st.text_input("Sell Symbol Name eg.'FIXED'")
        sell_amount_token = st.text_input("Sell Number of token")
        ask_price_wei = st.text_input("Ask Price in wei")

        # if st.button("Sell Token"):
        #     tx_hash = contract.functions.depositEther().transact(
        #         {'from': user_wallet_address, 'value':wei_deposit_amount,'gas': 1000000}
        #         )
        #     receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        #     st.write(receipt)
        #     st.markdown(f"{eth_deposit_amount} ETH deposited")
    st.markdown("---")

    st.subheader("Order Book")

    col2_1, col2_2 = st.columns(2)
    with col2_1:
        st.subheader("Bid")
        st.write(contract.functions.getBuyOrderBook("FIXED"))
        # buy_symbol_name = st.text_input("Buy Symbol Name eg.'FIXED'")
        # buy_amount_token = st.text_input("Buy Number of token")
        # bid_price_wei = st.text_input("Bid Price in wei")


        # Allow _spender to withdraw from your account, multiple times, up to the _value amount.
        # If this function is called again it overwrites the current allowance with _value.
        # function approve(address _spender, uint256 _amount) public returns (bool success) {
        # approveToken_return = contract.functions.approve(
        #     approve_address,
        #     aprove_token_amount
        # ).transact({'from': address, 'gas': 1000000})
        

    with col2_2:
        st.subheader("Ask")
        st.write(contract.functions.getSellOrderBook("FIXED"))
        
        # sell_symbol_name = st.text_input("Sell Symbol Name eg.'FIXED'")
        # sell_amount_token = st.text_input("Sell Number of token")
        # ask_price_wei = st.text_input("Ask Price in wei")
        
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
        aprove_token_amount = st.text_input("Approve token amount")
        approve_address = st.text_input("Approved address")
        st.write("Approve the address to be allowed to send a token from your address to another address. This is important for the Exchange. When you fund the token in the exchange then it will deduct in your name the token from your address to the token address.")

        # Allow _spender to withdraw from your account, multiple times, up to the _value amount.
        # If this function is called again it overwrites the current allowance with _value.
        # function approve(address _spender, uint256 _amount) public returns (bool success) {
        # approveToken_return = contract.functions.approve(
        #     approve_address,
        #     aprove_token_amount
        # ).transact({'from': address, 'gas': 1000000})
        

    with col2:
        st.subheader("Send Token")
        #st.image("https://static.streamlit.io/examples/cat.jpg")

        send_amount_token = st.text_input("Enter the name of token")
        send_to_address = st.text_input("Enter the 'to' address")  
        st.write("Directly send a token from your address to another address.")

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
    
    




# ################################################################################
# # Register New Artwork
# ################################################################################
# st.markdown("## Register New Artwork")

# artwork_name = st.text_input("Enter the name of the artwork")
# artist_name = st.text_input("Enter the artist name")
# initial_appraisal_value = st.text_input("Enter the initial appraisal amount")
# artwork_uri = st.text_input("Enter the URI to the artwork")

# if st.button("Register Artwork"):
#     tx_hash = contract.functions.registerArtwork(
#         address,
#         artwork_name,
#         artist_name,
#         int(initial_appraisal_value),
#         artwork_uri
#     ).transact({'from': address, 'gas': 1000000})
#     receipt = w3.eth.waitForTransactionReceipt(tx_hash)
#     st.write("Transaction receipt mined:")
#     st.write(dict(receipt))
# st.markdown("---")


# ################################################################################
# # Appraise Art
# ################################################################################
# st.markdown("## Appraise Artwork")
# tokens = contract.functions.totalSupply().call()
# token_id = st.selectbox("Choose an Art Token ID", list(range(tokens)))
# new_appraisal_value = st.text_input("Enter the new appraisal amount")
# report_uri = st.text_area("Enter notes about the appraisal")
# if st.button("Appraise Artwork"):

#     # Use the token_id and the report_uri to record the appraisal
#     tx_hash = contract.functions.newAppraisal(
#         token_id,
#         int(new_appraisal_value),
#         report_uri
#     ).transact({"from": w3.eth.accounts[0]})
#     receipt = w3.eth.waitForTransactionReceipt(tx_hash)
#     st.write(receipt)
# st.markdown("---")

# ################################################################################
# # Get Appraisals
# ################################################################################
# st.markdown("## Get the appraisal report history")
# art_token_id = st.number_input("Artwork ID", value=0, step=1)
# if st.button("Get Appraisal Reports"):
#     appraisal_filter = contract.events.Appraisal.createFilter(
#         fromBlock=0,
#         argument_filters={"tokenId": art_token_id}
#     )
#     appraisals = appraisal_filter.get_all_entries()
#     if appraisals:
#         for appraisal in appraisals:
#             report_dictionary = dict(appraisal)
#             st.markdown("### Appraisal Report Event Log")
#             st.write(report_dictionary)
#             st.markdown("### Appraisal Report Details")
#             st.write(report_dictionary["args"])
#     else:
#         st.write("This artwork has no new appraisals")
