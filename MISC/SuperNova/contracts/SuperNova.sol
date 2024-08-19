// SPDX-License-Identifier: MIT
pragma solidity 0.8.17;

contract Supernova {
    bytes32 private passwordSlot;
    struct CartItem {
        uint8 quantity;
        bool exists;
    }

    mapping(string => uint8) private flagRequirements;
    mapping(address => mapping(string => CartItem)) public cart;
    address YOUR_WALLET_ADDRESS;

    string[9] private superNova = ["S", "U", "P", "E", "R", "N", "O", "V", "A"];

    event LetterPurchased(address indexed buyer, string letter, uint8 quantity);
    event ChallengeSolved(address indexed solver);

    constructor(address _wallet) {
        YOUR_WALLET_ADDRESS = _wallet;
        // SU SU SU SUPERNOVA
        flagRequirements["S"] = 4;
        flagRequirements["U"] = 4;
        flagRequirements["P"] = 1;
        flagRequirements["E"] = 1;
        flagRequirements["R"] = 1;
        flagRequirements["N"] = 1;
        flagRequirements["O"] = 1;
        flagRequirements["V"] = 1;
        flagRequirements["A"] = 1;

        passwordSlot = generateRandomPassword();
    }

    function generateRandomPassword() internal view returns (bytes32) {
        return keccak256(
            abi.encodePacked(
                block.timestamp, 
                block.difficulty, 
                msg.sender,
                blockhash(block.number - 1)
            )
        );
    }

    function isValidLetter(string memory letter) internal pure returns (bool) {
        bytes memory b = bytes(letter);
        if (b.length != 1) {
            return false;
        }
        bytes1 char = b[0];
        return (char >= 0x41 && char <= 0x5A) || (char >= 0x61 && char <= 0x7A);
    }

    function purchaseLetter(string memory letter, bytes32 password) public payable {
        require(msg.sender == YOUR_WALLET_ADDRESS, "Please use the wallet provided to you");
        require(isValidLetter(letter), "Invalid letter. Only a-z, A-Z allowed");
        require(password == passwordSlot, "Invalid password");

        CartItem storage item = cart[msg.sender][letter];
        if (item.exists) {
            item.quantity += 1;
        } else {
            cart[msg.sender][letter] = CartItem(1, true);
        }

        emit LetterPurchased(msg.sender, letter, item.quantity);
    }

    function isChallSolved() public view returns (bool solved) {
        require(msg.sender == YOUR_WALLET_ADDRESS, "Please use the wallet provided to you");
        for (uint256 i = 0; i < superNova.length; i++) {
            string memory letter = superNova[i];
            CartItem memory item = cart[msg.sender][letter];
            if (!item.exists || item.quantity < flagRequirements[letter]) {
                return false;
            }
        }
        return true;
    }
}
