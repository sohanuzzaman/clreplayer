import gspread, random, pyperclip, time, pyautogui
from datetime import datetime, date
from oauth2client.service_account import ServiceAccountCredentials
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#importing local files
from sheet_control import get_data, rand_re_link
from mail_login import login_gmail

#geeting todays date as string
today = "{:%d.%m.%Y}".format(datetime.now())

# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

# sheet = client.open("clreplay").sheet1

# Find a workbook by name and open the 2nd sheet
body_text_sheet = client.open("mailbody").sheet1
mailbody = body_text_sheet.get_all_records()

#get random mailbody
def load_mailbody(mb=mailbody):
	amb = [] #defining an empty list for all mailbody
	for text in mb:
		amb.append(text)
	random.shuffle(amb)
	return amb
body_text = load_mailbody()

#defining the cell to marking for job done
cell_value = 1

# Geeting list of links collected from cl
# def get_replay_links():
# 	links = []
# 	with open ('replay_links.txt') as f:
# 		for line in f:
# 			links.append(line)
# 	random.shuffle(links)
# 	return (links)
# replay_links = get_replay_links()

for row in get_data():
	email = row['Email']
	password = row['Password']
	remail = row['Recovery']
	reporting_date = row['Reporting Date']
	cell_value += 1

	if reporting_date == today:
		continue

	driver = webdriver.Chrome()
	#driver = webdriver.Firefox(executable_path='G:\cl_reolay\geckodriver.exe')
	login_gmail(driver, email, password, remail, cell_value)
	if login_gmail == False:
		driver.quit()
		continue
	# #Selenium
	# #chrome_options = Options()
	# #chrome_options.add_argument('--dns-prefetch-disable')
	# driver = webdriver.Chrome()
	# #driver = webdriver.Firefox(executable_path='G:\cl_reolay\geckodriver.exe')
	# driver.get("https://accounts.google.com/Login")
	# wait = WebDriverWait(driver, 10)
	# gmail_user_id_field = wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="identifierId"]')))
	# gmail_user_id_field.click()
	# gmail_user_id_field.send_keys(email)
	# gmail_user_id_field.send_keys(Keys.RETURN)
	# gmail_password_field = wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="password"]/div[1]/div/div[1]/input')))
	# gmail_password_field.send_keys(password)
	# gmail_password_field.send_keys(Keys.RETURN)
	# try:
	# 	remail_field = wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="view_container"]/form/div[2]/div/div/div/ul/li[1]/div/div[2]')))
	# 	remail_field.click()
	# 	remail_field_imput = wait.until(EC.element_to_be_clickable((By.ID, 'knowledge-preregistered-email-response')))
	# 	remail_field_imput.send_keys(remail)
	# 	remail_field_imput.send_keys(Keys.RETURN)
	# except:
	# 	pass
	# # Print reporting date to google sheet after log in
	# sheet.update_cell(cell_value, 4, today)

	# try:
	# 	wait.until(EC.element_to_be_clickable((By.XPATH, '//*[text()[contains(.,"Account disabled")]]')))
	# 	sheet.update_cell(cell_value, 5, "Problem (Account disabled)")
	# 	driver.quit()
	# 	continue
	# except:
	# 	pass
	#for loop
	# with open ('replay_links.txt') as f:
	# 	cllink = ""
	# 	for line in f():
	# 		cllink = line
	# 		driver.get(cllink)
	# 		mailbody_imput = wait.until(EC.element_to_be_clickable((By.ID, 'knowledge-preregistered-email-response')))
	# 		mailbody_imput.send_keys(random.choice(body_text))
	for _ in range(25):
		time.sleep(5)
		replay_link = rand_re_link()
		driver.get("{}".format(replay_link))
		wait = WebDriverWait(driver, 120)
		mailbody_imput = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id=":nn"]')))
		mailbody_imput.click()
		rand_body_text = random.choice(body_text)
		#pyperclip.copy('{}'.format(rand_body_text))
		pyperclip.copy(str(rand_body_text)[2:-2])
		mailbody_imput.send_keys(Keys.UP * 2)
		mailbody_imput.send_keys(rand_body_text)
		# mailbody_imput.send_keys(Keys.CONTROL + "v")
		mail_send_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id=":p0"]')))
		mail_send_button.click()
		#print (cllink)
		time.sleep(3)
	time.sleep(3)
	driver.quit()
	#sheet.update_cell(cell_value, 4, today)
	#sheet.update_cell(cell_value, 5, "Problem")
	# print ('{0} {1}'.format (email, password))
