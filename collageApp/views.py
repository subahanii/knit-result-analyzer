from django.shortcuts import render

from collageApp.models import Students,Marks,Carryover

from django.db import IntegrityError
from collections import defaultdict as dfd



#############################

from selenium import webdriver 
import time 
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from collections import defaultdict as dfd
from selenium.webdriver.chrome.options import Options

options = Options()
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
options.headless = True


# brower = webdriver.Chrome(executable_path ="C:\\chromedriver.exe", chrome_options=options)
# brower.get("https://govexams.com/knit/searchresult.aspx") 


#############################

# Create your views here.
def rollNoGenerator(year):
	year=str(year)

	lateral_code='8'
	course_code=['1','2','3','4','5','6']
	linear=60
	lateral=12
	def rollconvert(param):
		if param<10:k='0'+str(param)
		else:k=str(param)
		return str(k)

	roll=[]
	for h in course_code:
		for i in range(1,linear+1):roll.append(year+h+rollconvert(i))

		year=str(int(year)+1)
		for i in range(1,lateral+1):roll.append(year+lateral_code+h+rollconvert(i))
		year=str(int(year)-1)

	# print(roll)
	# rool=['16207','16208','16209','16210']
	return roll[86::]
		
def home(request):
	
		if request.method=="POST":
			rollno=request.POST.get('rollno','')
			select=Marks.objects.filter(roll=rollno)
			idx=[]
			semester_list=[]
			obtain_marks_list=[]
			total_marks_list=[]
			percent_list=[]
			date=None
			aggrigate_percent=None
			for i in select:
				date=i.dinank
				idx.append(i)
				semester_=list(map(str,i.semester.split(': ')))
				print("--->",i.semester,"||",semester_[-1])
				semester_list.append("Semester: "+semester_[-1])
				obtain_marks_list.append(i.obtain_marks)
				total_marks_list.append(i.total_marks)
				percent_list.append(i.obtain_marks*100/i.total_marks)

			print(rollno,semester_list,obtain_marks_list,percent_list)
			if sum(total_marks_list)==0:
				return render(request,'home1.html',{'flag':1,'msg':'Result not available or wrong roll number!','date':date,'aggrigate_percent':aggrigate_percent})
			
			aggrigate_percent=sum(obtain_marks_list)*100/sum(total_marks_list)
			print("Totak",aggrigate_percent)
			std_detail=Students.objects.filter(roll=rollno)
			

			return render(request,'home1.html',{'flag':1,'date':date,'std_detail':std_detail ,'aggrigate_percent':aggrigate_percent,'percent_list':percent_list,'rollno':rollno,'semester_list':semester_list,'obtain_marks_list':obtain_marks_list,'total_marks_list':total_marks_list,'allData':select})

		else:
			return render(request,'home1.html',{'flag':0})


def index(request):
	roll='178204'
	select=Marks.objects.filter(roll=roll)
	
	return render(request,'index.html',{'msg':"hi Ghulam",'data':select})


def update(request):

	
	brower = webdriver.Chrome(executable_path ="C:\\chromedriver.exe", chrome_options=options)
	brower.get("https://govexams.com/knit/searchresult.aspx") 


	brower.get("https://govexams.com/knit/searchresult.aspx") 
	year=17
	rollno=rollNoGenerator(year)
	print("====>>>",len(rollno))

	

	file1 = open("cse_student_2020.txt","w+")

	def letsdo(roll):

		brower = webdriver.Chrome(executable_path ="C:\\chromedriver.exe", chrome_options=options)
		brower.get("https://govexams.com/knit/searchresult.aspx") 

		count=0
		i=-1
		while 1:
			i+=1
			if len(roll)==i:
				break
			print("--->",roll[i])
			user=brower.find_element_by_xpath("//*[@id='txtrollno']").clear()
			user=brower.find_element_by_xpath("//*[@id='txtrollno']").send_keys(roll[i])

			brower.find_element_by_xpath("//*[@id='btnSearch']").click()
			
			
			select = Select(brower.find_element_by_id("ddlResult"))


			text=[]
			el = brower.find_element_by_id('ddlResult')
			for option in el.find_elements_by_tag_name('option'):
			    text.append(option.get_attribute("value"))

			#msg=brower.find_element_by_xpath("//*[@id='lblmsg']").text
			if len(text)==0:
					print("Invalid student id",roll[i])
					continue
			count+=1
			#st_detail=semWise(text,roll[i])
			select.select_by_value(text[1])
			brower.find_element_by_xpath("//*[@id='btnGo']").click()
			
			brower.forward()
				

	
			name = brower.find_element_by_xpath("//*[@id='lblname']").text
			fname= brower.find_element_by_xpath("//*[@id='lblfname']").text
			course = brower.find_element_by_xpath("//*[@id='lblbranch']").text
			#carryOver = brower.find_element_by_xpath("//*[@id='tblYear']/tbody/tr[3]/td[2]").text
			#if name not in detail[id]:

			execute=Students(roll=roll[i],name=name,fname=fname,course=course)
			execute.save()


				
			time.sleep(1)
			brower.back()
			brower.refresh()


	letsdo(rollno)
	
	time.sleep(1)
	brower.close()



	return render(request,'index.html')




def semWise(textt,id):

		brower = webdriver.Chrome(executable_path ="C:\\chromedriver.exe", chrome_options=options)
		brower.get("https://govexams.com/knit/searchresult.aspx") 

		detail=dfd(list)
		j=-1
		while 1:
			j+=1
			if len(textt)-1==j:
				break

				
			user=brower.find_element_by_xpath("//*[@id='txtrollno']").clear()
			user=brower.find_element_by_xpath("//*[@id='txtrollno']").send_keys(id)
			brower.find_element_by_xpath("//*[@id='btnSearch']").click()		

			select = Select(brower.find_element_by_id("ddlResult"))
			select.select_by_value(textt[j])

			brower.find_element_by_xpath("//*[@id='btnGo']").click()

			brower.forward()			

			totalMarks = brower.find_element_by_xpath("//*[@id='lbltotlmarksDisp']").text
			name = brower.find_element_by_xpath("//*[@id='lblname']").text
			semester= brower.find_element_by_xpath("//*[@id='lblsem']").text
			status = brower.find_element_by_xpath("//*[@id='tblYear']/tbody/tr[2]/td[2]").text
			carryOver1 = brower.find_element_by_xpath("//*[@id='tblYear']/tbody/tr[3]/td[2]").text
			yearOfResult = brower.find_element_by_xpath("//*[@id='lblsession']").text
			print(yearOfResult)
			yearOfResult=yearOfResult[-1:-8:-1][::-1]
			carryOver=list(map(str,carryOver1.split(',')))
			try:
				obtain_mark,total_mark=map(int,totalMarks.split(' / '))
			except:
				obtain_mark,total_mark=float(totalMarks),10.0

			semester=semester[11::]
			print()

			print("semester",semester)
			print("marks",totalMarks)
			print("obtain_mark",obtain_mark)
			print("total_mark",total_mark)
			print("status",status)
			print("yearOfResult",yearOfResult)
			
			noOfCarry=0
			if len(carryOver)-1>0:
				carry_over_status=1
				print("carryOver",carryOver,len(carryOver)-1)
				noOfCarry=len(carryOver)-1
				execute=Carryover(roll=id, subject_code=carryOver1,semester=semester,obtain_marks=obtain_mark,year_of_result=yearOfResult)
				execute.save()
			try:
				execute1=Marks(roll=id,semester=semester,year_of_result=yearOfResult,obtain_marks=obtain_mark,total_marks=total_mark,status=status,carry_over_status=noOfCarry)
				execute1.save()
			except IntegrityError as e:
				print("duplicate Exception")
		

				markss=Marks.objects.get(roll=id,semester=semester)

				markss.obtain_mark=obtain_mark
				markss.total_marks=total_mark
				markss.status=status
				markss.carry_over_status=noOfCarry
				markss.save()



					
        			

			
			

			brower.back()
			brower.refresh()
			time.sleep(1)
			#brower.close()
		return detail


	




def rollNumberWise(roll):

	brower = webdriver.Chrome(executable_path ="C:\\chromedriver.exe", chrome_options=options)
	brower.get("https://govexams.com/knit/searchresult.aspx") 

	st_detail=dfd(list)
	i=-1
	while 1:
		i+=1
		if len(roll)==i:
			break
		print("--->",roll[i])
		user=brower.find_element_by_xpath("//*[@id='txtrollno']").clear()
		user=brower.find_element_by_xpath("//*[@id='txtrollno']").send_keys(roll[i])

		brower.find_element_by_xpath("//*[@id='btnSearch']").click()
		
		
		select = Select(brower.find_element_by_id("ddlResult"))


		text=[]
		el = brower.find_element_by_id('ddlResult')
		for option in el.find_elements_by_tag_name('option'):
		    text.append(option.get_attribute("value"))
		print(text)
		if len(text)==0:
				print("Invalid student id",roll[i])
				continue
		text=text[::-1]
		print(text)
		st_detail=semWise(text,roll[i])
		#print(st_detail)
		





def marks_update(request):
	year=17
	rollNumberWise(rollNoGenerator(year))

	return render(request,'index.html')



def clearData(list_detail):
			list_detail1=[]
			for i in list_detail:
				if len(i[1])==1:
					print(i[1])
					f=1
					for j in list_detail:
					
						if (i[1] in j[1]) and len(j[1])>1:
							f=0
							break
					if f:
						list_detail1.append(i)

					
						
					
				else:
					list_detail1.append(i)

			return list(list_detail1)


def prepareFinalData(final_data,year_with_semestetr,year,allname,c=0):
	roll=[]
	obtain_marks_list=[]
	total_marks_list=[]
	if c==0:
		for i in final_data:
		
			try:
				
				print(i,final_data[i][year_with_semestetr[year]])
				obtain_marks_list.append(list(map(str,final_data[i][year_with_semestetr[year]].split('_')))[0])
				total_marks_list.append(list(map(str,final_data[i][year_with_semestetr[year]].split('_')))[1])
				roll.append(i)
			except:
				c+=1
				print("except",c)
	else:
		c=0
		for i in final_data:
		
			try:
				print(year_with_semestetr[year].split(" - ")[0],year_with_semestetr[year].split(" - ")[0])
				#print(i,final_data[i][year_with_semestetr[year]])
				obtain_marks_list.append(list(map(str,final_data[i][year_with_semestetr[year].split(" - ")[0]].split('_')))[0])
				total_marks_list.append(list(map(str,final_data[i][year_with_semestetr[year].split(" - ")[0]].split('_')))[1])
				roll.append(i)
			except:
				c+=1
				print("except2",c)


	print(roll,len(roll))
	print(obtain_marks_list,len(obtain_marks_list))
	print(total_marks_list,len(total_marks_list))
	sortList=[]
	for i in range(len(roll)):
		sortList.append([obtain_marks_list[i],total_marks_list[i],roll[i]])
	sortList.sort(reverse=True)
	print(sortList)

	roll=[]
	obtain_marks_list=[]
	total_marks_list=[]
	count1=0
	for i in sortList:
		count1+=1
		roll.append(str(count1)+'-'+allname[i[2]][:3:]+i[2])
		obtain_marks_list.append(i[0])
		total_marks_list.append(i[1])

	return roll,obtain_marks_list,c

def class_rank(request,flag=0):
	branch_list={"CSE":"B. Tech. / Computer Science and Engineering",
				"CE":"B. Tech. / Civil Engineering",
				"EL":"B. Tech. / Electronics Engineering",
				"EE":"B. Tech. / Electrical Engineering",
				"MC":"B. Tech. / Mechanical Engineering",
				"IT":"B. Tech. / Information Technology"
				}
	if flag==1:
		if request.method=="POST":
			batch=request.POST.get('batch','')
			branch=request.POST.get('branch','')
			year=int(request.POST.get('year',''))
			branch=branch_list[branch]

			year_with_semestetr=['0','1 - 2','3 - 4','5 - 6','7 - 8']
			#batch='2020'
			#branch="B. Tech. / Civil Engineering"
			#year=3
			print(batch,branch,year)
			allroll=[]
			allname=dfd(str)

			rollformat=int(batch[2::])-4
			rollformat1=rollformat+1

			select1= Students.objects.filter(course=branch) &  (Students.objects.filter(roll__startswith=str(rollformat)) | Students.objects.filter(roll__startswith=str(rollformat1)))
			for stdnt in select1:
				if stdnt.roll.startswith(str(rollformat)) and len(stdnt.roll)==5:
					allroll.append(stdnt.roll)
					allname[stdnt.roll]=stdnt.name
				if stdnt.roll.startswith(str(rollformat1)) and len(stdnt.roll)==6:
					allroll.append(stdnt.roll)
					allname[stdnt.roll]=stdnt.name


			#print(allroll,len(allroll))
			
			final_data=dfd(dfd)  #multidiamentional dict

			

			for i in allroll:
				select=Marks.objects.filter(roll=i)

				list_detail=[]
				for j in select:
					list_detail.append([j.roll,j.semester,j.obtain_marks,j.total_marks])

				print(list_detail)

				list_detail=clearData(list_detail)
				print(list_detail,'l')
				for k in list_detail:
					final_data[i][k[1]]=str(k[2])+'_'+str(k[3])

			print(final_data)
			print(len(final_data))
			if len(final_data)==0:
				return render(request,'classRank1.html',{"sem":'Result not available',"branch":branch,"batch":batch})

			sem=year_with_semestetr[year]
			if year==1:
				roll,obtain_marks_list,c=prepareFinalData(final_data,year_with_semestetr,year,allname)
				if c>40:
					roll,obtain_marks_list,c=prepareFinalData(final_data,year_with_semestetr,year,allname,c)
					if c>40:
						return render(request,'classRank1.html',{"roll_list":roll,"mark":obtain_marks_list,"sem":'Result not available',"branch":branch,"batch":batch})
				
					return render(request,'classRank.html',{"roll_list":roll,"mark":obtain_marks_list,"sem":'1',"branch":branch,"batch":batch})

				
				return render(request,'classRank.html',{"roll_list":roll,"mark":obtain_marks_list,"sem":sem,"branch":branch,"batch":batch})
			
					

			if year==2:
				roll,obtain_marks_list,c=prepareFinalData(final_data,year_with_semestetr,year,allname)
				if c>40:
					roll,obtain_marks_list,c=prepareFinalData(final_data,year_with_semestetr,year,allname,c)
					if c>40:
						return render(request,'classRank1.html',{"roll_list":roll,"mark":obtain_marks_list,"sem":'Result not available',"branch":branch,"batch":batch})
				
					return render(request,'classRank.html',{"roll_list":roll,"mark":obtain_marks_list,"sem":'3',"branch":branch,"batch":batch})

				
				return render(request,'classRank.html',{"roll_list":roll,"mark":obtain_marks_list,"sem":sem,"branch":branch,"batch":batch})
			
					

			if year==3:
				roll,obtain_marks_list,c=prepareFinalData(final_data,year_with_semestetr,year,allname)
				if c>40:
					roll,obtain_marks_list,c=prepareFinalData(final_data,year_with_semestetr,year,allname,c)
					if c>40:
						return render(request,'classRank.html',{"roll_list":roll,"mark":obtain_marks_list,"sem":'Result not available',"branch":branch})
				
					return render(request,'classRank.html',{"roll_list":roll,"mark":obtain_marks_list,"sem":'5',"branch":branch,"batch":batch})

				
				return render(request,'classRank.html',{"roll_list":roll,"mark":obtain_marks_list,"sem":sem,"branch":branch,"batch":batch})
			
					

			if year==4:
				roll,obtain_marks_list,c=prepareFinalData(final_data,year_with_semestetr,year,allname)
				if c>40:
					roll,obtain_marks_list,c=prepareFinalData(final_data,year_with_semestetr,year,allname,c)
					if c>40:
						return render(request,'classRank.html',{"roll_list":roll,"mark":obtain_marks_list,"sem":'Result not available',"branch":branch,"batch":batch})
				
					return render(request,'classRank.html',{"roll_list":roll,"mark":obtain_marks_list,"sem":'7',"branch":branch,"batch":batch})

				
				return render(request,'classRank.html',{"roll_list":roll,"mark":obtain_marks_list,"sem":sem,"branch":branch,"batch":batch})
			
					

					
			
					

	return render(request,'classRank.html')


