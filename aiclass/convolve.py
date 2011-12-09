from scipy import signal as sg
source = [[255, 7, 3],
         [212, 240, 4],
         [218, 216, 230]]
kernel = [[-1,1]]
before =  sg.convolve(source, kernel, "valid")
result = map(lambda x: map(lambda y: -y,x),before )
for line in result:
   print line
