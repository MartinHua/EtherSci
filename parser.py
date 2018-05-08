"""A client to interact with geth node and to save data to data structure."""


import parser_util
import requests
import json
import sys
import os
import pickle
import logging
import time



class Parser(object):
    """
    A client to migrate blockchain from geth to mongo.
    Description:
    ------------
    Before starting, make sure geth is running in RPC (port 8545 by default).
    Parameters:
    -----------
    rpc_port: <int> default 8545 	# The port on which geth RPC can be called
    host: <string> default "http://localhost" # The geth host
    start: <bool> default True		# Create the graph upon instantiation
    Usage:
    ------
    Default behavior:
        parser = Parser()
    Interactive mode:
        parser = Parser(start=False)
    Get the data from a particular block:
        block = parser.getBlock(block_number)
    """
    # narsil-1
    def __init__(
        self,
        start=False,
        rpc_port=8545,
        host="http://128.83.144.125",
        delay=0.0001,
        startBlock = None,
        endBlock = None,
        fileName = None
    ):
        """Initialize the Crawler."""
        logging.debug("Starting Crawler")
        self.url = "{}:{}".format(host, rpc_port)
        self.headers = {"content-type": "application/json"}

        # The max block number in the public blockchain
        self.max_block_geth = None

        # The delay between requests to geth
        self.delay = delay

        self.block = {}
        if start:
            self.run(startBlock, endBlock, fileName)

    def _rpcRequest(self, method, params, key):
        """Make an RPC request to geth on port 8545."""
        payload = {
            "method": method,
            "params": params,
            "jsonrpc": "2.0",
            "id": 0
        }
        time.sleep(self.delay)
        res = requests.post(
              self.url,
              data=json.dumps(payload),
              headers=self.headers
            ).json()
        return res[key]

    def getBlock(self, n):
        """Get a specific block from the blockchain and filter the data."""
        data = self._rpcRequest("eth_getBlockByNumber", [hex(n), True], "result")
        block = parser_util.decodeBlock(data)
        if block:
            txFee = 0
            for t in block["transactions"]:
                receipt = self._rpcRequest("eth_getTransactionReceipt", [t["txHash"]], "result")
                t["gasUsed"] = int(receipt["gasUsed"], 16)
                t["txFee"] = t["gasUsed"] * t["gasPrice"]
                txFee += t["txFee"]
            block["txFee"] = txFee
        return block

    def highestBlockEth(self):
        """Find the highest numbered block in geth."""
        num_hex = self._rpcRequest("eth_blockNumber", [], "result")
        return int(num_hex, 16)

    def saveBlock(self, block):
        """Insert a given parsed block into database."""
        self.block[block["blockNum"]] = block
        return

    def addBlock(self, n):
        """Add a block to database."""
        b = self.getBlock(n)
        if b:
            self.saveBlock(b)
            time.sleep(0.001)
        else:
            self.saveBlock({"number": n, "transactions": []})

    def run(self, startBlock, endBlock, fileName):
        """
        Run the process.
        Iterate through the blockchain on geth and save it to disk
        """
        fileName -= 1000

        print("Processing remainder of the blockchain...")
        for n in range(startBlock, endBlock):

            if n % 1000 == 0:
                self.block = {}
                fileName += 1000
            self.addBlock(n)
            if n % 100 == 99:
                pickle.dump(self.block, open("/scratch/cluster/xh3426/etherData/" + str(fileName) + ".p", "wb"))
                print("On ", fileName, "Done: ", n, "\n")
                f = open('/scratch/cluster/xh3426/etherData/' + str(fileName) + ".log", 'w')
                f.write("On "+str(fileName)+"Done: "+str(n)+"\n")
                f.close()

        print("Done!\n")

if __name__ == "__main__":
    parser = Parser()

    # print(parser.getBlock(5000000))
    parser = Parser(start=True, startBlock=int(sys.argv[1]), endBlock=int(sys.argv[1])+1000, fileName=int(sys.argv[1]))
    # parser = Parser(start=True, startBlock=0, endBlock=100, fileName="100")
    # d = pickle.load(open("/scratch/cluster/xh3426/etherData/100.p", "rb"))
    # print(d)
    # print(parser.highestBlockEth())


