#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import unittest

from inflex import Verb


class TestVerbs(unittest.TestCase):

    def test_is_verb(self):
        verb = Verb("fly")
        self.assertTrue(verb.is_verb())
        self.assertFalse(verb.is_noun())
        self.assertFalse(verb.is_adj())

    def test_as_regex(self):
        verb = Verb("fly")
        pattern = verb.as_regex()
        self.assertEqual(pattern, re.compile("flying|fly|flown|flies|flew", re.IGNORECASE),
                         "Check whether as_regex produces a compiled regex object correctly.")

    def test_classical(self):
        verb = Verb("fly")
        self.assertEqual(verb, verb.classical(),
                         "Check whether Verb(...) = Verb(...).classical()")

    def test_repr(self):
        verb = Verb("fly")
        self.assertEqual(f"{verb!r}", "Verb('fly')")

    def test_other_person_singular(self):
        for person, output in [(1, "am"), (2, "are"), (3, "is")]:
            for term in ["is", "am", "are"]:
                with self.subTest():
                    prediction = Verb(term).singular(person)
                    self.assertEqual(prediction, output,
                                     "Check whether singular() with a supplied person works with 'to be'.")

    def test_plural_wrong_person(self):
        with self.assertRaises(ValueError):
            Verb("fly").plural(5)
        with self.assertRaises(ValueError):
            Verb("fly").plural("hello")
        with self.assertRaises(ValueError):
            Verb("fly").plural("first")

    def test_singular_wrong_person(self):
        with self.assertRaises(ValueError):
            Verb("fly").singular(5)
        with self.assertRaises(ValueError):
            Verb("fly").singular("hello")
        with self.assertRaises(ValueError):
            Verb("fly").singular("first")

    def test_empty(self):
        verb = Verb("")
        verb.is_singular()
        verb.is_plural()
        verb.is_past()
        verb.is_pres_part()
        verb.is_past_part()
        verb.singular()
        verb.plural()
        verb.past()
        verb.pres_part()
        verb.past_part()

    def test_singular_to_singular(self):
        test_data = [('overcrops', {'overcrops'}),
                     ('peels', {'peels'}),
                     ('disencumbers', {'disencumbers'}),
                     ('chews out', {'chews out'}),
                     ('gleams', {'gleams'}),
                     ('obscures', {'obscures'}),
                     ('nibbles', {'nibbles'}),
                     ('toughens', {'toughens'}),
                     ('supervises', {'supervises'}),
                     ('sues', {'sues'}),
                     ('smuts', {'smuts'}),
                     ('succeeds', {'succeeds'}),
                     ('images', {'images'}),
                     ('shrugs', {'shrugs'}),
                     ('gauges', {'gauges'}),
                     ('debugs', {'debugs'}),
                     ('goes through', {'goes through'}),
                     ('contemplates', {'contemplates'}),
                     ('pops', {'pops'}),
                     ('abounds in', {'abounds in'}),
                     ('passes by', {'passes by'}),
                     ('subjugates', {'subjugates'}),
                     ('rains out', {'rains out'}),
                     ('shows around', {'shows around'}),
                     ('unites', {'unites'}),
                     ('acts up', {'acts up'}),
                     ('engrosses', {'engrosses'}),
                     ('fucks', {'fucks'}),
                     ('negates', {'negates'}),
                     ('recedes', {'recedes'}),
                     ('pouts', {'pouts'}),
                     ('fills out', {'fills out'}),
                     ('deals', {'deals'}),
                     ('slews', {'slews'}),
                     ('wags', {'wags'}),
                     ('resurrects', {'resurrects'}),
                     ('commandeers', {'commandeers'}),
                     ('reappears', {'reappears'}),
                     ('misguides', {'misguides'}),
                     ('environs', {'environs'}),
                     ('bevels', {'bevels'}),
                     ('abnegates', {'abnegates'}),
                     ('peddles', {'peddles'}),
                     ('canvasses', {'canvasses'}),
                     ('sets against', {'sets against'}),
                     ('whips up', {'whips up'}),
                     ('raps', {'raps'}),
                     ('manipulates', {'manipulates'}),
                     ('drones away', {'drones away'}),
                     ('accredits', {'accredits'})]
        for before, after in test_data:
            with self.subTest():
                self.assertIn(Verb(before).singular(), after,
                              f"Verb({repr(before)}).singular() => {repr(after)}")

    def test_plural_to_singular(self):
        test_data = [('transliterate', {'transliterates'}),
                     ('sour', {'sours'}),
                     ('annul', {'annuls'}),
                     ('fix', {'fixes'}),
                     ('centre', {'centres'}),
                     ('develop', {'develops'}),
                     ('admit of', {'admits of'}),
                     ('stereotype', {'stereotypes'}),
                     ('overrun', {'overruns'}),
                     ('prostrate', {'prostrates'}),
                     ('fluster', {'flusters'}),
                     ('about-face', {'about-faces'}),
                     ('receive', {'receives'}),
                     ('offend', {'offends'}),
                     ('hoot down', {'hoots down'}),
                     ('fuss over', {'fusses over'}),
                     ('come before', {'comes before'}),
                     ('bollix up', {'bollixes up'}),
                     ('balance', {'balances'}),
                     ('preheat', {'preheats'}),
                     ('whip up', {'whips up'}),
                     ('immure', {'immures'}),
                     ('roughen', {'roughens'}),
                     ('come on', {'comes on'}),
                     ('move for', {'moves for'}),
                     ('chicken out', {'chickens out'}),
                     ('crown', {'crowns'}),
                     ('slaver', {'slavers'}),
                     ('disgrace', {'disgraces'}),
                     ('fathom', {'fathoms'}),
                     ('work off', {'works off'}),
                     ('awaken', {'awakens'}),
                     ('clock off', {'clocks off'}),
                     ('steady', {'steadies'}),
                     ('court-martial', {'court-martials'}),
                     ('muffle', {'muffles'}),
                     ('prize out', {'prizes out'}),
                     ('intervene', {'intervenes'}),
                     ('brace', {'braces'}),
                     ('harden to', {'hardens to'}),
                     ('leak out', {'leaks out'}),
                     ('kick out', {'kicks out'}),
                     ('contrast', {'contrasts'}),
                     ('dehumanize', {'dehumanizes'}),
                     ('move in', {'moves in'}),
                     ('run out', {'runs out'}),
                     ('diversify', {'diversifies'}),
                     ('insist', {'insists'}),
                     ('overcharge', {'overcharges'}),
                     ('solidify', {'solidifies'})]
        for before, after in test_data:
            with self.subTest():
                self.assertIn(Verb(before).singular(), after,
                              f"Verb({repr(before)}).singular() => {repr(after)}")

    """
    past to singular is not properly supported.
    """

    """
    past participle to singular is not properly supported.
    """

    """
    present participle to singular is not properly supported.
    """

    def test_singular_to_plural(self):
        test_data = [('wages', {'wage'}),
                     ('redoubles', {'redouble'}),
                     ('participates', {'participate'}),
                     ('ululates', {'ululate'}),
                     ('vides', {'vide'}),
                     ('foams', {'foam'}),
                     ('knocks around', {'knock around'}),
                     ('works out', {'work out'}),
                     ('diverges', {'diverge'}),
                     ('limps', {'limp'}),
                     ('darts', {'dart'}),
                     ('carbonates', {'carbonate'}),
                     ('panhandles', {'panhandle'}),
                     ('dumbfounds', {'dumbfound'}),
                     ('banks', {'bank'}),
                     ('realigns', {'realign'}),
                     ('assorts', {'assort'}),
                     ('reins back', {'rein back'}),
                     ('foals', {'foal'}),
                     ('snows under', {'snow under'}),
                     ('sibilates', {'sibilate'}),
                     ('lolls', {'loll'}),
                     ('inhales', {'inhale'}),
                     ('sequesters', {'sequester'}),
                     ('pens up', {'pen up'}),
                     ('forges', {'forge'}),
                     ('constitutes', {'constitute'}),
                     ('creeps', {'creep'}),
                     ('embraces', {'embrace'}),
                     ('falls for', {'fall for'}),
                     ('blows over', {'blow over'}),
                     ('fogs', {'fog'}),
                     ('wizens', {'wizen'}),
                     ('snorts', {'snort'}),
                     ('arms', {'arm'}),
                     ('mothers', {'mother'}),
                     ('packs off', {'pack off'}),
                     ('caters to', {'cater to'}),
                     ('causes', {'cause'}),
                     ('appreciates', {'appreciate'}),
                     ('christens', {'christen'}),
                     ('looks forward to', {'look forward to'}),
                     ('personifies', {'personify'}),
                     ('colours', {'colour'}),
                     ('finishes with', {'finish with'}),
                     ('spotlights', {'spotlight'}),
                     ('strikes upon', {'strike upon'}),
                     ('involves', {'involve'}),
                     ('rains', {'rain'}),
                     ('puts forth', {'put forth'})]
        for before, after in test_data:
            with self.subTest():
                self.assertIn(Verb(before).plural(), after,
                              f"Verb({repr(before)}).plural() => {repr(after)}")

    def test_plural_to_plural(self):
        test_data = [('construe', {'construe'}),
                     ('clear off', {'clear off'}),
                     ('holler', {'holler'}),
                     ('germinate', {'germinate'}),
                     ('execrate', {'execrate'}),
                     ('reprove', {'reprove'}),
                     ('leucotomize', {'leucotomize'}),
                     ('give on', {'give on'}),
                     ('waft', {'waft'}),
                     ('diminish', {'diminish'}),
                     ('inebriate', {'inebriate'}),
                     ('live up to', {'live up to'}),
                     ('fizzle out', {'fizzle out'}),
                     ('bulldoze', {'bulldoze'}),
                     ('automate', {'automate'}),
                     ('batten down', {'batten down'}),
                     ('panel', {'panel'}),
                     ('judder', {'judder'}),
                     ('landscape', {'landscape'}),
                     ('indulge', {'indulge'}),
                     ('bully', {'bully'}),
                     ('rejoice', {'rejoice'}),
                     ('condescend', {'condescend'}),
                     ('screen', {'screen'}),
                     ('fake', {'fake'}),
                     ('riddle with', {'riddle with'}),
                     ('dock', {'dock'}),
                     ('delete', {'delete'}),
                     ('forgo', {'forgo'}),
                     ('presuppose', {'presuppose'}),
                     ('filter out', {'filter out'}),
                     ('vest', {'vest'}),
                     ('wish on', {'wish on'}),
                     ('urge', {'urge'}),
                     ('rein back', {'rein back'}),
                     ('persuade', {'persuade'}),
                     ('clunk', {'clunk'}),
                     ('rake up', {'rake up'}),
                     ('chart', {'chart'}),
                     ('aid', {'aid'}),
                     ('unfit for', {'unfit for'}),
                     ('wed', {'wed'}),
                     ('inherit', {'inherit'}),
                     ('mollify', {'mollify'}),
                     ('clip', {'clip'}),
                     ('mutiny', {'mutiny'}),
                     ('laicize', {'laicize'}),
                     ('freak out', {'freak out'}),
                     ('brush up on', {'brush up on'}),
                     ('damascene', {'damascene'})]
        for before, after in test_data:
            with self.subTest():
                self.assertIn(Verb(before).plural(), after,
                              f"Verb({repr(before)}).plural() => {repr(after)}")

    """
    past to plural is not properly supported.
    """

    """
    past participle to plural is not properly supported.
    """

    """
    present participle to plural is not properly supported.
    """

    def test_singular_to_past(self):
        test_data = [('inculcates', {'inculcated'}),
                     ('solidifies', {'solidified'}),
                     ('bodes', {'boded'}),
                     ('bums about', {'bummed about'}),
                     ('gives over', {'gave over'}),
                     ('boosts', {'boosted'}),
                     ('tinkers', {'tinkered'}),
                     ('convinces', {'convinced'}),
                     ('somersaults', {'somersaulted'}),
                     ('prescribes', {'prescribed'}),
                     ('test-drives', {'test-drove'}),
                     ('misnames', {'misnamed'}),
                     ('mishandles', {'mishandled'}),
                     ('plods', {'plodded'}),
                     ('consists of', {'consisted of'}),
                     ('unmans', {'unmanned'}),
                     ('scatters', {'scattered'}),
                     ('lets', {'let'}),
                     ('quarries', {'quarried'}),
                     ('crosses', {'crossed'}),
                     ('shrieks', {'shrieked'}),
                     ('snoops', {'snooped'}),
                     ('rears', {'reared'}),
                     ('digs up', {'dug up'}),
                     ('nails', {'nailed'}),
                     ('instils', {'instilled'}),
                     ('guards against', {'guarded against'}),
                     ('overestimates', {'overestimated'}),
                     ('zaps', {'zapped'}),
                     ('gums', {'gummed'}),
                     ('weasels out', {'weaselled out'}),
                     ('loiters', {'loitered'}),
                     ('acclimatizes', {'acclimatized'}),
                     ('implements', {'implemented'}),
                     ('dehorns', {'dehorned'}),
                     ('subscribes', {'subscribed'}),
                     ('strikes upon', {'struck upon'}),
                     ('keys up', {'keyed up'}),
                     ('peals', {'pealed'}),
                     ('makes with', {'made with'}),
                     ('blows down', {'blew down'}),
                     ('clips', {'clipped'}),
                     ('outvies', {'outvied'}),
                     ('lops', {'lopped'}),
                     ('retraces', {'retraced'}),
                     ('closes', {'closed'}),
                     ('chugs', {'chugged'}),
                     ('flattens', {'flattened'}),
                     ('bends to', {'bent to'}),
                     ('renders down', {'rendered down'})]
        for before, after in test_data:
            with self.subTest():
                self.assertIn(Verb(before).past(), after,
                              f"Verb({repr(before)}).past() => {repr(after)}")

    def test_plural_to_past(self):
        test_data = [('premise', {'premised'}),
                     ('unbalance', {'unbalanced'}),
                     ('squire', {'squired'}),
                     ('sliver', {'slivered'}),
                     ('conflate', {'conflated'}),
                     ('fold in', {'folded in'}),
                     ('trek', {'trekked'}),
                     ('avenge', {'avenged'}),
                     ('water', {'watered'}),
                     ('suck', {'sucked'}),
                     ('retort', {'retorted'}),
                     ('revive', {'revived'}),
                     ('waft', {'wafted'}),
                     ('bootleg', {'bootlegged'}),
                     ('employ in', {'employed in'}),
                     ('lute', {'luted'}),
                     ('blemish', {'blemished'}),
                     ('run on', {'ran on'}),
                     ('line up', {'lined up'}),
                     ('machine', {'machined'}),
                     ('unveil', {'unveiled'}),
                     ('tip up', {'tipped up'}),
                     ('splatter', {'splattered'}),
                     ('foment', {'fomented'}),
                     ('plight', {'plighted'}),
                     ('dredge up', {'dredged up'}),
                     ('dig in', {'dug in'}),
                     ('partner up', {'partnered up'}),
                     ('nationalize', {'nationalized'}),
                     ('endow with', {'endowed with'}),
                     ('pancake', {'pancaked'}),
                     ('pile on', {'piled on'}),
                     ('thirst after', {'thirsted after'}),
                     ('mince', {'minced'}),
                     ('taxi', {'taxied'}),
                     ('point out', {'pointed out'}),
                     ('round up', {'rounded up'}),
                     ('cage', {'caged'}),
                     ('poll', {'polled'}),
                     ('entwine', {'entwined'}),
                     ('box up', {'boxed up'}),
                     ('swerve', {'swerved'}),
                     ('abbreviate', {'abbreviated'}),
                     ('colour', {'coloured'}),
                     ('detrain', {'detrained'}),
                     ('cartoon', {'cartooned'}),
                     ('remainder', {'remaindered'}),
                     ('thrum', {'thrummed'}),
                     ('rush on', {'rushed on'}),
                     ('pit against', {'pitted against'})]
        for before, after in test_data:
            with self.subTest():
                self.assertIn(Verb(before).past(), after,
                              f"Verb({repr(before)}).past() => {repr(after)}")

    def test_past_to_past(self):
        test_data = [('declined', {'declined'}),
                     ('faced', {'faced'}),
                     ('harked back', {'harked back'}),
                     ('nailed down', {'nailed down'}),
                     ('abhorred', {'abhorred'}),
                     ('canoodled', {'canoodled'}),
                     ('guillotined', {'guillotined'}),
                     ('curled', {'curled'}),
                     ('upholstered', {'upholstered'}),
                     ('retraced', {'retraced'}),
                     ('stagnated', {'stagnated'}),
                     ('gesticulated', {'gesticulated'}),
                     ('bothered', {'bothered'}),
                     ('kept', {'kept'}),
                     ('carved', {'carved'}),
                     ('went in for', {'went in for'}),
                     ('perambulated', {'perambulated'}),
                     ('ranted', {'ranted'}),
                     ('discharged', {'discharged'}),
                     ('impugned', {'impugned'}),
                     ('made of', {'made of'}),
                     ('anticipated', {'anticipated'}),
                     ('handed on', {'handed on'}),
                     ('reneged', {'reneged'}),
                     ('got out of', {'got out of'}),
                     ('muddled through', {'muddled through'}),
                     ('bottle-fed', {'bottle-fed'}),
                     ('promenaded', {'promenaded'}),
                     ('clocked off', {'clocked off'}),
                     ('attenuated', {'attenuated'}),
                     ('limbered', {'limbered'}),
                     ('ejaculated', {'ejaculated'}),
                     ('shod', {'shod'}),
                     ('conduced towards', {'conduced towards'}),
                     ('bayed', {'bayed'}),
                     ('tightened', {'tightened'}),
                     ('put into', {'put into'}),
                     ('interlaced', {'interlaced'}),
                     ('blethered', {'blethered'}),
                     ('tackled', {'tackled'}),
                     ('webbed', {'webbed'}),
                     ('worked over', {'worked over'}),
                     ('rattled', {'rattled'}),
                     ('de-iced', {'de-iced'}),
                     ('genned up', {'genned up'}),
                     ('gasped', {'gasped'}),
                     ('supposed', {'supposed'}),
                     ('skinned', {'skinned'}),
                     ('assumed', {'assumed'}),
                     ('preferred', {'preferred'})]
        for before, after in test_data:
            with self.subTest():
                self.assertIn(Verb(before).past(), after,
                              f"Verb({repr(before)}).past() => {repr(after)}")

    def test_past_part_to_past(self):
        test_data = [('done away with', {'did away with'}),
                     ('needed', {'needed'}),
                     ('grounded', {'grounded'}),
                     ('backed out', {'backed out'}),
                     ('underscored', {'underscored'}),
                     ('awoke', {'awoke'}),
                     ('disremembered', {'disremembered'}),
                     ('rebuffed', {'rebuffed'}),
                     ('countenanced', {'countenanced'}),
                     ('advanced', {'advanced'}),
                     ('roused to', {'roused to'}),
                     ('overcalled', {'overcalled'}),
                     ('limned', {'limned'}),
                     ('expunged', {'expunged'}),
                     ('massacred', {'massacred'}),
                     ('pinged', {'pinged'}),
                     ('updated', {'updated'}),
                     ('hauled off', {'hauled off'}),
                     ('purported', {'purported'}),
                     ('falsified', {'falsified'}),
                     ('scalped', {'scalped'}),
                     ('hung about', {'hung about'}),
                     ('kipped', {'kipped'}),
                     ('followed', {'followed'}),
                     ('laved', {'laved'}),
                     ('offered', {'offered'}),
                     ('glistened', {'glistened'}),
                     ('interviewed', {'interviewed'}),
                     ('brainwashed', {'brainwashed'}),
                     ('spit', {'spat', 'spitted', 'spit'}),
                     ('vituperated', {'vituperated'}),
                     ('doused', {'doused'}),
                     ('dashed', {'dashed'}),
                     ('displeased', {'displeased'}),
                     ('prowled', {'prowled'}),
                     ('looked after', {'looked after'}),
                     ('knotted', {'knotted'}),
                     ('continued', {'continued'}),
                     ('whipped up', {'whipped up'}),
                     ('haggled', {'haggled'}),
                     ('doubled up', {'doubled up'}),
                     ('read into', {'read into'}),
                     ('bamboozled', {'bamboozled'}),
                     ('overprinted', {'overprinted'}),
                     ('emoted', {'emoted'}),
                     ('undersold', {'undersold'}),
                     ('sculpted', {'sculpted'}),
                     ('brushed', {'brushed'}),
                     ('outrivalled', {'outrivalled'}),
                     ('pushed', {'pushed'})]
        for before, after in test_data:
            with self.subTest():
                self.assertIn(Verb(before).past(), after,
                              f"Verb({repr(before)}).past() => {repr(after)}")

    """
    present participle to past is not properly supported.
    """

    def test_singular_to_past_part(self):
        test_data = [('respires', {'respired'}),
                     ('undercuts', {'undercut'}),
                     ('decays', {'decayed'}),
                     ('truckles to', {'truckled to'}),
                     ('pairs up', {'paired up'}),
                     ('dimples', {'dimpled'}),
                     ('plays up to', {'played up to'}),
                     ('mugs', {'mugged'}),
                     ('mates', {'mated'}),
                     ('tenants', {'tenanted'}),
                     ('rations out', {'rationed out'}),
                     ('stuffs up', {'stuffed up'}),
                     ('sandwiches', {'sandwiched'}),
                     ('lays', {'laid'}),
                     ('commences', {'commenced'}),
                     ('evacuates', {'evacuated'}),
                     ('slobbers', {'slobbered'}),
                     ('burns off', {'burned off', 'burnt off'}),
                     ('wastes away', {'wasted away'}),
                     ('dawdles', {'dawdled'}),
                     ('glorifies', {'glorified'}),
                     ('dismounts', {'dismounted'}),
                     ('shews', {'shewn', 'shewed'}),
                     ('eventuates in', {'eventuated in'}),
                     ('diminishes', {'diminished'}),
                     ('swears by', {'sworn by'}),
                     ('redresses', {'redressed'}),
                     ('ends in', {'ended in'}),
                     ('titivates', {'titivated'}),
                     ('mars', {'marred'}),
                     ('slips', {'slipped'}),
                     ('hacks', {'hacked'}),
                     ('phrases', {'phrased'}),
                     ('pulls through', {'pulled through'}),
                     ('ploughs under', {'ploughed under'}),
                     ('skitters', {'skittered'}),
                     ('subtracts', {'subtracted'}),
                     ('embarrasses', {'embarrassed'}),
                     ('disorders', {'disordered'}),
                     ('sweeps', {'swept'}),
                     ('corrects', {'corrected'}),
                     ('hurdles', {'hurdled'}),
                     ('welds', {'welded'}),
                     ('defames', {'defamed'}),
                     ('garbles', {'garbled'}),
                     ('taxes with', {'taxed with'}),
                     ('impassions', {'impassioned'}),
                     ('hulls', {'hulled'}),
                     ('noses around', {'nosed around'}),
                     ('footles', {'footled'})]
        for before, after in test_data:
            with self.subTest():
                self.assertIn(Verb(before).past_part(), after,
                              f"Verb({repr(before)}).past_part() => {repr(after)}")

    def test_plural_to_past_part(self):
        test_data = [('function', {'functioned'}),
                     ('mutate', {'mutated'}),
                     ('get ahead', {'gotten ahead', 'got ahead'}),
                     ('sponge', {'sponged'}),
                     ('buttress', {'buttressed'}),
                     ('blether', {'blethered'}),
                     ('politicize', {'politicized'}),
                     ('bone up on', {'boned up on'}),
                     ('rebuke', {'rebuked'}),
                     ('pair off', {'paired off'}),
                     ('segregate', {'segregated'}),
                     ('salify', {'salified'}),
                     ('typecast', {'typecast'}),
                     ('print', {'printed'}),
                     ('gainsay', {'gainsaid'}),
                     ('gape', {'gaped'}),
                     ('balk', {'balked'}),
                     ('token', {'tokened'}),
                     ('occasion', {'occasioned'}),
                     ('mimeograph', {'mimeographed'}),
                     ('extirpate', {'extirpated'}),
                     ('braze', {'brazed'}),
                     ('reissue', {'reissued'}),
                     ('drug', {'drugged'}),
                     ('screw up', {'screwed up'}),
                     ('save on', {'saved on'}),
                     ('bore', {'bored'}),
                     ('hitch up', {'hitched up'}),
                     ('slip', {'slipped'}),
                     ('drain', {'drained'}),
                     ('adjourn', {'adjourned'}),
                     ('shovel', {'shovelled'}),
                     ('read up', {'read up'}),
                     ('build upon', {'built upon'}),
                     ('muscle in', {'muscled in'}),
                     ('afford', {'afforded'}),
                     ('derestrict', {'derestricted'}),
                     ('hemstitch', {'hemstitched'}),
                     ('repudiate', {'repudiated'}),
                     ('wonder', {'wondered'}),
                     ('puzzle over', {'puzzled over'}),
                     ('coast', {'coasted'}),
                     ('desire', {'desired'}),
                     ('breathe', {'breathed'}),
                     ('enkindle', {'enkindled'}),
                     ('hurl', {'hurled'}),
                     ('remake', {'remade'}),
                     ('disarm', {'disarmed'}),
                     ('husband', {'husbanded'}),
                     ('arch', {'arched'})]
        for before, after in test_data:
            with self.subTest():
                self.assertIn(Verb(before).past_part(), after,
                              f"Verb({repr(before)}).past_part() => {repr(after)}")

    def test_past_to_past_part(self):
        test_data = [('twigged', {'twigged'}),
                     ('nonplussed', {'nonplussed'}),
                     ('appertained to', {'appertained to'}),
                     ('trifled with', {'trifled with'}),
                     ('filleted', {'filleted'}),
                     ('plumped down', {'plumped down'}),
                     ('scarified', {'scarified'}),
                     ('wrapped up', {'wrapped up'}),
                     ('juiced up', {'juiced up'}),
                     ('blended in', {'blended in', 'blent in'}),
                     ('jived', {'jived'}),
                     ('worked in', {'worked in'}),
                     ('forwent', {'forgone'}),
                     ('cremated', {'cremated'}),
                     ('dispensed', {'dispensed'}),
                     ('bequeathed', {'bequeathed'}),
                     ('sacked', {'sacked'}),
                     ('preceded', {'preceded'}),
                     ('backed away', {'backed away'}),
                     ('punched', {'punched'}),
                     ('portended', {'portended'}),
                     ('repainted', {'repainted'}),
                     ('restricted', {'restricted'}),
                     ('anticipated', {'anticipated'}),
                     ('hived', {'hived'}),
                     ('shinnied', {'shinnied'}),
                     ('gorged with', {'gorged with'}),
                     ('evanesced', {'evanesced'}),
                     ('suppurated', {'suppurated'}),
                     ('bit', {'bitten'}),
                     ('jumbled', {'jumbled'}),
                     ('upholstered', {'upholstered'}),
                     ('aged', {'aged'}),
                     ('laid flat', {'laid flat'}),
                     ('melded', {'melded'}),
                     ('reneged', {'reneged'}),
                     ('chloroformed', {'chloroformed'}),
                     ('hulled', {'hulled'}),
                     ('silhouetted', {'silhouetted'}),
                     ('outdated', {'outdated'}),
                     ('teemed with', {'teemed with'}),
                     ('acquainted with', {'acquainted with'}),
                     ('decarbonized', {'decarbonized'}),
                     ('hung around', {'hung around'}),
                     ('ferried', {'ferried'}),
                     ('pointed out', {'pointed out'}),
                     ('accorded', {'accorded'}),
                     ('prefabricated', {'prefabricated'}),
                     ('sallied out', {'sallied out'}),
                     ('contraindicated', {'contraindicated'})]
        for before, after in test_data:
            with self.subTest():
                self.assertIn(Verb(before).past_part(), after,
                              f"Verb({repr(before)}).past_part() => {repr(after)}")

    def test_past_part_to_past_part(self):
        test_data = [('stayed on', {'stayed on'}),
                     ('trafficked', {'trafficked'}),
                     ('rustproofed', {'rustproofed'}),
                     ('showed off', {'shown off', 'showed off'}),
                     ('kitted up', {'kitted up'}),
                     ('theorized', {'theorized'}),
                     ('cheered', {'cheered'}),
                     ('outdone', {'outdone'}),
                     ('fallen on', {'fallen on'}),
                     ('raided', {'raided'}),
                     ('inched', {'inched'}),
                     ('teemed', {'teemed'}),
                     ('begun', {'begun'}),
                     ('scampered', {'scampered'}),
                     ('tabulated', {'tabulated'}),
                     ('kept together', {'kept together'}),
                     ('enciphered', {'enciphered'}),
                     ('rationed', {'rationed'}),
                     ('mistimed', {'mistimed'}),
                     ('joshed', {'joshed'}),
                     ('huddled', {'huddled'}),
                     ('refuted', {'refuted'}),
                     ('positioned', {'positioned'}),
                     ('arrayed', {'arrayed'}),
                     ('legislated for', {'legislated for'}),
                     ('toddled', {'toddled'}),
                     ('populated', {'populated'}),
                     ('hit at', {'hit at'}),
                     ('unwound', {'unwound'}),
                     ('debugged', {'debugged'}),
                     ('interviewed', {'interviewed'}),
                     ('plunged', {'plunged'}),
                     ('raved about', {'raved about'}),
                     ('smudged', {'smudged'}),
                     ('jarred', {'jarred'}),
                     ('flaked out', {'flaked out'}),
                     ('vomited', {'vomited'}),
                     ('indwelt', {'indwelt'}),
                     ('juiced up', {'juiced up'}),
                     ('notarized', {'notarized'}),
                     ('barked', {'barked'}),
                     ('plunged in', {'plunged in'}),
                     ('decreased', {'decreased'}),
                     ('phoned', {'phoned'}),
                     ('sentenced', {'sentenced'}),
                     ('lassoed', {'lassoed'}),
                     ('stigmatized', {'stigmatized'}),
                     ('cudgelled', {'cudgelled'}),
                     ('puttered around', {'puttered around'}),
                     ('manacled', {'manacled'})]
        for before, after in test_data:
            with self.subTest():
                self.assertIn(Verb(before).past_part(), after,
                              f"Verb({repr(before)}).past_part() => {repr(after)}")

    """
    present participle to past participle is not properly supported.
    """

    def test_singular_to_pres_part(self):
        test_data = [('imprints', {'imprinting'}),
                     ('clarifies', {'clarifying'}),
                     ('prospects', {'prospecting'}),
                     ('files down', {'filing down'}),
                     ('blazes', {'blazing'}),
                     ('disencumbers', {'disencumbering'}),
                     ('outstrips', {'outstripping'}),
                     ('commands', {'commanding'}),
                     ('chronicles', {'chronicling'}),
                     ('undernourishes', {'undernourishing'}),
                     ('spiritualizes', {'spiritualizing'}),
                     ('signalizes', {'signalizing'}),
                     ('ruins', {'ruining'}),
                     ('divvies', {'divvying'}),
                     ('reckons up', {'reckoning up'}),
                     ('runs back over', {'running back over'}),
                     ('pins back', {'pinning back'}),
                     ('snaps at', {'snapping at'}),
                     ('muddles along', {'muddling along'}),
                     ('striates', {'striating'}),
                     ('bungs up', {'bunging up'}),
                     ('creeps into', {'creeping into'}),
                     ('ravens', {'ravening'}),
                     ('waylays', {'waylaying'}),
                     ('fouls up', {'fouling up'}),
                     ('asphalts', {'asphalting'}),
                     ('eases off', {'easing off'}),
                     ('swallows', {'swallowing'}),
                     ('fizzles', {'fizzling'}),
                     ('shrinks from', {'shrinking from'}),
                     ('globe-trots', {'globe-trotting'}),
                     ('patronizes', {'patronizing'}),
                     ('contains', {'containing'}),
                     ('nudges', {'nudging'}),
                     ('denunciates', {'denunciating'}),
                     ('nears', {'nearing'}),
                     ('sets down', {'setting down'}),
                     ('studs', {'studding'}),
                     ('banishes', {'banishing'}),
                     ('vivifies', {'vivifying'}),
                     ('bakes', {'baking'}),
                     ('fragments', {'fragmenting'}),
                     ('snoozes', {'snoozing'}),
                     ('rubbernecks', {'rubbernecking'}),
                     ('precludes from', {'precluding from'}),
                     ('obtains', {'obtaining'}),
                     ('chips in', {'chipping in'}),
                     ('overcapitalizes', {'overcapitalizing'}),
                     ('chinks', {'chinking'}),
                     ('confabulates', {'confabulating'})]
        for before, after in test_data:
            with self.subTest():
                self.assertIn(Verb(before).pres_part(), after,
                              f"Verb({repr(before)}).pres_part() => {repr(after)}")

    def test_plural_to_pres_part(self):
        test_data = [('expatiate on', {'expatiating on'}),
                     ('stockpile', {'stockpiling'}),
                     ('behave', {'behaving'}),
                     ('keep down', {'keeping down'}),
                     ('dote on', {'doting on'}),
                     ('contraindicate', {'contraindicating'}),
                     ('disembarrass of', {'disembarrassing of'}),
                     ('usurp', {'usurping'}),
                     ('depreciate', {'depreciating'}),
                     ('sentimentalize', {'sentimentalizing'}),
                     ('war', {'warring'}),
                     ('carry over', {'carrying over'}),
                     ('pour out', {'pouring out'}),
                     ('sledge', {'sledging'}),
                     ('stand in', {'standing in'}),
                     ('plunge into', {'plunging into'}),
                     ('coexist', {'coexisting'}),
                     ('pay back', {'paying back'}),
                     ('mass', {'massing'}),
                     ('remodel', {'remodelling'}),
                     ('over-heat', {'over-heating'}),
                     ('regale on', {'regaling on'}),
                     ('arrange for', {'arranging for'}),
                     ('drum', {'drumming'}),
                     ('fix with', {'fixing with'}),
                     ('foreshorten', {'foreshortening'}),
                     ('page', {'paging'}),
                     ('copy', {'copying'}),
                     ('outsail', {'outsailing'}),
                     ('unload', {'unloading'}),
                     ('slug', {'slugging'}),
                     ('track', {'tracking'}),
                     ('hunt down', {'hunting down'}),
                     ('sabre', {'sabring'}),
                     ('tarnish', {'tarnishing'}),
                     ('dine off', {'dining off'}),
                     ('tincture', {'tincturing'}),
                     ('step in', {'stepping in'}),
                     ('queer', {'queering'}),
                     ('discharge', {'discharging'}),
                     ('park', {'parking'}),
                     ('face', {'facing'}),
                     ('heave at', {'heaving at'}),
                     ('hop', {'hopping'}),
                     ('levitate', {'levitating'}),
                     ('deluge', {'deluging'}),
                     ('stylize', {'stylizing'}),
                     ('remonstrate', {'remonstrating'}),
                     ('distress', {'distressing'}),
                     ('syringe', {'syringing'})]
        for before, after in test_data:
            with self.subTest():
                self.assertIn(Verb(before).pres_part(), after,
                              f"Verb({repr(before)}).pres_part() => {repr(after)}")

    """
    past to present participle is not properly supported.
    """

    """
    past participle to present participle is not properly supported.
    """

    def test_pres_part_to_pres_part(self):
        test_data = [('footling', {'footling'}),
                     ('pinking', {'pinking'}),
                     ('crowning', {'crowning'}),
                     ('rending', {'rending'}),
                     ('peeving', {'peeving'}),
                     ('giving away', {'giving away'}),
                     ('typecasting', {'typecasting'}),
                     ('dredging', {'dredging'}),
                     ('expropriating', {'expropriating'}),
                     ('denuding', {'denuding'}),
                     ('repatriating', {'repatriating'}),
                     ('assuring', {'assuring'}),
                     ('needling', {'needling'}),
                     ('functioning', {'functioning'}),
                     ('bedding out', {'bedding out'}),
                     ('disconnecting', {'disconnecting'}),
                     ('binding down', {'binding down'}),
                     ('bolstering up', {'bolstering up'}),
                     ('covering up', {'covering up'}),
                     ('funking', {'funking'}),
                     ('prolonging', {'prolonging'}),
                     ('ripping off', {'ripping off'}),
                     ('perking up', {'perking up'}),
                     ('surprising', {'surprising'}),
                     ('energizing', {'energizing'}),
                     ('commemorating', {'commemorating'}),
                     ('rucking', {'rucking'}),
                     ('rocketing', {'rocketing'}),
                     ('garnishing', {'garnishing'}),
                     ('domineering', {'domineering'}),
                     ('passing', {'passing'}),
                     ('outclassing', {'outclassing'}),
                     ('peppering', {'peppering'}),
                     ('moving off', {'moving off'}),
                     ('engaging upon', {'engaging upon'}),
                     ('beating up', {'beating up'}),
                     ('enthroning', {'enthroning'}),
                     ('rendering down', {'rendering down'}),
                     ('plumping down', {'plumping down'}),
                     ('wiping up', {'wiping up'}),
                     ('mildewing', {'mildewing'}),
                     ('prefabricating', {'prefabricating'}),
                     ('touching off', {'touching off'}),
                     ('slanging', {'slanging'}),
                     ('potting at', {'potting at'}),
                     ('ennobling', {'ennobling'}),
                     ('pushing off', {'pushing off'}),
                     ('changing over', {'changing over'}),
                     ('eavesdropping', {'eavesdropping'}),
                     ('nosediving', {'nosediving'})]
        for before, after in test_data:
            with self.subTest():
                self.assertIn(Verb(before).pres_part(), after,
                              f"Verb({repr(before)}).pres_part() => {repr(after)}")

    def test_is_singular(self):
        test_data = ['wrongs', 'steers', 'weasels out', 'truckles to', 'crawls', 'rucks',
                     'anaesthetizes', 'brings together', 'moons about', 'nears', 'disports',
                     'pricks up', 'switches over', 'finishes off', 'flashes', 'wiretaps', 'tattoos',
                     'snips', 'shellacs', 'chisels', 'homes in on', 'compacts', 'figures',
                     'colours', 'polls', 'gibbets', 'badgers', 'shakes', 'tousles', 'racks',
                     'reprehends', 'lessens', 'unifies', 'ventures upon', 'slits', 'entails',
                     'beats', 'revolutionizes', 'devastates', 'discontents', 'chalks up',
                     'tilts at', 'follows through', 'lasts', 'employs in', 'retreads',
                     'cashiers', 'mucks around', 'buoys up', 'junkets']
        for term in test_data:
            with self.subTest():
                self.assertTrue(Verb(term).is_singular(),
                                f"Verb({repr(term)}).is_singular => True")

    def test_is_plural(self):
        test_data = ['inform upon', 'lengthen', 'encrust', 'gibe', 'enchain', 'read for', 'ransom',
                     'pickle', 'scant', 'tie together', 'fascinate', 'repay', 'dehumanize',
                     'habituate', 'vaunt of', 'invoice', 'impede', 'co-ordinate', 'put in',
                     'study', 'plant out', 'card', 'tranquillize', 'rejoin', 'assemble', 'gazette',
                     'fudge', 'trail', 'augur', 'rubber-stamp', 'skulk', 'tick', 'scorn',
                     'palisade', 'bead', 'toilet train', 'dance', 'peel', 'blush', 'imagine',
                     'write down', 'yelp', 'quiet', 'recollect', 'yank', 'couch', 'regain',
                     'nip', 'dramatize', 'prove']
        for term in test_data:
            with self.subTest():
                self.assertTrue(Verb(term).is_plural(),
                                f"Verb({repr(term)}).is_plural => True")

    def test_is_past(self):
        test_data = ['rained on', 'started up', 'stitched', 'drizzled', 'buffered', 'eventuated in',
                     'misnamed', 'ice-skated', 'snicked', 'screamed', 'thatched', 'bicycled',
                     'bawled out', 'oscillated', 'busked', 'interpreted', 'skyjacked',
                     'scratched out', 'warred', 'asterisked', 'silhouetted', 'attorned',
                     'befriended', 'macadamized', 'spelled', 'deserted', 'cemented', 'chaffed',
                     'guaranteed', 'quilted', 'heeded', 'mainlined', 'abraded', 'undernourished',
                     'fell on', 'horrified', 'pulled over', 'paved', 'memorized', 'razored',
                     'barked', 'served', 'ruled off', 'played on', 'aspirated', 'flurried',
                     'bevelled', 'gybed', 'colluded', 'censored']
        for term in test_data:
            with self.subTest():
                self.assertTrue(Verb(term).is_past(),
                                f"Verb({repr(term)}).is_past => True")

    def test_is_past_part(self):
        test_data = ['plumbed', 'induced', 'vested', 'bitten back', 'stopped by', 'edged out',
                     'stretched', 'beefed up', 'laid aside', 'garnered', 'modelled upon', 'mashed',
                     'reinforced', 'trisected', 'waddled', 'burlesqued', 'staked', 'cloaked',
                     'limbered', 'ciphered', 'cudgelled', 'specialized', 'finished with',
                     'pounded out', 'dislodged', 'bemused', 'test-driven', 'quavered', 'ruled off',
                     'dabbed', 'settled on', 'pollarded', 'hurtled', 'leased', 'gotten on',
                     'annihilated', 'reinsured', 'laced into', 'exhumed', 'melted down',
                     'ridden out', 'likened to', 'lusted after', 'caroused', 'misprinted',
                     'answered', 'preheated', 'let', 'plonked down', 'patrolled']
        for term in test_data:
            with self.subTest():
                self.assertTrue(Verb(term).is_past_part(),
                                f"Verb({repr(term)}).is_past_part => True")

    def test_is_pres_part(self):
        test_data = ['turning away', 'throttling', 'raining down', 'toughening', 'winching',
                     'sweating out', 'underquoting', 'deifying', 'tossing off', 'scrummaging',
                     'cuddling up', 'mottling', 'filing', 'prodding', 'pleating', 'entwining',
                     'guessing', 'shrilling', 'churning', 'partnering', 'discomfiting',
                     'doing over', 'juxtaposing', 'apostrophizing', 'looking over',
                     'leaking out', 'maturating', 'streamlining', 'managing', 'erasing',
                     'decking out', 'ticketing', 'hungering after', 'handing', 'slandering',
                     'blowing down', 'gumming up', 'budding', 'canoodling', 'deluging', 'funding',
                     'building on', 'intruding', 'outbraving', 'divagating', 'furnishing',
                     'reducing', 'tailoring', 'boxing up', 'making towards']
        for term in test_data:
            with self.subTest():
                self.assertTrue(Verb(term).is_pres_part(),
                                f"Verb({repr(term)}).is_pres_part => True")

    def test_is_not_singular(self):
        test_data = ['inform upon', 'lengthen', 'encrust', 'gibe', 'enchain', 'read for', 'ransom',
                     'pickle', 'scant', 'tie together', 'fascinate', 'repay', 'dehumanize',
                     'habituate', 'vaunt of', 'invoice', 'impede', 'co-ordinate', 'study',
                     'plant out', 'card', 'tranquillize', 'rejoin', 'assemble', 'gazette',
                     'fudge', 'trail', 'augur', 'rubber-stamp', 'skulk', 'tick', 'scorn',
                     'palisade', 'bead', 'toilet train', 'dance', 'peel', 'blush', 'imagine',
                     'write down', 'yelp', 'quiet', 'recollect', 'yank', 'couch', 'regain',
                     'nip', 'dramatize', 'prove']
        for term in test_data:
            with self.subTest():
                self.assertFalse(Verb(term).is_singular(),
                                 f"Verb({repr(term)}).is_singular => False")

    def test_is_not_plural(self):
        test_data = ['wrongs', 'steers', 'weasels out', 'truckles to', 'crawls', 'rucks',
                     'anaesthetizes', 'brings together', 'moons about', 'nears', 'disports',
                     'pricks up', 'switches over', 'finishes off', 'flashes', 'wiretaps', 'tattoos',
                     'snips', 'shellacs', 'chisels', 'homes in on', 'compacts', 'figures',
                     'colours', 'polls', 'gibbets', 'badgers', 'shakes', 'tousles', 'racks',
                     'reprehends', 'lessens', 'unifies', 'ventures upon', 'slits', 'entails',
                     'beats', 'revolutionizes', 'devastates', 'discontents', 'chalks up',
                     'tilts at', 'follows through', 'lasts', 'employs in', 'retreads',
                     'cashiers', 'mucks around', 'buoys up', 'junkets']
        for term in test_data:
            with self.subTest():
                self.assertFalse(Verb(term).is_plural(),
                                 f"Verb({repr(term)}).is_plural => False")

    def test_is_not_past(self):
        test_data = ['turning away', 'throttling', 'raining down', 'toughening', 'winching',
                     'sweating out', 'underquoting', 'deifying', 'tossing off', 'scrummaging',
                     'cuddling up', 'mottling', 'filing', 'prodding', 'pleating', 'entwining',
                     'guessing', 'shrilling', 'churning', 'partnering', 'discomfiting',
                     'doing over', 'juxtaposing', 'apostrophizing', 'looking over',
                     'leaking out', 'maturating', 'streamlining', 'managing', 'erasing',
                     'decking out', 'ticketing', 'hungering after', 'handing', 'slandering',
                     'blowing down', 'gumming up', 'budding', 'canoodling', 'deluging', 'funding',
                     'building on', 'intruding', 'outbraving', 'divagating', 'furnishing',
                     'reducing', 'tailoring', 'boxing up', 'making towards']
        for term in test_data:
            with self.subTest():
                self.assertFalse(Verb(term).is_past(),
                                 f"Verb({repr(term)}).is_past => False")

    def test_is_not_past_part(self):
        test_data = ['turning away', 'throttling', 'raining down', 'toughening', 'winching',
                     'sweating out', 'underquoting', 'deifying', 'tossing off', 'scrummaging',
                     'cuddling up', 'mottling', 'filing', 'prodding', 'pleating', 'entwining',
                     'guessing', 'shrilling', 'churning', 'partnering', 'discomfiting',
                     'doing over', 'juxtaposing', 'apostrophizing', 'looking over',
                     'leaking out', 'maturating', 'streamlining', 'managing', 'erasing',
                     'decking out', 'ticketing', 'hungering after', 'handing', 'slandering',
                     'blowing down', 'gumming up', 'budding', 'canoodling', 'deluging', 'funding',
                     'building on', 'intruding', 'outbraving', 'divagating', 'furnishing',
                     'reducing', 'tailoring', 'boxing up', 'making towards']
        for term in test_data:
            with self.subTest():
                self.assertFalse(Verb(term).is_past_part(),
                                 f"Verb({repr(term)}).is_past_part => False")

    def test_is_not_pres_part(self):
        test_data = ['plumbed', 'induced', 'vested', 'bitten back', 'stopped by', 'edged out',
                     'stretched', 'beefed up', 'laid aside', 'garnered', 'modelled upon', 'mashed',
                     'reinforced', 'trisected', 'waddled', 'burlesqued', 'staked', 'cloaked',
                     'limbered', 'ciphered', 'cudgelled', 'specialized', 'finished with',
                     'pounded out', 'dislodged', 'bemused', 'test-driven', 'quavered', 'ruled off',
                     'dabbed', 'settled on', 'pollarded', 'hurtled', 'leased', 'gotten on',
                     'annihilated', 'reinsured', 'laced into', 'exhumed', 'melted down',
                     'ridden out', 'likened to', 'lusted after', 'caroused', 'misprinted',
                     'answered', 'preheated', 'let', 'plonked down', 'patrolled']
        for term in test_data:
            with self.subTest():
                self.assertFalse(Verb(term).is_pres_part(),
                                 f"Verb({repr(term)}).is_pres_part => False")


if __name__ == "__main__":
    unittest.main()
