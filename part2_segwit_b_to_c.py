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
    wallet_name = "segwit_wallet"
    # rpc.loadwallet(wallet_name)
    
    with open("segwit_tx_info.json", "r") as f:
        tx_info = json.load(f)
    
    address_b_prime = tx_info["address_b_prime"]
    address_c_prime = tx_info["address_c_prime"]
    tx_a_to_b = tx_info["tx_a_to_b"]
    
    print(f"Address B': {address_b_prime}")
    print(f"Address C': {address_c_prime}")
    print(f"Previous transaction (A' to B'): {tx_a_to_b}")
    
    unspent_outputs = rpc.listunspent(1, 9999999, [address_b_prime])
    
    if not unspent_outputs:
        raise Exception("No unspent outputs found for address B'")
    
    utxo = None
    for output in unspent_outputs:
        if output['txid'] == tx_a_to_b:
            utxo = output
            break
    
    if not utxo:
        raise Exception(f"Could not find UTXO from transaction {tx_a_to_b}")
    
    print(f"Found UTXO: {utxo}")
    
    print("Creating raw transaction from B' to C'")
    txid = utxo['txid']
    vout = utxo['vout']
    amount = utxo['amount'] - decimal.Decimal(0.0001)  
    
    raw_inputs = [{"txid": txid, "vout": vout}]
    raw_outputs = {address_c_prime: amount}
    
    raw_tx = rpc.createrawtransaction(raw_inputs, raw_outputs)
    print(f"Raw transaction created: {raw_tx}")
    
    print("Decoding raw transaction")
    decoded_tx = rpc.decoderawtransaction(raw_tx)
    print(f"Raw transaction decoded: {json.dumps(decoded_tx, indent=2)}")
    
    print("Signing transaction")
    signed_tx = rpc.signrawtransactionwithwallet(raw_tx)
    
    if signed_tx['complete']:
        print("Transaction signed successfully")
    else:
        raise Exception("Transaction signing failed")
    
    decoded_signed_tx = rpc.decoderawtransaction(signed_tx['hex'])
    
    print("ScriptSig (unlocking script):")
    print(json.dumps(decoded_signed_tx['vin'][0].get('scriptSig', {}), indent=2))
    
    if 'witness' in decoded_signed_tx['vin'][0]:
        print("Witness data:")
        print(json.dumps(decoded_signed_tx['vin'][0]['witness'], indent=2))
    
    prev_tx = rpc.getrawtransaction(txid, True)
    prev_script_pubkey = prev_tx['vout'][vout]['scriptPubKey']
    
    print("Previous ScriptPubKey (locking script):")
    print(json.dumps(prev_script_pubkey, indent=2))
    
    print("Broadcasting transaction")
    tx_b_to_c = rpc.sendrawtransaction(signed_tx['hex'])
    print(f"Transaction from B' to C' broadcast: {tx_b_to_c}")
    
    rpc.generatetoaddress(1, rpc.getnewaddress())
    
    with open("segwit_tx_info_final.json", "w") as f:
        json.dump({
            "address_a_prime": tx_info["address_a_prime"],
            "address_b_prime": address_b_prime,
            "address_c_prime": address_c_prime,
            "tx_a_to_b": tx_a_to_b,
            "tx_b_to_c": tx_b_to_c,
            "scriptSig": decoded_signed_tx['vin'][0].get('scriptSig', {}),
            "previousScriptPubKey": prev_script_pubkey,
        }, f)
    
    print("Final transaction information saved to segwit_tx_info_final.json")
    
    rpc.unloadwallet(wallet_name)
     
if __name__ == "__main__":
    main()
