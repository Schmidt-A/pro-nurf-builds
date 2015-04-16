m = function() {
        for (i=0; i<this.participants.length; i++) {
	    p = this.participants[i]
            emit(p.championId, 1);
        }
    };
r = function(key, values) {
        obj = {
            championId: key,
            games: Array.sum(values)
        };
        return Array.sum(values);
    };

db.match.mapReduce(m, r, {out: 'mrtest'});
db.mrtest.find()
