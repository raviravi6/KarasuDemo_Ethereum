// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "../interfaces/IBadge.sol";

contract Badge is IBadge {
    // Badge's name
    string private _name;

    // Badge's symbol
    string private _symbol;

    // Badge's URI
    string private _URI;

    // Mapping from token ID to owner's address
    mapping(uint256 => address) private _owners;

    // Mapping from owner's address to Token
    mapping(address => Token) private _tokens;

    constructor(string memory name_, string memory symbol_) {
        _name = name_;
        _symbol = symbol_;
    }

    // Returns the badge's name
    function name() public view virtual override returns (string memory) {
        return _name;
    }

    // Returns the badge's symbol
    function symbol() public view virtual override returns (string memory) {
        return _symbol;
    }

    // Returns the badge's URI
    function URI() public view virtual override returns (string memory) {
        return _URI;
    }

    // Returns the token owned by `owner`, if it exists, and an empty Token otherwise
    function tokenOf(address owner)
        public
        view
        virtual
        override
        returns (Token memory)
    {
        require(owner != address(0), "Invalid owner at zero address");

        return _tokens[owner];
    }

    // Returns the owner of a given token ID, reverts if the token does not exist
    function ownerOf(uint256 tokenId)
        public
        view
        virtual
        override
        returns (address)
    {
        require(tokenId != 0, "Invalid tokenId value");

        address owner = _owners[tokenId];

        require(owner != address(0), "Invalid owner at zero address");

        return owner;
    }

    // Sets a new badge URI
    function _setURI(string memory newURI) internal virtual {
        _URI = newURI;
    }

    // Checks if a token ID exists
    function _exists(uint256 tokenId) internal view virtual returns (bool) {
        return _owners[tokenId] != address(0);
    }

    /**
     * @dev Mints `tokenId` and transfers it to `to`.
     * Requirements:
     *
     * - `tokenId` must not exist.
     * - `to` cannot be the zero address.
     *
     * Emits a {Minted} event.
     */
    function _mint(address to, uint256 tokenId) internal virtual {
        require(to != address(0), "Invalid owner at zero address");
        require(!_exists(tokenId), "Token already minted");
        require(tokenOf(to).id == 0, "Owner already has a token");
        require(tokenId != 0, "Token ID can't be zero");

        Token memory newToken;
        newToken.id = tokenId;
        newToken.timestamp = block.timestamp;

        _tokens[to] = newToken;
        _owners[tokenId] = to;

        emit Minted(to, tokenId, block.timestamp);
    }

    /**
     * @dev Updates the token's timestamp owned by `owner`
     * Requirements:
     *
     * - `owner` cannot be the zero address.
     * - `owner` must have a token.
     *
     * Emits a {Updated} event.
     */
    function _updateTimestamp(address owner) internal virtual {
        require(owner != address(0), "Invalid owner at zero address");
        require(tokenOf(owner).id != 0, "Owner does not have a token");

        Token storage token = _tokens[owner];
        token.timestamp = block.timestamp;

        emit Updated(owner, token.id, token.timestamp);
    }

    /**
     * @dev Burns `tokenId`.
     *
     * Requirements:
     *
     * - `tokenId` must exist.
     *
     * Emits a {Burned} event.
     */
    function _burn(uint256 tokenId) internal virtual {
        address owner = Badge.ownerOf(tokenId);

        delete _tokens[owner];
        delete _owners[tokenId];

        emit Burned(owner, tokenId, block.timestamp);
    }
}
