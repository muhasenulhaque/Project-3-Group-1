pragma solidity ^0.5.0;

contract owned {
    address owner;

    modifier onlyowner() {
        require(msg.sender == owner);
        _;

    }

//{ *** Defining constructors as functions with the same name as the contract is deprecated. Use "constructor(...) { ... }" instead [duplicate]
//   function owned() public {
    constructor() public {

        owner = msg.sender;
    }
}
