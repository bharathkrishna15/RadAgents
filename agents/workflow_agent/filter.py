import sys

capture = False
for line in sys.stdin:
    if "📄 Result:" in line:
        capture = True
        print(line.split("📄 Result:", 1)[1].strip())
        continue
    
    if "INFO     [agent] ✅ Task completed" in line:
        break
    
    if capture:
        print(line, end="")
