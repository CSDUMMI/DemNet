module Main exposing (..)

import Browser

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
