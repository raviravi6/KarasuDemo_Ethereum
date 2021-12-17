// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "./Badge.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract BadgeToken is Badge, Ownable {
    struct TokenParameters {
        address owner;
        uint256 tokenId;
    }

    constructor(string memory badgeName_, string memory badgeSymbol_)
        Badge(badgeName_, badgeSymbol_)
    {}

    function exists(uint256 tokenId) external view returns (bool) {
        return _exists(tokenId);
    }

    function mint(address to, uint256 tokenId) external onlyOwner {
        _mint(to, tokenId);
    }

    function batchMint(TokenParameters[] memory tokensToMint)
        external
        onlyOwner
    {
        for (uint256 i = 0; i < tokensToMint.length; i++) {
            _mint(tokensToMint[i].owner, tokensToMint[i].tokenId);
        }
    }

    function burn(uint256 tokenId) external onlyOwner {
        _burn(tokenId);
    }
}
