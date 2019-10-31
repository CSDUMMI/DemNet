module Main exposing (..)

import Browser
import Browser.Navigation as Nav
import Url

import Viewing
import Requests
import Cycle

-- MAIN
main = Browser.application
  { init = init
  , view = view
  , update = update
  , subscriptions = subscriptions
  , onUrlRequest = onUrlRequest
  , onUrlChange = onUrlChange
  }

-- MODEL
type User = User { username : String }

type Model = Model
  { navigation : Viewing.Nav_Items
  , user : User
  , messages : List (Viewing.Post Msg)
  , key : Nav.Key
  , url : Url.Url
  }


-- UPDATE
type Msg
  = EnterPassword
