from pathlib          import Path
from argparse         import ArgumentParser
from snps_dl.scrapper import download
from snps_dl.fs_utils import wait_files 

parser = ArgumentParser(description="A webscrapper to download Synopsys tools from eftstream website")
parser.add_argument("product", type=str, help="Synopsys tool name as in eftstream folder like vcs_all")
parser.add_argument("version", type=str, help="Version string like vX-2025.06-SP2")
args = parser.parse_args()

product = args.product
version = args.version

src_dir = Path.home()/'Downloads'
siteID = download(product, version)

conf = f"""
SourceDir: {src_dir}
SiteId: {siteID}
PRODUCTS: {product.split('_')[0]}
RELEASES: ${version[1:]}
PLATFORMS: common linux64
""".strip()

with open(f'{product}.conf', 'w') as f:
	f.write(conf)

wait_files(product, version)
