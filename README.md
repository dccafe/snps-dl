# Synopsys Downloader

This software uses web scrapping to download assets from eftstream.synopsys.com using aspera fasp protocol.

# How to install

 pip install -r requirements.txt

## Run the downloader

 python main.py <tool> <version>

 Ex: python main.py vcs_all vX-2025.06-SP2

This should download files to your Downloads folder
and create the config file vcs.conf,
Then, run the installer

 /opt/synopsys/installer/batch_installer -config vcs.conf -target /opt/synopsys
