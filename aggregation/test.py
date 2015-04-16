import pymongo
from bson.son import SON
from bson.code import Code

c = pymongo.MongoClient()
m = c.prourfbuilds.match

# for each participant
#   teamId
#   championId
#   stats -> winner in here, items as well

# use map reduce

doc = '''
            // setup return doc format
            doc = {
                championId: 0,
                games: 0,
                win: 0,
                loss: 0,
                // items
                ibuilt: {},
                iwin: {},
                iloss: {},
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

            // loop through items
            for (j=0; j<item_names.length; j++) {
                doc.ibuilt[p.stats[item_names[j]]] = 1;
                if (p.stats.winner)
                    doc.iwin[p.stats[item_names[j]]] = 1;
                else
                    doc.iloss[p.stats[item_names[j]]] = 1;
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
            doc.debug = doc.debug.concat(v.debug);
            sum_aarray(doc.ibuilt, v.ibuilt);
            sum_aarray(doc.iwin, v.iwin);
            sum_aarray(doc.iloss, v.iloss);
        };
        return doc;
    }
''' % doc

map_results = m.map_reduce(mapfn, reducefn, 'map_results', full_response=True,
        limit=None)

print map_results

import pprint
for d in c.prourfbuilds.map_results.find():
    pprint.pprint(d)

print c.prourfbuilds.map_results.count()


