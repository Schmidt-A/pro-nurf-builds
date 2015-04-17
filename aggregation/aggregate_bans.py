
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
                debug: []
            };
'''

mapfn = '''
    function() {
        item_names = [];
        function pad(a,b){return(1e15+a+"").slice(-b)};


        // populate doc with participant info (p)
        populate_doc = function(champid) {
            %s

            doc.championId = champid;
            doc.games = 1;
            return doc;
        };

        // emit for each participant
        for (i=0; i<this.teams.length; i++) {
            team = this.teams[i];
            bans = team['bans'];
            if (bans) {
                for (j=0; j<bans.length; j++) {
                    d = populate_doc(team.bans[j].championId);
                    emit("000000000000" + pad(d.championId,12), d);
                }
            }
        }
    }
''' % doc

reducefn = '''
    function(key, values) {
        %s

        // aggregate the values within the doc
        for (i=0; i<values.length; i++) {
            v = values[i];
            doc.championId = v.championId;
            doc.games += v.games;
        };
        return doc;
    }
''' % doc

map_results = m.map_reduce(mapfn, reducefn, 'bans', full_response=True,
        limit=None)

print map_results

#import pprint
#for d in c.prourfbuilds.bans.find():
#    pprint.pprint(d)

print c.prourfbuilds.bans.count()


