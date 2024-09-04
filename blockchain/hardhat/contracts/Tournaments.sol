// SPDX-License-Identifier: MIT

pragma solidity ^0.8.24;

contract Tournament {
    address private owner;
    string[] public matchData;

    constructor() {
        owner = msg.sender;
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner can call this function");
        _;
    }

    function addMatch(string calldata _match) public onlyOwner {
        matchData.push(_match);
    }

    function getMatchIndex(uint _index) public view returns (string memory) {
        if (_index < matchData.length) {
            return matchData[_index];
        }
        return "No match found";
    }
}
