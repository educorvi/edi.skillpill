# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s edi.skillpill -t test_skill.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src edi.skillpill.testing.EDI_SKILLPILL_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot /src/edi/skillpill/tests/robot/test_skill.robot
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

Scenario: As a site administrator I can add a Skill
  Given a logged-in site administrator
    and an add Skill form
   When I type 'My Skill' into the title field
    and I submit the form
   Then a Skill with the title 'My Skill' has been created

Scenario: As a site administrator I can view a Skill
  Given a logged-in site administrator
    and a Skill 'My Skill'
   When I go to the Skill view
   Then I can see the Skill title 'My Skill'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add Skill form
  Go To  ${PLONE_URL}/++add++Skill

a Skill 'My Skill'
  Create content  type=Skill  id=my-skill  title=My Skill

# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.IBasic.title  ${title}

I submit the form
  Click Button  Save

I go to the Skill view
  Go To  ${PLONE_URL}/my-skill
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a Skill with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the Skill title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
