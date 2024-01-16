## How to Set Up a Miner From Scratch

### Overview
0. About NicheImage
1. Server creation
2. Install dependencies
3. Set up and register key
4. Launch miner

### About NicheImage
Mining on the network requires a GPU, but a single GPU can server multiple miners. For now there are only fixed image models, meaning that you need to pick one of the specified models, but in the future we will add open category where you can run any model and get incentive depending on how well your model scores.

### Server Creation
A GPU is needed to run any of the available image generation models. We recommend using a 3090 GPU if you have a small number of miners, or a 4090 if you have a large number of miners.

In this tutorial we will use a 3090 from runpod.io with the following container image: runpod/pytorch:2.1.0-py3.10-cuda11.8.0-devel-ubuntu22.04

The instance you create should have at least 50 GB disk memory, and as many ports open as miners you want to run. Alternatively, you could have one GPU server that generates images, and then another CPU server that runs the miners, and in such case the GPU server only needs one port open for inference. In this tutorial we will only be using one server.

### Install Dependencies

After you have started the instance, you can install dependencies by running:
```bash
apt update && apt upgrade -y
apt install sudo
sudo apt install python3-pip -y
```

Then install Bittensor and add it to path using:

```bash
pip install bittensor

echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

Then install pm2 by running:
```bash
sudo apt-get install nodejs -y -y
sudo apt-get install npm
sudo npm install pm2 -g
```
If you get any popus when installing pm2, you can just press enter.


## Set Up And Register Keys

It is recommended that you generate the keys using a safe wallet server, or generating them locally on your computer. And then, you can regenerate the public coldkey and the hotkeys on the miner server.

This adds an extra layer of security, preventing anyone with access to the server to be able to steal your Tao.

Regenerate coldkey_public using:
```bash
btcli wallet regen_coldkeypub --wallet.name <wallet_name> --ss58 <ss58_address>
```

And then hotkeys using:
```bash
btcli w regen_hotkey --wallet.name <wallet_name> --wallet.hotkey <hotkey_name> --mnemonic <hotkey_mnemonic>
```
Notice, that you need to replace the values in the <> with actual values.

You register by using:
```bash
btcli s register -subtensor.network finney --netuid 23 --wallet.name <wallet_name> --wallet.hotkey <hotkey_name>
```

## Launch Miner
When you have the keys and dependencies installed, just install the NicheTensor repo:

1. Clone the repository.
```bash
git clone https://github.com/NicheTensor/NicheImage.git
```
2. Install the dependencies.
```bash
cd NicheImage
pip install -r requirements.txt
```
3. Install the project.
```bash
pip install -e .
```
There are several models available to run:
- SDXLTurbo
```bash
pm2 start python --name "image_generation_endpoint_SDXLTurbo" -- -m dependency_modules.miner_endpoint.app --port 10006 --model_name SDXLTurbo
```

- RealisticVision
```bash
pm2 start python --name "image_generation_endpoint_RealisticVision" -- -m dependency_modules.miner_endpoint.app --port 10006 --model_name RealisticVision
```
- AnimeV3
```
pm2 start python --name "image_generation_endpoint_AnimeV3" -- -m dependency_modules.miner_endpoint.app --port 10006 --model_name RealisticVision
```
You also can follow the usage here:
```
python dependency_modules/miner_endpoint/app.py -h
usage: app.py [-h] [--port PORT] [--model_name {RealisticVision,SDXLTurbo,AnimeV3}]

options:
  -h, --help            show this help message and exit
  --port PORT
  --model_name {RealisticVision,SDXLTurbo,AnimeV3}
```
Notice that you can change the port 10006 to another value if that port is not open and you want miners to run on another server.

Then you can start miners like this:
```bash
pm2 start python --name "miner_1" -- -m neurons.miner.miner --netuid 23 --wallet.name <wallet_name> --wallet.hotkey <wallet_hotkey> --subtensor.network finney --generate_endpoint http://127.0.0.1:10006/generate --info_endpoint http://127.0.0.1:10006/info --axon.port <miner_port>
```
If the image generation API is on another server than the server you are starting the miner from, replace 127.0.0.1:10006 with the IP of the server and the port you selected.
