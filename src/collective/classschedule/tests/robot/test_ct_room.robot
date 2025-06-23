# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s collective.classschedule -t test_room.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src collective.classschedule.testing.COLLECTIVE_CLASSSCHEDULE_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot /src/collective/classschedule/tests/robot/test_room.robot
#
# See the http://docs.plone.org for further details (search for robot
# framework).
#
# ============================================================================

*** Settings *****************************************************************

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Open test browser
Test Teardown  Close all browsers


*** Test Cases ***************************************************************

Scenario: As a site administrator I can add a Room
  Given a logged-in site administrator
    and an add Building form
   When I type 'My Room' into the title field
    and I submit the form
   Then a Room with the title 'My Room' has been created

Scenario: As a site administrator I can view a Room
  Given a logged-in site administrator
    and a Room 'My Room'
   When I go to the Room view
   Then I can see the Room title 'My Room'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add Building form
  Go To  ${PLONE_URL}/++add++Building

a Room 'My Room'
  Create content  type=Building  id=my-room  title=My Room

# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.IBasic.title  ${title}

I submit the form
  Click Button  Save

I go to the Room view
  Go To  ${PLONE_URL}/my-room
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a Room with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the Room title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
