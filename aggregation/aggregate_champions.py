import pymongo
from bson.son import SON
from bson.code import Code

c = pymongo.MongoClient()
m = c.prourfbuilds.match

# js document to output
doc = '''
            // setup return doc format
            doc = {
                championId: 0,
                games: 0,
                win: 0,
                loss: 0,
                kills: 0,
                deaths: 0,
                assists: 0,
                first_blood: 0,
                // items
                ibuilt: {},
                iwin: {},
                iloss: {},
                ikills: {},
                ideaths: {},
                iassists: {},
                ifirst_blood: {},
                debug: []
            };
'''

mapfn = '''
    function() {
        item_names = [];
        for (i=0; i<7; i++) { item_names.push('item' + i); };

        // populate doc with participant info (p)
        populate_doc = function(p, that) {
            %s

            doc.championId = p.championId;
            doc.games = 1;
            if (p.stats.winner) {
                doc.win = 1;
            }
            else {
                doc.loss = 1;
            }
            // kda
            doc.kills = p.stats.kills;
            doc.deaths = p.stats.deaths;
            doc.assists = p.stats.assists;

            // fb
            if(p.stats.firstBloodKill)
                doc.first_blood = 1;

            // loop through items
            for (j=0; j<item_names.length; j++) {
                item = p.stats[item_names[j]];
                doc.ibuilt[item] = 1;
                if (p.stats.winner)
                    doc.iwin[item] = 1;
                else
                    doc.iloss[item] = 1;

                doc.ikills[item] = doc.kills;
                doc.ideaths[item] = doc.deaths;
                doc.iassists[item] = doc.assists;
                if (doc.first_blood == 1)
                    doc.ifirst_blood[item] = doc.first_blood;
            }
            return doc;
        };

        // emit for each participant
        for (i=0; i<this.participants.length; i++) {
            p = this.participants[i];
            d = populate_doc(p, this);
            emit(p.championId, d);
        }
    }
''' % doc

reducefn = '''
    function(key, values) {
        %s

        // sum associative array keys
        sum_aarray = function(dst, src) {
            for (k in src) {
                if (k in dst) {
                    dst[k] += src[k];
                } else {
                    dst[k] = src[k];
                }
            }
            return dst;
        }

        // aggregate the values within the doc
        for (i=0; i<values.length; i++) {
            v = values[i];
            doc.championId = key;
            doc.games += v.games;
            doc.win += v.win;
            doc.loss += v.loss;
            doc.kills += v.kills;
            doc.deaths += v.deaths;
            doc.assists += v.assists;
            doc.first_blood += v.first_blood;
            doc.debug = doc.debug.concat(v.debug);
            sum_aarray(doc.ibuilt, v.ibuilt);
            sum_aarray(doc.iwin, v.iwin);
            sum_aarray(doc.iloss, v.iloss);
            sum_aarray(doc.ikills, v.ikills);
            sum_aarray(doc.ideaths, v.ideaths);
            sum_aarray(doc.iassists, v.iassists);
            sum_aarray(doc.ifirst_blood, v.ifirst_blood);
        };
        return doc;
    }
''' % doc

map_results = m.map_reduce(mapfn, reducefn, 'champion', full_response=True,
        limit=None)

print map_results

import pprint
for d in c.prourfbuilds.champion.find():
    pprint.pprint(d)

print c.prourfbuilds.champion.count()


