a="Ayesha"

#to find length of string
print(len(a))


#--------upper and lower case---------
# to make the string in upper case by making a new string
print(a.upper())  #a new string is created with all uppercase oa string "a" as strings itself are immutable

# to make the string in lower case by making a new string
print(a.lower())


#------stripping------
b="Fatima@@@@@@"
print(b.rstrip("@"))
#also
c="@@@@@Ali"
print(c.rstrip("@"))    #rstrip does not remove the preceding marks


#------replacing-------
d="Umer!!!!!!!Umer"
print(d.replace("Fatima","Umer"))    #it replaces everywhere in string
print(d.replace("!",""))


#------splitting-------       #split convert the string into list based on the condition provided in split brackets
e="Ayesha Fatima Sehab"
print(e.split(" "))      #I split here using space character


#--------capitalize and title-------
blogheading="my name is ayesha fatimA"
print(blogheading.capitalize())        #use to capitalize the first letter of first word and rest will be in lower case in string
print(blogheading.title())             #use to capitalize the first letter of each word in string

#---------center------
home="Welcome Home"
print(home.center(23))
print(len(home.center(23)))

#-------count-------
name="My name is Ayesha.Ayesha is a Student of cs major."
print(name.count("Ayesha"))


#-------Find something at end-------
str1 = "Welcome to the Console !!!"
print(str1.endswith("!!!"))

str1 = "Welcome to the Console !!!"
print(str1.endswith("to", 4, 10))

#---------find/index------
str1 = "He's name is Dan. He is an honest man."
print(str1.find("ishh"))
#print(str1.index("ishh"))     #use for validation

str1 = "WelcomeToTheConsole4"
print(str1.isalnum())     #return true if entire string consists of A-Z,a-z,0-9,return false for any other character

str1 = "WelcomeToTheConsole4"
print(str1.isalpha())    #returns true only if A-Z,a-z are present