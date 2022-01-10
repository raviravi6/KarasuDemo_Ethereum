//SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract ERC20EscrowCID is Ownable {
    event Deposited(
        address indexed payer,
        string cid,
        address tokenAddress,
        uint256 amount,
        string action
    );
    event Withdrawn(
        address indexed payer,
        string cid,
        address tokenAddress,
        uint256 amount,
        string action
    );

    // cid string => token address => amount
    mapping(string => mapping(address => uint256)) public deposits;

    // cid string => token address => expiration time
    mapping(string => mapping(address => uint256)) public expirations;

    // cid string => payee address
    mapping(string => address) public payees;

    constructor() {}

    function deposit(
        string memory _cid,
        uint256 _amount,
        uint256 _expiration,
        IERC20 token
    ) public onlyOwner {
        require(
            token.transferFrom(msg.sender, address(this), _amount),
            "Could not transfer amount"
        );

        deposits[_cid][address(token)] += _amount;
        expirations[_cid][address(token)] = block.timestamp + _expiration;
        emit Deposited(msg.sender, _cid, address(token), _amount, "deposited");
    }

    function setPayee(string memory _cid, address payable _payee)
        public
        onlyOwner
    {
        payees[_cid] = _payee;
    }

    function withdraw(
        string memory _cid,
        uint256 _amount,
        IERC20 token
    ) public {
        uint256 totalPayment = deposits[_cid][address(token)];
        require(totalPayment >= _amount, "Not enough value");

        address _payee = payees[_cid];
        require(msg.sender == _payee, "Don't have permission to withdraw");

        token.approve(_payee, _amount);
        require(token.transfer(_payee, _amount));
        deposits[_cid][address(token)] = totalPayment - _amount;

        emit Withdrawn(msg.sender, _cid, address(token), _amount, "completed");
    }

    function refund(string memory _cid, IERC20 token) public onlyOwner {
        require(
            block.timestamp > expirations[_cid][address(token)],
            "The payment is still in escrow."
        );
        uint256 payment = deposits[_cid][address(token)];
        token.approve(msg.sender, payment);
        require(token.transfer(msg.sender, payment), "Transfer failed");
        deposits[_cid][address(token)] = 0;
        emit Withdrawn(msg.sender, _cid, address(token), payment, "refunded");
    }
}
