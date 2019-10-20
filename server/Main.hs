module Main where

import qualified Data.Map as Map

import Server.App

app { init = init, route = route }


-- Just Store the Username, if they are logged in, otherwise Nothing
type Model = { username :: Maybe String }

type Username = String

type Request_Body = { route :: String
                    , arguments :: Map.Map String String -- Query Strings, Bodys, all are the same.
                    }

data Request =
    GET  Body
  | POST Body
  | UPDATE Body
  | DELETE Body

data Cmd =
    Verify { name :: Username, password :: String }
  | Post { recipient :: Username, }
  | Vote { vote :: Vote }
  | ServeStatic String -- Serve this Static File as response to the user.

-- Initial State of each User
init :: Model
init = Model { username = Nothing }

route :: Route -> Cmd -- Associate any Route with a certain Cmd.
route GET "/" arguments =
