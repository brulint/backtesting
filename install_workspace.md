# Install workspace

## Sudo

To give administrator rights to 'USER':

```bash
/sbin/adduser 'USER' sudo
```

## Python + libs

Install IPython, Pip and some usefull libs:

```bash
sudo apt install ipython3 python3-pip
sudo pip3 install requests numpy pandas bokey
```

## TA_Lib

To take full advantage of all features (technical indicators), you have to install TALib:

```bash
sudo apt install -y build-essential wget
wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz
tar -xvf ta-lib-0.4.0-src.tar.gz
cd ta-lib
./configure --prefix=/usr
make
sudo make install
sudo pip3 install TA-lib
```





