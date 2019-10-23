/*
Vote and Publish Election
*/
const express = require('express');
const app = express();

function count_votes( votes, participants, options )
{

  for( let i = 0; i < options.length; i++ ) {
    options[i] = {
      option : options[i],
      support : new Array(votes.filter( vote => options[i] == vote[vote.length-1] ) )
    }
  }
  console.log( options );
  _count_votes( [], options, participants );
}

function _count_votes( votes, options, participants ) {
  // Add votes to the selected options
  for( let i = 0; i < options.length; i++ ) {
    options[i].support.push( ... votes.filter( vote => options[i].option == vote[vote.length-1] ))
  }

  console.log( typeof( options[0].support ) );
  options.sort( ( fE, sE ) => {
    if (fE.support.length > sE.suppport.length) {
      return -1;
    } else if( fE.support.length < sE.support.length ) {
      return 1;
    } else {
      return 0;
    }
  });

  if( options[0].support.length > participants *0.5 ) {
    return options[0]; // Winner by virtue of having more than 50% of the support
  } else {
    options[options.length-1] = options[options.length-1].support.map( e => e.pop() );
    options.pop();
    return _count_votes( options[ options.length-1 ], options, participants )
  }
}


votes = [
          [
            'A', 'B', 'C'
          ],
          [
            'B', 'C', 'A'
          ],
          [
            'C', 'A', 'B'
          ],
          [
            'A', 'B', 'C'
          ]
        ];

console.log( count_votes( votes, 4, ['A','B','C']));

module.exports = count_votes;
