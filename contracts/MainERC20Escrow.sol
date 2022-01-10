//SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract MainERC20Escrow is Ownable {
    enum PaymentStatus {
        Pending,
        Completed,
        Refunded
    }

    event Deposited(
        address indexed payee,
        address tokenAddress,
        uint256 amount
    );
    event Withdrawn(
        address indexed payee,
        address tokenAddress,
        uint256 amount
    );

    // payee address => token address => amount
    mapping(address => mapping(address => uint256)) public deposits;

    // payee address => token address => expiration time
    mapping(address => mapping(address => uint256)) public expirations;

    constructor() {}

    function deposit(
        address _payee,
        uint256 _amount,
        uint256 _expiration,
        IERC20 token
    ) public onlyOwner {
        require(
            token.transferFrom(msg.sender, address(this), _amount),
            "Could not transfer amount"
        );
        deposits[_payee][address(token)] += _amount;
        expirations[_payee][address(token)] = block.timestamp + _expiration;
        emit Deposited(_payee, address(token), _amount);
    }

    function withdraw(
        address payable _payee,
        uint256 _amount,
        IERC20 token
    ) public {
        uint256 totalPayment = deposits[_payee][address(token)];
        require(totalPayment >= _amount, "Not enough value");
        token.approve(_payee, _amount);
        require(token.transfer(_payee, _amount));
        deposits[_payee][address(token)] = totalPayment - _amount;
        emit Withdrawn(_payee, address(token), _amount);
    }

    function refund(address payable _payee, IERC20 token) public onlyOwner {
        require(
            block.timestamp > expirations[_payee][address(token)],
            "The payment is still in escrow."
        );
        uint256 payment = deposits[_payee][address(token)];
        token.approve(msg.sender, payment);
        require(token.transfer(msg.sender, payment), "Transfer failed");
        deposits[_payee][address(token)] = 0;
        emit Withdrawn(msg.sender, address(token), payment);
    }
}
