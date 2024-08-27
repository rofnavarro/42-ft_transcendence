//SPDX-License-Identifier: UNLICENSED

pragma solidity ^0.8.24;

contract Tournment
{
    string[] public matchData;

	mapping(address => uint256) matchAddress;

	constructor()
	{
		matchAddress[msg.sender] = 0;
	}

    function addMatchData(string memory _matchData) public {
        matchData.push(_matchData);
    }

	function getTournments() public view returns (string[] memory, bytes32) {
        return (matchData, blockhash(block.number - 1));
    }

	function getTournmentAddress(address _address) public view returns (uint256) {
		return matchAddress[_address];
	}
}
