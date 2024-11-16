module.exports = {
    solidity: "0.8.25",
    networks:{
      hardhat:{
        throwOnTransactionFailures: false,
        throwOnCallFailures: false,
        chainId: 1,
        mining: {
          mempool: {
            order: "fifo"
          }
        },
        accounts: {
          count: 2
        }
      }
    }
  };
  