from plone import api
from plone.app.textfield.value import RichTextValue

def CleanHtml(obj, event):
    success = 0
    for i in obj.antworten:
        if i['bewertung'] in ['richtig', 'success']:
            success += 1
    if success == 0:
        obj.plone_utils.addPortalMessage(u'Sie müssen mindestens eine Antwortoption als richtig kennzeichnen. Bitte bearbeiten\
                                           Sie den Skill erneut und korrigieren diese Einstellung.', 'error')
    if success > 1:
        obj.plone_utils.addPortalMessage(u'Sie haben mehr als eine Antwortoption als richtig gekennzeichnet. Bitte bearbeiten\
                                           Sie den Skill erneut und korrigieren diese Einstellung.', 'error')
