"""A client to interact with geth node and to save data to data structure."""


import parser_util
import requests
import json
import sys
import os
import logging
import time
# import tqdm
# sys.path.append(os.path.realpath(os.path.dirname(__file__)))
#
# DIR = os.environ['BLOCKCHAIN_MONGO_DATA_DIR']
# LOGFIL = "parser.log"
# if "BLOCKCHAIN_ANALYSIS_LOGS" in os.environ:
#     LOGFIL = "{}/{}".format(os.environ['BLOCKCHAIN_ANALYSIS_LOGS'], LOGFIL)
# parser_util.refresh_logger(LOGFIL)
# logging.basicConfig(filename=LOGFIL, level=logging.DEBUG)
# logging.getLogger("urllib3").setLevel(logging.WARNING)


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

    def __init__(
        self,
        start=False,
        rpc_port=8545,
        host="http://128.83.144.143",
        delay=0.0001
    ):
        """Initialize the Crawler."""
        logging.debug("Starting Crawler")
        self.url = "{}:{}".format(host, rpc_port)
        self.headers = {"content-type": "application/json"}

        # The max block number in the public blockchain
        self.max_block_geth = None

        # The delay between requests to geth
        self.delay = delay

        if start:
            self.max_block_geth = self.highestBlockEth()
            self.max_block_EtherDB = self.highestBlockDatabase()
            self.run()

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
              headers=self.headers).json()
        return res[key]

    def getBlock(self, n):
        """Get a specific block from the blockchain and filter the data."""
        data = self._rpcRequest("eth_getBlockByNumber", [hex(n), True], "result")
        block = parser_util.decodeBlock(data)
        txFee = 0
        for t in block["transactions"]:
            receipt = self._rpcRequest("eth_getTransactionReceipt", [t["txHash"]], "result")
            t["gasUsed"] = int(receipt["gasUsed"], 16)
            t["contractAddress"] = receipt["contractAddress"]
            txFee += t["gasUsed"] * t["gasPrice"]
        block["txFee"] = txFee
        return block

    def highestBlockEth(self):
        """Find the highest numbered block in geth."""
        num_hex = self._rpcRequest("eth_blockNumber", [], "result")
        return int(num_hex, 16)

    def saveBlock(self, block):
        """Insert a given parsed block into database."""
        return

    def highestBlockDatabase(self):
        """Find the highest numbered block in the database."""
        return 0

    def addBlock(self, n):
        """Add a block to database."""
        b = self.getBlock(n)
        if b:
            self.saveBlock(b)
            time.sleep(0.001)
        else:
            self.saveBlock({"number": n, "transactions": []})

    def run(self):
        """
        Run the process.
        Iterate through the blockchain on geth and fill up EtherDB with block data.
        """
        # logging.debug("Processing geth blockchain:")
        # logging.info("Highest block found as: {}".format(self.max_block_geth))
        # logging.info("Number of blocks to process: {}".format(len(self.block_queue)))

        # # Make sure the database isn't missing any blocks up to this point
        # logging.debug("Verifying that mongo isn't missing any blocks...")
        # self.max_block_mongo = 1
        # if len(self.block_queue) > 0:
        #     print("Looking for missing blocks...")
        #     self.max_block_mongo = self.block_queue.pop()
        #     for n in tqdm.tqdm(range(1, self.max_block_mongo)):
        #         if len(self.block_queue) == 0:
        #             # If we have reached the max index of the queue,
        #             # break the loop
        #             break
        #         else:
        #             # -If a block with number = current index is not in
        #             # the queue, add it to mongo.
        #             # -If the lowest block number in the queue (_n) is
        #             # not the current running index (n), then _n > n
        #             # and we must add block n to mongo. After doing so,
        #             # we will add _n back to the queue.
        #             _n = self.block_queue.popleft()
        #             if n != _n:
        #                 self.add_block(n)
        #                 self.block_queue.appendleft(_n)
        #                 logging.info("Added block {}".format(n))

        # Get all new blocks
        print("Processing remainder of the blockchain...")
        for n in range(self.max_block_EtherDB, self.max_block_geth):
            self.addBlock(n)

        print("Done!\n")


if __name__ == "__main__":
    parser = Parser()
    print(time.time())
    for n in range(5):
        print(parser.getBlock(n+5000000))
    print(time.time())