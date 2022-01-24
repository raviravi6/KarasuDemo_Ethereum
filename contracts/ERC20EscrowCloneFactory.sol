// SPDX-License-Identifier: MIT
// OpenZeppelin Contracts v4.4.1 (proxy/Clones.sol)

pragma solidity ^0.8.0;

import "./ClonesUpgradeable.sol";
import "./ERC20EscrowCounter.sol";

contract ERC20EscrowCloneFactory {
    event CloneCreated(address cloneAddress, address implementation);

    function createERC20EscrowCounter(address implementation) public {
        address cloned = ClonesUpgradeable.clone(implementation);
        ERC20EscrowCounter(cloned).initialize();
        ERC20EscrowCounter(cloned).transferOwnership(msg.sender);
        emit CloneCreated(cloned, implementation);
    }
}
