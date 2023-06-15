import os

print(*[filename.split(".")[0] for filename in os.listdir('opinions')])