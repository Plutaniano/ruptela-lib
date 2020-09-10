h = 'https://track.ruptela.lt'
js = '''
	document.querySelector("#delay_hour").value = 0;
	document.querySelector("#delay_min").value = 5; 
	document.querySelector("#save_button").click();
	'''

def change_delay(driver, delay, links):
	for i in links:
		driver.get(h + i)
		driver.execute_script(js)
		try:
			driver.switch_to.alert.dismiss()
		except:
			pass
		print(i)
