import time
timestamp = time.strftime('%H:%M:%S')
print(timestamp)
timestamp = time.strftime('%H')
print(timestamp)
timestamp = time.strftime('%M')
print(timestamp)
timestamp = time.strftime('%S')
print(timestamp)
# https://docs.python.org/3/library/time.html#time.strftime

#-----------Exercise---------
import time

# Get the current hour as an integer (0 to 23)
current_hour = int(time.strftime('%H'))

# Determine the appropriate greeting based on the hour
if current_hour >= 5 and current_hour < 12:
    greeting = "Good morning"
elif current_hour >= 12 and current_hour < 17:
    greeting = "Good afternoon"
elif current_hour >= 17 and current_hour < 21:
    greeting = "Good evening"
else:
    greeting = "Good night"

# Print the greeting
print(f"{greeting}!")