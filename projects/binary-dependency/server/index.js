const bcrypt = require('bcrypt');

export class BinaryDependencyTest {
    async test() {
        const saltRounds = 10;
        const myPlaintextPassword = 's0/\/\P4$$w0rD';

        const promise = new Promise((resolve, reject) => {
            bcrypt.genSalt(saltRounds, function(err, salt) {
                bcrypt.hash(myPlaintextPassword, salt, function(err, hash) {
                    resolve(hash)
                });
            });
        })
     
        const hash = await promise;
        return hash;
    }
}