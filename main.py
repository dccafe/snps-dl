from pathlib          import Path
from argparse         import ArgumentParser
from snps_dl.scrapper import download
from snps_dl.fs_utils import wait_files 
from snps_dl.database import list_of_files

parser = ArgumentParser(description="A webscrapper to download Synopsys tools from eftstream website")
parser.add_argument("product", type=str, help="Synopsys tool name as in eftstream folder like vcs_all")
parser.add_argument("version", type=str, help="Version string like vX-2025.06-SP2")
args = parser.parse_args()

product = args.product
version = args.version

src_dir = Path.home()/'Downloads'
siteID = download(product, version)

vcs_conf = f"""
SourceDir: {src_dir}
SiteId: {siteID}
PRODUCTS: vcs
RELEASES: X-2025.06-SP2
PLATFORMS: common linux64
""".strip()

with open('vcs.conf', 'w') as f:
	f.write(vcs_conf)

files = list_of_files[product][version]
wait_files(files)
