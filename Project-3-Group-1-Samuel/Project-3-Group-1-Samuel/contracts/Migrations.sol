pragma solidity ^0.5.0;

contract Migrations {
  address public owner;
  uint public last_completed_migration;

  modifier restricted() {
    if (msg.sender == owner) _;
  }

//  Constructor
//  function Migrations() {
// FIXED - Defining constructors as functions with the same name as the contract is deprecated. Use "constructor(...) { ... }" instead [duplicate]
//https://ethereum.stackexchange.com/questions/47175/defining-constructors-as-functions-with-the-same-name-as-the-contract-is-depreca

  constructor() public {  
    owner = msg.sender;
  }

  function setCompleted(uint completed) public {  // "restricted" visibility replaced with public
    last_completed_migration = completed;
  }

  function upgrade(address new_address) public {  // "restricted" visibility replaced with public
    Migrations upgraded = Migrations(new_address);
    upgraded.setCompleted(last_completed_migration);
  }
}
