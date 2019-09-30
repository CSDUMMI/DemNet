const IPFS = require( 'ipfs' );

async function main() {
  const node    = await IPFS.create();
  const users   = {};
  let   state   = node.get(
    process.env.NETWORK_INDEX,
    ( error, files ) => {
      users[]
    }
   );
}

function init_election() {
  
}

main();
