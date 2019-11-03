# -*- coding: utf-8 -*-

from Products.Five.browser import BrowserView
from collective.beaker.interfaces import ISession


class Validate(BrowserView):

    def __call__(self):
        antworten = self.context.antworten
        uid = self.context.UID()
        yours = int(self.request.get(uid))
        success = False
        validated = []
        for i in antworten:
            index = antworten.index(i)
            i['btnclass'] = 'btn btn-secondary btn-sm btn-block'
            if i.get('bewertung') in ['richtig', 'success']:
                i['btnclass'] = 'btn btn-success btn-sm btn-block'
            if index == yours:
                i['yours'] = True
                if i.get('bewertung') in ['richtig', 'success']:
                    success = True
                else:
                    i['btnclass'] = 'btn btn-danger btn-sm btn-block'
            else:
                i['yours'] = False
            validated.append(i)
        cookie = {'success':success, 'validated':validated}
        session = ISession(self.request)
        if uid not in session:
            session[uid] = cookie
            session.save()
        url = "%s%s" % (self.context.absolute_url(), '#ergebnis')
        return self.request.response.redirect(url)
