from __future__ import print_function
# ------------------------------------------------------------------------------------------------
# Copyright (c) 2016 Microsoft Corporation
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and
# associated documentation files (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge, publish, distribute,
# sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or
# substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT
# NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
# ------------------------------------------------------------------------------------------------

# Tutorial sample #1: Run simple mission

from builtins import range

import random

import MalmoPython
import os
import sys
import time

if sys.version_info[0] == 2:
    # flush print output immediately
    sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)
else:
    import functools
    print = functools.partial(print, flush=True)

# Create default Malmo objects:

agent_host = MalmoPython.AgentHost()
try:
    agent_host.parse(sys.argv)
except RuntimeError as e:
    print('ERROR:', e)
    print(agent_host.getUsage())
    exit(1)
if agent_host.receivedArgument("help"):
    print(agent_host.getUsage())
    exit(0)


missionXML='''<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
            <Mission xmlns="http://ProjectMalmo.microsoft.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
            
              <About>
                <Summary>Hello world!</Summary>
              </About>
              
              <ServerSection>
                <ServerHandlers>
                  <FlatWorldGenerator generatorString="3;7,220*1,5*3,2;3;,biome_1"/>
                  <ServerQuitFromTimeUp timeLimitMs="30000"/>
                  <ServerQuitWhenAnyAgentFinishes/>
                </ServerHandlers>
              </ServerSection>
              
              <AgentSection mode="Survival">
                <Name>MalmoTutorialBot</Name>
                <AgentStart/>
                <AgentHandlers>
                  <ObservationFromFullStats/>
                  <ContinuousMovementCommands turnSpeedDegs="180"/>
                </AgentHandlers>
              </AgentSection>
            </Mission>'''


my_mission = MalmoPython.MissionSpec(missionXML, True)
my_mission.requestVideo(640, 480)
my_mission.timeLimitInSeconds(15)

"""
    MissionRecordSpec

    @param
        @String filename -- filename to name recording as

"""


# var recordedFileName = $"./mission_data{DateTime.Now:hh mm ss}.tgz";
# var missionRecord = new MissionRecordSpec(recordedFileName);
# missionRecord.recordCommands();
# missionRecord.recordMP4(20, 400000);
# missionRecord.recordRewards();
# missionRecord.recordObservations();
# _agentHost.startMission(mission, missionRecord);

from datetime import datetime

date_time_string = datetime.now().strftime("%m-%d-%Y_%H-%M-%S")
print(date_time_string)
#file_name = "\\Users\\Jee\\CS175Project\\Malmo-0.37.0-Windows-64bit_withBoost_Python3.7 (1)\\Github\\Phoenix\\Python_Examples\\mission_records\\" + date_time_string + ".tgz"
#print(file_name)
my_mission_record = MalmoPython.MissionRecordSpec("./video/" + date_time_string + ".tgz")
my_mission_record.recordCommands()
my_mission_record.recordMP4(30, 400000)
#my_mission_record.recordMP4(MalmoPython.FrameType.COLOUR_MAP, 1, 400000, True)
my_mission_record.recordObservations()


# Attempt to start a mission:
max_retries = 3
for retry in range(max_retries):
    try:
        agent_host.startMission(my_mission, my_mission_record)
        break
    except RuntimeError as e:
        if retry == max_retries - 1:
            2
            print("Error starting mission:", e)
            exit(1)
        else:
            time.sleep(2)

# Loop until mission starts:
print("Waiting for the mission to start ", end=' ')
world_state = agent_host.getWorldState()
while not world_state.has_mission_begun:
    print(".", end="")
    time.sleep(0.1)
    world_state = agent_host.getWorldState()
    for error in world_state.errors:
        print("Error:", error.text)

print()
print("Mission running ", end=' ')

# Loop until mission ends:
while world_state.is_mission_running:
    print(".", end="")
    time.sleep(0.1)

    world_state = agent_host.getWorldState()
    for error in world_state.errors:
        print("Error:", error.text)

print()
print("Mission ended")
# Mission has ended.