from snps_dl.scrapper import download
from snps_dl.fs_utils import wait_files 
from snps_dl.database import list_of_files
from pathlib          import Path

product = 'verdi'
version = 'vX-2025.06-SP2'
src_dir = Path.home()/'Downloads'

siteID = download(product, version)

site_info = f"""
	siteId={siteID}
	siteAdmin=
	siteContact=
"""

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
