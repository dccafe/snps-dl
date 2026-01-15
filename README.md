# Synopsys Downloader

This software uses web scrapping to download assets from eftstream.synopsys.com using aspera fasp protocol.

# How to install

/opt/synopsys/installer/installer   \
	-batch_installer                \
	-source /home/daniel/Downloads  \
	-target /opt/synopsys           \
	-product scl                    \
	-release 2025.03-SP2            \
	-platform linux64 