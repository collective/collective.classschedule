# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s collective.classschedule -t test_academic_calendar.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src collective.classschedule.testing.COLLECTIVE_CLASSSCHEDULE_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot /src/collective/classschedule/tests/robot/test_academic_calendar.robot
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

Scenario: As a site administrator I can add a AcademicCalendar
  Given a logged-in site administrator
    and an add AcademicCalendar form
   When I type 'My AcademicCalendar' into the title field
    and I submit the form
   Then a AcademicCalendar with the title 'My AcademicCalendar' has been created

Scenario: As a site administrator I can view a AcademicCalendar
  Given a logged-in site administrator
    and a AcademicCalendar 'My AcademicCalendar'
   When I go to the AcademicCalendar view
   Then I can see the AcademicCalendar title 'My AcademicCalendar'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add AcademicCalendar form
  Go To  ${PLONE_URL}/++add++AcademicCalendar

a AcademicCalendar 'My AcademicCalendar'
  Create content  type=AcademicCalendar  id=my-academic_calendar  title=My AcademicCalendar

# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.IBasic.title  ${title}

I submit the form
  Click Button  Save

I go to the AcademicCalendar view
  Go To  ${PLONE_URL}/my-academic_calendar
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a AcademicCalendar with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the AcademicCalendar title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
