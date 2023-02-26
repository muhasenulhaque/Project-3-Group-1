
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

option = st.sidebar.selectbox("Which Option?", ('DTE', 'Exchange Overview', 'FIXED Token Trading', 'Manage Token'), 3)


#   DISPLAY SELECTED OPTION PAGE

#st.header(option)

if option == 'DTE':
    st.write ("DTE Option")

if option == 'Exchange Overview':
    st.write ("Exchange Overview Option")

if option == 'FIXED Token Trading':
    st.write ("FIXED Token Trading Option")

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
        send_amount_token = st.text_input("Approve token")
        send_to_address = st.text_input("Approved address")
        st.write("Approve the address to be allowed to send a token from your address to another address. This is important for the Exchange. When you fund the token in the exchange then it will deduct in your name the token from your address to the token address.")

    with col2:
        st.subheader("Send Token")
        #st.image("https://static.streamlit.io/examples/cat.jpg")

        apr_amount_token = st.text_input("Enter the name of token")
        apr_to_address = st.text_input("Enter the 'to' address")  
        st.write("Directly send a token from your address to another address.")
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
