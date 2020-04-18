import random
import operator
import csv
import sys

import tkinter
import requests
import bs4

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot
import matplotlib.animation

import agentframework


def total_stored(agents):
  """Calculate total stored by all agents and append to stored.txt file"""
  total_stored = 0
  for a in agents:
    total_stored += a.store

  with open('output/stored.txt', 'a') as f:
    f.write( "{}\n".format( str(total_stored) ) )


def create_environment(path):
  """
  Construct the environment form a CSV-like file given in `path`.
  Return a 2D list with floats that define the environment
  """
  env = []
  with open(path, 'r') as csvfile:
    reader = csv.reader(csvfile)

    for row in reader:
      env.append( list( map(float, row) ) ) # Convert ints to floats for matplotlib

  return env


def save_environment(filename):
  """Dump current environment into a CSV file given in `filename`"""
  with open(filename, 'w') as csvfile:
    writer = csv.writer(csvfile)

    for row in environment:
      writer.writerow(map(int, row))


if __name__ == '__main__':

  # Read arguments from the Terminal
  assert len(sys.argv) >= 4, """
    To run model.py, you need to specify at least 3 integer arguments:
    number of agents, number of iterations, and neighbourhood
    """

  # Make sure arguments are integers
  try:
    num_of_agents, num_of_iterations, neighbourhood = map(int, sys.argv[1:4])
    show_visual = False if (len(sys.argv) == 5 and sys.argv[4] == 'nodisplay') else True

  except:
    print( "Could not convert arguments into integers. Aborting." )
    sys.exit()

  # Construct the environment from csv
  environment = create_environment('in.txt')

  # Read the data from the web with BeautifulSoup
  data = requests.get('http://www.geog.leeds.ac.uk/courses/computing/practicals/python/agent-framework/part9/data.html')
  soup = bs4.BeautifulSoup(data.text, 'html.parser')

  # Create a list of tuples of (y, x) coordinates
  ys = [int(y.text) for y in soup.find_all(attrs={'class': 'y'})]
  xs = [int(x.text) for x in soup.find_all(attrs={'class': 'x'})]
  coords = list( zip(ys, xs) )

  # Generate a list of agents
  agents = []
  for i in range(num_of_agents):
    y, x = coords[i] if i < len(coords) else (None, None)
    agents.append(agentframework.Agent(environment, agents, y, x))


  def single_iteration():
    """
    Update all `agents` one step forward (move-eat-share steps).
    Shuffle list of agents to avoid model artifacts.
    """
    random.shuffle(agents)

    # Process each agent (move-eat-share)
    for i in range(num_of_agents):
        agents[i].move()
        agents[i].eat()
        agents[i].share_with_neighbours(neighbourhood)


  def update(x):
    """ Runs a single iteration and updates the frame """
    single_iteration()

    # Display the new environment
    fig.clear()
    matplotlib.pyplot.imshow(environment)

    # Draw each agent on top of the new environment
    for i in range(num_of_agents):
        matplotlib.pyplot.scatter(agents[i].x, agents[i].y)


  def run():
    """ Starts the animation (called by GUI) """
    animation = matplotlib.animation.FuncAnimation(fig, update, frames=num_of_iterations, repeat=False)
    # Use canvas.draw(), not canvas.show(), to avoid
    # AttributeError: 'FigureCanvasTkAgg' object has no attribute 'show'
    canvas.draw()


  # Choose how to run the program: quietly with the output as text, or interactively
  if show_visual:

    # Build the main GUI window
    root = tkinter.Tk()
    root.wm_title("Environment Model") # Set window's title

    # Add canvas to the GUI window
    fig = matplotlib.pyplot.figure(figsize=(7, 7))
    ax = fig.add_axes([0, 0, 300, 300])

    canvas = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(fig, master=root)
    canvas._tkcanvas.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

    # Add menu
    menu = tkinter.Menu(root)
    root.config(menu=menu)
    model_menu = tkinter.Menu(menu)
    menu.add_cascade(label="Model", menu=model_menu)
    model_menu.add_command(label="Run model", command=run)

    # Wait for GUI events
    tkinter.mainloop() 

  else:
    for i in range(num_of_iterations):
      single_iteration()

    # Output the sum the environment to `output/stored.txt`
    total_stored(agents)

    # Save the resulting environment
    save_environment('output/{}-{}-{}.txt'.format(
      num_of_agents,
      num_of_iterations,
      neighbourhood)
    )