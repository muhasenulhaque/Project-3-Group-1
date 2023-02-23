pragma solidity ^0.5.0;

contract owned {
    address owner;

    modifier onlyowner() {
        require(msg.sender == owner);
        _;

    }

//  Constructor
//   function owned() public {
// FIXED - Defining constructors as functions with the same name as the contract is deprecated. Use "constructor(...) { ... }" instead [duplicate]
//https://ethereum.stackexchange.com/questions/47175/defining-constructors-as-functions-with-the-same-name-as-the-contract-is-depreca

    constructor() public {

        owner = msg.sender;
    }
}
