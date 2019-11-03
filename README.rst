.. This README is meant for consumption by humans and pypi. Pypi can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide.html
   This text does not appear on pypi or github. It is a comment.

=============
edi.skillpill
=============

Skillpill is a ContentType for Plone to publish one skill for readers. Every skill should have a multiple choice question about the content.
The quiz question will be shown like mobile app "quizduell" in kind of lightning window. After answering the validated answer
will appear below the skill content.

Features
--------

- Slogan: one skill, one quiz, one pill


Examples
--------

This add-on can be seen in action at the following sites:
https://kurs.educorvi.de


Translations
------------

This product is only available in German yet.


Installation
------------

Install edi.skillpill by adding it to your buildout::

    [buildout]

    ...

    eggs =
        edi.skillpill


and then running ``bin/buildout``


Contribute
----------

- Issue Tracker: https://github.com/educorvi/edi.skillpill/issues
- Source Code: https://github.com/educorvi/edi.skillpill


Support
-------

If you are having issues, please let us know.
Please send us an email: info@educorvi.de


License
-------

The project is licensed under the GPLv2.
