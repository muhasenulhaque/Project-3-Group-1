pragma solidity ^0.5.0;

// ----------------------------------------------------------------------------------------------
// Sample fixed supply token contract
// Enjoy. (c) BokkyPooBah 2017. The MIT Licence.
// ----------------------------------------------------------------------------------------------


// ERC Token Standard #20 Interface
// https://github.com/ethereum/EIPs/issues/20



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

contract ERC20Interface {
    // Get the total token supply
    function totalSupply() view public returns (uint256);

    // Get the account balance of another account with address _owner
    function balanceOf(address _owner) view public returns (uint256);

    // Send _value amount of tokens to address _to
    function transfer(address _to, uint256 _value) public returns (bool success);

    // Send _value amount of tokens from address _from to address _to
    function transferFrom(address _from, address _to, uint256 _value) public returns (bool success);

    // Allow _spender to withdraw from your account, multiple times, up to the _value amount.
    // If this function is called again it overwrites the current allowance with _value.
    // this function is required for some DEX functionality
    function approve(address _spender, uint256 _value) public returns (bool success);

    // Returns the amount which _spender is still allowed to withdraw from _owner
    function allowance(address _owner, address _spender) view public returns (uint256 remaining);

    // Triggered when tokens are transferred.
    event Transfer(address indexed _from, address indexed _to, uint256 _value);

    // Triggered whenever approve(address _spender, uint256 _value) is called.
    event Approval(address indexed _owner, address indexed _spender, uint256 _value);
}


contract FixedSupplyToken is ERC20Interface {
    string public constant symbol = "FIXED";
    string public constant name = "Example Fixed Supply Token";
    uint8 public constant decimals = 18;
    uint256 _totalSupply = 1000000;

//      Project-3-Group-1
//      *****************
// Using SafeMath Library for improved security
    using SafeMath for uint256;

    // Owner of this contract
    address public owner;

    // Balances for each account
    mapping (address => uint256) balances;

    // Owner of account approves the transfer of an amount to another account
    mapping (address => mapping (address => uint256)) allowed;

    // Functions with this modifier can only be executed by the owner
    modifier onlyOwner() {
        require(msg.sender == owner);
        _;
    }

    // Constructor
    //function FixedSupplyToken() public {
    // FIXED -  Defining constructors as functions with the same name as the contract is deprecated. Use "constructor(...) { ... }" instead [duplicate]
    //https://ethereum.stackexchange.com/questions/47175/defining-constructors-as-functions-with-the-same-name-as-the-contract-is-depreca
    
    constructor() public {  // New Constructor definition

        owner = msg.sender;
        balances[owner] = _totalSupply;
    }

    function totalSupply() view public returns (uint256) {
        return _totalSupply;
    }

    // What is the balance of a particular account?
    function balanceOf(address _owner) view public returns (uint256) {
        return balances[_owner];
    }

    // Transfer the balance from owner's account to another account
    function transfer(address _to, uint256 _amount) public returns (bool success) {
        if (balances[msg.sender] >= _amount
        && _amount > 0


	//      Project-3-Group-1
    //      *****************
	//	Converted arithmetic operations to SafeMath equivalent	
	//
        //&& balances[_to] + _amount > balances[_to]) {  
        && (balances[_to].add(_amount)) > balances[_to]) {

            //balances[msg.sender] -= _amount;
            balances[msg.sender] = balances[msg.sender].sub(_amount);
            
            //balances[_to] += _amount;            
            balances[_to] = balances[_to].add(_amount);
            
            emit Transfer(msg.sender, _to, _amount);
            return true;
        }
        else {
            return false;
        }
    }

    // Send _value amount of tokens from address _from to address _to
    // The transferFrom method is used for a withdraw workflow, allowing contracts to send
    // tokens on your behalf, for example to "deposit" to a contract address and/or to charge
    // fees in sub-currencies; the command should fail unless the _from account has
    // deliberately authorized the sender of the message via some mechanism; we propose
    // these standardized APIs for approval:
    function transferFrom(
    address _from,
    address _to,
    uint256 _amount
    ) public returns (bool) {

	//      Project-3-Group-1
    //      *****************
	//	Converted arithmetic operations to SafeMath equivalent	
	//
        if (balances[_from] >= _amount
        && allowed[_from][msg.sender] >= _amount
        && _amount > 0

        //&& balances[_to] + _amount > balances[_to]) {
        && balances[_to].add(_amount) > balances[_to]) {

            //balances[_from] -= _amount;
            balances[_from] = balances[_from].sub(_amount);
            
            //allowed[_from][msg.sender] -= _amount;            
            allowed[_from][msg.sender] = allowed[_from][msg.sender].sub(_amount);
            
            //balances[_to] += _amount;            
            balances[_to] = balances[_to].add(_amount);
            
            emit Transfer(_from, _to, _amount);
            return true;
        }
        else {
            return false;
        }
    }


    // Allow _spender to withdraw from your account, multiple times, up to the _value amount.
    // If this function is called again it overwrites the current allowance with _value.
    function approve(address _spender, uint256 _amount) public returns (bool success) {
        allowed[msg.sender][_spender] = _amount;
        emit Approval(msg.sender, _spender, _amount);
        return true;
    }

    function allowance(address _owner, address _spender) view public returns (uint256 remaining) {
        return allowed[_owner][_spender];
    }

}
