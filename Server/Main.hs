module Main where

import Happstack.Server

main :: IO ()
main = do
  simpleHTTP nullConf $ ok "Hello, World!"
