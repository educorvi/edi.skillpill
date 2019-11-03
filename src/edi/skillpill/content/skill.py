# -*- coding: utf-8 -*-
from zope.interface import Interface
from plone.app.textfield import RichText
from collective.z3cform.datagridfield import DataGridFieldFactory
from collective.z3cform.datagridfield import DictRow
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from plone.autoform import directives
from plone.dexterity.content import Container
from plone.namedfile.field import NamedBlobImage
# from plone.namedfile import field as namedfile
from plone.supermodel import model
# from plone.supermodel.directives import fieldset
# from z3c.form.browser.radio import RadioFieldWidget
from zope import schema
from zope.interface import implementer


# from edi.skillpill import _


wertvalues = SimpleVocabulary(
    [SimpleTerm(value=u'falsch', token=u'falsch', title=u'falsch'),
     SimpleTerm(value=u'richtig', token=u'richtig', title=u'richtig')]
    )

values = [5,6,7,8,9]
successrate = SimpleVocabulary.fromValues(values)


class IAnswerOptions(model.Schema):
    antwort = schema.TextLine(title=u"Antwort")

    bewertung = schema.Choice(title=u"Bewertung",
                              vocabulary=wertvalues,
                              default='richtig',
                              required=True)


class ISkill(model.Schema):
    """ Marker interface and Dexterity Python Schema for Skill
    """

    text = RichText(
         title=u'Skill',
         description=u'Beschreibe hier alles was der Lernende wissen muss. Bei Bedarf kannst Du Bilder oder Dateien\
                       hochladen und in den Text einbinden. Schreibe so kurz und präzise wie möglich und so ausführlich\
                       wie nötig.',
         required=True
    )

    titleimage = NamedBlobImage(title = u"Titelbild für den Skill zur Anzeige in Ordnern",
                               required = False)

    quizfrage = schema.TextLine(title = u"Quizfrage zum Skill",
                                description = u"Formuliere hier eine Quizfrage zu den Inhalten des Skills",
                                required = True)

    quizimage = NamedBlobImage(title = u"Bild zur Quizfrage",
                               description = u"Wenn zur Quizfrage ein Bild angezeigt werden soll kannst Du es hier\
                               hochladen. Achte darauf, dass das Motiv klar erkennbar ist und das Bild auch für die\
                               Anzeige auf einem SmartPhone geeignet ist.",
                               required = False)

    directives.widget(antworten = DataGridFieldFactory)
    antworten = schema.List(title=u"Antwortoptionen für Quizfrage",
                            required=True,
                            min_length=4,
                            max_length=4,
                            value_type=DictRow(title=u"Optionen", schema=IAnswerOptions))

    difficulty = schema.Choice(title=u"Erfolgsrate der Quizfrage",
                               description=u"Gib hier an, wieviele von 10 Schülern nach Deiner Einschätzung die Frage richtig beantworten.\
                               Achte darauf, dass Deine Quizfrage nicht zu schwer und nicht zu leicht ist. Alles zwischen 5 und 9 Schülern ist ok.",
                               vocabulary=successrate,
                               default=8,
                               required=True)


    # url = schema.URI(
    #     title=_(u'Link'),
    #     required=False
    # )

    # fieldset('Images', fields=['logo', 'advertisement'])
    # logo = namedfile.NamedBlobImage(
    #     title=_(u'Logo'),
    #     required=False,
    # )

    # advertisement = namedfile.NamedBlobImage(
    #     title=_(u'Advertisement (Gold-sponsors and above)'),
    #     required=False,
    # )

    # directives.read_permission(notes='cmf.ManagePortal')
    # directives.write_permission(notes='cmf.ManagePortal')
    # notes = RichText(
    #     title=_(u'Secret Notes (only for site-admins)'),
    #     required=False
    # )


@implementer(ISkill)
class Skill(Container):
    """
    """
