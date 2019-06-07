from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import datetime
import csv
from selenium.webdriver.support.ui import Select
import conf
import myconf

conf = conf.conf()
myconf = myconf.myconf()
driver = myconf.driver

def clickThenWait(selector_type, selector, wait_time):
	if selector_type == "id":
		element = driver.find_element_by_id(selector)
	if selector_type == "name":
		element = driver.find_element_by_name(selector)
	if selector_type == "xpath":
		element = driver.find_element_by_xpath(selector)
	if selector_type == "text":
		element = driver.find_element_by_link_text(selector)
	driver.execute_script('arguments[0].scrollIntoView({block: "center",});', element)
	element.click()
	time.sleep(wait_time)
#TODOクラス化する
def goSiteManagementPage():
	clickThenWait('xpath', '//*[@id="site_navigation_column "]/div[3]/span/a/span[2]/span', 1)#マーチャントツール
	clickThenWait('xpath', '//*[@id="site_navigation_column "]/div[3]/div/div[2]/div[2]/div/div/div/div[2]/div[1]/div/a', 2)

def goContentsLibraryPage():
	clickThenWait('xpath', '//*[@id="site_navigation_column "]/div[3]/span/a/span[2]/span', 1)#マーチャントツール
	clickThenWait('xpath', '//*[@id="site_navigation_column "]/div[3]/div/div[2]/div[2]/div/div/div/div[2]/div[3]/div/a', 2)

def goCatalogPage():
	clickThenWait('xpath', '//*[@id="site_navigation_column "]/div[1]/span/a/span[2]/span', 1)#マーチャントツール
	clickThenWait('xpath', '//*[@id="site_navigation_column "]/div[1]/div/div[2]/div[2]/div[1]/div/div/div[2]/div[3]/div/a', 2)

def goPricebookPage():
	clickThenWait('xpath', '//*[@id="site_navigation_column "]/div[1]/span/a/span[2]/span', 1)#マーチャントツール
	clickThenWait('xpath', '//*[@id="site_navigation_column "]/div[1]/div/div[2]/div[2]/div[1]/div/div/div[2]/div[7]/div/a', 2)

def goInvestoryPage():
	clickThenWait('xpath', '//*[@id="site_navigation_column "]/div[1]/span/a/span[2]/span', 1)#マーチャントツール
	clickThenWait('xpath', '//*[@id="site_navigation_column "]/div[1]/div/div[2]/div[2]/div[1]/div/div/div[2]/div[8]/div/a', 2)

def goSearchIndexPage():
	clickThenWait('xpath', '//*[@id="site_navigation_column "]/div[1]/span/a/span[2]/span', 1)#マーチャントツール
	clickThenWait('xpath', '//*[@id="site_navigation_column "]/div[1]/div/div[2]/div[3]/div/div/div/div[2]/div[1]/div/a', 2)

def goImportExportPage():
	clickThenWait('xpath', '//*[@id="site_navigation_column "]/div[1]/span/a/span[2]/span', 1)#マーチャントツール
	clickThenWait('xpath', '//*[@id="site_navigation_column "]/div[1]/div/div[2]/div[4]/div[1]/div/div/div[2]/div[10]/div/a', 2)

def goRegionInfoPage():
	clickThenWait('xpath', '//*[@id="site_navigation_column "]/div[1]/span/a/span[2]/span', 1)#マーチャントツール
	clickThenWait('xpath', '//*[@id="site_navigation_column "]/div[1]/div/div[2]/div[5]/div/div/div/div[2]/div[4]/div/a', 2)

def goOrderImportExportPage():
	clickThenWait('xpath', '//*[@id="site_navigation_column "]/div[1]/span/a/span[2]/span', 1)#マーチャントツール
	clickThenWait('xpath', '//*[@id="site_navigation_column "]/div[1]/div/div[2]/div[2]/div[2]/div/div/div[2]/div[6]/div/a', 2)
#/TODOクラス化する
def doTextInput(selector_type, selector, input_text, wait_time):
	if selector_type == "name":
		driver.find_element_by_name(selector).clear()
		driver.find_element_by_name(selector).send_keys(input_text)
	time.sleep(wait_time)

def chooseSelectbox(selector_type, selector, value, wait_time):
	if selector_type == "name":
		element = driver.find_element_by_name(selector)
	select_element = Select(element)
	select_element.select_by_value(value)
	time.sleep(wait_time)

#Web siteへのログイン
##ログインパスワードはよしなに。
def doLogin(SITE_LOGIN_URL, SITE_LOGIN_ID, SITE_LOGIN_PW):
	driver.get(SITE_LOGIN_URL)
	driver.maximize_window()
	time.sleep(2)
	doTextInput('name', 'LoginForm_Login', SITE_LOGIN_ID, 0)
	doTextInput('name', 'LoginForm_Password', SITE_LOGIN_PW, 2)
	driver.find_element_by_name("login").click()
	print('ログインプロセス完了しました。')
#/Web siteへのログイン

def createNewSite(SITE_ID,SITE_NAME,CARTRIDGE_PATH):
	goSiteManagementPage()
	clickThenWait('name', 'new', 2)
	doTextInput("name", "ChannelForm_RepositoryID", SITE_ID, 1)
	doTextInput("name", "ChannelForm_DisplayName", SITE_NAME, 1)
	#TODO TIME SETTING
	chooseSelectbox("name","ChannelForm_SiteTimeZone","Japan",2)
	chooseSelectbox("name","ChannelForm_CurrencyCode","JPY",2)
	driver.find_element_by_name('create').click()
	#Site Setting Tab
	clickThenWait('xpath', '//*[@id="bm_content_column"]/table/tbody/tr/td/table/tbody/tr/td[2]/table[1]/tbody/tr/td[2]', 2)
	doTextInput("name", "UpdateSite_Cartridges", CARTRIDGE_PATH, 2)
	driver.find_element_by_name('update').click()
	#Site Cache Tab
	clickThenWait('xpath', '//*[@id="bm_content_column"]/table/tbody/tr/td/table/tbody/tr/td[2]/table[1]/tbody/tr/td[3]/a', 2)
	doTextInput("name", "DomainStaticContentMaxAge", "0", 1)
	clickThenWait('name', 'DomainPageCachingAllowed', 2)
	driver.find_element_by_name('Ok').click()
	print('サイト作成プロセス完了')

def switchSite(SITE_NAME):
	clickThenWait("xpath", '//*[@id="SelectedSiteID-wrap"]/span', 1)
	SITE_XPATH = '''//*[@title="''' + SITE_NAME + '''"]'''
	driver.find_element_by_xpath(SITE_XPATH).click()
	time.sleep(2)

def getExportFileName(prefix):
	export_file_name = prefix + conf.EXPORT_FILE_SUFFIX
	return export_file_name

def exportContentsSlot(SITE_NAME_COPY_FROM):
	switchSite(SITE_NAME_COPY_FROM)
	goImportExportPage()
	clickThenWait('xpath', '//*[@id="bm_content_column"]/table/tbody/tr/td/table/tbody/tr/td[2]/form/table/tbody/tr/td/table[20]/tbody/tr/td[2]/table/tbody/tr/td[2]/button', 1)
	export_file_name = getExportFileName("ContentsSlot")
	doTextInput('name', "SlotExportForm_ExportFile", export_file_name, 1)
	clickThenWait('name', 'Export', 5)

def importContentsSlot(SITE_NAME):
	switchSite(SITE_NAME)
	#マーチャントツールを開く
	goImportExportPage()
	clickThenWait('xpath', '//*[@id="bm_content_column"]/table/tbody/tr/td/table/tbody/tr/td[2]/form/table/tbody/tr/td/table[20]/tbody/tr/td[2]/table/tbody/tr/td[1]/button', 2)
	import_filename = getExportFileName("ContentsSlot")
	INPUT_XPATH = '''//*[@value="''' + import_filename + '''.xml"]'''
	driver.find_element_by_xpath(INPUT_XPATH).click()
	driver.find_element_by_name('ValidateFile').click()
	time.sleep(20)
	driver.find_element_by_name('SelectMode').click()
	time.sleep(2)
	driver.find_element_by_name('Import').click()
	time.sleep(20)

#Unfinished
def applyContentsLibrary(SITE_NAME):
	switchSite(SITE_NAME)
	goContentsLibraryPage()
	clickThenWait('text', 'RefArchSharedLibrary', 2)
	clickThenWait('name', 'add', 2)
	print('手動：適用するサイトを選択してください。')
	time.sleep(10)
	#★選択する必要あり。

#Unfinished
def applyCatalog(SITE_NAME, catalog_name):
	switchSite(SITE_NAME)
	goCatalogPage()
	clickThenWait("text", catalog_name, 2)
	clickThenWait("name", "edit", 2)
	clickThenWait("text", "サイトの割り当て", 2)
	print('手動：適用するサイトを選択してください。')
	time.sleep(10)
	#★選択する必要あり。

#Unfinished
def applyPricebook(SITE_NAME, pricebook_name):
	switchSite(SITE_NAME)
	goPricebookPage()
	doTextInput('name', 'SearchTerm', pricebook_name, 1)
	clickThenWait("name", "simpleSearch", 3)
	clickThenWait("text", pricebook_name, 2)
	clickThenWait("text", "サイトの割り当て", 2)
	print('手動：適用するサイトを選択してください。')
	time.sleep(10)
	#★選択する必要あり。

def applyInvestory(SITE_NAME, investory_name):
	switchSite(SITE_NAME)
	goInvestoryPage()
	clickThenWait("text", investory_name, 2)
	clickThenWait("text", "サイトの割り当て", 2)
	print('手動：適用するサイトを選択してください。')
	time.sleep(10)
	#★選択する必要あり。

def createSearchIndex(SITE_NAME):
	switchSite(SITE_NAME)
	goSearchIndexPage()
	clickThenWait("name", "GlobalGroup", 1)
	clickThenWait("xpath", '//*[@id="bm_content_column"]/table/tbody/tr/td/table/tbody/tr/td[2]/form/table/tbody/tr[8]/td[1]/input', 1)
	clickThenWait("name","index",3)
	print('サイトの検索インデックス作成を開始しました')

def addSiteLangSetting(SITE_NAME):
	switchSite(SITE_NAME)
	goRegionInfoPage()
	clickThenWait("name", "AllowedLocale_ja_JP", 1)
	#TODO デフォルトにもチェックを入れる
	clickThenWait("xpath", '//*[@id="bm_content_column"]/table/tbody/tr/td/table/tbody/tr/td[2]/table[1]/tbody/tr[16]/td[4]/input', 1)
	clickThenWait("name", "update", 1)
	print('サイトの言語設定プロセスが完了しました')

def exportOrderRelatedInfo(TARGET,SITE_NAME_COPY_FROM):
	switchSite(SITE_NAME_COPY_FROM)
	goOrderImportExportPage()
	if TARGET == 'TAX':
		clickThenWait('name', 'TaxationExport', 1)
		export_file_name = getExportFileName(TARGET)
		doTextInput('name', "TaxTableExportForm_ExportFile", export_file_name, 1)
	if TARGET == 'SHIPPING':
		clickThenWait('name', 'ShippingMethodExport', 1)
		clickThenWait('name', 'SelectConfiguration', 1)
		export_file_name = getExportFileName(TARGET)
		doTextInput('name', "ShippingMethodExportForm_ExportFile", export_file_name, 1)
	if TARGET == 'PAYMENT':	
		clickThenWait('name', 'PaymentMethodExport', 1)
		export_file_name = getExportFileName(TARGET)
		doTextInput('name', "PaymentMethodExportForm_ExportFile", export_file_name, 1)
	clickThenWait('name', 'Export', 5)
	print(TARGET + 'のエクスポートが完了しました')

def importOrderRelatedInfo(TARGET,SITE_NAME):
	switchSite(SITE_NAME)
	goOrderImportExportPage()
	if TARGET == 'TAX':
		clickThenWait('name', 'TaxationImport', 2)
	if TARGET == 'SHIPPING':
		clickThenWait('name', 'ShippingMethodImport', 2)
	if TARGET == 'PAYMENT':	
		clickThenWait('name', 'PaymentMethodImport', 2)
	import_filename = getExportFileName(TARGET)
	INPUT_XPATH = '''//*[@value="''' + import_filename + '''.xml"]'''
	driver.find_element_by_xpath(INPUT_XPATH).click()
	clickThenWait('name', 'ValidateFile', 20)
	clickThenWait('name', 'SelectMode', 20)
	clickThenWait('name', 'Import', 20)
	print(TARGET + 'のインポートが完了しました')

def createSiteFacade():
	doLogin(myconf.SITE_HOME_URL, myconf.SITE_LOGIN_ID, myconf.SITE_LOGIN_PW)
	createNewSite(conf.SITE_ID, conf.SITE_NAME,conf.CARTRIDGE_PATH)
	print('要手動プロセス開始')
	applyContentsLibrary(conf.SITE_NAME)
	applyCatalog(conf.SITE_NAME, "storefront-catalog-m-non-en")
	applyPricebook(conf.SITE_NAME, "jpy-m-list-prices")
	applyPricebook(conf.SITE_NAME, "jpy-m-sale-prices")
	applyInvestory(conf.SITE_NAME, "inventory_m")
	print('要手動プロセス完了')
	exportContentsSlot(conf.SITE_NAME_COPY_FROM)
	importContentsSlot(conf.SITE_NAME)
	exportOrderRelatedInfo('TAX',conf.SITE_NAME_COPY_FROM)
	importOrderRelatedInfo('TAX',conf.SITE_NAME)
	exportOrderRelatedInfo('SHIPPING',conf.SITE_NAME_COPY_FROM)
	importOrderRelatedInfo('SHIPPING',conf.SITE_NAME)
	exportOrderRelatedInfo('PAYMENT',conf.SITE_NAME_COPY_FROM)
	importOrderRelatedInfo('PAYMENT',conf.SITE_NAME)			
	addSiteLangSetting(conf.SITE_NAME)#TODO デフォルトにチェックを入れる
	createSearchIndex(conf.SITE_NAME)
	print('サイトの作成プロセスが完了しました。インデックス作成後にサイトをご覧になれます')
#Main処理
createSiteFacade()


#addSiteLangSetting(conf.SITE_NAME)#TODO デフォルトにチェックを入れる

