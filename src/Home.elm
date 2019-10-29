module Home exposing (..)
import Browser
import Html exposing (..)
import Time
import Viewing exposing (..)
import Array
import Delay

main = Browser.element
        {  init = init
        , update = update
        , subscriptions = subscriptions
        , view = view
        }

descriptions =  Array.fromList
                [ "Democracy"
                , "DemNet"
                , "The democratic social network"
                ]

type alias Model =  { queue : List String
                    , current : String
                    }

init : () -> (Model, Cmd Msg)
init _ = ({ queue = [ "Transparent"
          , "Free"
          , "Libre"
          , "The democratic social network"]
          , current = "Democratic"
          }, cycleDescriptions )
type Msg = Change Time.Posix

update : Msg -> Model -> (Model, Cmd Msg)
update msg model =
  case msg of
    Change _ -> let newCurrent  = case List.head model.queue of
                      Just c -> c
                      Nothing -> model.current
                    newQueue    = model.queue ++ [model.current]
                in  ( { current = newCurrent
                      , queue   = newQueue
                      }, Cmd.none )

-- SUBSCRIPTIONS
subscriptions : Model -> Sub Msg
subscriptions model =
  Time.every Time.second Change

view : Model -> Html Msg
view model =
  div []
    [ viewHeader
    , text model.current
    ]
