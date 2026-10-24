-e #!/usr/bin/env python3
import sys
nums = [int(x) for x in sys.stdin.read().split()]
print(sum(nums))
