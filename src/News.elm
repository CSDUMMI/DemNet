module News exposing (..)

import Viewing
import Http

-- MAIN
main =
  Browser.element
    { init = init
    , update = update
    , subscriptions = subscriptions
    , view = view
    }

-- MODEL
type Model = Model { news : List (Viewing.Posting Msg) }

init : () -> (Model, Cmd Msg)
init _ = ( Model { news = [] },
