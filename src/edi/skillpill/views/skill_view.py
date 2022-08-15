# -*- coding: utf-8 -*-
import random
from edi.skillpill import _
from Products.Five.browser import BrowserView
from collective.beaker.interfaces import ISession


# from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

def sizeof_fmt(num, suffix='Byte'):
    for unit in ['','k','M','G','T','P','E','Z']:
        if abs(num) < 1024.0:
            return "%3.2f %s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.2f %s%s" % (num, 'Y', suffix)

class SkillView(BrowserView):

    def get_quiz(self):
        quiz = {}
        quiz['uid'] = self.context.UID()
        quiz['frage'] = self.context.quizfrage
        antworten = []
        for i in self.context.antworten:
            antworten.append((self.context.antworten.index(i), i.get('antwort')))
        #random.shuffle(antworten)
        quiz['antworten'] = antworten
        quiz['image'] = ''
        if self.context.quizimage:
            quiz['image'] = "%s/@@images/quizimage" % self.context.absolute_url()
        return quiz

    def get_validated(self):
        validated = {}
        uid = self.context.UID()
        session = ISession(self.request)
        if uid in session:
            validated = session[uid]['validated']
        return validated

    def get_action(self):
        return self.context.absolute_url() + '/validate'

    def is_master(self):
        if self.context.text:
            if self.context.text.raw == '<!DOCTYPE html>\r\n<html>\r\n<head>\r\n</head>\r\n<body>\r\n\r\n</body>\r\n</html>':
                return False
            else:
                return True
        return False

    def getMedia(self):
        datei = {}
        if self.context.datei:
            datei = {}
            datei['url'] = "%s/@@download/datei/%s" %(self.context.absolute_url(), self.context.datei.filename)
            if self.context.datei.contentType.startswith('audio'):
                datei['contentType'] = 'audio/mpeg'
            else:
                datei['contentType'] = self.context.datei.contentType
            datei['size'] = sizeof_fmt(self.context.datei.size)
            datei['filename'] = self.context.datei.filename
        return datei

    def getEmbed(self):
        retcode = ''
        if self.context.embed:
            retcode = self.context.embed
        return retcode

    def getPoster(self):
        image = {'src':'', 'title':''}
        if self.context.titleimage:
            image['src'] = "%s/@@images/titleimage" % self.context.absolute_url()
            image['title'] = self.context.titleimage.filename
        return image

    def getTitleimage(self):
        ret = False
        if self.context.titleimage:
            ret = True
        if self.context.datei or self.context.embed:
            ret = False
        return ret

    def getAufgaben(self):
        aufgaben = []
        fc = self.context.getFolderContents()
        for entry in fc:
            if entry.portal_type == 'Aufgabe':
                aufgabe = {}
                aufgabe['url'] = entry.getURL()
                aufgabe['title'] = entry.Title
                aufgaben.append(aufgabe)
        return aufgaben
