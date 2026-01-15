from time       import sleep
from getpass    import getpass
from subprocess import STDOUT
from threading  import Thread, Event
from selenium   import webdriver
from selenium.webdriver.common.by  import By
from selenium.webdriver.support.ui import WebDriverWait as wait 
from selenium.webdriver.support.expected_conditions \
	import presence_of_element_located as presence_of
from selenium.webdriver.firefox.options import Options
from snps_dl.database import list_of_files


def getInfo(info):
	info['siteID'] = input('Site ID:  ')
	info['user']   = input('Username: ')
	info['pass']   = getpass()

def download(product, version):
	info = {}
	t = Thread(target=getInfo, args=(info,))
	t.start()

	options = Options()
	options.add_argument("--headless")
	driver = webdriver.Firefox(options=options)
	
	driver.install_addon('data/aspera.xpi')
	driver.get('https://eftstream.synopsys.com')
	t.join()

	print('Solvnet/Okta Login')
	btn_match = (By.ID, "okta-signin-submit")
	form_btn = wait(driver, 20).until(presence_of(btn_match))
	form_usr = driver.find_element(By.ID, "okta-signin-username")
	form_pwd = driver.find_element(By.ID, "okta-signin-password")

	form_usr.send_keys(info['user'])
	form_pwd.send_keys(info['pass'])
	form_btn.click()

	print('Requesting OTP code')
	mail_match = (By.CLASS_NAME, "mask-email")
	mail = wait(driver, 20).until(presence_of(mail_match))
	info['mail'] = mail.text

	btn  = driver.find_element(By.CLASS_NAME, "button")
	btn.click()

	field_match = (By.ID, "input48")
	field = wait(driver, 20).until(presence_of(field_match))

	print('Check your e-mail')
	field.send_keys(input(f'Provide code sent to {info['mail']}: ')) 

	btn  = driver.find_element(By.CLASS_NAME, "button")
	btn.click()

	print('Loading eftstream info')

	btn_match = (By.ID, "download_button")
	btn = wait(driver, 20).until(presence_of(btn_match))

	print('Opening VCS folder')
	#TODO: Get share number
	url = driver.current_url
	print(url)
	driver.get(f'{url}?path=/site{info['siteID']}/MyProducts/rev/{product}_{version}')

	for file in list_of_files[product][version]:
		driver.find_element(By.ID, f'files_cbx_{file}').click()

	print('Requesting download')
	sleep(2)

	download_btn = driver.find_element(By.ID, "download_button")
	download_btn.click()

	print('Download in progress')
	sleep(2)

	driver.quit()
	return info['siteID']
