module Main where

import Control.Monad
import Happstack.Server ( nullConf, simpleHTTP,  toResponse, ok, dir )

main :: IO ()
main = simpleHTTP nullConf $ msum [ dir "vote" $ ok "No Voting possible yet"
                                  , dir "post" $ ok "No Postin possible yet"
                                  ]
