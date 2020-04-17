import random

class Agent:
  """
  This class represents an agent in a 2D space,
  with a move() function that allows it to move 1 unit
  in a random direction.
  """

  def set_x(self, x):
    """Setter function for the x-coordinate"""
    self._x = x

  def set_y(self, y):
    """Setter function for the y-coordinate"""
    self._y = y
  
  def get_x(self):
    """Getter function for the x-coordinate"""
    return self._x

  def get_y(self):
    """Getter function for the y-coordinate"""
    return self._y


  """
  Allow x and y be accessed from outside the class.
  We do not have a delete function because both
  coordinates are necessary and should not be deleted
  """
  x = property(get_x, set_x, None, 'x coordinate')
  y = property(get_y, set_y, None, 'y coordinate')


  def __init__(self, environment, agents, y=None, x=None):
    """
    Initialise the agent with (x, y) coordinates. If coordinates
    are not passed, set (x, y) to a random location within the environment.
    
    Environment is a 2D matrix of floats, expressed
    as a list of length `env_height` of lists of length `env_width` 
    """
    self.environment = environment
    self.agents = agents
    self.env_height = len(environment)
    self.env_width = len(environment[0])
    self.store = 0

    # Make sure x and y, if defined, are within environment boundaries
    assert x is None or ( x >= 0 and y < self.env_width ), """
      x-coordinate of an agent falls outside of the environment bounds
      """
    assert y is None or ( y >= 0 and y < self.env_width ), """
      y-coordinate of an agent falls outside of the environment bounds
      """

    self._x = x if x is not None else random.randint( 0, self.env_width-1 )
    self._y = y if y is not None else random.randint( 0, self.env_height-1 )


  def move(self):
    """
    Moves the agent 1 unit in any of the four directions,
    making sure coordinates do not go beyond environment's boundaries
    """
    if random.random() < 0.5:
        self._x = (self._x + 1) % self.env_width
    else:
        self._x = (self._x - 1) % self.env_width

    if random.random() < 0.5:
        self._y = (self._y + 1) % self.env_height
    else:
        self._y = (self._y - 1) % self.env_height


  def __str__(self):
    """ Nicely formatted output when agent is converted to string """
    return "Agent's location is ({}, {}). Currently stores {}.".format(
      self.y,
      self.x,
      self.store
    )


  def eat(self):
    """
    Reduce the environment value at current position, unless the agent is full.
    If agent stores over 100 units, throw up
    (add to the environment) and skip eating at this step
    """
    # If full, throw up
    if self.store > 100:
      self.environment[self.y][self.x] += self.store
      self.store = 0

    # If not full, eat
    else:
      if self.environment[self.y][self.x] > 10:
        self.environment[self.y][self.x] -= 10
        self.store += 10 
      else: # If less than 10 left, eat whatever is left
        self.store += self.environment[self.y][self.x]
        self.environment[self.y][self.x] = 0


  def distance_between(self, agent):
    """
    Calculate Pythagoras distance between itself and
    another `agent` (passed as a parameter).
    Return distance as a double
    """
    return (((self.x - agent.x)**2) + ((self.y - agent.y)**2))**0.5


  def share_with_neighbours(self, neighbourhood):
    """
    Split the resoures with the neighbours that are located
    within `neighbourhood` distance, one by one
    """
    for agent in self.agents:
      distance = self.distance_between(agent)

      if distance <= neighbourhood:
        combined = self.store + agent.store
        self.store = combined / 2
        agent.store = combined / 2