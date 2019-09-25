__all__ = ['addressProcessor']

#  (c) Kyrylo Zakharov (@Amice13), 2019
# Don't look below, you will not understand this Python code :) I don't.

from js2py.pyjs import *
# setting scope
var = Scope( JS_BUILTINS )
set_global_object(var)

# Code follows:
var.registers(['mixedCyrillicLatinPattern', 'spaceAfterPunctuationPattern', 'replaceAllCyrillicToLatin', 'latinToCyrillic', 'otherPhoneNumbersPattern', 'removeSebastopolKyivPattern', 'quoteSpacePatternEnd', 'firstLettersPattern', 'replaceApostrophes', 'quoteSpacePatternStart', 'districtPattern2', 'beforePunctuationPattern', 'removeStreetPattern2', 'removeLocalityPattern', 'zgLettersPattern', 'startSpace', 'linebreakPattern', 'placeholder', 'noSpacesAfterPunctuationPattern', 'firstLetters', 'replaceCarriages', 'postalCodePattern', 'fixStupidTitles', 'getAddress', 'noSpacesBeforePunctuationPattern', 'preprocessingStringWithPunctuation', 'replaceSpaces', 'reverseCommonRegionPattern', 'removeRegionPattern', 'replaceHyphens', 'localityTypes', 'fixApostrophes', 'localityPattern3', 'regions', 'replaceQuotes', 'removeBuilingPattern', 'districtPattern', 'removeApartmentPattern', 'regionPattern', 'addSpacesAfterPunctuation', 'replaceSpacesBeforePunctuation', 'capitalizeFirst', 'removeDistrictPattern3', 'streetPattern', 'removeExtraSpaces', 'wrongQuotePattern', 'removeSlash', 'doublePunctuationPattern', 'apostrophePattern', 'stringPreprocessing', 'numberPattern', '_geonymTypes', 'removeSpaceAfterPunctuationPattern', 'streetPattern2', 'textPreprocessing', 'russianPattern', 'preserveLinebreakPattern', 'zgLetters', 'crimeaPattern', 'districtPattern3', 'listPattern1', 'addStreetSpaces', 'translit', 'latinInCyrillicPattern', 'removeUkrainePattern', 'otherLetters', 'removeDistrictPattern', 'endSpace', 'localityPattern2', 'allLetters', 'numbersToCyrillic', 'replaceWrongQuote', 'addSpacesBeforePunctuation', 'fullPhoneNumbersPattern', 'removeExtraHyphens', 'buildingPattern', 'removeDistrictPattern2', 'reverseStreetPattern', 'spaceAfterPunctuationPattern2', 'latinPattern', 'removeStreetPattern', 'fixLists', 'spacePattern', 'commonRegionPattern', 'removeReverseDistrictPattern', 'replaceEllipsis', 'apartmentPattern', 'geonymTypes', 'replaceDoublePunctuation', 'preprocessingTextWithPunctuation', 'titleCasePattern', 'restoreLinebreakPattern', 'firstLetter', 'stupidTitlePattern', 'sixPhoneNumbersPattern', 'phonePunctuationPattern', 'replaceLinebreaks', 'commonMistakes', 'removeReverseStreetPattern', 'replaceLatinInCyrillic', 'listPattern2', 'sebastopolKyivPattern', 'removeLocalityPattern2', 'reverseDistrictPattern', 'fixApostrophePattern', 'fixCommonMistakes', 'ellipsisPattern', 'carriagePattern', 'cyrillicToLatin', 'russianToUkraine', 'toTitleCase', 'replaceAllNumbers', 'removeStartEndSpaces', 'replaceAllRussian', 'removeInBracesPattern', 'replaceApostrophePattern', 'cyrillicPattern', 'fivePhoneNumbersPattern', 'latinInCyrillicPattern2', 'buildingPattern2', 'removeCommonRegionPattern', 'replaceSmartLatin', 'localityPattern', 'multipleSpacePattern', 'hyphenPattern', 'replaceSpacesAfterPunctuation', 'removeDoubleSpaces', 'quoteSpacePatternMiddle', 'formatPhone', 'spaceBeforePunctuationPattern', 'shortPhoneNumbersPattern', 'removePostalCodePattern', '_defineProperty', 'removeGarbagePattern', 'removeLocalityPattern3', 'fixStupidTitlePattern', 'doubleSpace', 'removeBuilingPattern2', 'replaceAllLatin', 'fixApostrophePattern2'])
@Js
def PyJsHoisted__defineProperty_(obj, key, value, this, arguments, var=var):
    var = Scope({'obj':obj, 'key':key, 'value':value, 'this':this, 'arguments':arguments}, var)
    var.registers(['obj', 'value', 'key'])
    if var.get('obj').contains(var.get('key')):
        PyJs_Object_0_ = Js({'value':var.get('value'),'enumerable':Js(True),'configurable':Js(True),'writable':Js(True)})
        var.get('Object').callprop('defineProperty', var.get('obj'), var.get('key'), PyJs_Object_0_)
    else:
        var.get('obj').put(var.get('key'), var.get('value'))
    return var.get('obj')
PyJsHoisted__defineProperty_.func_name = '_defineProperty'
var.put('_defineProperty', PyJsHoisted__defineProperty_)
@Js
def PyJsHoisted_capitalizeFirst_(s, this, arguments, var=var):
    var = Scope({'s':s, 'this':this, 'arguments':arguments}, var)
    var.registers(['s'])
    @Js
    def PyJs_anonymous_1_(letter, this, arguments, var=var):
        var = Scope({'letter':letter, 'this':this, 'arguments':arguments}, var)
        var.registers(['letter'])
        return var.get('letter').callprop('toUpperCase')
    PyJs_anonymous_1_._set_name('anonymous')
    var.put('s', var.get('s').callprop('replace', var.get('firstLetter'), PyJs_anonymous_1_))
    return var.get('s')
PyJsHoisted_capitalizeFirst_.func_name = 'capitalizeFirst'
var.put('capitalizeFirst', PyJsHoisted_capitalizeFirst_)
@Js
def PyJsHoisted_replaceQuotes_(s, this, arguments, var=var):
    var = Scope({'s':s, 'this':this, 'arguments':arguments}, var)
    var.registers(['s'])
    var.put('s', var.get('s').callprop('replace', var.get('quoteSpacePatternStart'), Js('$1')))
    var.put('s', var.get('s').callprop('replace', var.get('quoteSpacePatternEnd'), Js('$1')))
    var.put('s', var.get('s').callprop('replace', var.get('quoteSpacePatternMiddle'), Js(' "')))
    return var.get('s')
PyJsHoisted_replaceQuotes_.func_name = 'replaceQuotes'
var.put('replaceQuotes', PyJsHoisted_replaceQuotes_)
@Js
def PyJsHoisted_replaceApostrophes_(s, this, arguments, var=var):
    var = Scope({'s':s, 'this':this, 'arguments':arguments}, var)
    var.registers(['s'])
    var.put('s', var.get('s').callprop('replace', var.get('apostrophePattern'), Js("'")))
    return var.get('s')
PyJsHoisted_replaceApostrophes_.func_name = 'replaceApostrophes'
var.put('replaceApostrophes', PyJsHoisted_replaceApostrophes_)
@Js
def PyJsHoisted_replaceHyphens_(s, this, arguments, var=var):
    var = Scope({'s':s, 'this':this, 'arguments':arguments}, var)
    var.registers(['s'])
    var.put('s', var.get('s').callprop('replace', var.get('hyphenPattern'), Js('-')))
    return var.get('s')
PyJsHoisted_replaceHyphens_.func_name = 'replaceHyphens'
var.put('replaceHyphens', PyJsHoisted_replaceHyphens_)
@Js
def PyJsHoisted_replaceSpaces_(s, this, arguments, var=var):
    var = Scope({'s':s, 'this':this, 'arguments':arguments}, var)
    var.registers(['s'])
    var.put('s', var.get('s').callprop('replace', var.get('spacePattern'), Js(' ')))
    var.put('s', var.get('s').callprop('replace', var.get('multipleSpacePattern'), Js(' ')))
    return var.get('s')
PyJsHoisted_replaceSpaces_.func_name = 'replaceSpaces'
var.put('replaceSpaces', PyJsHoisted_replaceSpaces_)
@Js
def PyJsHoisted_removeStartEndSpaces_(s, this, arguments, var=var):
    var = Scope({'s':s, 'this':this, 'arguments':arguments}, var)
    var.registers(['s'])
    var.put('s', var.get('s').callprop('replace', var.get('startSpace'), Js('')))
    var.put('s', var.get('s').callprop('replace', var.get('endSpace'), Js('')))
    return var.get('s')
PyJsHoisted_removeStartEndSpaces_.func_name = 'removeStartEndSpaces'
var.put('removeStartEndSpaces', PyJsHoisted_removeStartEndSpaces_)
@Js
def PyJsHoisted_removeDoubleSpaces_(s, this, arguments, var=var):
    var = Scope({'s':s, 'this':this, 'arguments':arguments}, var)
    var.registers(['s'])
    var.put('s', var.get('s').callprop('replace', var.get('doubleSpace'), Js(' ')))
    return var.get('s')
PyJsHoisted_removeDoubleSpaces_.func_name = 'removeDoubleSpaces'
var.put('removeDoubleSpaces', PyJsHoisted_removeDoubleSpaces_)
@Js
def PyJsHoisted_replaceAllLatin_(s, this, arguments, var=var):
    var = Scope({'s':s, 'this':this, 'arguments':arguments}, var)
    var.registers(['s'])
    @Js
    def PyJs_anonymous_2_(match, this, arguments, var=var):
        var = Scope({'match':match, 'this':this, 'arguments':arguments}, var)
        var.registers(['match'])
        return var.get('latinToCyrillic').get(var.get('match'))
    PyJs_anonymous_2_._set_name('anonymous')
    var.put('s', var.get('s').callprop('replace', var.get('latinPattern'), PyJs_anonymous_2_))
    return var.get('s')
PyJsHoisted_replaceAllLatin_.func_name = 'replaceAllLatin'
var.put('replaceAllLatin', PyJsHoisted_replaceAllLatin_)
@Js
def PyJsHoisted_replaceAllCyrillicToLatin_(s, this, arguments, var=var):
    var = Scope({'s':s, 'this':this, 'arguments':arguments}, var)
    var.registers(['s'])
    @Js
    def PyJs_anonymous_3_(match, this, arguments, var=var):
        var = Scope({'match':match, 'this':this, 'arguments':arguments}, var)
        var.registers(['match'])
        return var.get('cyrillicToLatin').get(var.get('match'))
    PyJs_anonymous_3_._set_name('anonymous')
    var.put('s', var.get('s').callprop('replace', var.get('cyrillicPattern'), PyJs_anonymous_3_))
    return var.get('s')
PyJsHoisted_replaceAllCyrillicToLatin_.func_name = 'replaceAllCyrillicToLatin'
var.put('replaceAllCyrillicToLatin', PyJsHoisted_replaceAllCyrillicToLatin_)
@Js
def PyJsHoisted_replaceAllRussian_(s, this, arguments, var=var):
    var = Scope({'s':s, 'this':this, 'arguments':arguments}, var)
    var.registers(['s'])
    @Js
    def PyJs_anonymous_4_(match, this, arguments, var=var):
        var = Scope({'match':match, 'this':this, 'arguments':arguments}, var)
        var.registers(['match'])
        return var.get('russianToUkraine').get(var.get('match'))
    PyJs_anonymous_4_._set_name('anonymous')
    var.put('s', var.get('s').callprop('replace', var.get('russianPattern'), PyJs_anonymous_4_))
    return var.get('s')
PyJsHoisted_replaceAllRussian_.func_name = 'replaceAllRussian'
var.put('replaceAllRussian', PyJsHoisted_replaceAllRussian_)
@Js
def PyJsHoisted_fixApostrophes_(s, this, arguments, var=var):
    var = Scope({'s':s, 'this':this, 'arguments':arguments}, var)
    var.registers(['s'])
    var.put('s', var.get('s').callprop('replace', var.get('fixApostrophePattern'), Js("'")))
    var.put('s', var.get('s').callprop('replace', var.get('fixApostrophePattern2'), Js("'")))
    return var.get('s')
PyJsHoisted_fixApostrophes_.func_name = 'fixApostrophes'
var.put('fixApostrophes', PyJsHoisted_fixApostrophes_)
@Js
def PyJsHoisted_replaceLatinInCyrillic_(s, this, arguments, var=var):
    var = Scope({'s':s, 'this':this, 'arguments':arguments}, var)
    var.registers(['s'])
    @Js
    def PyJs_anonymous_5_(match, this, arguments, var=var):
        var = Scope({'match':match, 'this':this, 'arguments':arguments}, var)
        var.registers(['match'])
        @Js
        def PyJs_anonymous_6_(letter, this, arguments, var=var):
            var = Scope({'letter':letter, 'this':this, 'arguments':arguments}, var)
            var.registers(['letter'])
            return var.get('latinToCyrillic').get(var.get('letter'))
        PyJs_anonymous_6_._set_name('anonymous')
        var.put('match', var.get('match').callprop('split', Js('')).callprop('map', PyJs_anonymous_6_).callprop('join', Js('')))
        return var.get('match')
    PyJs_anonymous_5_._set_name('anonymous')
    var.put('s', var.get('s').callprop('replace', var.get('latinInCyrillicPattern'), PyJs_anonymous_5_))
    @Js
    def PyJs_anonymous_7_(match, this, arguments, var=var):
        var = Scope({'match':match, 'this':this, 'arguments':arguments}, var)
        var.registers(['match'])
        var.put('match', var.get('replaceAllLatin')(var.get('match')))
        return var.get('match')
    PyJs_anonymous_7_._set_name('anonymous')
    var.put('s', var.get('s').callprop('replace', var.get('latinInCyrillicPattern2'), PyJs_anonymous_7_))
    return var.get('s')
PyJsHoisted_replaceLatinInCyrillic_.func_name = 'replaceLatinInCyrillic'
var.put('replaceLatinInCyrillic', PyJsHoisted_replaceLatinInCyrillic_)
@Js
def PyJsHoisted_replaceSmartLatin_(s, this, arguments, var=var):
    var = Scope({'s':s, 'this':this, 'arguments':arguments}, var)
    var.registers(['s'])
    @Js
    def PyJs_anonymous_8_(match, this, arguments, var=var):
        var = Scope({'match':match, 'this':this, 'arguments':arguments}, var)
        var.registers(['countCyrillic', 'countLatin', 'match'])
        var.put('countLatin', var.get('match').callprop('match', JsRegExp('/[a-z]/gi')))
        var.put('countCyrillic', var.get('match').callprop('match', JsRegExp("/[а-яєіїґ\\']/gi")))
        if var.get('countLatin').neg():
            return var.get('match')
        if var.get('countCyrillic').neg():
            return var.get('match')
        if (var.get('countCyrillic')>=var.get('countLatin')):
            return var.get('replaceAllLatin')(var.get('match'))
        else:
            return var.get('replaceAllCyrillicToLatin')(var.get('match'))
    PyJs_anonymous_8_._set_name('anonymous')
    var.put('s', var.get('s').callprop('replace', var.get('mixedCyrillicLatinPattern'), PyJs_anonymous_8_))
    return var.get('s')
PyJsHoisted_replaceSmartLatin_.func_name = 'replaceSmartLatin'
var.put('replaceSmartLatin', PyJsHoisted_replaceSmartLatin_)
@Js
def PyJsHoisted_replaceAllNumbers_(s, this, arguments, var=var):
    var = Scope({'s':s, 'this':this, 'arguments':arguments}, var)
    var.registers(['s'])
    @Js
    def PyJs_anonymous_9_(match, this, arguments, var=var):
        var = Scope({'match':match, 'this':this, 'arguments':arguments}, var)
        var.registers(['match'])
        return var.get('numbersToCyrillic').get(var.get('match'))
    PyJs_anonymous_9_._set_name('anonymous')
    var.put('s', var.get('s').callprop('replace', var.get('numberPattern'), PyJs_anonymous_9_))
    return var.get('s')
PyJsHoisted_replaceAllNumbers_.func_name = 'replaceAllNumbers'
var.put('replaceAllNumbers', PyJsHoisted_replaceAllNumbers_)
@Js
def PyJsHoisted_replaceCarriages_(s, this, arguments, var=var):
    var = Scope({'s':s, 'this':this, 'arguments':arguments}, var)
    var.registers(['s'])
    var.put('s', var.get('s').callprop('replace', var.get('carriagePattern'), Js('\n')))
    return var.get('s')
PyJsHoisted_replaceCarriages_.func_name = 'replaceCarriages'
var.put('replaceCarriages', PyJsHoisted_replaceCarriages_)
@Js
def PyJsHoisted_replaceLinebreaks_(s, this, arguments, var=var):
    var = Scope({'s':s, 'this':this, 'arguments':arguments}, var)
    var.registers(['s'])
    var.put('s', var.get('s').callprop('replace', var.get('preserveLinebreakPattern'), Js('~linebreak~')))
    var.put('s', var.get('s').callprop('replace', var.get('linebreakPattern'), Js(' ')))
    var.put('s', var.get('s').callprop('replace', var.get('restoreLinebreakPattern'), Js('\n\n')))
    return var.get('s')
PyJsHoisted_replaceLinebreaks_.func_name = 'replaceLinebreaks'
var.put('replaceLinebreaks', PyJsHoisted_replaceLinebreaks_)
@Js
def PyJsHoisted_replaceSpacesBeforePunctuation_(s, this, arguments, var=var):
    var = Scope({'s':s, 'this':this, 'arguments':arguments}, var)
    var.registers(['s'])
    var.put('s', var.get('s').callprop('replace', var.get('spaceBeforePunctuationPattern'), Js('$1')))
    return var.get('s')
PyJsHoisted_replaceSpacesBeforePunctuation_.func_name = 'replaceSpacesBeforePunctuation'
var.put('replaceSpacesBeforePunctuation', PyJsHoisted_replaceSpacesBeforePunctuation_)
@Js
def PyJsHoisted_addSpacesAfterPunctuation_(s, this, arguments, var=var):
    var = Scope({'s':s, 'this':this, 'arguments':arguments}, var)
    var.registers(['s'])
    var.put('s', var.get('s').callprop('replace', var.get('spaceAfterPunctuationPattern'), Js('$1 ')))
    var.put('s', var.get('s').callprop('replace', var.get('spaceAfterPunctuationPattern2'), Js('$1 ')))
    var.put('s', var.get('s').callprop('replace', var.get('removeSpaceAfterPunctuationPattern'), Js('$1$2')))
    return var.get('s')
PyJsHoisted_addSpacesAfterPunctuation_.func_name = 'addSpacesAfterPunctuation'
var.put('addSpacesAfterPunctuation', PyJsHoisted_addSpacesAfterPunctuation_)
@Js
def PyJsHoisted_replaceSpacesAfterPunctuation_(s, this, arguments, var=var):
    var = Scope({'s':s, 'this':this, 'arguments':arguments}, var)
    var.registers(['s'])
    var.put('s', var.get('s').callprop('replace', var.get('noSpacesAfterPunctuationPattern'), Js('$1')))
    return var.get('s')
PyJsHoisted_replaceSpacesAfterPunctuation_.func_name = 'replaceSpacesAfterPunctuation'
var.put('replaceSpacesAfterPunctuation', PyJsHoisted_replaceSpacesAfterPunctuation_)
@Js
def PyJsHoisted_addSpacesBeforePunctuation_(s, this, arguments, var=var):
    var = Scope({'s':s, 'this':this, 'arguments':arguments}, var)
    var.registers(['s'])
    var.put('s', var.get('s').callprop('replace', var.get('noSpacesBeforePunctuationPattern'), Js('$1 $2')))
    return var.get('s')
PyJsHoisted_addSpacesBeforePunctuation_.func_name = 'addSpacesBeforePunctuation'
var.put('addSpacesBeforePunctuation', PyJsHoisted_addSpacesBeforePunctuation_)
@Js
def PyJsHoisted_replaceEllipsis_(s, this, arguments, var=var):
    var = Scope({'s':s, 'this':this, 'arguments':arguments}, var)
    var.registers(['s'])
    var.put('s', var.get('s').callprop('replace', var.get('ellipsisPattern'), Js('...')))
    return var.get('s')
PyJsHoisted_replaceEllipsis_.func_name = 'replaceEllipsis'
var.put('replaceEllipsis', PyJsHoisted_replaceEllipsis_)
@Js
def PyJsHoisted_replaceWrongQuote_(s, this, arguments, var=var):
    var = Scope({'s':s, 'this':this, 'arguments':arguments}, var)
    var.registers(['s'])
    var.put('s', var.get('s').callprop('replace', var.get('wrongQuotePattern'), Js("$1'$2")))
    return var.get('s')
PyJsHoisted_replaceWrongQuote_.func_name = 'replaceWrongQuote'
var.put('replaceWrongQuote', PyJsHoisted_replaceWrongQuote_)
@Js
def PyJsHoisted_replaceDoublePunctuation_(s, this, arguments, var=var):
    var = Scope({'s':s, 'this':this, 'arguments':arguments}, var)
    var.registers(['s'])
    @Js
    def PyJs_anonymous_10_(match, this, arguments, var=var):
        var = Scope({'match':match, 'this':this, 'arguments':arguments}, var)
        var.registers(['match'])
        return var.get('match').get('0')
    PyJs_anonymous_10_._set_name('anonymous')
    var.put('s', var.get('s').callprop('replace', var.get('doublePunctuationPattern'), PyJs_anonymous_10_))
    return var.get('s')
PyJsHoisted_replaceDoublePunctuation_.func_name = 'replaceDoublePunctuation'
var.put('replaceDoublePunctuation', PyJsHoisted_replaceDoublePunctuation_)
@Js
def PyJsHoisted_toTitleCase_(s, this, arguments, var=var):
    var = Scope({'s':s, 'this':this, 'arguments':arguments}, var)
    var.registers(['s'])
    var.put('s', var.get('s').callprop('toLowerCase'))
    @Js
    def PyJs_anonymous_11_(match, this, arguments, var=var):
        var = Scope({'match':match, 'this':this, 'arguments':arguments}, var)
        var.registers(['match'])
        return var.get('match').callprop('toUpperCase')
    PyJs_anonymous_11_._set_name('anonymous')
    var.put('s', var.get('s').callprop('replace', var.get('titleCasePattern'), PyJs_anonymous_11_))
    return var.get('s')
PyJsHoisted_toTitleCase_.func_name = 'toTitleCase'
var.put('toTitleCase', PyJsHoisted_toTitleCase_)
@Js
def PyJsHoisted_formatPhone_(s, this, arguments, var=var):
    var = Scope({'s':s, 'this':this, 'arguments':arguments}, var)
    var.registers(['s'])
    var.put('s', var.get('s').callprop('replace', var.get('phonePunctuationPattern'), Js('')))
    while 1:
        SWITCHED = False
        CONDITION = (Js(True))
        if SWITCHED or PyJsStrictEq(CONDITION, (var.get('s').callprop('match', JsRegExp('/^0/')) and PyJsStrictEq(var.get('s').get('length'),Js(10.0)))):
            SWITCHED = True
            var.put('s', var.get('s').callprop('replace', var.get('fullPhoneNumbersPattern'), Js('($1) $2 $3 $4')))
            var.put('s', (Js('+38 ')+var.get('s')))
            break
        if SWITCHED or PyJsStrictEq(CONDITION, PyJsStrictEq(var.get('s').get('length'),Js(7.0))):
            SWITCHED = True
            var.put('s', var.get('s').callprop('replace', var.get('shortPhoneNumbersPattern'), Js('$1 $2 $3')))
            break
        if SWITCHED or PyJsStrictEq(CONDITION, (var.get('s').callprop('match', JsRegExp('/^8/')) and PyJsStrictEq(var.get('s').get('length'),Js(11.0)))):
            SWITCHED = True
            var.put('s', var.get('s').callprop('replace', JsRegExp('/^8/'), Js('')))
            var.put('s', var.get('s').callprop('replace', var.get('fullPhoneNumbersPattern'), Js('($1) $2 $3 $4')))
            var.put('s', (Js('+38 ')+var.get('s')))
            break
        if SWITCHED or PyJsStrictEq(CONDITION, (var.get('s').callprop('match', JsRegExp('/^3/')) and PyJsStrictEq(var.get('s').get('length'),Js(12.0)))):
            SWITCHED = True
            var.put('s', var.get('s').callprop('replace', JsRegExp('/^38/'), Js('')))
            var.put('s', var.get('s').callprop('replace', var.get('fullPhoneNumbersPattern'), Js('($1) $2 $3 $4')))
            var.put('s', (Js('+38 ')+var.get('s')))
            break
        if SWITCHED or PyJsStrictEq(CONDITION, (var.get('s').get('length')>=Js(11.0))):
            SWITCHED = True
            var.put('s', var.get('s').callprop('replace', var.get('otherPhoneNumbersPattern'), Js('($1) $2 $3 $4')))
            break
        if SWITCHED or PyJsStrictEq(CONDITION, PyJsStrictEq(var.get('s').get('length'),Js(8.0))):
            SWITCHED = True
            var.put('s', var.get('s').callprop('replace', var.get('fivePhoneNumbersPattern'), Js('($1) $2 $3 $4')))
            break
        if SWITCHED or PyJsStrictEq(CONDITION, PyJsStrictEq(var.get('s').get('length'),Js(9.0))):
            SWITCHED = True
            var.put('s', var.get('s').callprop('replace', var.get('sixPhoneNumbersPattern'), Js('($1) $2 $3 $4')))
            break
        if SWITCHED or PyJsStrictEq(CONDITION, PyJsStrictEq(var.get('s').get('length'),Js(6.0))):
            SWITCHED = True
            var.put('s', var.get('s').callprop('replace', var.get('sixPhoneNumbersPattern'), Js('$2 $3 $4')))
            break
        if SWITCHED or PyJsStrictEq(CONDITION, PyJsStrictEq(var.get('s').get('length'),Js(5.0))):
            SWITCHED = True
            var.put('s', var.get('s').callprop('replace', var.get('fivePhoneNumbersPattern'), Js('$2 $3 $4')))
            break
        if True:
            SWITCHED = True
            var.put('s', var.get(u"null"))
        SWITCHED = True
        break
    return var.get('s')
PyJsHoisted_formatPhone_.func_name = 'formatPhone'
var.put('formatPhone', PyJsHoisted_formatPhone_)
@Js
def PyJsHoisted_stringPreprocessing_(s, this, arguments, var=var):
    var = Scope({'s':s, 'this':this, 'arguments':arguments}, var)
    var.registers(['s'])
    var.put('s', var.get('replaceSpaces')(var.get('s')))
    var.put('s', var.get('fixApostrophes')(var.get('s')))
    var.put('s', var.get('replaceHyphens')(var.get('s')))
    var.put('s', var.get('replaceQuotes')(var.get('s')))
    var.put('s', var.get('replaceApostrophes')(var.get('s')))
    var.put('s', var.get('removeStartEndSpaces')(var.get('s')))
    var.put('s', var.get('removeDoubleSpaces')(var.get('s')))
    var.put('s', var.get('replaceEllipsis')(var.get('s')))
    return var.get('s')
PyJsHoisted_stringPreprocessing_.func_name = 'stringPreprocessing'
var.put('stringPreprocessing', PyJsHoisted_stringPreprocessing_)
@Js
def PyJsHoisted_textPreprocessing_(s, this, arguments, var=var):
    var = Scope({'s':s, 'this':this, 'arguments':arguments}, var)
    var.registers(['s'])
    var.put('s', var.get('stringPreprocessing')(var.get('s')))
    var.put('s', var.get('replaceCarriages')(var.get('s')))
    var.put('s', var.get('replaceLinebreaks')(var.get('s')))
    return var.get('s')
PyJsHoisted_textPreprocessing_.func_name = 'textPreprocessing'
var.put('textPreprocessing', PyJsHoisted_textPreprocessing_)
@Js
def PyJsHoisted_fixStupidTitles_(s, this, arguments, var=var):
    var = Scope({'s':s, 'this':this, 'arguments':arguments}, var)
    var.registers(['s'])
    @Js
    def PyJs_anonymous_12_(text, this, arguments, var=var):
        var = Scope({'text':text, 'this':this, 'arguments':arguments}, var)
        var.registers(['text'])
        return var.get('replaceLatinInCyrillic')(var.get('text').callprop('replace', var.get('spacePattern'), Js('')))
    PyJs_anonymous_12_._set_name('anonymous')
    var.put('s', var.get('s').callprop('replace', var.get('stupidTitlePattern'), PyJs_anonymous_12_))
    var.put('s', var.get('s').callprop('replace', var.get('fixStupidTitlePattern'), Js('$1 ')))
    return var.get('s')
PyJsHoisted_fixStupidTitles_.func_name = 'fixStupidTitles'
var.put('fixStupidTitles', PyJsHoisted_fixStupidTitles_)
@Js
def PyJsHoisted_preprocessingStringWithPunctuation_(s, this, arguments, var=var):
    var = Scope({'s':s, 'this':this, 'arguments':arguments}, var)
    var.registers(['s'])
    var.put('s', var.get('stringPreprocessing')(var.get('s')))
    var.put('s', var.get('replaceSpacesBeforePunctuation')(var.get('s')))
    var.put('s', var.get('addSpacesAfterPunctuation')(var.get('s')))
    var.put('s', var.get('replaceSpacesAfterPunctuation')(var.get('s')))
    var.put('s', var.get('addSpacesBeforePunctuation')(var.get('s')))
    var.put('s', var.get('replaceDoublePunctuation')(var.get('s')))
    return var.get('s')
PyJsHoisted_preprocessingStringWithPunctuation_.func_name = 'preprocessingStringWithPunctuation'
var.put('preprocessingStringWithPunctuation', PyJsHoisted_preprocessingStringWithPunctuation_)
@Js
def PyJsHoisted_preprocessingTextWithPunctuation_(s, this, arguments, var=var):
    var = Scope({'s':s, 'this':this, 'arguments':arguments}, var)
    var.registers(['s'])
    var.put('s', var.get('textPreprocessing')(var.get('s')))
    var.put('s', var.get('replaceDoublePunctuation')(var.get('s')))
    var.put('s', var.get('replaceSpacesBeforePunctuation')(var.get('s')))
    var.put('s', var.get('addSpacesAfterPunctuation')(var.get('s')))
    var.put('s', var.get('replaceSpacesAfterPunctuation')(var.get('s')))
    var.put('s', var.get('addSpacesBeforePunctuation')(var.get('s')))
    return var.get('s')
PyJsHoisted_preprocessingTextWithPunctuation_.func_name = 'preprocessingTextWithPunctuation'
var.put('preprocessingTextWithPunctuation', PyJsHoisted_preprocessingTextWithPunctuation_)
@Js
def PyJsHoisted_fixCommonMistakes_(s, this, arguments, var=var):
    var = Scope({'s':s, 'this':this, 'arguments':arguments}, var)
    var.registers(['s'])
    for PyJsTemp in var.get('commonMistakes'):
        var.put('i', PyJsTemp)
        var.put('s', var.get('s').callprop('replace', var.get('commonMistakes').get(var.get('i')), var.get('i')))
    return var.get('s')
PyJsHoisted_fixCommonMistakes_.func_name = 'fixCommonMistakes'
var.put('fixCommonMistakes', PyJsHoisted_fixCommonMistakes_)
@Js
def PyJsHoisted_fixLists_(s, this, arguments, var=var):
    var = Scope({'s':s, 'this':this, 'arguments':arguments}, var)
    var.registers(['s'])
    var.put('s', var.get('s').callprop('replace', var.get('listPattern1'), Js('')))
    var.put('s', var.get('s').callprop('replace', var.get('listPattern2'), Js('$1$2 ')))
    return var.get('s')
PyJsHoisted_fixLists_.func_name = 'fixLists'
var.put('fixLists', PyJsHoisted_fixLists_)
@Js
def PyJsHoisted_translit_(s, letterCase, this, arguments, var=var):
    var = Scope({'s':s, 'letterCase':letterCase, 'this':this, 'arguments':arguments}, var)
    var.registers(['s', 'letterCase'])
    @Js
    def PyJs_anonymous_18_(match, this, arguments, var=var):
        var = Scope({'match':match, 'this':this, 'arguments':arguments}, var)
        var.registers(['match'])
        return var.get('match').callprop('replace', Js("'"), Js(''))
    PyJs_anonymous_18_._set_name('anonymous')
    var.put('s', var.get('s').callprop('replace', var.get('replaceApostrophePattern'), PyJs_anonymous_18_))
    @Js
    def PyJs_anonymous_19_(match, this, arguments, var=var):
        var = Scope({'match':match, 'this':this, 'arguments':arguments}, var)
        var.registers(['match'])
        return var.get('zgLetters').get(var.get('match'))
    PyJs_anonymous_19_._set_name('anonymous')
    var.put('s', var.get('s').callprop('replace', var.get('zgLettersPattern'), PyJs_anonymous_19_))
    @Js
    def PyJs_anonymous_20_(match, this, arguments, var=var):
        var = Scope({'match':match, 'this':this, 'arguments':arguments}, var)
        var.registers(['match'])
        for PyJsTemp in var.get('firstLetters'):
            var.put('l', PyJsTemp)
            var.put('match', var.get('match').callprop('replace', var.get('l'), var.get('firstLetters').get(var.get('l'))))
        return var.get('match')
    PyJs_anonymous_20_._set_name('anonymous')
    var.put('s', var.get('s').callprop('replace', var.get('firstLettersPattern'), PyJs_anonymous_20_))
    @Js
    def PyJs_anonymous_21_(match, this, arguments, var=var):
        var = Scope({'match':match, 'this':this, 'arguments':arguments}, var)
        var.registers(['match'])
        return var.get('otherLetters').get(var.get('match'))
    PyJs_anonymous_21_._set_name('anonymous')
    var.put('s', var.get('s').callprop('replace', var.get('allLetters'), PyJs_anonymous_21_))
    if (var.get('letterCase') and PyJsStrictEq(var.get('letterCase'),Js('lower'))):
        var.put('s', var.get('s').callprop('toLowerCase'))
    else:
        if (var.get('letterCase') and PyJsStrictEq(var.get('letterCase'),Js('upper'))):
            var.put('s', var.get('s').callprop('toUpperCase'))
        else:
            if (var.get('letterCase') and PyJsStrictEq(var.get('letterCase'),Js('title'))):
                var.put('s', var.get('s').callprop('toTitleCase'))
    return var.get('s')
PyJsHoisted_translit_.func_name = 'translit'
var.put('translit', PyJsHoisted_translit_)
@Js
def PyJsHoisted_getAddress_(s, this, arguments, var=var):
    var = Scope({'s':s, 'this':this, 'arguments':arguments}, var)
    var.registers(['locality', 'postalCodeMatch', 'streetType', 'district', 'localityName', 'address', 'streetMatch', 'districtMatch', 'postalCode', 'streetName', 'source', 'building', 'localityType', 'apartment', 'buildingMatch', 's', 'region', 'street', 'apartmentMatch', 'localityMatch', 'regionMatch'])
    var.put('source', var.get('s'))
    var.put('s', var.get('preprocessingStringWithPunctuation')(var.get('s')))
    var.put('s', var.get('replaceAllLatin')(var.get('s')))
    var.put('s', var.get('replaceAllRussian')(var.get('s')))
    var.put('s', var.get('replaceWrongQuote')(var.get('s')))
    var.put('s', var.get('s').callprop('replace', var.get('removeExtraSpaces'), Js('-')))
    var.put('s', var.get('s').callprop('replace', var.get('removeExtraHyphens'), Js('-')))
    var.put('s', var.get('s').callprop('replace', var.get('addStreetSpaces'), Js('$1 ')))
    var.put('s', var.get('s').callprop('replace', Js('КИІВ'), Js('КИЇВ')))
    var.put('s', var.get('s').callprop('replace', var.get('removeInBracesPattern'), Js('')))
    var.put('s', var.get('s').callprop('replace', var.get('removeSlash'), Js('м.')))
    var.put('postalCodeMatch', var.get('s').callprop('match', var.get('postalCodePattern')))
    if var.get('postalCodeMatch'):
        var.put('postalCode', var.get('postalCodeMatch').get('1'))
        var.put('s', var.get('s').callprop('replace', var.get('removePostalCodePattern'), Js('')))
    var.put('regionMatch', var.get('s').callprop('match', var.get('commonRegionPattern')))
    if var.get('regionMatch'):
        var.put('region', (var.get('toTitleCase')(var.get('regionMatch').get('1'))+Js(' область')))
        if var.get('region').callprop('match', var.get('crimeaPattern')):
            var.put('region', Js('Автономна Республіка Крим'))
        var.put('s', var.get('s').callprop('replace', var.get('removeCommonRegionPattern'), Js('')))
    else:
        var.put('regionMatch', var.get('s').callprop('match', var.get('regionPattern')))
        if var.get('regionMatch'):
            if var.get('regionMatch').get('1').callprop('match', var.get('crimeaPattern')):
                var.put('region', Js('Автономна Республіка Крим'))
            else:
                if var.get('regionMatch').get('1').callprop('match', var.get('sebastopolKyivPattern')):
                    var.put('region', (Js('місто ')+var.get('toTitleCase')(var.get('regionMatch').get('1'))))
                    var.put('s', var.get('s').callprop('replace', var.get('removeSebastopolKyivPattern'), Js('')))
                else:
                    var.put('region', (var.get('toTitleCase')(var.get('regionMatch').get('1'))+Js(' область')))
            var.put('s', var.get('s').callprop('replace', var.get('removeRegionPattern'), Js('')))
    var.put('s', var.get('s').callprop('replace', var.get('reverseCommonRegionPattern'), Js('')))
    var.put('districtMatch', var.get('s').callprop('match', var.get('districtPattern')))
    if var.get('districtMatch'):
        var.put('district', (var.get('toTitleCase')(var.get('districtMatch').get('1'))+Js(' район')))
    else:
        var.put('districtMatch', var.get('s').callprop('match', var.get('reverseDistrictPattern')))
        if var.get('districtMatch'):
            var.put('district', (var.get('toTitleCase')(var.get('districtMatch').get('1'))+Js(' район')))
    var.put('s', var.get('s').callprop('replace', var.get('removeDistrictPattern'), Js('')))
    var.put('s', var.get('s').callprop('replace', var.get('removeReverseDistrictPattern'), Js('')))
    var.put('s', var.get('s').callprop('replace', var.get('removeGarbagePattern'), Js('')))
    if (var.get('region')==Js('місто Київ')):
        var.put('locality', Js('місто Київ'))
    if (var.get('region')==Js('місто Севастополь')):
        var.put('locality', Js('місто Севастополь'))
    if var.get('locality').neg():
        var.put('localityMatch', var.get('s').callprop('match', var.get('localityPattern')))
        if var.get('localityMatch'):
            var.put('localityType', var.get('localityTypes').get(var.get('localityMatch').get('1').callprop('toLowerCase')))
            var.put('localityName', var.get('toTitleCase')(var.get('localityMatch').get('2')))
            var.put('locality', ((var.get('localityType')+Js(' '))+var.get('localityName')))
    var.put('s', var.get('s').callprop('replace', var.get('removeLocalityPattern'), Js('')))
    var.put('s', var.get('s').callprop('replace', var.get('removeGarbagePattern'), Js('')))
    if (((var.get('s').get('length')>Js(1.0)) and var.get('s').callprop('match', var.get('streetPattern')).neg()) and var.get('s').callprop('match', var.get('reverseStreetPattern')).neg()):
        var.put('s', (Js('вул ')+var.get('s')))
    var.put('streetMatch', var.get('s').callprop('match', var.get('streetPattern')))
    if var.get('streetMatch'):
        var.put('streetType', var.get('geonymTypes').get(var.get('streetMatch').get('1').callprop('toLowerCase')))
        var.put('streetName', var.get('toTitleCase')(var.get('streetMatch').get('2')))
        var.put('street', ((var.get('streetType')+Js(' '))+var.get('streetName')))
    else:
        var.put('streetMatch', var.get('s').callprop('match', var.get('reverseStreetPattern')))
        if var.get('streetMatch'):
            var.put('streetType', var.get('geonymTypes').get(var.get('streetMatch').get('2').callprop('toLowerCase')))
            var.put('streetName', var.get('toTitleCase')(var.get('streetMatch').get('1')))
            var.put('street', ((var.get('streetType')+Js(' '))+var.get('streetName')))
    var.put('s', var.get('s').callprop('replace', var.get('removeStreetPattern'), Js('')))
    var.put('s', var.get('s').callprop('replace', var.get('removeReverseStreetPattern'), Js('')))
    var.put('s', var.get('s').callprop('replace', var.get('removeGarbagePattern'), Js('')))
    var.put('buildingMatch', var.get('s').callprop('match', var.get('buildingPattern')))
    if var.get('buildingMatch'):
        var.put('building', var.get('buildingMatch').get('1'))
    var.put('s', var.get('s').callprop('replace', var.get('removeBuilingPattern'), Js('')))
    var.put('s', var.get('s').callprop('replace', var.get('removeGarbagePattern'), Js('')))
    var.put('apartmentMatch', var.get('s').callprop('match', var.get('apartmentPattern')))
    if var.get('apartmentMatch'):
        var.put('apartment', var.get('apartmentMatch').get('1'))
    var.put('s', var.get('s').callprop('replace', var.get('removeApartmentPattern'), Js('')))
    var.put('s', var.get('s').callprop('replace', var.get('removeGarbagePattern'), Js('')))
    if var.get('region').neg():
        var.put('regionMatch', var.get('s').callprop('match', var.get('regionPattern')))
        if var.get('regionMatch'):
            var.put('region', (var.get('toTitleCase')(var.get('regionMatch').get('1'))+Js(' область')))
            var.put('s', var.get('s').callprop('replace', var.get('removeRegionPattern'), Js('')))
    if var.get('locality').neg():
        var.put('localityMatch', var.get('s').callprop('match', var.get('localityPattern2')))
        if var.get('localityMatch'):
            var.put('locality', (Js('місто ')+var.get('toTitleCase')(var.get('localityMatch').get('1'))))
            if var.get('localityMatch').get('2'):
                if var.get('district').neg():
                    var.put('district', (var.get('toTitleCase')(var.get('localityMatch').get('2'))+Js(' район')))
            var.put('s', var.get('s').callprop('replace', var.get('removeLocalityPattern2'), Js('')))
        else:
            var.put('localityMatch', var.get('s').callprop('match', var.get('localityPattern3')))
            if var.get('localityMatch'):
                var.put('locality', (Js('місто ')+var.get('toTitleCase')(var.get('localityMatch').get('1'))))
                var.put('s', var.get('s').callprop('replace', var.get('removeLocalityPattern3'), Js('')))
    if var.get('district').neg():
        var.put('districtMatch', var.get('s').callprop('match', var.get('districtPattern2')))
        if var.get('districtMatch'):
            var.put('district', (var.get('toTitleCase')(var.get('districtMatch').get('1'))+Js(' район')))
            var.put('s', var.get('s').callprop('replace', var.get('removeDistrictPattern2'), Js('')))
    else:
        var.put('districtMatch', var.get('s').callprop('match', var.get('districtPattern3')))
        if var.get('districtMatch'):
            var.put('district', (var.get('toTitleCase')(var.get('districtMatch').get('1'))+Js(' район')))
            var.put('s', var.get('s').callprop('replace', var.get('removeDistrictPattern3'), Js('')))
    var.put('s', var.get('s').callprop('replace', var.get('removeUkrainePattern'), Js('')))
    if var.get('street').neg():
        var.put('streetMatch', var.get('s').callprop('match', var.get('streetPattern2')))
        if var.get('streetMatch'):
            var.put('street', var.get('streetMatch').get('1'))
            if var.get('streetMatch').get('2').neg():
                var.put('apartment', var.get('streetMatch').get('3'))
            else:
                var.put('building', var.get('streetMatch').get('2'))
                var.put('apartment', var.get('streetMatch').get('3'))
    var.put('s', var.get('s').callprop('replace', var.get('streetPattern2'), Js('')))
    if var.get('building').neg():
        var.put('buildingMatch', var.get('s').callprop('match', var.get('buildingPattern2')))
        if var.get('buildingMatch'):
            var.put('building', var.get('buildingMatch').get('1'))
            if var.get('buildingMatch').get('2'):
                var.put('apartment', var.get('buildingMatch').get('2'))
    PyJs_Object_26_ = Js({})
    var.put('address', PyJs_Object_26_)
    var.get('address').put('source', var.get('source'))
    var.get('address').put('countryName', Js('Україна'))
    if var.get('postalCode'):
        var.get('address').put('postalCode', var.get('postalCode'))
    if var.get('region'):
        var.get('address').put('region', var.get('region').callprop('replace', JsRegExp('/\\s+/'), Js(' ')))
    if var.get('district'):
        var.get('address').put('district', var.get('district'))
    if var.get('locality'):
        var.get('address').put('locality', var.get('locality'))
    if var.get('building'):
        var.get('address').put('streetNumber', var.get('building'))
    if (var.get('street') and var.get('building')):
        var.get('address').put('streetAddress', var.get('street'))
    else:
        if var.get('street'):
            var.get('address').put('streetAddress', var.get('street'))
    if var.get('apartment'):
        var.get('address').put('apartment', var.get('apartment'))
    @Js
    def PyJs_anonymous_27_(n, this, arguments, var=var):
        var = Scope({'n':n, 'this':this, 'arguments':arguments}, var)
        var.registers(['n'])
        return (var.get('n')!=var.get('undefined'))
    PyJs_anonymous_27_._set_name('anonymous')
    var.get('address').put('fullAddress', Js([var.get('address').get('postalCode'), var.get('address').get('region'), var.get('address').get('district'), var.get('address').get('locality'), var.get('address').get('streetAddress'), var.get('address').get('streetNumber'), var.get('address').get('apartment')]).callprop('filter', PyJs_anonymous_27_).callprop('join', Js(', ')))
    return var.get('address')
PyJsHoisted_getAddress_.func_name = 'getAddress'
var.put('getAddress', PyJsHoisted_getAddress_)
Js('use strict')
pass
pass
Js('use strict')
pass
pass
pass
pass
pass
pass
pass
pass
pass
pass
pass
pass
pass
pass
pass
pass
pass
pass
pass
pass
pass
pass
pass
pass
pass
pass
pass
pass
pass
pass
pass
PyJs_Object_13_ = Js({'A':Js('А'),'B':Js('В'),'C':Js('С'),'E':Js('Е'),'H':Js('Н'),'I':Js('І'),'K':Js('К'),'M':Js('М'),'O':Js('О'),'P':Js('Р'),'T':Js('Т'),'X':Js('Х'),'a':Js('а'),'c':Js('с'),'e':Js('е'),'i':Js('і'),'o':Js('о'),'p':Js('р'),'y':Js('у'),'x':Js('х')})
var.put('latinToCyrillic', PyJs_Object_13_)
PyJs_Object_14_ = Js({'А':Js('A'),'В':Js('B'),'С':Js('C'),'Е':Js('E'),'Н':Js('H'),'І':Js('I'),'К':Js('K'),'М':Js('M'),'О':Js('O'),'Р':Js('P'),'Т':Js('T'),'Х':Js('X'),'а':Js('a'),'с':Js('c'),'е':Js('e'),'і':Js('i'),'о':Js('o'),'р':Js('p'),'у':Js('y'),'х':Js('x')})
var.put('cyrillicToLatin', PyJs_Object_14_)
PyJs_Object_15_ = Js({'Ы':Js('І'),'Ъ':Js('Ї'),'ы':Js('і'),'ъ':Js('Ї')})
var.put('russianToUkraine', PyJs_Object_15_)
PyJs_Object_16_ = Js({'0':Js('О'),'1':Js('І'),'3':Js('З'),'6':Js('б')})
var.put('numbersToCyrillic', PyJs_Object_16_)
var.put('firstLetter', JsRegExp('/^./'))
var.put('apostrophePattern', JsRegExp('/(’|‘|′|`|´)/g'))
var.put('hyphenPattern', JsRegExp('/(‒|–|—|―)/g'))
var.put('quoteSpacePatternStart', JsRegExp('/(“|„|«)\\s*/g'))
var.put('quoteSpacePatternEnd', JsRegExp('/\\s*(”|»|″)/g'))
var.put('quoteSpacePatternMiddle', JsRegExp('/(?<= )" +(?=[А-ЯЄІЇҐ])/g'))
var.put('startSpace', JsRegExp('/^[\\t\\v\\f \\u00a0\\u2000-\\u200b\\u2028-\\u2029\\u3000]+/gm'))
var.put('endSpace', JsRegExp('/[\\t\\v\\f \\u00a0\\u2000-\\u200b\\u2028-\\u2029\\u3000]+$/gm'))
var.put('doubleSpace', JsRegExp('/[\\t\\v\\f \\u00a0\\u2000-\\u200b\\u2028-\\u2029\\u3000]{2,}/g'))
var.put('latinPattern', var.get('RegExp').create(((Js('(')+var.get('Object').callprop('keys', var.get('latinToCyrillic')).callprop('join', Js('|')))+Js(')')), Js('g')))
var.put('cyrillicPattern', var.get('RegExp').create(((Js('(')+var.get('Object').callprop('keys', var.get('cyrillicToLatin')).callprop('join', Js('|')))+Js(')')), Js('g')))
var.put('latinInCyrillicPattern', var.get('RegExp').create(((Js('(')+var.get('Object').callprop('keys', var.get('latinToCyrillic')).callprop('join', Js('|')))+Js(')+(?![a-z])')), Js('g')))
var.put('latinInCyrillicPattern2', var.get('RegExp').create(((Js("[а-яєіїґ'](")+var.get('Object').callprop('keys', var.get('latinToCyrillic')).callprop('join', Js('|')))+Js(')+(?!^|[^a-z])')), Js('g')))
var.put('mixedCyrillicLatinPattern', JsRegExp('/(?:^|[^а-яєіїґ\\\'\\-a-z])(?=[^\\s"]*[a-z])(?=[^\\s]*[а-яєіїґ])[а-яєіїґ\\\'\\-a-z]+/gi'))
var.put('russianPattern', var.get('RegExp').create(((Js('(')+var.get('Object').callprop('keys', var.get('russianToUkraine')).callprop('join', Js('|')))+Js(')')), Js('g')))
var.put('numberPattern', var.get('RegExp').create(((Js('(')+var.get('Object').callprop('keys', var.get('numbersToCyrillic')).callprop('join', Js('|')))+Js(')')), Js('g')))
var.put('carriagePattern', JsRegExp('/\\r/g'))
var.put('preserveLinebreakPattern', JsRegExp('/\\n{2,}/g'))
var.put('linebreakPattern', JsRegExp('/\\n/g'))
var.put('restoreLinebreakPattern', JsRegExp('/~linebreak~/g'))
var.put('spaceBeforePunctuationPattern', JsRegExp('/\\s+([.,:;?!№#\\)\\]])/g'))
var.put('spaceAfterPunctuationPattern', JsRegExp('/([;?!])(?!\\s|\\n)/g'))
var.put('spaceAfterPunctuationPattern2', JsRegExp('/(?<=[а-я])([.,])(?!\\s|\\n|,|\\d)/g'))
var.put('removeSpaceAfterPunctuationPattern', JsRegExp('/(\\d)([.,])\\s(?=\\d)/g'))
var.put('noSpacesBeforePunctuationPattern', JsRegExp('/([^\\n ])(\\(|#|№)/g'))
var.put('noSpacesAfterPunctuationPattern', JsRegExp('/([\\[\\(])\\s+/g'))
var.put('ellipsisPattern', JsRegExp('/…/g'))
var.put('spacePattern', JsRegExp('/[\\u0020\\u00A0\\u1680\\u180E\\u2000\\u2001\\u2002\\u2003\\u2004\\u2005\\u2006\\u2007\\u2008\\u2009\\u200A\\u200B\\u202F\\u205F\\u3000\\uFEFF]/g'))
var.put('multipleSpacePattern', JsRegExp('/[\\t\\v\\f \\u00a0\\u2000-\\u200b\\u2028-\\u2029\\u3000]{2,}/g'))
var.put('titleCasePattern', JsRegExp("/([^a-zа-яєіїґ']|^)([a-zа-яєіїґ])/gi"))
var.put('wrongQuotePattern', JsRegExp('/([а-яєіїґ])"([а-яєіїґ])/gi'))
var.put('doublePunctuationPattern', JsRegExp('/(,{2,}|:{2,}|;{2,}|\\?{2,}|!{2,}|№{2,}|#{2,})/gi'))
var.put('beforePunctuationPattern', JsRegExp('/(^.+?)(?:[,;.\\/]|$)/i'))
var.put('phonePunctuationPattern', JsRegExp('/([\\(\\)\\s\\-\\+,\\.]|факс|[мбф])/g'))
var.put('fullPhoneNumbersPattern', JsRegExp('/(\\d{3})(\\d{3})(\\d{2})(\\d{2})/'))
var.put('shortPhoneNumbersPattern', JsRegExp('/(\\d{3})(\\d{2})(\\d{2})/'))
var.put('fivePhoneNumbersPattern', JsRegExp('/(\\d*)(\\d{1})(\\d{2})(\\d{2})$/'))
var.put('sixPhoneNumbersPattern', JsRegExp('/(\\d*)(\\d{2})(\\d{2})(\\d{2})$/'))
var.put('otherPhoneNumbersPattern', JsRegExp('/(\\d+)(\\d{3})(\\d{2})(\\d{2})/'))
var.put('listPattern1', JsRegExp('/^\\s+(?=\\d)/gm'))
var.put('listPattern2', JsRegExp('/^(\\d+)([\\.\\)])(?!\\s)(?=[а-яєіїґ])/gmi'))
var.put('fixApostrophePattern', JsRegExp('/(?<=[бпвмфгґкхжчшр])[\\*’‘′`´“«»″"](?=[яюєї])/g'))
var.put('fixApostrophePattern2', JsRegExp('/(?<= [БПВДМФГҐКХЖЧШРО])[\\*’‘′`´“«»″"](?=[яюєї])/g'))
pass
var.put('stupidTitlePattern', JsRegExp('/placholder/'))
var.put('fixStupidTitlePattern', JsRegExp('/(?<=\\n)(заочно?е|[иі]менем|судовий|судове|судебный|судебное|суть)/gi'))
PyJs_Object_17_ = Js({'відкласти':var.get('RegExp').create(Js('в і д к л а с т и'), Js('g')),'відмовити':var.get('RegExp').create(Js('в і д м о в и т и'), Js('g')),'відхилити':var.get('RegExp').create(Js('в і д х и л и т и'), Js('g')),'задовільнити':var.get('RegExp').create(Js('з а д о в і л ь н и т и'), Js('g')),'задоволити':var.get('RegExp').create(Js('з а д о в о л и т и'), Js('g')),'ухвалити':var.get('RegExp').create(Js('у х в а л и т и'), Js('g')),'частково':var.get('RegExp').create(Js('ч а с т к о в о'), Js('g'))})
var.put('commonMistakes', PyJs_Object_17_)
pass
PyJs_Object_22_ = Js({'Є':Js('Ye'),'Ї':Js('Yi'),'Й':Js('Y'),'Ю':Js('Yu'),'Я':Js('Ya'),'є':Js('ye'),'ї':Js('yi'),'й':Js('y'),'ю':Js('yu'),'я':Js('ya')})
var.put('firstLetters', PyJs_Object_22_)
PyJs_Object_23_ = Js({'А':Js('A'),'Б':Js('B'),'В':Js('V'),'Г':Js('H'),'Ґ':Js('G'),'Д':Js('D'),'Е':Js('E'),'Є':Js('Ie'),'Ж':Js('Zh'),'З':Js('Z'),'И':Js('Y'),'І':Js('I'),'Ї':Js('I'),'Й':Js('I'),'К':Js('K'),'Л':Js('L'),'М':Js('M'),'Н':Js('N'),'О':Js('O'),'П':Js('P'),'Р':Js('R'),'С':Js('S'),'Т':Js('T'),'У':Js('U'),'Ф':Js('F'),'Х':Js('Kh'),'Ц':Js('Ts'),'Ч':Js('Ch'),'Ш':Js('Sh'),'Щ':Js('Shch'),'Ь':Js(''),'Ъ':Js(''),'Ы':Js('Y'),'Э':Js('E'),'Ю':Js('Iu'),'Я':Js('Ia'),'а':Js('a'),'б':Js('b'),'в':Js('v'),'г':Js('h'),'ґ':Js('g'),'д':Js('d'),'е':Js('e'),'є':Js('ie'),'ж':Js('zh'),'з':Js('z'),'и':Js('y'),'і':Js('i'),'ї':Js('i'),'й':Js('i'),'к':Js('k'),'л':Js('l'),'м':Js('m'),'н':Js('n'),'о':Js('o'),'п':Js('p'),'р':Js('r'),'с':Js('s'),'т':Js('t'),'у':Js('u'),'ф':Js('f'),'х':Js('kh'),'ц':Js('ts'),'ч':Js('ch'),'ш':Js('sh'),'щ':Js('shch'),'ь':Js(''),'ъ':Js(''),'ы':Js('Y'),'э':Js('E'),'ю':Js('iu'),'я':Js('ia')})
var.put('otherLetters', PyJs_Object_23_)
PyJs_Object_24_ = Js({'Зг':Js('Zgh'),'зг':Js('zgh'),'ЗГ':Js('ZgH')})
var.put('zgLetters', PyJs_Object_24_)
var.put('firstLettersPattern', JsRegExp("/(^|[^а-яєіїґ\\']|[^а-яєіїґ\\']\\')([єїйюя])/gi"))
var.put('allLetters', JsRegExp('/[а-яєіїґ]/gi'))
var.put('zgLettersPattern', JsRegExp('/зг/gi'))
var.put('replaceApostrophePattern', JsRegExp("/[а-яєіїґ]'[а-яєіїґ]/gi"))
PyJs_Object_25_ = Js({'capitalizeFirst':var.get('capitalizeFirst'),'replaceQuotes':var.get('replaceQuotes'),'replaceApostrophes':var.get('replaceApostrophes'),'fixApostrophes':var.get('fixApostrophes'),'replaceHyphens':var.get('replaceHyphens'),'replaceSpaces':var.get('replaceSpaces'),'removeStartEndSpaces':var.get('removeStartEndSpaces'),'removeDoubleSpaces':var.get('removeDoubleSpaces'),'replaceAllLatin':var.get('replaceAllLatin'),'replaceLatinInCyrillic':var.get('replaceLatinInCyrillic'),'replaceAllCyrillicToLatin':var.get('replaceAllCyrillicToLatin'),'replaceSmartLatin':var.get('replaceSmartLatin'),'replaceCarriages':var.get('replaceCarriages'),'replaceLinebreaks':var.get('replaceLinebreaks'),'replaceSpacesBeforePunctuation':var.get('replaceSpacesBeforePunctuation'),'addSpacesAfterPunctuation':var.get('addSpacesAfterPunctuation'),'replaceSpacesAfterPunctuation':var.get('replaceSpacesAfterPunctuation'),'addSpacesBeforePunctuation':var.get('addSpacesBeforePunctuation'),'replaceEllipsis':var.get('replaceEllipsis'),'replaceAllNumbers':var.get('replaceAllNumbers'),'replaceDoublePunctuation':var.get('replaceDoublePunctuation'),'stringPreprocessing':var.get('stringPreprocessing'),'textPreprocessing':var.get('textPreprocessing'),'preprocessingStringWithPunctuation':var.get('preprocessingStringWithPunctuation'),'preprocessingTextWithPunctuation':var.get('preprocessingTextWithPunctuation'),'toTitleCase':var.get('toTitleCase'),'replaceWrongQuote':var.get('replaceWrongQuote'),'replaceAllRussian':var.get('replaceAllRussian'),'beforePunctuationPattern':var.get('beforePunctuationPattern'),'formatPhone':var.get('formatPhone'),'fixLists':var.get('fixLists'),'fixStupidTitles':var.get('fixStupidTitles'),'fixCommonMistakes':var.get('fixCommonMistakes'),'translit':var.get('translit')})
var.put('placeholder', PyJs_Object_25_)
pass
var.put('regions', Js([Js('Автономна Республіка Крим'), Js('Вінницька'), Js('Волинська'), Js('Дніпропетровська'), Js('Донецька'), Js('Житомирська'), Js('Закарпатська'), Js('Запорізька'), Js('Івано-?Франківська'), Js('Кіровоградська'), Js('Київська'), Js('Луганська'), Js('Львівська'), Js('Миколаївська'), Js('Одеська'), Js('Тернопільська'), Js('Полтавська'), Js('Рівненська'), Js('Сумська'), Js('Харківська'), Js('Чернігівська'), Js('Херсонська'), Js('Хмельницька'), Js('Черкаська'), Js('Чернівецька'), Js('Севастополь'), Js('Київ')]))
PyJs_Object_28_ = Js({'м.':Js('місто'),'місто':Js('місто'),'м':Js('місто'),'с.':Js('село'),'с':Js('село'),'с-ще':Js('селище'),'сільрада':Js('село'),'сільська рада':Js('село'),'село':Js('село'),'сел.':Js('селище'),'селище':Js('селище'),'пос.':Js('селище'),'селище міського типу':Js('селище міського типу'),'смт':Js('селище міського типу'),'смт.':Js('селище міського типу')})
var.put('localityTypes', PyJs_Object_28_)
def PyJs_LONG_30_(var=var):
    PyJs_Object_29_ = Js({'балка':Js('балка'),'бул':Js('бульвар'),'бульв':Js('бульвар'),'бульва':Js('бульвар'),'бульвар':Js('бульвар'),'б-р':Js('бульвар'),'булвар':Js('бульвар'),'бул-р':Js('бульвар'),"в'їзд":Js("в'їзд"),'вул':Js('вулиця'),'ву':Js('вулиця'),'вл.':Js('вулиця'),'вулиця':Js('вулиця'),'вулиц':Js('вулиця'),'в.':Js('вулиця'),'ж.м.':Js('житловий масив'),'ж. м. ':Js('житловий масив'),'ж/м':Js('житловий масив'),'житловий масив':Js('житловий масив'),'ж-м':Js('житловий масив'),'житломасив':Js('житловий масив'),'дорога':Js('дорога'),'квартал':Js('квартал'),'кварт':Js('квартал'),'квар':Js('квартал'),'кв':Js('квартал'),'майдан':Js('майдан'),'мкр-н':Js('мікрорайон'),'мкр':Js('мікрорайон'),'мікр.':Js('мікрорайон')})
    return PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(var.put('_geonymTypes', PyJs_Object_29_),var.get('_defineProperty')(var.get('_geonymTypes'), Js('мкр'), Js('мікрорайон'))),var.get('_defineProperty')(var.get('_geonymTypes'), Js('м-н'), Js('мікрорайон'))),var.get('_defineProperty')(var.get('_geonymTypes'), Js('мис'), Js('мис'))),var.get('_defineProperty')(var.get('_geonymTypes'), Js('мікрорайон'), Js('мікрорайон'))),var.get('_defineProperty')(var.get('_geonymTypes'), Js('наб.'), Js('набережна'))),var.get('_defineProperty')(var.get('_geonymTypes'), Js('набережна'), Js('набережна'))),var.get('_defineProperty')(var.get('_geonymTypes'), Js('острів'), Js('острів'))),var.get('_defineProperty')(var.get('_geonymTypes'), Js('о.'), Js('острів'))),var.get('_defineProperty')(var.get('_geonymTypes'), Js('пл.'), Js('площа'))),var.get('_defineProperty')(var.get('_geonymTypes'), Js('площа'), Js('площа'))),var.get('_defineProperty')(var.get('_geonymTypes'), Js('провулок'), Js('провулок'))),var.get('_defineProperty')(var.get('_geonymTypes'), Js('провул'), Js('провулок'))),var.get('_defineProperty')(var.get('_geonymTypes'), Js('пров'), Js('провулок'))),var.get('_defineProperty')(var.get('_geonymTypes'), Js('пер.'), Js('провулок'))),var.get('_defineProperty')(var.get('_geonymTypes'), Js('переулок'), Js('провулок'))),var.get('_defineProperty')(var.get('_geonymTypes'), Js('пров.'), Js('провулок'))),var.get('_defineProperty')(var.get('_geonymTypes'), Js('п-к.'), Js('провулок'))),var.get('_defineProperty')(var.get('_geonymTypes'), Js('пр.'), Js('проспект'))),var.get('_defineProperty')(var.get('_geonymTypes'), Js('прc.'), Js('проспект'))),var.get('_defineProperty')(var.get('_geonymTypes'), Js('прcп.'), Js('проспект'))),var.get('_defineProperty')(var.get('_geonymTypes'), Js('просп.'), Js('проспект'))),var.get('_defineProperty')(var.get('_geonymTypes'), Js('проспект'), Js('проспект'))),var.get('_defineProperty')(var.get('_geonymTypes'), Js('пр-т'), Js('проспект'))),var.get('_defineProperty')(var.get('_geonymTypes'), Js('пр-кт'), Js('проспект'))),var.get('_defineProperty')(var.get('_geonymTypes'), Js('прк'), Js('проспект'))),var.get('_defineProperty')(var.get('_geonymTypes'), Js('п-ст'), Js('проспект'))),var.get('_defineProperty')(var.get('_geonymTypes'), Js('п-т'), Js('проспект'))),var.get('_defineProperty')(var.get('_geonymTypes'), Js('проїзд'), Js('проїзд'))),var.get('_defineProperty')(var.get('_geonymTypes'), Js('станція'), Js('станція'))),var.get('_defineProperty')(var.get('_geonymTypes'), Js('ст.'), Js('станція'))),var.get('_defineProperty')(var.get('_geonymTypes'), Js('станц.'), Js('станція'))),var.get('_defineProperty')(var.get('_geonymTypes'), Js('тупік'), Js('тупик'))),var.get('_defineProperty')(var.get('_geonymTypes'), Js('тупик'), Js('тупик'))),var.get('_defineProperty')(var.get('_geonymTypes'), Js('туп.'), Js('тупик'))),var.get('_defineProperty')(var.get('_geonymTypes'), Js('спуск'), Js('узвіз'))),var.get('_defineProperty')(var.get('_geonymTypes'), Js('узвіз'), Js('узвіз'))),var.get('_defineProperty')(var.get('_geonymTypes'), Js('узв'), Js('узвіз'))),var.get('_defineProperty')(var.get('_geonymTypes'), Js('шосе'), Js('шосе'))),var.get('_defineProperty')(var.get('_geonymTypes'), Js('урочише'), Js('урочише'))),var.get('_defineProperty')(var.get('_geonymTypes'), Js('ш.'), Js('шосе'))),var.get('_geonymTypes'))
var.put('geonymTypes', PyJs_LONG_30_())
var.put('removeInBracesPattern', JsRegExp('/\\(.*?\\)/g'))
var.put('removeExtraSpaces', JsRegExp('/\\s*-\\s*/g'))
var.put('removeExtraHyphens', JsRegExp('/-{2,}/g'))
var.put('removeSlash', JsRegExp('/\\/м\\./gi'))
var.put('addStreetSpaces', var.get('RegExp').create(Js('(вулиця|бульвар|площа|проспект|тупик|узвіз|квартал|провулок)(?=[а-яєіїґ0-9])'), Js('gi')))
var.put('postalCodePattern', JsRegExp('/(\\d{5})(?:,\\s?|\\s)/'))
var.put('removePostalCodePattern', var.get('RegExp').create(var.get('postalCodePattern').get('source'), Js('gi')))
var.put('commonRegionPattern', JsRegExp("/(?:,\\s|^)([а-яєіїґ'\\-\\s]+)\\s?обл(?:\\.|асть)?(?:,\\s?|$)?/i"))
var.put('removeCommonRegionPattern', JsRegExp("/([а-яєіїґ'\\-]+)\\s?обл(?:\\.|[а-яєіїґ]+)?(?:,\\s?|$)?/gi"))
var.put('reverseCommonRegionPattern', JsRegExp("/обл(?:\\.|[а-яєіїґ]+)?\\s([а-яєіїґ'\\-]+)(?:,\\s|$)?/i"))
var.put('regionPattern', var.get('RegExp').create(((Js('(?:^|,s)(')+var.get('regions').callprop('join', Js('|')))+Js(')(?![а-яєіїґ])(?:,\\s|\\s|$)')), Js('i')))
var.put('removeRegionPattern', var.get('RegExp').create(var.get('regionPattern').get('source'), Js('gi')))
var.put('crimeaPattern', JsRegExp('/(Автономна\\s*Республіка\\s*Крим|АР\\s*Крим|(?<![А-ЯІЇ])АРК(?![А-ЯІЇ]))/i'))
var.put('sebastopolKyivPattern', JsRegExp('/(Севастополь|Київ)/i'))
var.put('removeSebastopolKyivPattern', JsRegExp('/м(\\.|істо)\\s?(Севастополь|Київ)(,\\s?|$)/gi'))
var.put('localityPattern', JsRegExp('/(?:(?:^|,\\s)(м\\.|місто|м|с\\.|с-ще|с|сільрада|сільська рада|село|сел\\.|селище(?:\\sміського\\sтипу)?|смт)\\.?\\s)(.+?)(?=,\\s|\\sвулиця|$)/i'))
var.put('removeLocalityPattern', var.get('RegExp').create(var.get('localityPattern').get('source'), Js('gi')))
var.put('localityPattern2', JsRegExp("/(?:,\\s|^)(?!вул)([^0-9\\.,]{4,}),\\s(?:([а-яєіїґ\\s\\-']{4,}?)|-),\\sУкраїна$/i"))
var.put('removeLocalityPattern2', var.get('RegExp').create(var.get('localityPattern2').get('source'), Js('gi')))
var.put('localityPattern3', JsRegExp('/(?:,\\s|^)(?!вул)([^0-9\\.,]{4,}),\\sУкраїна$/i'))
var.put('removeLocalityPattern3', var.get('RegExp').create(var.get('localityPattern3').get('source'), Js('gi')))
var.put('districtPattern', JsRegExp('/(?:^|,\\s)([^,]+?)\\s(?:р-н|район)\\.?(?=,|\\s|$)/i'))
var.put('removeDistrictPattern', var.get('RegExp')(var.get('districtPattern').get('source'), Js('gi')))
var.put('reverseDistrictPattern', JsRegExp('/(?:^|,\\s)(?:р-н|район)\\s([^,]+?)(?=,|$)/i'))
var.put('removeReverseDistrictPattern', var.get('RegExp').create(var.get('reverseDistrictPattern').get('source'), Js('gi')))
var.put('districtPattern2', JsRegExp('/(?:,\\s|^)(?!вул)([^0-9,]*?ий),\\sУкраїна$/i'))
var.put('removeDistrictPattern2', var.get('RegExp')(var.get('districtPattern2').get('source'), Js('gi')))
var.put('districtPattern3', JsRegExp('/(?:,\\s|^)р\\s([^0-9,]*?ий)(?=,\\s|$)/i'))
var.put('removeDistrictPattern3', var.get('RegExp')(var.get('districtPattern3').get('source'), Js('gi')))
var.put('streetPattern', var.get('RegExp').create(((Js('(?:^|,\\s)(?:.{1,4})?(')+var.get('Object').callprop('keys', var.get('geonymTypes')).callprop('join', Js('|')).callprop('replace', JsRegExp('/\\./gi'), Js('\\.')))+Js(')\\.?\\s(.{4,}?)(?=,\\s|$)')), Js('i')))
var.put('removeStreetPattern', var.get('RegExp').create(var.get('streetPattern').get('source'), Js('gi')))
var.put('reverseStreetPattern', var.get('RegExp').create(((Js('(?:^|,\\s)(.{4,}?)\\s(')+var.get('Object').callprop('keys', var.get('geonymTypes')).callprop('join', Js('|')).callprop('replace', JsRegExp('/\\./gi'), Js('\\.')))+Js(')(?=,\\s|$)')), Js('i')))
var.put('removeReverseStreetPattern', var.get('RegExp').create(var.get('reverseStreetPattern').get('source'), Js('gi')))
var.put('streetPattern2', JsRegExp('/(?:^|,\\s)([^0-9,]+)(?:(?:,\\s([^,]+))?(?:,\\s?([^,]+))|$)?/i'))
var.put('removeStreetPattern2', var.get('RegExp').create(var.get('streetPattern2').get('source'), Js('gi')))
var.put('buildingPattern', JsRegExp('/(?:^|,\\s)(?:б\\.|буд\\.|будинок|будівля)\\s(.+?)(?=,\\s|$)/i'))
var.put('removeBuilingPattern', var.get('RegExp').create(var.get('buildingPattern').get('source'), Js('gi')))
var.put('buildingPattern2', JsRegExp('/(?:^|,\\s)([0-9][^,]+)(?:,\\s?([^,]+)|$)?/i'))
var.put('removeBuilingPattern2', var.get('RegExp').create(var.get('buildingPattern2').get('source'), Js('gi')))
var.put('apartmentPattern', JsRegExp('/(?:^|,\\s)(?:кв?\\.|квартира|кімн(?:ата|\\.)|офіс|оф\\.)\\s+(.+?)(?=,|$)/i'))
var.put('removeApartmentPattern', var.get('RegExp').create(var.get('apartmentPattern').get('source'), Js('gi')))
var.put('removeGarbagePattern', JsRegExp('/^(,|\\s)+/g'))
var.put('removeUkrainePattern', JsRegExp('/(?:^|,\\s)УкраЇна/gi'))
pass


# Add lib to the module scope
addressProcessor = var.to_python()