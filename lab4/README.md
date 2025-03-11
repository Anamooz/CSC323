


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
-  Nividia GTX 10x series card (Pascal) or newer ([GPU-accelerated mining](#gpu-acceleration) only)

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

Usage: `python3 zc-client.py \<Cal Poly Username\> \<Port Number greater than 8000\>` 
Example : `python3 /home/tiger/lab4/zc-client.py bkwong01 9015`

On the first time launch, the ZachCoin™ Client will generate an ESDSA public-private key pair used as your Zachcoin wallet. The private key will be stored as \<username\>.key in the same directory as the program.  You would want to keep this key PRIVATE, as anyone with this key will have access to your wallet.  

When committing code into a VCS such as git, make sure \*.key is in your gitignore to prevent your key from being checked in\!

Once connected, you will be brought to the main menu which looks like this

There are 6 available options.  Input the number corresponding to that option to select it 

0. Prints your public and private key  
1. Writes the current state of the blockchain to  blockchain.json  
2. Writes the current state of the UTX pool to utx.json  
3. Opens a new screen that allows the user to start a transaction   
   1. Enter the public key address of the recipient you would like to send to  
   2. Enter the amount of Zachcoin you would like to send (Only full amounts are supported)  
   3. Review and press enter to send the transaction   
4. Starts mining on either the CPU or GPU   
   1. If GPU mining is supported you will be prompted if you want to use it to mine  
   2. Next you will be prompted if you want to auto generate new transactions if the miner sits idle for 30 or more seconds   
   3. Afterwards mining will be dispatched into a new thread  
   4. The number of hashes will be reported every x,000,000 hashes where x is the number of available cpres or \[batch rate for GPU\]  
   5. At the end of each block the hashrate in megahashes will be reported   
   6. Pressing 4 from the main menu will terminate mining after the next block has been mined  
5. Prints the current state of your Zachcoin wallet including all available past transactions that can be used for input for future transactions and your total balance   
6. Exits the ZachCoin™ wallet  
   1. Waits for any mining thread to finish   
   2. Cleans up and disconnects from the server  
   3. DO NOT press Ctrl+C (SIGINT)  to exit the program, You could introduce zombie processes if mining is still running 