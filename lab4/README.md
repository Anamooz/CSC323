
[Introduction](#introduction)

[Available Features](#available-features)

[Hardware Requirements](#hardware-requirements)

[Setting Up the Environment](#setting-up-the-environment)

[GPU Acceleration](#gpu-acceleration)

[Using the ZachCoin™ Client](#using-the-zachcoin™-client)

---

# **Introduction** 

ZachCoin™ Client is a Python-built, CLI-based mining application that connects with the Zachcoin peer-to-peer network and allows users to interact with it.

# **Available Features**  

- Send and receive transactions from other users on the Zachcoin network  
- Ability to mine newly announced verified transactions  
- A wallet system for users to know which transactions they have available to spend

---

# **Hardware Requirements** 

- 2GHz dual-Core processor or higher  
- 4GB+  
-  Nvidia GTX 10x series card (Pascal) or newer ([GPU-accelerated mining](#gpu-acceleration) only)

# **Setting Up the Environment**

To run ZachCoin™ Client, you will need to make sure you have the following dependencies installed on your machine 

- [Python 3](https://www.python.org/downloads/) (3..10+ for GPU mining)  
- [Pip](https://packaging.python.org/en/latest/tutorials/installing-packages/) 


  Next, install the required Python packages 


- pycryptodome  
- ecdsa  
- p2pnetwork


  `pip install pycryptodome ecdso p2pnetwork`


# **GPU Acceleration**  

ZachCoin™ client supports GPU acceleration for enhanced mining performance if they have a supported graphics card. GPU acceleration can be used both in Linux and through WSL2 for Windows users

[WSL Guide](https://docs.nvidia.com/cuda/wsl-user-guide/index.html) 

 To set up GPU acceleration 

1. Verify that the computer has a [compatible GPU.](https://en.wikipedia.org/wiki/CUDA#GPUs_supported)  Currently, only Nivida cards with support of CUDA 11.2+ and Compute capability 6+ are compatible   
2. Ensure the Nividia graphics drivers have been installed   
- To check, run `nvidia-smi`  
- WSL users should have the GPU drivers installed automatically   
3.  Download and install the [CUDA SDK](https://developer.nvidia.com/cuda-11.2.0-download-archive) from the Nividia website  
- To verify that the CUDA SDK was installed run `nvcc --version`  
4. Add the paths to the CUDA sdk to your shell .rc file  
- For BASH, the default shell on most Linux distros and WSL run 
```
echo 'export PATH=/usr/local/cuda-11.2/bin:$PATH' >> ~/.bashrc
echo 'export LD_LIBRARY_PATH=/usr/local/cuda-11.2/lib64:$LD_LIBRARY_PATH' >> ~/.bashrc

source ~/.bashrc
```

- Replace `cuda-11.2` wih your version of CUDA

5. Lastly, install the necessary Python libraries necessary for GPU accelerated crypto mining   
- Numpy:  for CPU-based vector arrays  
- Cupy: for CUDA-based vector arrays   
- Cudf for CUDA-based SHA256 hashing 


  `pip install --extra-index-url=https://pypi.nvidia.com cudf-cu11`

  `pip install cupy`

  `pip install numpy`


  Depending on the graphics card and the amount of compute and VRAM available on the card, mining on the GPU can be 2 to 10 times faster than CPU-based mining.  


  You may also tune how many hashes are taken per round by adjusting the batch size in the hashGPU function.  


  By default, the miner takes 1,000,000 hashes per round.   A higher batch rate could help eliminate the bottleneck between CPU and GPU data transfer but at a cost of higher system and, more importantly, dedicated VRAM.  As an estimate, a batch size of 1,000,000 costs around \~3.5GB of VRAM 


  Note: While GPU acceleration will help in hash rates, this implementation will still be nowhere close to the potential hash rate of your GPU in dedicated crypto mining software such as Nicehash. Some various reasons for the performance gap could be that the current implementation has the conversion of the nonce from bytes to hex still done on the CPU, using off-the-shelf CUDA libraries designed for data analysis than mining instead of directly writing kernel code in C++,  and the Python GIL prevents full multithreading.

---

# **Using the ZachCoin™ Client**

Once you have all the dependencies installed, you can start  ZachCoin™ Client from the terminal

Usage: `python3 zc-client.py <Cal Poly Username> <Port Number greater than 8000>` 

Example : `python3 /home/tiger/lab4/zc-client.py bkwong01 9015`

On the first time launch, the ZachCoin™ Client will generate an ESDSA public-private key pair used as your Zachcoin wallet. The private key will be stored as \<username\>.key in the same directory as the program.  You would want to keep this key PRIVATE, as anyone with this key will have access to your wallet.  

When committing code into a VCS such as git, make sure `\*.key` is in your `.gitignore` file to prevent your key from being checked in\!

Once connected, you will be brought to the main menu which looks like this

There are 6 available options.  Input the number corresponding to that option to select it 

```
======================== ZachCoin™ ========================
 You can't spell "It's a Ponzi scheme!" without "ZachCoin" 
=========================================================== 

Balance:  14944 

  0: Print keys
  1: Write blockchain
  2: Write UTX pool
  3: New Transaction
  4: Mine Zackcoin
  5. Show Wallet
  6. Exit

Enter your choice -> 

```


0. Prints your public and private key  

  ```
  ======================== ZachCoin™ ========================
   You can't spell "It's a Ponzi scheme!" without "ZachCoin" 
  =========================================================== 

  Balance:  14944 

    0: Print keys
    1: Write blockchain
    2: Write UTX pool
    3: New Transaction
    4: Mine Zackcoin
    5. Show Wallet
    6. Exit

  Enter your choice -> 0
  sk:  --------------------------------
  vk:  b860c1d191c3dd0da23d158569f01a686d9b03572b9486dd4d6bf48adfd484ef03747bf2324232b9d88b1704ed02be7a
  ```

1. Writes the current state of the blockchain to  blockchain.json  

  ```
  ======================== ZachCoin™ ========================
   You can't spell "It's a Ponzi scheme!" without "ZachCoin" 
  =========================================================== 

  Balance:  14944 

    0: Print keys
    1: Write blockchain
    2: Write UTX pool
    3: New Transaction
    4: Mine Zackcoin
    5. Show Wallet
    6. Exit

  Enter your choice -> 1
  Blockchain written to blockchain.json

  ```

  Output of `blockchain.json` could look like:

  ```JSON
  [
 {
  "type": 0,
  "id": "b4b9b8f78ab3dc70833a19bf7f2a0226885ae2416d41f4f0f798762560b81b60",
  "nonce": "1950b006f9203221515467fe14765720",
  "pow": "00000027e2eb250f341b05ffe24f43adae3b8181739cd976ea263a4ae0ff8eb7",
  "prev": "b4b9b8f78ab3dc70833a19bf7f2a0226885ae2416d41f4f0f798762560b81b60",
  "tx": {
   "type": 1,
   "input": {
    "id": "0000000000000000000000000000000000000000000000000000000000000000",
    "n": 0
   },
   "sig": "adf494f10d30814fd26c6f0e1b2893d0fb3d037b341210bf23ef9705479c7e90879f794a29960d3ff13b50ecd780c872",
   "output": [
    {
     "value": 50,
     "pub_key": "c26cfef538dd15b6f52593262403de16fa2dc7acb21284d71bf0a28f5792581b4a6be89d2a7ec1d4f7849832fe7b4daa"
    }
   ]
  }
 },
 {
  "type": 0,
  "id": "aa31fb4ef777b9e3e0cbeccba6ff58b5b2fecb61b6902f4f4561f7291fcad17c",
  "nonce": "a3ce6c333e8b1af83bcf07f847a37db1",
  "pow": "000000429675a2c5f52756f1630eed4b596fa93a25d69f61beb8d6feaff18916",
  "prev": "b4b9b8f78ab3dc70833a19bf7f2a0226885ae2416d41f4f0f798762560b81b60",
  "tx": {
   "type": 1,
   "input": {
    "id": "b4b9b8f78ab3dc70833a19bf7f2a0226885ae2416d41f4f0f798762560b81b60",
    "n": 0
   },
   "sig": "ca0ebbc83ac5777f12f727d1cb9ef77d1daf6b152aac3f8c58f376ffccfeb40bebed17d732b9ebeb56468c66e7b8105f",
   "output": [
    {
     "value": 25,
     "pub_key": "825f8bdb84e691f8a0ff1f4b65aadb0dc036cd006672653ff77f3dbc4667c85aded761de13e115708e03f66c1e327b69"
    },
    {
     "value": 25,
     "pub_key": "c26cfef538dd15b6f52593262403de16fa2dc7acb21284d71bf0a28f5792581b4a6be89d2a7ec1d4f7849832fe7b4daa"
    },
    {
     "value": 50,
     "pub_key": "c26cfef538dd15b6f52593262403de16fa2dc7acb21284d71bf0a28f5792581b4a6be89d2a7ec1d4f7849832fe7b4daa"
    }
   ]
  }
 },
 {
  "type": 0,
  "id": "6ffabedafcc2de43bc36075a35339f200b51bf49a35a39f696f86cde470aaccf",
  "nonce": "1b043557fd01b0d913ef37c131ea0770",
  "pow": "0000003924f722d046f68666b2f6bb24dc9da129e335ce3110da7f8583956e69",
  "prev": "aa31fb4ef777b9e3e0cbeccba6ff58b5b2fecb61b6902f4f4561f7291fcad17c",
  "tx": {
   "type": 1,
   "input": {
    "id": "aa31fb4ef777b9e3e0cbeccba6ff58b5b2fecb61b6902f4f4561f7291fcad17c",
    "n": 1
   },
   "sig": "aaa0a47a6f5b827de876cae48e3838d0f4fbbc83548f1ee0006df27eb043a380e8d85fc262f86db7099747961a5fd17f",
   "output": [
    {
     "value": 25,
     "pub_key": "c26cfef538dd15b6f52593262403de16fa2dc7acb21284d71bf0a28f5792581b4a6be89d2a7ec1d4f7849832fe7b4daa"
    },
    {
     "value": 50,
     "pub_key": "c26cfef538dd15b6f52593262403de16fa2dc7acb21284d71bf0a28f5792581b4a6be89d2a7ec1d4f7849832fe7b4daa"
    }
   ]
  }
 },
 {
  "insert more blocks here ..."
 },
 {
  "type": 0,
  "id": "955363c00054dd80b5e2a2ca85238e05b31e2ccd10a1ee523b490903579d1a17",
  "prev": "54d06c3641e631a8418c1fa95a30ddf108c04f5d82fe43705fa9c2d9095bd759",
  "tx": {
   "type": 1,
   "input": {
    "id": "acc36372df9b4591e7a7615d506a2fa31768da1ef0e1e4de27edb99cbab8e812",
    "n": 0
   },
   "sig": "05a9c528fafcfe3c61075694ec276f26a7029326a455ab659573c0f05fe20d122655e6b11d216f96a26fafef0ded529e",
   "output": [
    {
     "value": 1,
     "pub_key": "ZachCoin for Life!"
    },
    {
     "value": 50,
     "pub_key": "de95e072946fabd29e853eddb9e88d16fcebaf5aa63cf5c286716c1ff84ed9a6d0ee0bec4e764ee606a0437065bf3691"
    }
   ]
  },
  "nonce": "3a3d21cedd97cd813ae6a6646fcc9b07",
  "pow": "000000299d728f6163bf7bd0180f4066cbd6acce8db2ccd14a78202d65c08a45"
 }
]
  ```

2. Writes the current state of the UTX pool to utx.json  

  ```
  ======================== ZachCoin™ ========================
   You can't spell "It's a Ponzi scheme!" without "ZachCoin" 
  =========================================================== 

  Balance:  14944 

    0: Print keys
    1: Write blockchain
    2: Write UTX pool
    3: New Transaction
    4: Mine Zackcoin
    5. Show Wallet
    6. Exit

  Enter your choice -> 2
  UTX pool written to utxpool.json
  ```

  Output of `utxpool.json` could look like:

  ```JSON
[
 {
  "type": 1,
  "input": {
   "id": "7dc68d4134d544b4e7dd7d6672134cbe7f2e09cbd7ee24331d6fa10a0ff1c2d4",
   "n": 0
  },
  "sig": "45cdba3beaa173d88ae592fc5a1a90fb6a6c7d46227f17c70f74c2671432858db1be07033b991d7ca61cc2a38d689da1",
  "output": [
   {
    "value": 25,
    "pub_key": "856e98824150ae0175ba799a8d3eae6ad7bbe5c7e9b4c409027d35cf6d2690960e2a5c1b5573c9e8a0e579b7cd18cb2b"
   }
  ]
 },
 {
  "insert more transaction here"
 },
 {
  "type": 1,
  "input": {
   "id": "fc3313e22aa74ee4f4ff63136f3ebcb41bc9fee7b2e97a75584ee340c61dae67",
   "n": 1
  },
  "output": [
   {
    "pub_key": "de95e072946fabd29e853eddb9e88d16fcebaf5aa63cf5c286716c1ff84ed9a6d0ee0bec4e764ee606a0437065bf3691",
    "value": 20
   },
   {
    "pub_key": "b860c1d191c3dd0da23d158569f01a686d9b03572b9486dd4d6bf48adfd484ef03747bf2324232b9d88b1704ed02be7a",
    "value": 28
   }
  ],
  "sig": "a8db12840033e5c8d8ccc31b8c0f28d856ee24900c1a72c27f180ec7e873390f5a2d86f1a432980e2ca343e8c6ab08bf"
 }
]
  ```


3. Opens a new screen that allows the user to start a transaction   
   1. Enter the public key address of the recipient you would like to send to  
   2. Enter the amount of Zachcoin you would like to send (Only full amounts are supported)  
   3. Review and press enter to send the transaction   


  ```
  ============================== New Transaction ==============================
  Enter the recipient's public key: de95e072946fabd29e853eddb9e88d16fcebaf5aa63cf5c286716c1ff84ed9a6d0ee0bec4e764ee606a0437065bf3691
  Enter the amount to send: 20
  Confirm?
    To: de95e072946fabd29e853eddb9e88d16fcebaf5aa63cf5c286716c1ff84ed9a6d0ee0bec4e764ee606a0437065bf3691
    Amount: 20
    Press Enter to confirm


  ```


4. Starts mining on either the CPU or GPU   
   1. If GPU mining is supported you will be prompted if you want to use it to mine  
   2. Next you will be prompted if you want to auto generate new transactions if the miner sits idle for 30 or more seconds   
   3. Afterwards mining will be dispatched into a new thread  
   4. The number of hashes will be reported every x,000,000 hashes where x is the number of available cpres or \[batch rate for GPU\]  
   5. At the end of each block the hashrate in megahashes will be reported   
   6. Pressing 4 from the main menu will terminate mining after the next block has been mined  

5. Prints the current state of your Zachcoin wallet including all available past transactions that can be used for input for future transactions and your total balance   

  ```
  ======================== ZachCoin™ ========================
 You can't spell "It's a Ponzi scheme!" without "ZachCoin" 
=========================================================== 

Balance:  14944 

  0: Print keys
  1: Write blockchain
  2: Write UTX pool
  3: New Transaction
  4: Mine Zackcoin
  5. Show Wallet
  6. Exit

Enter your choice -> node_message from server
5
============================== Wallet ==============================
Block Id fc3313e22aa74ee4f4ff63136f3ebcb41bc9fee7b2e97a75584ee340c61dae67
Index:  0
Amount:  1
----------------------------------------------------------------------
Block Id 820f715dec522820ce0d56104869572ff57e9802459c7a6de944b75a3430e816
Index:  0
Amount:  1
----------------------------------------------------------------------
Block Id 820f715dec522820ce0d56104869572ff57e9802459c7a6de944b75a3430e816
Index:  1
Amount:  49
----------------------------------------------------------------------
Block Id 820f715dec522820ce0d56104869572ff57e9802459c7a6de944b75a3430e816
Index:  2
Amount:  50
...
...
...
Block Id 54d06c3641e631a8418c1fa95a30ddf108c04f5d82fe43705fa9c2d9095bd759
Index:  1
Amount:  23
----------------------------------------------------------------------
Balance:  14944
  ```


6. Exits the ZachCoin™ wallet  
   1. Waits for any mining thread to finish   
   2. Cleans up and disconnects from the server  
   3. DO NOT press Ctrl+C (SIGINT)  to exit the program, You could introduce zombie processes if mining is still running 

  ```
  ======================== ZachCoin™ ========================
 You can't spell "It's a Ponzi scheme!" without "ZachCoin" 
=========================================================== 

Balance:  14944 

  0: Print keys
  1: Write blockchain
  2: Write UTX pool
  3: New Transaction
  4: Mine Zackcoin
  5. Show Wallet
  6. Exit

Enter your choice -> 6
Exiting ZachCoin™ Client
node is requested to stop!
Node stopping...
outbound_node_disconnected: server
Node stopped
  ```