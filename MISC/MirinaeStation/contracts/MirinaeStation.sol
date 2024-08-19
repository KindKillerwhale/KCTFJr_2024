// SPDX-License-Identifier: MIT
pragma solidity ^0.7.0;

contract MirinaeStation {
    uint48 constant ticket_price = 281474976710655;
    uint256 amount_you_have = 0;
    uint48 loaned = 0;
    bool has_ticket = false;
    address YOUR_WALLET_ADDRESS;

    constructor(address _wallet) {
        YOUR_WALLET_ADDRESS = _wallet;
    }

    function buy_token(uint256 amount) public payable {
        require(msg.sender == YOUR_WALLET_ADDRESS, "Please use the wallet provided to you");
        msg.sender.call{value: amount}("");
        amount_you_have += amount;

    }

    function loan(uint48 amount) public payable {
        require(msg.sender == YOUR_WALLET_ADDRESS, "Please use the wallet provided to you");
        loaned += amount;
        msg.sender.call{value: amount}("");
    }

    function buyTicket() public {
        require(msg.sender == YOUR_WALLET_ADDRESS, "Please use the wallet provided to you");
        require(amount_you_have >= ticket_price, "Not enough funds to buy the ticket");
        amount_you_have -= ticket_price;
        has_ticket = true;
    }


    function isChallSolved() public view returns (bool solved) {
        if (has_ticket && (loaned == 0)) {
            return true;
        } else {
            return false;
        }
    }
}
