# -*- coding: utf-8 -*-
from plone.app.multilingual.browser.interfaces import make_relation_root_path
from zope.interface import Interface
from plone.app.textfield import RichText
from collective.z3cform.datagridfield import DataGridFieldFactory
from collective.z3cform.datagridfield import DictRow
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from plone.autoform import directives
from plone.dexterity.content import Container
from plone.namedfile.field import NamedBlobImage, NamedBlobFile
from z3c.relationfield.schema import RelationChoice
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from plone.supermodel import model
from zope import schema
from zope.interface import implementer
from zope.interface import Invalid
from zope.interface import invariant

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
                              default='falsch',
                              required=True)

class ISkill(model.Schema):
    """ Marker interface and Dexterity Python Schema for Skill
    """


    bachelor = RichText(
         title=u'Bachelor-Skill - das muss der Lernende wissen',
         description=u'Beschreibe hier das unbedingt notwendige Grundwissen für den Lernenden. Dieser Text wird dem Lernenden\
                       neben der Kurzbeschreibung direkt unter dem Titelbild angezeigt. Vermeide hier das Hochladen zusätzlicher\
                       Bilder und Dateien.',
         required=False
    )
         

    text = RichText(
         title=u'Master-Skill - das könnte der Lernende wissen',
         description=u'Beschreibe hier zusätzliches Wissen für den Lernenden. Bei Bedarf kannst Du Bilder oder Dateien\
                       hochladen und in den Text einbinden. Schreibe so kurz und präzise wie möglich und so ausführlich\
                       wie nötig.',
         required=False
    )

    titleimage = NamedBlobImage(title = u"Titelbild für den Skill zur Anzeige in Ordnern",
                               required = False)

    quizfrage = schema.TextLine(title = u"Quizfrage zum Skill",
                                description = u"Formuliere hier eine Quizfrage zu den Inhalten des Skills",
                                required = True)

    directives.widget(antworten = DataGridFieldFactory)
    antworten = schema.List(title=u"Antwortoptionen für die Quizfrage (Markieren Sie eine Antwortoption als richtig).",
                            required=True,
                            min_length=4,
                            max_length=4,
                            value_type=DictRow(title=u"Optionen", schema=IAnswerOptions))

    quizimage = NamedBlobImage(title = u"Bild zur Quizfrage",
                               description = u"Wenn zur Quizfrage ein Bild angezeigt werden soll kannst Du es hier\
                               hochladen. Achte darauf, dass das Motiv klar erkennbar ist und das Bild auch für die\
                               Anzeige auf einem SmartPhone geeignet ist.",
                               required = False)

    difficulty = schema.Choice(title=u"Erfolgsrate der Quizfrage",
                               description=u"Gib hier an, wieviele von 10 Schülern nach Deiner Einschätzung die Frage richtig beantworten.\
                               Achte darauf, dass Deine Quizfrage nicht zu schwer und nicht zu leicht ist. Alles zwischen 5 und 9 Schülern ist ok.",
                               vocabulary=successrate,
                               default=8,
                               required=True)

    model.fieldset(
        'audiovideo',
        label=u"Audio/Video",
        fields=['dateiref', 'embed']
    )

    #datei = NamedBlobFile(title=u"Audio- oder Video-Datei",
    #                      description=u"Hier hast Du die Möglichkeit zum Hochladen einer Audiodatei im *.mp3 Format oder Videodatai im *.mp4 Format.\
    #                                    Das Video wird direkt auf der Startseite des Skills angezeigt. Für Videos solltest Du zusätzlich ein\
    #                                    Titelbild hochladen, das dann als Poster für das Video verwendet werden kann.",
    #                      required=False)

    dateiref = RelationChoice(
        title=u"Referenz auf Videodatei",
        description=u"Hier können Sie eine Referenz auf eine bereits vorhandene Videodatei eintragen.", 
        vocabulary='plone.app.vocabularies.Catalog',
        required=False,
    )

    directives.widget(
        "dateiref",
        RelatedItemsFieldWidget,
        pattern_options={
            "selectableTypes": ["File"],
            "basePath": make_relation_root_path,
        },
    )

    embed = schema.Text(title=u"Einbettungscode einer Videoplattform",
                        description=u"Als Alternative zur Datei kann hier der Einbettungscode einer Videoplattform\
                                    z.B. YouTube, Vimeo eingetragen werden.",
                        required=False)


    @invariant
    def antworten_invariant(data):
        success = 0
        if 'antworten' in data.__dict__:
            for i in data.antworten:
                if i['bewertung'] in ['richtig', 'success']:
                   success += 1
            if success == 0:
                raise Invalid(u'Bitte markiere eine Antwortoption als richtig.')
            if success > 1:
                raise Invalid(u'Es darf nur eine Antwortoption als richtig markiert werden.')


@implementer(ISkill)
class Skill(Container):
    """
    """
