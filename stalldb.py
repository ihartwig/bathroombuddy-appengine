import time
import copy


class RoomConfig:
  # temp table of room and contained stalls
  rooms = []

  def __init__(self):
    """Create instance of RoomConfig table logic"""
    self.first_time_setup()

  def get_locations(self):
    """Return a flat list of known locations for all rooms"""
    locations = []
    for room in self.rooms:
      for stall in room['stalls']:
        locations.append(stall['location'])
    return locations

  def get_layout(self):
    """Returns a dict structure for stalls in rooms

    [
      {
        'name': <room name>
        'stalls':
          [
            {
              'name': <stall name>
              'location': <stall location id>
            },
            ...
          ]
      },
      ...
    ]
    """
    return copy.deepcopy(self.rooms)

  def first_time_setup(self):
    """since we don't have presistent db or config tool, fill in sample config"""
    self.rooms = [
      {
        'name': "MTV650-4 Men's",
        'stalls': [
          {
            'name': "Stall 0",
            'location': "00000001"
          },
          {
            'name': "Stall 1",
            'location': "00000002"
          },
          {
            'name': "Stall 2",
            'location': "00000003"
          }
        ]
      },
      {
        'name': "MTV650-3 Men's",
        'stalls': [
          {
            'name': "Stall 0",
            'location': "00000004"
          },
          {
            'name': "Stall 1",
            'location': "00000005"
          },
          {
            'name': "Stall 2",
            'location': "00000006"
          }
        ]
      },
      {
        'name': "MTV650-2 Men's",
        'stalls': [
          {
            'name': "Stall 0",
            'location': "00000007"
          },
          {
            'name': "Stall 1",
            'location': "00000008"
          },
          {
            'name': "Stall 2",
            'location': "00000009"
          }
        ]
      }
    ]


class StallStatus:
  # temp table of status per location
  # {
  #   <location>: {
  #     busy: <True|False>,
  #     last_update_time: <time.time timestamp>
  #   },
  #   ...
  # }
  stalls = {}
  room_config = None
  locations = None

  def __init__(self):
    """Create instance of StallStatus table logic"""
    self.room_config = RoomConfig()
    self.locations = self.room_config.get_locations()
    # since we don't have presistent db or config tool, fill in sample config
    # make empty stall record for each stall we expect
    for location in self.locations:
      self.stalls[location] = {'busy': False, 'last_update_time': time.time()}

  def get_stalls_latest(self):
    """Get latest status info stored for each stall

    Returns dict of dicts:
    {
      <location>: {
        busy: <True|False>,
        last_update_time: <int time.time timestamp>
        since_update_time: <int seconds>
      },
      ...
    }
    """
    req_time = time.time()
    # may be query with sort and unique
    stalls_latest = copy.deepcopy(self.stalls)
    # add int last update time and server computed since update time
    for location, stall in stalls_latest.iteritems():
      stall['since_update_time'] = int(req_time - stall['last_update_time'])
      stall['last_update_time'] = int(stall['last_update_time'])
    return stalls_latest 

  def update_stall(self, location, new_busy):
    """Add updated stall info to db including server update time

    Args:
    location string stall location id
    new_busy string "free" or "busy"

    Returns True on successful save"""
    if(location not in self.locations):
      return False
    if(new_busy not in ('true', 'false')):
      return False

    self.stalls[location]['busy'] = True if new_busy == 'true' else False
    self.stalls[location]['last_update_time'] = time.time()
    return True
    

class StallReview:
  # temp table of review list per location
  # as db this would be query of records for location w/ sort and count
  # {
  #   <location>: <float review_avg>,
  #   ...
  # }
  stalls = {}
  room_config = None
  locations = None

  MAX_REVIEWS = 50

  def __init__(self):
    """Create instance of StallReview table logic"""
    self.room_config = RoomConfig()
    self.locations = self.room_config.get_locations()
    # make empty list for each stall we expect to make logic easier w/o queries
    for location in self.locations:
      self.stalls[location] = []

  def get_stalls_review_avg(self):
    """Return avg of last 50 (or fewer if not available) reviews"""
    avg_for_location = {}
    for location in self.locations:
      # get reviews
      reviews_for_location = self.stalls[location][-self.MAX_REVIEWS:]
      # avg with default to 0
      if(len(reviews_for_location) == 0):
        avg_for_location[location] = 0
      else:
        avg_for_location[location] = float(sum(reviews_for_location))/len(reviews_for_location)
    return avg_for_location

  def update_stall_review(self, location, new_review):
    """Add new review to db, removing extra entries if any

    Args:
    location string stall location id
    new_review string new rating to record '1'-'5'

    Returns True on successful save
    """
    if(location not in self.locations):
      return False
    if(new_review not in [str(i) for i in range(1,6)]):
      return False

    # add new review
    self.stalls[location].append(int(new_review))
    # then trim saved reviews to max we care about
    self.stalls[location] = self.stalls[location][-self.MAX_REVIEWS:]
    return True
