import os
import json
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

# Define and connect a new Web3 provider
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))

################################################################################
# Contract Helper function:
# 1. Loads the contract once using cache
# 2. Connects to the contract using the contract address and ABI
################################################################################


@st.cache(allow_output_mutation=True) 


################################################################################
# @st.cache_data(allow_output_mutation=True) 
################################################################################

def load_contract():

    # Load the contract ABI
    with open(Path('./contracts/compiled/Exchange_abi.json')) as f:
        contract_abi = json.load(f)

    # Set the contract address (this is the address of the deployed contract)
    contract_address = os.getenv("SMART_CONTRACT_ADDRESS")
    # st.write("contract address******",contract_address)

    # Get the contract
    contract = w3.eth.contract(
        address=contract_address,
        abi=contract_abi
    )

    return contract


# Load the contract
contract = load_contract()
st.write("contract address******",contract.address)


st.title("Welcome to our DEX Center!!!")


st.write("***************************")

##################################################################################################
# For Admin of the DEX

# Adding New Tokens
##################################################################################################
token_symbolName = st.text_input("Enter the symbol name of the token")
address= st.text_input("Enter the wallet address")

if st.button("Add Token"):
    tx_hash = contract.functions.addToken(
        token_symbolName,
        address
    ).transact({'from': address, 'gas': 1000000})
    
    receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    st.write("Transaction receipt mined:")
    st.write(dict(receipt))
st.markdown("---")


##################################################################################################
# For User of the DEX

# Deposit ETH into the DEX Center
##################################################################################################

# user_wallet_address = st.text_input("Enter the wallet address from where you wannt to transfer the ETH")

# eth_deposit_amount = st.number_input("How much ETH do you want to deposit?")

# # eth_deposit_amount=int(eth_deposit_amount)
# wei_deposit_amount = w3.toWei(eth_deposit_amount, "ether")



# if st.button("Deposit"):
#     tx_hash = contract.functions.depositEther().transact(
#         {'from': user_wallet_address, 'value':wei_deposit_amount,'gas': 1000000}
#         )
#     receipt = w3.eth.waitForTransactionReceipt(tx_hash)
#     st.write(receipt)
#     st.markdown(f"{eth_deposit_amount} ETH deposited")




    # user_wallet_address = st.text_input("Enter the wallet address from where you wannt to transfer the ETH")
eth_deposit_amount = st.number_input("How many ETH do you want to deposit?")

    #eth_deposit_amount=int(eth_deposit_amount)

wei_deposit_amount = w3.toWei(eth_deposit_amount, "ether")

if st.button("Deposit"):
    tx_hash = contract.functions.depositEther().transact(
        {'value':wei_deposit_amount,'gas': 1000000}
        )
    receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    st.write(receipt)
    st.markdown(f"{eth_deposit_amount} ETH deposited")










# address= st.text_input("Enter your wallet address")
# address="0xf071d66b6A298D2AdEA73Ae6BDF7E93d4ffb7F83"
# private_key="dedaef419dfce412a0a12bb7e7c90075c721df721474af3a165246c3c98e63cc"

# eth_deposit_amount = st.number_input("How much ETH do you want to deposit?")

# if st.button("Deposit"):
#     # Convert the ether amount to Wei (the smallest unit of ether)
#     wei_deposit_amount = w3.toWei(eth_deposit_amount, "ether")
    
#     st.write(contract.address)
#     # build the transaction
#     transaction = {
#         'to': contract.address,
#         'value': wei_deposit_amount,
#         'gas': 21000,  # gas limit for a standard transaction
#         'gasPrice': w3.toWei(50, 'gwei'),  # gas price in wei
#         'nonce': w3.eth.getTransactionCount(address)
#     }


#     # Sign the transaction object with the user's private key
#     signed_tx = w3.eth.account.sign_transaction(transaction, private_key)
    
#     # Send the signed transaction to the network
#     tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    
#     # Wait for the transaction to be mined and get the receipt
#     receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    
#     # Display the receipt to the user
#     st.write(receipt)
#     st.markdown(f"{eth_deposit_amount} ETH deposited from wallet address : {address} to {contract.address}")




##################################################################################################
# For User of the DEX

# Check Ether Balance
##################################################################################################

# if st.button("Check Ether Balance"):
#     balance_wei = contract.functions.getEthBalanceInWei().call()
#     balance_eth = w3.fromWei(balance_wei,"ether")
#     # tx_hash = contract.functions.getEthBalanceInWei().transact({'from': contract.address, 'gas': 1000000})
#     # receipt = w3.eth.waitForTransactionReceipt(tx_hash)
#     # st.write("Transaction receipt mined:")
#     # st.write(dict(receipt))
#     st.write(f"The balance of Ether held by the smart contract is {balance_eth:.2f} ETH")
# st.markdown("---")

if st.button("Check Ether Balance"):
    st.write(f"{contract.address}")
    balance_wei = contract.functions.getEthBalanceInWei().call()
    balance_eth = w3.fromWei(balance_wei,"ether")
    st.write(f"The balance of wei held by the smart contract is {balance_wei} wei")
    # tx_hash = contract.functions.getEthBalanceInWei().transact({'from': contract.address, 'gas': 1000000})
    # receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    # st.write("Transaction receipt mined:")
    # st.write(dict(receipt))
    st.write(f"The balance of Ether held by the smart contract is {balance_eth} ETH")
st.markdown("---")




# st.write("Choose an account to get started")
# accounts = w3.eth.accounts
# address = st.selectbox("Select Account", options=accounts)
# st.markdown("---")

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