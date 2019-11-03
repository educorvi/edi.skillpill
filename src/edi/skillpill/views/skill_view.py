# -*- coding: utf-8 -*-
import random
from edi.skillpill import _
from Products.Five.browser import BrowserView


# from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class SkillView(BrowserView):

    def get_quiz(self):
        quiz = {}
        quiz['frage'] = self.context.quizfrage
        antworten = []
        for i in self.context.antworten:
            antworten.append((self.context.antworten.index(i), i.get('antwort')))
        random.shuffle(antworten)
        quiz['antworten'] = antworten
        quiz['image'] = ''
        if self.context.quizimage:
            quiz['image'] = "%s/@@images/quizimage" % self.context.absolute_url()
        return quiz

    def get_action(self):
        return self.context.absolute_url() + '/validate'
