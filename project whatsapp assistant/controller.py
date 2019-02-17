from selenium import webdriver as wb
from selenium.common.exceptions import *
from selenium.webdriver.common.keys import Keys
import time
from urllib3.exceptions import MaxRetryError

driver=wb.Edge()
driver.get("https://web.whatsapp.com")
global message_not_served
message_not_served=0
global token
token = int(20190200)
def wait():
    try: 
        while(driver.find_element_by_xpath("//div[@class='_2NbD3']")):
            pass
    except:
        print("progressing")
        time.sleep(3)
        return
def confirm():
    global token
    t=driver.find_element_by_xpath("//div[@class='_2S1VP copyable-text selectable-text']")
    t.click()
    t.send_keys("Your Appointment with the doctor was booked successfully.")
    t.send_keys(Keys.RETURN)
    t.send_keys(Keys.RETURN)
    t.send_keys("Do visit. TOKEN NO:"+str(token))
    token+=1
    t.send_keys(Keys.RETURN)

def served_earlier():             #caller handle
    msgs=driver.find_elements_by_class_name("_3_7SH _3DFk6 message-in")
    if not msgs:
    	return True
    i=msgs[-1]
    if "Book" in i.text or "Appointment" in i.text:
        return False
    t=driver.find_element_by_xpath("//div[@class='_2S1VP copyable-text selectable-text']")
    t.click()
    time.sleep(3)
    t.send_keys("Reply_with_Book_an_appointment_or_Appointment_to_fix_an_appointment_or_'Cancled'_to_abort_booking.\n")
    t.send_keys(Keys.RETURN)
    t.send_keys(Keys.RETURN)
    wait_for_msg()

    e=driver.find_elements_by_class_name("_3_7SH _3DFk6 message-in")
    i=e[-1].text
    if "Book" in i or "Appointment" in i or "book" in i:
        return False

    t.send_keys("Appointment_Canceld")
    t.send_keys(Keys.RETURN)
    t.click()
    time.sleep(3)
    return True

def msg(person,text,name):   #caller handle
	while 1:
		try:
		    print("Sending message to the doc:-")
		    e=driver.find_element_by_xpath("//input[@title='Search or start new chat']")
		    e.send_keys(person)
		    e.send_keys(Keys.RETURN)
		    t=driver.find_element_by_xpath("//div[@class='_2S1VP copyable-text selectable-text']")
		    t.click()
		    text="whatsapp no: "+name+" "+text
		    t.send_keys(text)
		    t.send_keys(Keys.RETURN)
		    print("processed")
		    return
		except MaxRetryError as m:
		    pass

def wait_for_msg():   #caller take input, served earlier
	y=driver.find_elements_by_class_name("_3_7SH _3DFk6 message-in")# present msg sets
	t=driver.find_element_by_xpath("//div[@class='_2S1VP copyable-text selectable-text']")
	t.click()    #keep clicking to prove gesture of an arrow
	if y:
		t=y[-1].text
	else :
		t=""
	while 1:
		try:
		    while 1:
		        x=driver.find_elements_by_class_name("_3_7SH _3DFk6 message-in")#new msgs sets
		        if x:
		        	t2=x[-1].text
		        else:
		        	t2=""
		        if t!=t2:
		            break
		    print("got text",t2)
		    return
		except :
			pass

def take_input():   #caller handle
        t=driver.find_element_by_xpath("//div[@class='_2S1VP copyable-text selectable-text']")
        t.click()
        t.send_keys("reply with your name, age, sex in one msg.\n")
        t.send_keys(Keys.RETURN)
        t.send_keys("eg:-Amandeep. 25. M.")
        t.send_keys(Keys.RETURN)
        print("waiting")
        wait_for_msg()
        e=driver.find_elements_by_class_name("_3_7SH _3DFk6 message-in")
        x=e[-1].text.split("\n")[2:]
        return " ".join(x)

def handle():      #caller serve_people
    global message_not_served
    if not served_earlier():
        message_not_served=1
        print("serving")
        t=driver.find_element_by_xpath("//div[@class='_2S1VP copyable-text selectable-text']")
        t.click()
        t.send_keys("Here are the List of available doctors with us.")
        t.send_keys(Keys.RETURN)
        t.send_keys("Reply with doctor name")
        t.send_keys(Keys.RETURN)
        t.send_keys(Keys.RETURN)
        with open("peoples.txt",'r') as f:
            while 1:
                name=f.readline().strip()
                t.send_keys(name)
                t.send_keys(Keys.RETURN)
                if not name:
                    break
        time.sleep(3)
        
        wait_for_msg()
        
        print("about to book appointment")
        e=driver.find_elements_by_class_name("_3_7SH _3DFk6 message-in")
        text=""
        x=""
        try:
            x=e[-1].text.split("\n")[2]
            x=x.split(" ")[1]
            print("required doc:-",x)
            time.sleep(3)
            text=take_input()
            print("received data:-",text)
            confirm()
            name=driver.find_elements_by_class_name("_1wjpf")
            name=name[-1].text
            print("patient name:-",name)
            msg(x,text,name)
            message_not_served=0
            time.sleep(3)
        except Exception as exp:
            print(exp)
            confirm()
            name=driver.find_elements_by_class_name("_1wjpf")
            name=name[-1].text
            print("patient name:-",name)
            msg(x,text,name)
            message_not_served=0
            time.sleep(3)
    else:
        if not message_not_served:
            return
        message_not_served=0
        t=driver.find_element_by_xpath("//div[@class='_2S1VP copyable-text selectable-text']")
        t.click()

# def serve_people(): 
# 	# try:      #caller assistant
# 	    e=driver.find_elements_by_xpath("//span[@class='OUeyt']")
# 	    for i in e:
# 	        i.click()
# 	        handle()
# 	# except Exception as ex:
# 	#     print(ex.split("\n")[-1])
# 	    return assistant()

def assistant():       #to check if ther are msgs       caller main
    while 1:
        try:
            title=driver.title
            title=title.split(" ")
            if (len(title)>1):
                e=driver.find_elements_by_xpath("//span[@class='OUeyt']")
                for i in e:
                    i.click()
                    handle()
			# except Exception as ex:
			#     print(ex.split("\n")[-1])
        except (MaxRetryError,WebDriverException) as m:
            if message_not_served==1:
                t=driver.find_element_by_xpath("//div[@class='_2S1VP copyable-text selectable-text']")
                t.click()
                t.send_keys("Sorry_for_inconvenience")
                t.send_keys(Keys.RETURN)

if __name__=="__main__":
    print("starting")
    time.sleep(5)
    wait()
    print ("whatsapp ready\n\nBot ready to respond")
    assistant()
    input()