//SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/Counters.sol";

contract ERC20EscrowCounter is Ownable {
    using Counters for Counters.Counter;
    Counters.Counter private _depositIds;

    event Deposited(
        uint256 indexed depositId,
        string cid,
        address tokenAddress,
        uint256 amount,
        string action
    );

    event PayeeSet(
        uint256 indexed depositId,
        string cid,
        address payee,
        string action
    );

    event Withdrawn(
        uint256 indexed depositId,
        string cid,
        address tokenAddress,
        uint256 amount,
        string action
    );

    // deposit id => token address => amount
    mapping(uint256 => mapping(address => uint256)) public deposits;

    // deposit id => token address => expiration time
    mapping(uint256 => mapping(address => uint256)) public expirations;

    // deposit id => payee address
    mapping(uint256 => address) public payees;

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

        _depositIds.increment();
        uint256 newDepositId = _depositIds.current();

        deposits[newDepositId][address(token)] += _amount;
        expirations[newDepositId][address(token)] =
            block.timestamp +
            _expiration;
        emit Deposited(
            newDepositId,
            _cid,
            address(token),
            _amount,
            "deposited"
        );
    }

    function setPayee(
        uint256 _depositId,
        string memory _cid,
        address payable _payee
    ) public onlyOwner {
        payees[_depositId] = _payee;
        emit PayeeSet(_depositId, _cid, _payee, "payeeSet");
    }

    function withdraw(
        uint256 _depositId,
        string memory _cid,
        uint256 _amount,
        IERC20 token
    ) public {
        uint256 totalPayment = deposits[_depositId][address(token)];
        require(totalPayment >= _amount, "Not enough value");

        address _payee = payees[_depositId];
        require(msg.sender == _payee, "Don't have permission to withdraw");

        token.approve(_payee, _amount);
        require(token.transfer(_payee, _amount));
        deposits[_depositId][address(token)] = totalPayment - _amount;

        emit Withdrawn(_depositId, _cid, address(token), _amount, "completed");
    }

    function refund(
        uint256 _depositId,
        string memory _cid,
        IERC20 token
    ) public onlyOwner {
        require(
            block.timestamp > expirations[_depositId][address(token)],
            "The payment is still in escrow."
        );
        uint256 payment = deposits[_depositId][address(token)];
        token.approve(msg.sender, payment);
        require(token.transfer(msg.sender, payment), "Transfer failed");
        deposits[_depositId][address(token)] = 0;
        emit Withdrawn(_depositId, _cid, address(token), payment, "refunded");
    }
}
