# MineOverMatter-Bitcoin-Scripting

This repository contains the code for Assignment-3 of the course CS-216: Introduction to Blockchain. We script and compare Legacy (P2PKH) and SegWit (P2SH-P2WPKH) address formats in Bitcoin using `bitcoin-core` and `btcdeb`.

<div align="center">

### Team: MineOverMatter
| Name         | Roll No |
|--------------|---------|
| Abhinav Bitragunta        | 230001003     |
| Aman Gupta          | 230001006     |
| Srinidhi Sai Boorgu     | 230001072     |

</div>

## Dependencies

- `bitcoin-core` `(bitcoind)` running in regtest mode
- `btcdeb` for debugging and verifying Bitcoin scripts
- `python 3.6+`
- `python-bitcoinrpc` library
- `python-simplejson` library
- `python-decimal` library

## Setup and Execution

1. Start bitcoind in regtest mode:
```bash
bitcoind -regtest
```
2. Open each Python script and modify the `rpc_user` and `rpc_password` variables to match your configuration.
3. Update the `bitcoin.conf` file present in the repository with your credentials and place it in your `bitcoin-core` directory.
4. Depending on the autoload-wallet configuration of your `bitcoin-core`, you may or may not need to uncomment the loadwallet lines in each script. **Make sure to uncomment the loadwallet lines incase you encounter an error in any of the scripts.**
5. Run the scripts in the following order:

### Part 1: Legacy Address Transactions (P2PKH)
```bash
python part1_legacy_a_to_b.py
python part1_legacy_b_to_c.py
```

### Part 2: SegWit Address Transactions (P2SH-P2WPKH)
```bash
python part2_segwit_a_to_b.py
python part2_segwit_b_to_c.py
```

### Part 3: Analysis and Comparison
```bash
python part3_comparison.py
```

## Script Descriptions

### Part 1: Legacy Address Transactions
- `part1_legacy_a_to_b.py`: Creates legacy addresses A, B and C, funds A, and creates a transaction from A to B.
- `part1_legacy_b_to_c.py`: Transfers funds from B to C.

### Part 2: SegWit Address Transactions
- `part2_segwit_a_to_b.py`: Creates P2SH-SegWit addresses A', B' and C', funds A', and creates a transaction from A' to B'.
- `part2_segwit_b_to_c.py`: Transfers funds from B' to C'.

### Part 3: Comparison of both Transactions
- `part3_comparison.py`: Compares the transaction sizes, scripts, and structure between legacy and SegWit transactions.

## Output Files
- `tx_info.json`: Contains information about the legacy transactions from A to B.
- `tx_info_final.json`: Contains information about all legacy transactions.
- `segwit_tx_info.json`: Contains information about the SegWit transactions from A' to B'.
- `segwit_tx_info_final.json`: Contains information about all SegWit transactions.
- `comparison_results.json`: Contains detailed comparison between legacy and SegWit transactions.
