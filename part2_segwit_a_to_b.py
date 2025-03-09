from bitcoinrpc.authproxy import AuthServiceProxy
import simplejson as json
import decimal

def connect():
    rpc_user = "your_credential" 
    rpc_password = "your_credential"  
    rpc_connection = AuthServiceProxy(f"http://{rpc_user}:{rpc_password}@127.0.0.1:18443")
    return rpc_connection

def main():
    rpc = connect()
    blockchain_info = rpc.getblockchaininfo()
    print(f"Connected to Bitcoin Core {blockchain_info['chain']}")
    
    wallets = rpc.listwallets()
    wallet_name = "segwit_wallet"
    
    if wallet_name not in wallets:
        print(f"Creating new wallet: {wallet_name}")
        rpc.createwallet(wallet_name)
    
    # rpc.loadwallet(wallet_name)

    print("Generating blocks to make coins spendable")
    rpc.generatetoaddress(101, rpc.getnewaddress())
    
    address_a_prime = rpc.getnewaddress("", "p2sh-segwit")
    address_b_prime = rpc.getnewaddress("", "p2sh-segwit")
    address_c_prime = rpc.getnewaddress("", "p2sh-segwit")
    
    print(f"Address A': {address_a_prime}")
    print(f"Address B': {address_b_prime}")
    print(f"Address C': {address_c_prime}")
    
    print("Funding Address A'")
    txid_funding = rpc.sendtoaddress(address_a_prime, 1.0)
    print(f"Funding transaction ID: {txid_funding}")
    
    rpc.generatetoaddress(1, rpc.getnewaddress())
    
    unspent_outputs = rpc.listunspent(1, 9999999, [address_a_prime])
    
    if not unspent_outputs:
        raise Exception("No unspent outputs found for address A'")
    
    utxo = unspent_outputs[0]
    
    print("Creating raw transaction from A' to B'")
    txid = utxo['txid']
    vout = utxo['vout']
    amount = utxo['amount'] - decimal.Decimal(0.0001)  
    
    raw_inputs = [{"txid": txid, "vout": vout}]
    raw_outputs = {address_b_prime: amount}
    
    raw_tx = rpc.createrawtransaction(raw_inputs, raw_outputs)
    print(f"Raw transaction created: {raw_tx}")
    
    print("Decoding raw transaction")
    decoded_tx = rpc.decoderawtransaction(raw_tx)
    print(f"ScriptPubKey for address B': {json.dumps(decoded_tx['vout'][0]['scriptPubKey'], indent=2)}")
    
    print("Signing transaction")
    signed_tx = rpc.signrawtransactionwithwallet(raw_tx)
    
    if signed_tx['complete']:
        print("Transaction signed successfully")
    else:
        raise Exception("Transaction signing failed")
    
    print("Broadcasting transaction")
    tx_a_to_b = rpc.sendrawtransaction(signed_tx['hex'])
    print(f"Transaction from A' to B' broadcast: {tx_a_to_b}")
    
    rpc.generatetoaddress(1, rpc.getnewaddress())
    
    with open("segwit_tx_info.json", "w") as f:
        json.dump({
            "address_a_prime": address_a_prime,
            "address_b_prime": address_b_prime,
            "address_c_prime": address_c_prime,
            "tx_a_to_b": tx_a_to_b
        }, f)
    
    print("Transaction information saved to segwit_tx_info.json")
    
    final_tx = rpc.decoderawtransaction(signed_tx['hex'])
    print("Final Transaction Details:")
    print(json.dumps(final_tx, indent=2))
        
if __name__ == "__main__":
    main()
