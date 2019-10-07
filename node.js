/*
Server to access IPFS Files encrypted
and create new files on IPFS
*/

async function init_node() {
  const IPFS        = require( 'ipfs' );
  const node        = await IPFS.create();
  const result      = {
    node      : node,

    create    : async ( type, content ) => {
    const content_id  = await node.add( JSON.stringify( { type : type, content : content } ) );
    return content_id;
    },

    read      : async ( id, encoding ) => {
      const content     = await node.cat( id );
      return content.toString( encoding );
    },

    read_json : async ( id, encoding = "utf-8" ) => {
      const content     = await node.cat( id );
      return JSON.parse( content.toString( encoding ) );
    }

  };

  return await result;
}

module.exports = {
  init_node : init_node
}
