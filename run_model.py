import subprocess
import random

# Runs model.py with various parameters
# defined as ranges or lists

# Agents
num_of_agents = range(1, 100, 20)

# Iterations
num_of_iterations = [10, 100]

# Neighbourhood size
neighbourhood = [5]

for a in num_of_agents:
  for i in num_of_iterations:
    for n in neighbourhood:
      subprocess.call([
        'python',
        'model.py',
        str(a),
        str(i),
        str(n),
        'nodisplay'
      ])