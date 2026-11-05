def division_hash(k, n): 
    return k % n 
  
def mid_square_hash(k, n): 
    sq = str(k * k) 
    start =(len(sq) - 2) // 2      # start index of the middle 2 digits
    middle =int(sq[start:start+2] )
    return middle % n 
  
def folding_hash(k, n): 
    s = str(k) 
    total = 0  
    for i in range (len(s),0,-2):
        part = s [max(0,i-2):i]
        total += int (part)

  
keys = [56, 123, 456, 789, 1024] 
n = 10 
for k in keys: 
    print(f"Key {k} | Division: {division_hash(k, n)} | MidSquare: {mid_square_hash(k, n)} | Folding: {folding_hash(k, n)}")